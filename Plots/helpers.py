"""Utilities for the ttbar model-discrimination analysis.

This module provides four groups of helpers:

1. data acquisition and LHE parsing;
2. construction and scaling of pre-binned model templates;
3. Asimov/profile-likelihood and normalized-falloff significance calculations;
4. threshold/luminosity scans and plotting.

The statistical analysis is observable-independent. Each observable should have
its own pre-binned workspace (for example one workspace for ``m_tt`` and one
for ``pt_t``), containing the bin edges and all mass-scan templates for that
observable. The same fitting and luminosity-scan functions can then be reused
without re-binning or hard-coding an ``m_tt`` definition.

Conventions
-----------
* Cross sections are assumed to be in pb.
* Integrated luminosities are assumed to be in fb^-1.
* ``PB_TO_FB = 1000`` converts pb x fb^-1 to expected event counts.
* Histograms stored in the workspace are cross-section histograms unless a
  function explicitly documents that it expects event yields.
* For VLF and Scalar templates, the fitted scale ``k`` multiplies the stored
  signal as ``k**2``.
* For Z' templates, the stored pure contribution scales as ``k**2`` and the
  interference contribution scales as ``k``. Therefore negative ``k`` values
  are physically meaningful: they reverse the interference sign while leaving
  the pure contribution unchanged.

The statistical routines treat the supplied synthetic/Asimov data as fixed.
When a fractional systematic uncertainty is requested, it is implemented as an
independent Gaussian nuisance parameter in each bin, acting on the SM
background yield by default.
"""

from __future__ import annotations

import glob
import gzip
import os
import pickle
import re
import tempfile
import urllib.request
from collections.abc import Mapping
from urllib.parse import urljoin, urlparse

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
try:
    import pylhe
except ImportError:  # Optional: only required by get_run_metadata/load_lhe_with_corrections.
    pylhe = None
from matplotlib.lines import Line2D
from scipy.optimize import minimize, minimize_scalar
from tqdm.auto import tqdm

SQRT_S = 13_000.0  # proton-proton centre-of-mass energy, GeV
PB_TO_FB = 1000.0
DEFAULT_FAKE_SCALES = {
    "Scalar_1500": 7.5,
    "VLF_1500": 3.5,
    "Zprime_3000": -4.0,
}

# Default likelihood/significance windows for observables that have an agreed
# analysis range. Unknown observables default to the full range stored in their
# workspace unless ``analysis_range`` is supplied explicitly.
DEFAULT_ANALYSIS_RANGES = {
    "m_tt": (1200.0, 5000.0),
    "pt_t": (500.0, 3500.0),
    "pT": (500.0, 3500.0),
}


# ============================================================================
# Internal validation/statistics helpers
# ============================================================================


def _as_1d_float(name: str, values) -> np.ndarray:
    """Return *values* as a finite one-dimensional float array."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional; got shape {arr.shape}.")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains NaN or infinite values.")
    return arr


def _require_same_shape(**arrays: np.ndarray) -> None:
    """Raise if the supplied arrays do not all have the same shape."""
    shapes = {name: np.asarray(arr).shape for name, arr in arrays.items()}
    if len(set(shapes.values())) > 1:
        raise ValueError(f"Arrays must have identical shapes; got {shapes}.")


def _poisson_deviance(n_true, n_test) -> np.ndarray:
    """Return the bin-wise Poisson deviance for an Asimov data set.

    ``n_true`` may contain zero bins. ``n_test`` must be strictly positive.
    The returned quantity is

        2 [n_test - n_true + n_true log(n_true / n_test)],

    with the logarithmic term defined to be zero when ``n_true == 0``.
    """
    n_true = np.asarray(n_true, dtype=float)
    n_test = np.asarray(n_test, dtype=float)
    _require_same_shape(n_true=n_true, n_test=n_test)

    if np.any(n_true < 0):
        raise ValueError("Asimov/observed yields must be non-negative in every bin.")
    if np.any(n_test < 0):
        raise ValueError("Test-hypothesis yields must be non-negative in every bin.")
    impossible = (n_true > 0) & (n_test == 0)
    if np.any(impossible):
        raise ValueError(
            "A test expectation of zero is incompatible with a positive Asimov yield."
        )

    log_term = np.zeros_like(n_true)
    positive = n_true > 0
    log_term[positive] = n_true[positive] * np.log(
        n_true[positive] / n_test[positive]
    )
    return 2.0 * (n_test - n_true + log_term)


def _profiled_poisson_deviance(
    n_true,
    n_test,
    frac_syst: float = 0.0,
    syst_reference=None,
):
    """Profile independent Gaussian normalization nuisances bin by bin.

    Parameters
    ----------
    n_true, n_test:
        Asimov and nominal test-hypothesis yields.
    frac_syst:
        Fractional 1-sigma systematic uncertainty ``epsilon``.
    syst_reference:
        Yield to which the fractional uncertainty applies. If omitted, the
        uncertainty acts on ``n_test``. Passing the SM background implements
        an uncertainty on the background only.

    Returns
    -------
    q : float
        Sum of the profiled Poisson deviance and Gaussian penalties.
    theta_hat : ndarray
        Best-fit standard-normal nuisance parameter in each bin.
    profiled_test : ndarray
        Profiled test expectation in each bin.
    """
    n_true = _as_1d_float("n_true", n_true)
    n_test = _as_1d_float("n_test", n_test)
    _require_same_shape(n_true=n_true, n_test=n_test)

    if np.any(n_true < 0):
        raise ValueError("n_true must be non-negative in every bin.")
    if np.any(n_test <= 0):
        raise ValueError("n_test must be strictly positive in every bin.")

    epsilon = float(frac_syst)
    if epsilon < 0:
        raise ValueError("frac_syst must be non-negative.")

    if syst_reference is None:
        ref = n_test
    else:
        ref = _as_1d_float("syst_reference", syst_reference)
        _require_same_shape(n_true=n_true, n_test=n_test, syst_reference=ref)
        if np.any(ref < 0):
            raise ValueError("syst_reference must be non-negative.")

    if epsilon == 0.0:
        theta_hat = np.zeros_like(n_test)
        profiled_test = n_test.copy()
    else:
        # lambda(theta) = n_test + a*theta,  a = epsilon*syst_reference.
        # The stationary equation has a closed-form positive solution:
        # lambda^2 + (a^2 - n_test) lambda - a^2 n_true = 0.
        a = epsilon * ref
        a2 = a * a
        disc = (n_test - a2) ** 2 + 4.0 * a2 * n_true
        profiled_test = 0.5 * (n_test - a2 + np.sqrt(disc))

        # For a == 0 the nuisance has no effect and its optimum is theta=0.
        theta_hat = np.zeros_like(n_test)
        movable = a > 0
        theta_hat[movable] = (
            profiled_test[movable] - n_test[movable]
        ) / a[movable]

    q_bins = _poisson_deviance(n_true, profiled_test) + theta_hat**2
    return float(np.sum(q_bins)), theta_hat, profiled_test


def _model_signal(pure, scale: float, interference=None) -> np.ndarray:
    """Scale stored signal components according to their coupling dependence."""
    pure = np.asarray(pure, dtype=float)
    signal = (float(scale) ** 2) * pure
    if interference is not None:
        signal = signal + float(scale) * np.asarray(interference, dtype=float)
    return signal


def _resolve_sys_key(mapping: Mapping, requested: float) -> float:
    """Resolve a floating systematic key without silently falling back to 0."""
    if requested in mapping:
        return requested
    for key in mapping:
        if isinstance(key, (int, float, np.integer, np.floating)) and np.isclose(
            key, requested, rtol=0.0, atol=1e-12
        ):
            return key
    available = [k for k in mapping if isinstance(k, (int, float, np.number))]
    raise KeyError(
        f"No fitted result is available for sys_err={requested}. "
        f"Available systematic keys: {available}"
    )


def _resolve_workspace_file(observable, workspace_file=None, workspace_files=None):
    """Resolve the workspace associated with an observable.

    ``workspace_file`` selects one file explicitly. Alternatively,
    ``workspace_files`` may map observable names to files, e.g.
    ``{"m_tt": "mass_scan_mtt.pkl", "pt_t": "mass_scan_pt.pkl"}``.

    For backward compatibility, ``m_tt`` defaults to ``lite_workspace.pkl``.
    Other observables must specify their workspace explicitly so that an
    ``m_tt`` workspace cannot be used accidentally for a different observable.
    """
    observable = str(observable)
    if workspace_file is not None:
        return os.fspath(workspace_file)
    if workspace_files is not None:
        if observable not in workspace_files:
            raise KeyError(
                f"No workspace is configured for observable {observable!r}. "
                f"Available observables: {list(workspace_files)}"
            )
        return os.fspath(workspace_files[observable])
    if observable == "m_tt":
        return "lite_workspace.pkl"
    raise ValueError(
        f"A separate workspace file is required for observable {observable!r}. "
        "Pass workspace_file='...' or workspace_files={observable: '...'}."
    )


def _resolve_analysis_range(
    observable,
    bins,
    analysis_range=None,
    *,
    legacy_min=None,
    legacy_max=None,
):
    """Return a validated ``(lower, upper)`` analysis interval.

    Priority is: explicit ``analysis_range``; legacy lower/upper arguments; a
    configured default for the observable; otherwise the full workspace range.
    The lower edge is inclusive and the upper edge is exclusive when histogram
    bins are selected.
    """
    bins = _as_1d_float("bins", bins)
    observable = str(observable)

    if analysis_range is not None:
        if legacy_min is not None or legacy_max is not None:
            raise ValueError(
                "Use either analysis_range=(min, max) or the legacy min/max "
                "arguments, not both."
            )
        if len(analysis_range) != 2:
            raise ValueError("analysis_range must contain exactly two values.")
        lower, upper = map(float, analysis_range)
    elif legacy_min is not None or legacy_max is not None:
        if legacy_min is None or legacy_max is None:
            raise ValueError("Both legacy lower and upper bounds must be supplied.")
        lower, upper = float(legacy_min), float(legacy_max)
    elif observable in DEFAULT_ANALYSIS_RANGES:
        lower, upper = DEFAULT_ANALYSIS_RANGES[observable]
    else:
        lower, upper = float(bins[0]), float(bins[-1])

    if not np.isfinite(lower) or not np.isfinite(upper):
        raise ValueError("Analysis-range bounds must be finite.")
    if upper <= lower:
        raise ValueError("The upper analysis bound must be greater than the lower bound.")

    mask = (bins[:-1] >= lower) & (bins[:-1] < upper)
    if not np.any(mask):
        raise ValueError(
            f"Analysis range ({lower}, {upper}) contains no bins for observable "
            f"{observable!r}; workspace spans {bins[0]} to {bins[-1]}."
        )
    return float(lower), float(upper)


def _validate_observable_metadata(workspace, observable):
    """Check optional observable metadata stored in a workspace.

    Old workspaces do not need an ``observable`` key. New workspaces should
    store it because it catches accidental cross-use of, for example, an
    ``m_tt`` mass scan in a ``pt_t`` analysis.
    """
    stored = workspace.get("observable")
    if stored is not None and str(stored) != str(observable):
        raise ValueError(
            f"Workspace contains observable={stored!r}, but the analysis requested "
            f"observable={observable!r}."
        )


def _match_integral(reference, candidate, *, atol: float = 1e-15) -> np.ndarray:
    """Rescale *candidate* so its signed integral matches *reference*."""
    reference = np.asarray(reference, dtype=float)
    candidate = np.asarray(candidate, dtype=float)
    _require_same_shape(reference=reference, candidate=candidate)

    ref_sum = float(np.sum(reference))
    cand_sum = float(np.sum(candidate))
    if abs(cand_sum) <= atol:
        raise ValueError(
            "Cannot normalize a template whose signed integral is zero (or nearly zero)."
        )
    return candidate * (ref_sum / cand_sum)


def _parabolic_mass_estimate(masses, objective_values, idx_min: int) -> float:
    """Return a local three-point parabolic mass estimate for diagnostics only."""
    masses = np.asarray(masses, dtype=float)
    values = np.asarray(objective_values, dtype=float)
    if len(masses) < 3:
        return float(masses[idx_min])

    start = int(np.clip(idx_min - 1, 0, len(masses) - 3))
    idx = np.arange(start, start + 3)
    x = masses[idx]
    y = values[idx]
    if not np.all(np.isfinite(y)):
        return float(masses[idx_min])

    a, b, _ = np.polyfit(x, y, 2)
    if a <= 0:
        return float(masses[idx_min])
    vertex = -b / (2.0 * a)
    return float(np.clip(vertex, x.min(), x.max()))


# ============================================================================
# Data acquisition and model loading
# ============================================================================


def download_data_files(base_url, files_dict, out_dir="data"):
    """Download missing ``.lhe.gz`` files.

    Parameters
    ----------
    base_url : str or None
        Base URL used when a value in ``files_dict`` is a relative path. It is
        ignored for values that are already absolute URLs.
    files_dict : mapping
        Mapping ``dataset_name -> URL or relative remote path``.
    out_dir : str, default="data"
        Destination directory. Each file is saved as ``<name>.lhe.gz``.
    """
    os.makedirs(out_dir, exist_ok=True)
    for name, remote in files_dict.items():
        parsed = urlparse(str(remote))
        url = str(remote) if parsed.scheme else urljoin(base_url or "", str(remote))
        if not urlparse(url).scheme:
            raise ValueError(
                f"No absolute URL could be constructed for {name!r}: {remote!r}."
            )

        out = os.path.join(out_dir, f"{name}.lhe.gz")
        if os.path.exists(out):
            print(f"{out} already exists")
            continue
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, out)


def load_model_data(base_path, model_name, rescale=1.0):
    """Load and concatenate NPZ event samples for one model.

    Each matching NPZ file must contain arrays named ``mTT`` and ``weights`` of
    equal length. Files are processed in sorted order for reproducibility.

    Returns
    -------
    pandas.DataFrame
        Columns ``m_tt``, ``weight``, and ``label``.
    """
    pattern = os.path.join(base_path, f"*{model_name}*.npz")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"Warning: No files found for {model_name} at {base_path}")
        return pd.DataFrame(columns=["m_tt", "weight", "label"])

    mtt_list, weight_list = [], []
    for path in files:
        with np.load(path, allow_pickle=False) as data:
            if "mTT" not in data or "weights" not in data:
                raise KeyError(f"{path} must contain 'mTT' and 'weights' arrays.")
            mtt = np.asarray(data["mTT"], dtype=float)
            weights = np.asarray(data["weights"], dtype=float)
            if mtt.shape != weights.shape:
                raise ValueError(
                    f"Shape mismatch in {path}: mTT={mtt.shape}, weights={weights.shape}."
                )
            mtt_list.append(mtt)
            weight_list.append(weights * float(rescale))

    return pd.DataFrame(
        {
            "m_tt": np.concatenate(mtt_list),
            "weight": np.concatenate(weight_list),
            "label": model_name,
        }
    )


# ============================================================================
# Best-fit construction from the pre-binned workspace
# ============================================================================


def fit_and_assemble_data(
    fake_data_key,
    workspace_file=None,
    sys_err_list=None,
    lumi=500.0,
    zp_limit_csv="Safe_Limits_Zprime.csv",
    *,
    observable="m_tt",
    workspace_files=None,
    analysis_range=None,
    fit_min=None,
    fit_max=None,
    fake_scales=None,
    vlf_max_scale=7.0,
    scalar_max_scale=10.1,
    zprime_max_abs_scale=100.0,
):
    """
    Fit each model grid to an Asimov/synthetic data template.

    For every available mass point, the coupling-like scale is profiled
    continuously. The best available grid mass is used to construct the
    returned histogram. A local parabolic interpolation in mass is reported
    only as a diagnostic and is not used to construct a histogram.

    For sys_err = 0, the Poisson deviance is proportional to luminosity.
    The scale minimization is therefore performed using q/(L * PB_TO_FB),
    which removes this trivial overall normalization and makes the numerical
    minimization independent of luminosity.

    For sys_err > 0, the same normalization is also used during minimization.
    This is only a positive multiplicative constant at fixed luminosity and
    therefore does not alter the minimum.

    The physical, unnormalized q value is always stored in "min_q".

    For nonzero sys_err, the likelihood profiles one independent Gaussian
    nuisance parameter per bin acting on the SM background.
    """

    del zp_limit_csv

    observable = str(observable)

    if lumi <= 0:
        raise ValueError("lumi must be positive.")

    workspace_file = _resolve_workspace_file(
        observable,
        workspace_file=workspace_file,
        workspace_files=workspace_files,
    )

    sys_err_list = [0.0] if not sys_err_list else list(sys_err_list)

    if any(float(eps) < 0 for eps in sys_err_list):
        raise ValueError("Systematic uncertainties must be non-negative.")

    # ============================================================
    # Load workspace
    # ============================================================

    with open(workspace_file, "rb") as handle:
        ws = pickle.load(handle)

    _validate_observable_metadata(ws, observable)

    for key in ("bins", "SM", "FakeData", "Models"):
        if key not in ws:
            raise KeyError(f"Workspace is missing required key {key!r}.")

    bins = _as_1d_float("bins", ws["bins"])

    if len(bins) < 2 or np.any(np.diff(bins) <= 0):
        raise ValueError("Workspace bin edges must be strictly increasing.")

    n_bins = len(bins) - 1

    h_sm = _as_1d_float("workspace['SM']", ws["SM"])

    if len(h_sm) != n_bins:
        raise ValueError("SM histogram length does not match workspace bins.")

    # ============================================================
    # Analysis range
    # ============================================================

    analysis_min, analysis_max = _resolve_analysis_range(
        observable,
        bins,
        analysis_range=analysis_range,
        legacy_min=fit_min,
        legacy_max=fit_max,
    )

    fit_mask = (
        (bins[:-1] >= analysis_min)
        & (bins[:-1] < analysis_max)
    )

    # ============================================================
    # Synthetic / Asimov data
    # ============================================================

    if fake_data_key not in ws["FakeData"]:
        raise KeyError(
            f"Fake data {fake_data_key!r} not found. "
            f"Available keys: {list(ws['FakeData'])}"
        )

    fake_entry = ws["FakeData"][fake_data_key]

    h_fake_pure = _as_1d_float(
        "fake pure histogram",
        fake_entry["pure"],
    )

    h_fake_int = _as_1d_float(
        "fake interference histogram",
        fake_entry.get("int", np.zeros(n_bins)),
    )

    _require_same_shape(
        h_sm=h_sm,
        h_fake_pure=h_fake_pure,
        h_fake_int=h_fake_int,
    )

    scale_map = dict(DEFAULT_FAKE_SCALES)

    if fake_scales is not None:
        scale_map.update(fake_scales)

    if fake_data_key not in scale_map:
        raise KeyError(
            f"No fake-data scale is defined for {fake_data_key!r}. "
            "Pass fake_scales={key: value}."
        )

    fake_scale = float(scale_map[fake_data_key])

    # Only Z' has a separately stored contribution linear in the
    # signed coupling product.
    fake_uses_interference = fake_data_key.startswith("Zprime")

    fake_signal_xsec = _model_signal(
        h_fake_pure,
        fake_scale,
        h_fake_int if fake_uses_interference else None,
    )

    # Convert cross sections [pb] to yields:
    # pb * fb^-1 * 1000
    yield_factor = lumi * PB_TO_FB

    n_sm = h_sm * yield_factor
    n_fake = fake_signal_xsec * yield_factor
    n_obs = n_sm + n_fake

    if np.any(n_obs[fit_mask] < 0):
        bad = np.flatnonzero(fit_mask & (n_obs < 0))

        raise ValueError(
            "The synthetic total expectation is negative in fit bins "
            f"{bad.tolist()}; a Poisson likelihood is not defined there."
        )

    # ============================================================
    # Extract mass grids
    # ============================================================

    def extract_grid(model_pure, model_int=None):

        if model_pure not in ws["Models"]:
            return None, None, None

        pure_dict = ws["Models"][model_pure]
        int_dict = ws["Models"].get(model_int, {}) if model_int else None

        rows = []

        for mass_value, hist in pure_dict.items():

            pure = _as_1d_float(
                f"{model_pure}[{mass_value}]",
                hist,
            )

            if len(pure) != n_bins:
                raise ValueError(
                    f"Histogram {model_pure}[{mass_value}] has "
                    f"{len(pure)} bins; expected {n_bins}."
                )

            # Signed templates are allowed. Only remove completely empty ones.
            if not np.any(np.abs(pure) > 0):
                continue

            interference = None

            if model_int is not None:

                if mass_value not in int_dict:
                    raise KeyError(
                        f"Missing {model_int}[{mass_value}] for "
                        f"{model_pure}[{mass_value}]."
                    )

                interference = _as_1d_float(
                    f"{model_int}[{mass_value}]",
                    int_dict[mass_value],
                )

                if len(interference) != n_bins:
                    raise ValueError(
                        f"Histogram {model_int}[{mass_value}] "
                        "has the wrong length."
                    )

            rows.append(
                (
                    float(mass_value),
                    pure,
                    interference,
                )
            )

        if not rows:
            return None, None, None

        rows.sort(key=lambda row: row[0])

        masses = np.array(
            [row[0] for row in rows],
            dtype=float,
        )

        pure_grid = np.stack(
            [row[1] for row in rows]
        )

        int_grid = (
            np.stack([row[2] for row in rows])
            if model_int is not None
            else None
        )

        return masses, pure_grid, int_grid

    vlf_m, vlf_grid, _ = extract_grid("VLF")
    scalar_m, scalar_grid, _ = extract_grid("Scalar")

    zp_m, zp_grid, zp_grid_int = extract_grid(
        "Zprime",
        "Zprime_int",
    )

    zp20_m, zp20_grid, zp20_grid_int = extract_grid(
        "Zprime_20pc",
        "Zprime_20pc_int",
    )

    # ============================================================
    # Fit one complete mass grid
    # ============================================================

    def fit_grid(
        masses,
        pure_grid,
        max_abs_or_upper,
        sys_err,
        int_grid=None,
    ):
        """
        Profile the coupling at every discrete mass point.

        The physical objective is the profiled Poisson deviance q.

        During numerical minimization we use

            q_fit = q / (lumi * PB_TO_FB),

        which differs from q only by a positive constant at fixed luminosity.

        In particular, at sys_err = 0 this completely removes the trivial
        q ∝ luminosity scaling and therefore prevents the numerical optimizer
        from changing its behaviour as luminosity is varied.
        """

        if masses is None or pure_grid is None or len(masses) == 0:
            return None

        signed = int_grid is not None

        if signed:
            lower = -float(max_abs_or_upper)
            upper = +float(max_abs_or_upper)
        else:
            lower = 0.0
            upper = float(max_abs_or_upper)

        if upper <= lower:
            raise ValueError("Invalid scale bounds.")

        # Physical q values and luminosity-normalized q values.
        q_values = np.full(len(masses), np.inf, dtype=float)
        q_fit_values = np.full(len(masses), np.inf, dtype=float)
        k_values = np.full(len(masses), np.nan, dtype=float)

        n_obs_fit = n_obs[fit_mask]
        n_sm_fit = n_sm[fit_mask]

    
        fit_normalization = yield_factor


        N_SCAN = 301

        for i, pure in enumerate(pure_grid):

            interference = (
                int_grid[i]
                if signed
                else None
            )

            # ----------------------------------------------------
            # Physical Poisson deviance
            # ----------------------------------------------------

            def physical_objective(k):

                k = float(np.asarray(k).reshape(-1)[0])

                signal_xsec = _model_signal(
                    pure,
                    k,
                    interference,
                )

                n_test = n_sm + signal_xsec * yield_factor
                n_test_fit = n_test[fit_mask]

                if np.any(~np.isfinite(n_test_fit)):
                    return np.inf

                if np.any(n_test_fit <= 0):
                    return np.inf

                try:
                    q, _, _ = _profiled_poisson_deviance(
                        n_obs_fit,
                        n_test_fit,
                        frac_syst=sys_err,
                        syst_reference=n_sm_fit,
                    )

                except ValueError:
                    return np.inf

                return float(q)

            # ----------------------------------------------------
            # Numerically normalized objective
            # ----------------------------------------------------

            def fit_objective(k):

                q = physical_objective(k)

                if not np.isfinite(q):
                    return np.inf

                return q / fit_normalization

            # ----------------------------------------------------
            # Coarse global scan
            # ----------------------------------------------------

            scan_ks = np.linspace(
                lower,
                upper,
                N_SCAN,
            )

            scan_q = np.array(
                [fit_objective(k) for k in scan_ks],
                dtype=float,
            )

            finite = np.isfinite(scan_q)

            if not np.any(finite):
                continue

            finite_indices = np.flatnonzero(finite)

            # Always include the global scan minimum.
            global_scan_idx = finite_indices[
                np.argmin(scan_q[finite])
            ]

            candidate_indices = {
                int(global_scan_idx)
            }

            # Also collect every local minimum visible in the coarse
            # scan. This is especially useful for the signed Z' case,
            # where different coupling branches may exist.
            for j in finite_indices:

                qj = scan_q[j]

                q_left = (
                    scan_q[j - 1]
                    if j > 0
                    else np.inf
                )

                q_right = (
                    scan_q[j + 1]
                    if j < len(scan_q) - 1
                    else np.inf
                )

                if qj <= q_left and qj <= q_right:
                    candidate_indices.add(int(j))

            # ----------------------------------------------------
            # Refine every candidate minimum
            # ----------------------------------------------------

            best_k = np.nan
            best_q_fit = np.inf

            for j in sorted(candidate_indices):

                # The coarse scan point itself is always a valid
                # candidate.
                k_candidate = float(scan_ks[j])
                q_candidate = float(scan_q[j])

                if q_candidate < best_q_fit:
                    best_q_fit = q_candidate
                    best_k = k_candidate

                # Interior minimum with finite neighbours:
                # refine using a robust bounded 1D minimization.
                if (
                    0 < j < len(scan_ks) - 1
                    and np.isfinite(scan_q[j - 1])
                    and np.isfinite(scan_q[j + 1])
                ):

                    local_left = float(scan_ks[j - 1])
                    local_right = float(scan_ks[j + 1])

                    result = minimize_scalar(
                        fit_objective,
                        bounds=(local_left, local_right),
                        method="bounded",
                        options={
                            "xatol": 1e-10,
                            "maxiter": 500,
                        },
                    )

                    if (
                        result.success
                        and np.isfinite(result.fun)
                        and result.fun < best_q_fit
                    ):
                        best_q_fit = float(result.fun)
                        best_k = float(result.x)

            if not np.isfinite(best_k):
                continue

            # ----------------------------------------------------
            # Recompute and store the physical q
            # ----------------------------------------------------

            best_q_physical = physical_objective(best_k)

            if not np.isfinite(best_q_physical):
                continue

            k_values[i] = best_k
            q_values[i] = best_q_physical
            q_fit_values[i] = best_q_fit

        # ========================================================
        # Select the best discrete mass
        # ========================================================

        finite_masses = np.isfinite(q_fit_values)

        if not np.any(finite_masses):
            return None

        idx = int(
            np.nanargmin(q_fit_values)
        )

        # Use the normalized likelihood profile for the parabolic
        # interpolation. Multiplying q by luminosity can then never
        # alter the diagnostic continuous mass estimate.
        continuous_m = _parabolic_mass_estimate(
            masses,
            q_fit_values,
            idx,
        )

        return {
            "snap_m": float(masses[idx]),
            "continuous_m": float(continuous_m),
            "scale_factor": float(k_values[idx]),

            # Physical likelihood-ratio statistic
            "min_q": float(q_values[idx]),

            # Complete profiles
            "grid_masses": masses.copy(),
            "grid_q": q_values.copy(),
            "grid_q_fit": q_fit_values.copy(),
            "grid_scale": k_values.copy(),
        }

    # ============================================================
    # Model definitions
    # ============================================================

    model_specs = {
        "VLF": (
            vlf_m,
            vlf_grid,
            None,
            vlf_max_scale,
        ),

        "Scalar": (
            scalar_m,
            scalar_grid,
            None,
            scalar_max_scale,
        ),

        "Zprime": (
            zp_m,
            zp_grid,
            zp_grid_int,
            zprime_max_abs_scale,
        ),

        "Zprime_20pc": (
            zp20_m,
            zp20_grid,
            zp20_grid_int,
            zprime_max_abs_scale,
        ),
    }

    # ============================================================
    # Nominal fake-data mass
    # ============================================================

    fake_mass_match = re.search(
        r"_(\d+(?:\.\d+)?)$",
        fake_data_key,
    )

    fake_mass = (
        float(fake_mass_match.group(1))
        if fake_mass_match
        else np.nan
    )

    # ============================================================
    # Perform fits for each systematic uncertainty
    # ============================================================

    output = {}

    for sys_err in map(float, sys_err_list):

        print("\n" + "=" * 60)
        print(f"Fitting observable: {observable}")

        print(
            f"Analysis range: "
            f"{analysis_min:g} <= {observable} < {analysis_max:g} GeV"
        )

        print(
            f"Systematic error: "
            f"{100.0 * sys_err:.1f}%"
        )

        print("=" * 60)

        best_fits = {}

        for model_name, (
            masses,
            pure_grid,
            int_grid,
            bound,
        ) in model_specs.items():

            result = fit_grid(
                masses,
                pure_grid,
                bound,
                sys_err,
                int_grid,
            )

            if result is None:
                continue

            best_fits[model_name] = result

            print(
                f"{model_name:12s}: "
                f"grid mass = {result['snap_m']:.1f} GeV | "
                f"parabolic estimate = {result['continuous_m']:.1f} GeV | "
                f"scale = {result['scale_factor']:.8g} | "
                f"min q = {result['min_q']:.6g}"
            )

        # ========================================================
        # Fake-data entry
        # ========================================================

        best_fits["FakeData"] = {
            "snap_m": fake_mass,
            "continuous_m": fake_mass,
            "scale_factor": fake_scale,
            "min_q": 0.0,
        }

        print(
            f"{'FakeData':12s}: "
            f"nominal mass = {fake_mass:.1f} GeV | "
            f"scale = {fake_scale:.8g}"
        )

        print(
            "Synthetic signal yield in fit window: "
            f"{np.sum(n_fake[fit_mask], dtype=np.float64):.2f} events"
        )

        # ========================================================
        # Construct best-fit cross-section histograms
        # ========================================================

        fitted_hists = {
            "SM": h_sm.copy()
        }

        # Fake data
        fitted_hists["FakeData"] = (
            fake_scale**2
        ) * h_fake_pure

        fitted_hists["FakeData_int"] = (
            fake_scale * h_fake_int
            if fake_uses_interference
            else np.zeros_like(h_fake_pure)
        )

        # Fitted hypotheses
        for model_name, fit in best_fits.items():

            if (
                model_name == "FakeData"
                or model_name not in model_specs
            ):
                continue

            masses, pure_grid, int_grid, _ = (
                model_specs[model_name]
            )

            mass_index = int(
                np.argmin(
                    np.abs(
                        masses - fit["snap_m"]
                    )
                )
            )

            k = fit["scale_factor"]

            fitted_hists[model_name] = (
                k**2
            ) * pure_grid[mass_index]

            if int_grid is not None:

                fitted_hists[
                    f"{model_name}_int"
                ] = (
                    k
                    * int_grid[mass_index]
                )

        # ========================================================
        # Save output
        # ========================================================

        output[sys_err] = {
            "hists": fitted_hists,
            "best_fits": best_fits,
            "bins": bins.copy(),
            "observable": observable,
            "analysis_range": (
                analysis_min,
                analysis_max,
            ),

            # Legacy alias
            "fit_window": (
                analysis_min,
                analysis_max,
            ),

            "workspace_file": workspace_file,
        }

    return output

# ============================================================================
# Kinematics and LHE parsing
# ============================================================================


def rapidity(E, pz, eps=1e-12):
    """Return rapidity ``0.5*log((E+pz)/(E-pz))`` or NaN if undefined."""
    num, den = float(E) + float(pz), float(E) - float(pz)
    if num <= eps or den <= eps:
        return np.nan
    return 0.5 * np.log(num / den)


def pt(px, py):
    """Return transverse momentum ``sqrt(px**2 + py**2)``."""
    return np.hypot(px, py)


def phi(px, py):
    """Return azimuthal angle in the interval ``[-pi, pi]``."""
    return np.arctan2(py, px)


def delta_phi(phi1, phi2):
    """Return the wrapped angular difference ``phi1 - phi2`` in ``[-pi, pi)``."""
    difference = phi1 - phi2
    return (difference + np.pi) % (2.0 * np.pi) - np.pi


def mass(E, px, py, pz, *, tolerance=1e-9):
    """Return invariant mass from a four-vector ``(E, px, py, pz)``.

    Tiny negative mass-squared values caused by floating-point roundoff are
    clipped to zero. Substantially spacelike inputs return NaN rather than being
    silently converted to a zero mass.
    """
    m2 = E * E - px * px - py * py - pz * pz
    scale = max(abs(E * E), abs(px * px + py * py + pz * pz), 1.0)
    if m2 < -tolerance * scale:
        return np.nan
    return np.sqrt(max(m2, 0.0))


def boost_to_rest_frame(p4, parent):
    """Boost a four-vector into the rest frame of ``parent``.

    Four-vectors use the ordering ``(E, px, py, pz)``. A ``ValueError`` is
    raised if ``parent`` does not define a physical timelike rest frame.
    """
    p4 = np.asarray(p4, dtype=float)
    parent = np.asarray(parent, dtype=float)
    if p4.shape != (4,) or parent.shape != (4,):
        raise ValueError("p4 and parent must each contain exactly four components.")

    E, px, py, pz = p4
    EP, Px, Py, Pz = parent
    if EP <= 0:
        raise ValueError("Parent energy must be positive.")

    beta = np.array([Px, Py, Pz], dtype=float) / EP
    b2 = float(np.dot(beta, beta))
    if b2 >= 1.0:
        raise ValueError("Parent four-vector is not timelike; no rest frame exists.")
    if b2 < 1e-16:
        return p4.copy()

    gamma = 1.0 / np.sqrt(1.0 - b2)
    momentum = np.array([px, py, pz], dtype=float)
    bp = float(np.dot(beta, momentum))
    gamma2 = (gamma - 1.0) / b2
    boosted_p = momentum + (gamma2 * bp - gamma * E) * beta
    boosted_E = gamma * (E - bp)
    return np.array([boosted_E, *boosted_p], dtype=float)


def _scattering_cosine(top4, tt4, incoming_particles) -> float:
    """Compute cos(theta*) relative to the +z incoming beam in the tt rest frame."""
    if not incoming_particles:
        return np.nan

    # Choose the incoming parton travelling toward +z as the reference beam.
    beam = max(incoming_particles, key=lambda particle: particle["pz"])
    beam4 = np.array(
        [beam["E"], beam["px"], beam["py"], beam["pz"]], dtype=float
    )
    try:
        top_star = boost_to_rest_frame(top4, tt4)
        beam_star = boost_to_rest_frame(beam4, tt4)
    except ValueError:
        return np.nan

    p_top = top_star[1:]
    p_beam = beam_star[1:]
    denom = np.linalg.norm(p_top) * np.linalg.norm(p_beam)
    if denom < 1e-12:
        return np.nan
    return float(np.clip(np.dot(p_top, p_beam) / denom, -1.0, 1.0))


def parse_event_block(lines, rescale_weight_by=1.0):
    """Parse one LHE ``<event>`` block and compute ttbar observables.

    The function selects the first status-1 top and antitop. ``cos_theta_star``
    is the angle between the top and the +z incoming beam after both are boosted
    to the ttbar rest frame. This is preferable to simply using the boosted
    top's Cartesian z component when the ttbar system has transverse recoil.

    Returns ``None`` when the block is empty or contains no final-state ttbar
    pair.
    """
    content = [line.strip() for line in lines if line.strip()]
    if not content:
        return None

    header = content[0].split()
    if len(header) < 3:
        raise ValueError("Malformed LHE event header.")
    nup = int(header[0])
    xwgtup = float(header[2]) * float(rescale_weight_by)

    particles = []
    for line in content[1 : 1 + nup]:
        cols = line.split()
        if len(cols) < 11:
            continue
        particles.append(
            {
                "pid": int(cols[0]),
                "status": int(cols[1]),
                "px": float(cols[6]),
                "py": float(cols[7]),
                "pz": float(cols[8]),
                "E": float(cols[9]),
                "M": float(cols[10]),
            }
        )

    incoming = [particle for particle in particles if particle["status"] == -1]
    final = [particle for particle in particles if particle["status"] == 1]
    tops = [particle for particle in final if particle["pid"] == 6]
    antitops = [particle for particle in final if particle["pid"] == -6]
    if not tops or not antitops:
        return None

    top, antitop = tops[0], antitops[0]
    top4 = np.array([top["E"], top["px"], top["py"], top["pz"]], dtype=float)
    antitop4 = np.array(
        [antitop["E"], antitop["px"], antitop["py"], antitop["pz"]], dtype=float
    )
    tt4 = top4 + antitop4
    cos_theta_star = _scattering_cosine(top4, tt4, incoming)

    extra = [
        particle
        for particle in final
        if abs(particle["pid"]) in (1, 2, 3, 4, 5) or particle["pid"] == 21
    ]
    extra_pts = sorted(
        (pt(particle["px"], particle["py"]) for particle in extra), reverse=True
    )

    y_top = rapidity(top["E"], top["pz"])
    y_antitop = rapidity(antitop["E"], antitop["pz"])
    return {
        "weight": xwgtup,
        "m_t": mass(*top4),
        "m_tbar": mass(*antitop4),
        "m_tt": mass(*tt4),
        "pt_t": pt(top["px"], top["py"]),
        "pt_tbar": pt(antitop["px"], antitop["py"]),
        "pt_1": max(pt(top["px"], top["py"]), pt(antitop["px"], antitop["py"])),
        "pt_2": min(pt(antitop["px"], antitop["py"]),pt(top["px"], top["py"])),
        "pt_tt": pt(tt4[1], tt4[2]),
        "y_t": y_top,
        "y_tbar": y_antitop,
        "y_tt": rapidity(tt4[0], tt4[3]),
        "abs_delta_y": (
            abs(y_top - y_antitop)
            if np.isfinite(y_top) and np.isfinite(y_antitop)
            else np.nan
        ),
        "cos_theta_star": cos_theta_star,
        "abs_cos_theta_star": (
            abs(cos_theta_star) if np.isfinite(cos_theta_star) else np.nan
        ),
        "ptj1": extra_pts[0] if extra_pts else 0.0,
    }


def read_lhe_features(filepath, label=None, max_events=None, rescale_weight_by=1.0):
    """Stream an LHE/LHE.GZ file into an analysis-ready DataFrame.

    ``max_events`` counts successfully parsed ttbar events rather than raw LHE
    blocks. Set it to ``None`` to read the entire file.
    """
    if max_events is not None and int(max_events) <= 0:
        raise ValueError("max_events must be a positive integer or None.")

    data = {
        "weight": [],
        "m_t": [],
        "m_tbar": [],
        "m_tt": [],
        "pt_t": [],
        "pt_tbar": [],
        "pt_1": [],
        "pt_2": [],
        "pt_tt": [],
        "y_t": [],
        "y_tbar": [],
        "y_tt": [],
        "abs_delta_y": [],
        "cos_theta_star": [],
        "abs_cos_theta_star": [],
        "ptj1": [],
    }
    if label is not None:
        data["label"] = []

    block = []
    in_event = False
    event_count = 0
    opener = gzip.open if str(filepath).endswith(".gz") else open
    with opener(filepath, "rt", encoding="utf-8", errors="ignore") as handle:
        for line in tqdm(handle, desc=f"Reading {os.path.basename(filepath)}"):
            if "<event>" in line:
                in_event = True
                block = []
                continue
            if "</event>" in line:
                record = parse_event_block(block, rescale_weight_by)
                if record is not None:
                    for key, value in record.items():
                        data[key].append(value)
                    if label is not None:
                        data["label"].append(label)
                    event_count += 1
                    if max_events is not None and event_count >= int(max_events):
                        break
                in_event = False
                continue
            if in_event:
                block.append(line)

    return pd.DataFrame(data)


def read_root_features(rootTree, max_events=None):

    nevts = rootTree.GetEntries()
    if max_events is not None and int(max_events) > 0:
        nevts = min(nevts, int(max_events))
    
    data = {
                "weight": [],
                "m_t": [],
                "m_tbar": [],
                "m_tt": [],
                "pt_t": [],
                "pt_tbar": [],
                "pt_1": [],
                "pt_2": [],
                "pt_tt": [],
                "y_t": [],
                "y_tbar": [],
                "y_tt": [],
                # "abs_delta_y": [],
                # "cos_theta_star": [],
                # "abs_cos_theta_star": [],
                # "ptj1": [],
            }
    for ievt in range(nevts):        
        rootTree.GetEntry(ievt)
        t = [top for top in rootTree.topMothers if top.PID == 6]
        tbar = [top for top in rootTree.topMothers if top.PID == -6]
        if len(t) != 1:
            raise ValueError(f"Expected 1 top quark, found {len(t)}")
        else:
            t = t[0]
        if len(tbar) != 1:
            raise ValueError(f"Expected 1 anti-top quark, found {len(tbar)}")
        else:
            tbar = tbar[0]
        ttbar = t.P4() + tbar.P4()
        data["m_t"].append(t.Mass)
        data["m_tbar"].append(tbar.Mass)
        data["m_tt"].append(ttbar.M())
        data["pt_t"].append(t.PT)
        data["pt_tbar"].append(tbar.PT)
        data["pt_1"].append(max(t.PT, tbar.PT))
        data["pt_2"].append(min(tbar.PT, t.PT))        
        data["pt_tt"].append(ttbar.Pt())
        data["y_t"].append(t.Eta)
        data["y_tbar"].append(tbar.Eta)
        data["y_tt"].append(ttbar.Rapidity())
        data["weight"].append(rootTree.Event.At(0).Weight)

    root_features = pd.DataFrame(data)

    return root_features

def _parse_summary_cross_section(summary_path: str) -> float | None:
    """Extract the preferred cross section from a MadGraph ``summary.txt``."""
    try:
        text = open(summary_path, "r", encoding="utf-8", errors="ignore").read()
    except OSError:
        return None

    # Prefer a usable "Total cross section" line. If MadGraph marks it as
    # "DO NOT USE", fall back to nearby/available scale-variation output.
    lines = text.splitlines()
    candidates = []
    for index, line in enumerate(lines):
        if "Total cross section" in line and "DO NOT USE" not in line:
            candidates.append(line)
        if "Scale variation" in line:
            candidates.extend(lines[index + 1 : index + 4])

    number_re = re.compile(
        r"(?<![\w.])([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*(?:pb)?"
    )
    for line in candidates:
        # Prefer the number after a colon when one is present.
        search_text = line.split(":", 1)[1] if ":" in line else line
        match = number_re.search(search_text)
        if match:
            try:
                value = float(match.group(1))
            except ValueError:
                continue
            if value >= 0:
                return value
    return None


def get_run_metadata(filepath, is_nlo=False):
    """Read event count and cross-section metadata for one LHE file.

    For LO samples, ``xsec_true`` is the total cross section from the LHE
    ``<init>`` block. For NLO samples, a cross section from ``summary.txt`` is
    preferred when it can be parsed; otherwise the LHE value is retained.

    Multiple subprocess entries in the LHE initialization block are summed.
    """
    if pylhe is None:
        raise ImportError(
            "get_run_metadata requires the optional 'pylhe' package. "
            "Install pylhe to use LHE metadata normalization."
        )

    run_dir = os.path.dirname(filepath)
    info = {"nevents": -1, "xsec_lhe": -1.0, "xsec_true": -1.0}

    fd, temporary_lhe = tempfile.mkstemp(suffix=".lhe")
    os.close(fd)
    opener = gzip.open if str(filepath).endswith(".gz") else open
    try:
        with opener(filepath, "rt", encoding="utf-8", errors="ignore") as source, open(
            temporary_lhe, "w", encoding="utf-8"
        ) as target:
            for line in source:
                # Keep the historical workaround for malformed MadGraph banner
                # lines containing the word "generate".
                if "generate" not in line:
                    target.write(line)

        init_block = pylhe.read_lhe_init(temporary_lhe)
        proc_info = init_block.get("procInfo", [])
        xsecs = [float(proc["xSection"]) for proc in proc_info if "xSection" in proc]
        if xsecs:
            info["xsec_lhe"] = float(np.sum(xsecs))
            info["xsec_true"] = info["xsec_lhe"]
        info["nevents"] = int(pylhe.read_num_events(temporary_lhe))
    except Exception as exc:
        print(f"Error parsing LHE metadata from {os.path.basename(filepath)}: {exc}")
    finally:
        if os.path.exists(temporary_lhe):
            os.remove(temporary_lhe)

    if is_nlo:
        summary_value = _parse_summary_cross_section(os.path.join(run_dir, "summary.txt"))
        if summary_value is not None:
            info["xsec_true"] = summary_value

    if info["nevents"] <= 0:
        banners = sorted(glob.glob(os.path.join(run_dir, "*banner*txt")))
        if banners:
            banner_text = open(
                banners[0], "r", encoding="utf-8", errors="ignore"
            ).read()
            block_match = re.search(
                r"<MGGenerationInfo>(.*?)</MGGenerationInfo>",
                banner_text,
                flags=re.DOTALL,
            )
            if block_match:
                count_match = re.search(
                    r"(?:Number\s+of\s+Events|nevents)\s*[:=]\s*(\d+)",
                    block_match.group(1),
                    flags=re.IGNORECASE,
                )
                if count_match:
                    info["nevents"] = int(count_match.group(1))

    return info


def load_lhe_with_corrections(
    file_pattern,
    label=None,
    is_nlo=False,
    max_events=None,
    *,
    combine="sum",
):
    """Load LHE files and normalize each sample to its metadata cross section.

    The raw event weights are first parsed without assumptions about MadGraph's
    ``event_norm`` convention. For each file with a valid metadata cross
    section, all retained weights are multiplied by ``xsec_true / sum(weights)``.
    Consequently the retained sample sums to ``xsec_true`` exactly (before
    ``custom_rescale``).

    Parameters
    ----------
    file_pattern : str
        Glob pattern for LHE or LHE.GZ files.
    label : str, optional
        Label stored in the output DataFrame.
    is_nlo : bool
        If true, prefer the cross section in ``summary.txt``.
    max_events : int, optional
        Read only the first N valid ttbar events from each file. The retained
        subset is still normalized to the full metadata cross section, so this
        option is suitable for quick shape tests but not precision studies.
    combine : {"sum", "average"}
        ``"sum"`` treats files as additive subprocesses/samples. ``"average"``
        treats them as statistically independent replicas of the same process
        and divides the concatenated weights by the number of nonempty files.
    """
    files = sorted(glob.glob(file_pattern))
    if not files:
        print(f"Warning: No files found for pattern {file_pattern}")
        return pd.DataFrame(
            columns=[
                "weight",
                "m_t",
                "m_tbar",
                "m_tt",
                "pt_t",
                "pt_tbar",
                "pt_tt",
                "label",
            ]
        )
    if combine not in {"sum", "average"}:
        raise ValueError("combine must be either 'sum' or 'average'.")

    print(f"Loading {label} from {len(files)} LHE files...")
    frames = []
    for path in files:
        info = get_run_metadata(path, is_nlo=is_nlo)
        frame = read_lhe_features(
            path,
            label=label,
            max_events=max_events,
            rescale_weight_by=1.0,
        )
        if frame.empty:
            print(f"  -> Skipping {os.path.basename(path)} (no valid ttbar events)")
            continue

        raw_sum = float(frame["weight"].sum())
        target_xsec = float(info["xsec_true"])
        if np.isclose(raw_sum, 0.0, atol=1e-30):
            raise ValueError(
                f"Cannot normalize {path}: sum of retained event weights is zero."
            )
        factor = target_xsec / raw_sum
        frame.loc[:, "weight"] *= factor
        print(
            f"  -> {os.path.basename(path)}: normalized sum(weights) "
            f"from {raw_sum:.6e} to {target_xsec:.6e} pb"
        )

        frames.append(frame)

    if not frames:
        return pd.DataFrame()

    result = pd.concat(frames, ignore_index=True)
    if combine == "average":
        result.loc[:, "weight"] /= len(frames)
    return result


# ============================================================================
# Histogram and template operations
# ============================================================================


def class_normalized_weights(df, label_col="label", weight_col="weight"):
    """Normalize signed weights separately by class using their L1 norm.

    For each label, the returned weights satisfy ``sum(abs(w)) == 1`` (unless
    every original weight is zero). Signs are preserved.
    """
    weights = df[weight_col].astype(float).to_numpy(copy=True)
    output = np.zeros(len(df), dtype=float)
    labels = df[label_col].to_numpy()
    for label in pd.unique(labels):
        mask = labels == label
        norm = np.sum(np.abs(weights[mask]))
        output[mask] = weights[mask] / norm if norm > 0 else 0.0
    return output


def event_number_normalization(h_ref, h, lum=500.0):
    """Convert cross-section histograms to yields and match total event counts.

    Both inputs are interpreted as cross sections in pb. They are converted to
    expected yields at ``lum`` fb^-1, after which the candidate histogram is
    rescaled so its signed integral equals that of the reference.
    """
    if lum <= 0:
        raise ValueError("lum must be positive.")
    n_ref = np.asarray(h_ref, dtype=float) * lum * PB_TO_FB
    n = np.asarray(h, dtype=float) * lum * PB_TO_FB
    return _match_integral(n_ref, n)


def weighted_hist(x, w, bins):
    """Return a one-dimensional weighted histogram as float values."""
    x = np.asarray(x)
    w = np.asarray(w, dtype=float)
    if x.shape != w.shape:
        raise ValueError(f"x and w must have the same shape; got {x.shape} and {w.shape}.")
    hist, _ = np.histogram(x, bins=bins, weights=w)
    return hist.astype(float)


def build_template(x, w, bins, alpha=1e-12, density=False):
    """Build a weighted histogram, optionally normalized to unit probability."""
    hist = weighted_hist(x, w, bins)
    if density:
        if np.any(hist < 0):
            raise ValueError("A probability template cannot contain negative bins.")
        hist = hist + float(alpha)
        total = hist.sum()
        if total <= 0:
            raise ValueError("Cannot normalize a template with zero total weight.")
        hist = hist / total
    return hist


def build_shape_template(h, alpha=1e-12):
    """Normalize a non-negative yield histogram to unit integral."""
    hist = np.asarray(h, dtype=float)
    if np.any(hist < 0):
        raise ValueError("Shape-probability templates must be non-negative.")
    hist = hist + float(alpha)
    total = hist.sum()
    if total <= 0:
        raise ValueError("Cannot normalize a zero-integral histogram.")
    return hist / total


def build_signed_delta(h_hyp, h_sm, alpha=1e-12):
    """Return the fractional signed excess ``(h_hyp - h_sm) / h_sm``."""
    h_hyp = np.asarray(h_hyp, dtype=float)
    h_sm = np.asarray(h_sm, dtype=float)
    _require_same_shape(h_hyp=h_hyp, h_sm=h_sm)
    if np.any(h_sm < 0):
        raise ValueError("SM/background yields must be non-negative.")
    return (h_hyp - h_sm) / (h_sm + float(alpha))


def normalize_signed_template(delta, alpha=1e-12):
    """Normalize a signed excess by its L1 norm ``sum(abs(delta))``.

    Returns ``None`` when the excess is identically zero. In particular, the
    normalized-falloff observable is undefined for a pure-SM hypothesis.
    """
    delta = np.asarray(delta, dtype=float)
    norm = float(np.sum(np.abs(delta)))
    return delta / norm if norm > alpha else None


def _probability_pair(p, q, eps=1e-12):
    p = _as_1d_float("p", p)
    q = _as_1d_float("q", q)
    _require_same_shape(p=p, q=q)
    if np.any(p < 0) or np.any(q < 0):
        raise ValueError("Probability divergences require non-negative inputs.")
    p = p + eps
    q = q + eps
    return p / p.sum(), q / q.sum()


def js_divergence(p, q, eps=1e-12):
    """Return Jensen-Shannon divergence (natural logarithm)."""
    p, q = _probability_pair(p, q, eps=eps)
    midpoint = 0.5 * (p + q)
    return 0.5 * np.sum(p * np.log(p / midpoint)) + 0.5 * np.sum(
        q * np.log(q / midpoint)
    )


def kl_divergence(p, q, eps=1e-12):
    """Return Kullback-Leibler divergence ``D_KL(p || q)`` (natural logarithm)."""
    p, q = _probability_pair(p, q, eps=eps)
    return np.sum(p * np.log(p / q))


def signed_l2_distance(d1, d2):
    """Return RMS/L2 separation between two signed shape vectors."""
    d1 = np.asarray(d1, dtype=float)
    d2 = np.asarray(d2, dtype=float)
    _require_same_shape(d1=d1, d2=d2)
    return np.sqrt(np.mean((d1 - d2) ** 2))


def asimov_shape_llr_stat_only(p_true, p_test, N=10000, eps=1e-12):
    """Shape-only Asimov log-likelihood ratio at fixed total event count ``N``."""
    if N < 0:
        raise ValueError("N must be non-negative.")
    p_true, p_test = _probability_pair(p_true, p_test, eps=eps)
    n = float(N) * p_true
    q = 2.0 * np.sum(n * np.log(p_true / p_test))
    return float(q), float(np.sqrt(max(q, 0.0)))


# ============================================================================
# Variance and significance calculations
# ============================================================================


def calc_variance_hat_delta(h_hyp, h_sm, eps, alpha=1e-12):
    """Propagate uncertainties to the L1-normalized signed excess.

    The unnormalized quantity is

    ``delta_i = (h_hyp_i - h_sm_i) / h_sm_i``.

    The statistical term assumes Poisson variance ``Var(h_hyp_i)=h_hyp_i``.
    The systematic term assumes an independent fractional uncertainty ``eps``
    on the SM denominator in every bin. Correlations between bins are not
    included.
    """
    n_hyp = np.asarray(h_hyp, dtype=float)
    n_sm = np.asarray(h_sm, dtype=float)
    _require_same_shape(n_hyp=n_hyp, n_sm=n_sm)
    if np.any(n_hyp < 0) or np.any(n_sm < 0):
        raise ValueError("Poisson yields must be non-negative.")
    if eps < 0:
        raise ValueError("eps must be non-negative.")

    denom = n_sm + float(alpha)
    delta = (n_hyp - n_sm) / denom
    S = float(np.sum(np.abs(delta)))
    if S <= alpha:
        return np.full_like(delta, np.inf, dtype=float)

    sigma2_delta = n_hyp / (denom**2) + (n_hyp**2 * eps**2) / (denom**2)
    bracket_i = 1.0 / S**2 - 2.0 * np.abs(delta) / S**3 + delta**2 / S**4
    term_same = bracket_i * sigma2_delta
    sum_sigma2_other = np.sum(sigma2_delta) - sigma2_delta
    term_diff = (delta**2 / S**4) * sum_sigma2_other
    return term_same + term_diff


def asimov_signed_Z_rigorous(
    dA,
    dB,
    hA,
    hB,
    n_sm,
    eps,
    mode="test",
    alpha=1e-12,
):
    """Normalized-falloff separation significance for signed excess shapes.

    Parameters
    ----------
    dA, dB : array-like
        L1-normalized signed excesses for the true and test hypotheses.
    hA, hB : array-like
        Corresponding total expected yields (SM + signal).
    n_sm : array-like
        SM background yields.
    eps : float
        Fractional per-bin systematic uncertainty on the SM denominator.
    mode : {"test", "both"}
        ``"test"`` treats the Asimov/true template as fixed and uses only the
        variance of the test template. ``"both"`` adds the propagated
        variances of both templates.
    """
    if dA is None or dB is None:
        return np.nan, None, None

    dA = np.asarray(dA, dtype=float)
    dB = np.asarray(dB, dtype=float)
    _require_same_shape(dA=dA, dB=dB)

    var_a = calc_variance_hat_delta(hA, n_sm, eps, alpha=alpha)
    var_b = calc_variance_hat_delta(hB, n_sm, eps, alpha=alpha)
    if mode == "test":
        variance = var_b
    elif mode == "both":
        variance = var_a + var_b
    else:
        raise ValueError("mode must be 'test' or 'both'.")

    numerator = (dA - dB) ** 2
    denominator = variance + float(alpha)
    finite = np.isfinite(denominator) & (denominator > 0)
    if not np.any(finite):
        return np.nan, numerator, denominator
    q = np.sum(numerator[finite] / denominator[finite])
    return float(np.sqrt(max(q, 0.0))), numerator, denominator


def asimov_shape_Z_with_syst(
    p_true,
    p_test,
    frac_syst=0.05,
    eps=1e-12,
    *,
    syst_reference=None,
):
    """Profile-likelihood Asimov separation significance.

    ``p_true`` and ``p_test`` are expected **event yields**, not normalized
    probabilities. For ``frac_syst > 0``, each bin has an independent standard
    normal nuisance. The additive 1-sigma variation is
    ``frac_syst * syst_reference``. If ``syst_reference`` is omitted, the
    uncertainty is relative to the full test expectation; for this analysis it
    is normally preferable to pass the SM background yield explicitly.

    Returns ``(Z_A, q_A, theta_hat)`` with ``Z_A = sqrt(q_A)``.
    """
    del eps  # retained for API compatibility; the exact formula needs no regulator
    q_a, theta_hat, _ = _profiled_poisson_deviance(
        p_true,
        p_test,
        frac_syst=frac_syst,
        syst_reference=syst_reference,
    )
    return float(np.sqrt(max(q_a, 0.0))), q_a, theta_hat


# ============================================================================
# Plotting utilities and labels
# ============================================================================


def beautify_axis(ax, grid=False):
    """Apply the common axis formatting used by the analysis plots."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="in", top=False, right=False, length=5)
    if grid:
        ax.grid(True, alpha=0.22, linewidth=0.7)


def get_best_pair_and_cut(df, N=100000, metric=None):
    """Return ``(pair, mcut)`` at the maximum of a selected significance column.

    If ``metric`` is omitted, legacy column names are tried in a documented
    priority order. The function no longer falls back silently to an arbitrary
    last DataFrame column.
    """
    if df.empty:
        raise ValueError("df is empty.")

    candidates = (
        [metric]
        if metric is not None
        else [
            f"Z_{N}_a_true",
            f"Z_{N}_eps_00",
            f"Z_{N}_eps_02",
            "Z_eps_00",
            "Z_eps_02",
            "Z_shape",
        ]
    )
    column = next((name for name in candidates if name in df.columns), None)
    if column is None:
        raise KeyError(
            "No recognized significance column was found. "
            f"Tried: {candidates}."
        )
    values = pd.to_numeric(df[column], errors="coerce")
    if not values.notna().any():
        raise ValueError(f"Column {column!r} contains no finite numeric values.")
    row = df.loc[values.idxmax()]
    return row["pair"], int(row["mcut"])


def format_observable_label(observable):
    """Return a compact display label for common observables."""
    labels = {
        "m_tt": r"$m_{t\bar t}$",
        "pt_t": r"$p_T(t)$",
        "pt_tbar": r"$p_T(\bar t)$",
        "pt_tt": r"$p_T(t\bar t)$",
        "pT": r"$p_T$",
    }
    return labels.get(str(observable), str(observable))


def format_model_label(model_name):
    """Convert internal model labels to presentation-ready Matplotlib text."""
    formatted = str(model_name)
    formatted = formatted.replace("Zprime_20pcW", r"$Z^\prime$ $(\Gamma/M=0.2)$")
    formatted = formatted.replace("Zprime_20pc", r"$Z^\prime$ $(\Gamma/M=0.2)$")
    formatted = formatted.replace("Zprime", r"$Z^\prime$")
    formatted = formatted.replace("FakeData", "Fake Data")
    return formatted


def get_mass_label_from_fits(model_name, best_fits):
    """Return a mass label compatible with both old and revised fit dictionaries."""
    if not best_fits or model_name not in best_fits:
        return ""
    fit = best_fits[model_name]

    if model_name == "VLF":
        if "mPsiT" in fit:
            text = rf"$m_{{\psi_T}}={fit['mPsiT']:.0f}$ GeV"
            if "mSDM" in fit:
                text += rf", $m_{{\phi}}={fit['mSDM']:.0f}$ GeV"
            return text
        if "snap_m" in fit:
            return rf"$m_{{\psi_T}}={fit['snap_m']:.0f}$ GeV"

    if model_name == "Scalar":
        if "mST" in fit:
            text = rf"$m_{{\varphi_T}}={fit['mST']:.0f}$ GeV"
            if "mChi" in fit:
                text += rf", $m_{{\chi}}={fit['mChi']:.0f}$ GeV"
            return text
        if "snap_m" in fit:
            return rf"$m_{{\varphi_T}}={fit['snap_m']:.0f}$ GeV"

    if "Zprime" in model_name:
        mass_value = fit.get("mZp", fit.get("snap_m"))
        if mass_value is not None:
            return rf"$m_{{Z^\prime}}={mass_value:.0f}$ GeV"
    return ""


# ============================================================================
# Luminosity and mass-cut scans
# ============================================================================


def _signal_histogram(data, label, mask):
    """Return the scaled signal-only cross section for *label* in selected bins."""
    if label == "SM":
        return np.zeros(np.count_nonzero(mask), dtype=float)
    if label not in data["hists"]:
        return None
    signal = np.asarray(data["hists"][label], dtype=float)[mask].copy()
    int_key = f"{label}_int"
    if int_key in data["hists"]:
        signal += np.asarray(data["hists"][int_key], dtype=float)[mask]
    return signal


def _compute_pair_significances(
    true_total,
    test_total,
    n_sm,
    sys_err,
    *,
    alpha,
    allow_falloff=True,
):
    z_shape, _, _ = asimov_shape_Z_with_syst(
        true_total,
        test_total,
        frac_syst=sys_err,
        eps=alpha,
        syst_reference=n_sm,
    )

    if not allow_falloff:
        return np.nan, z_shape
    d_true = normalize_signed_template(
        build_signed_delta(true_total, n_sm, alpha=alpha), alpha=alpha
    )
    d_test = normalize_signed_template(
        build_signed_delta(test_total, n_sm, alpha=alpha), alpha=alpha
    )
    z_falloff, _, _ = asimov_signed_Z_rigorous(
        d_true,
        d_test,
        true_total,
        test_total,
        n_sm,
        sys_err,
        mode="test",
        alpha=alpha,
    )
    return z_falloff, z_shape


def run_fast_lumi_scan(
    fitted_data_by_lumi,
    labels,
    target_mcut=None,
    mcut_max=None,
    bin_width=None,
    lumi_targets=None,
    sys_err_list=None,
    var=None,
    alpha=1e-12,
    fake_model="FakeData",
    bin_offset=0.0,
    sig_norm=False,
    sm_cms=False,
    include_sm=True,
    *,
    observable=None,
    analysis_range=None,
):
    """Compute separation significances as a function of luminosity.

    This function is observable-independent. ``fitted_data_by_lumi[lumi]`` must
    contain outputs from :func:`fit_and_assemble_data` for the same observable.
    By default the significance is evaluated in the ``analysis_range`` stored by
    the fitter. A different range may be supplied explicitly.

    Parameters
    ----------
    observable : str, optional
        Expected observable name. If supplied, it is checked against the
        metadata stored by the fitter.
    analysis_range : (float, float), optional
        Fixed range used for the significance calculation. If omitted, the range
        saved by :func:`fit_and_assemble_data` is used.
    target_mcut, mcut_max : float, optional
        Legacy aliases for the lower and upper analysis bounds. They remain valid
        for old ``m_tt`` notebooks but should not be used in new observable-
        independent code.
    bin_width, var, bin_offset : optional
        Legacy arguments retained for API compatibility. No re-binning occurs;
        binning always comes from the selected observable workspace.

    Notes
    -----
    ``Z_sh`` is the profile-likelihood Asimov significance. ``Z_fa`` is the
    normalized-falloff significance and is reported as NaN for the SM test,
    because an L1-normalized signal falloff is undefined when the test excess is
    identically zero.
    """
    del bin_width, var, bin_offset
    if lumi_targets is None or sys_err_list is None:
        raise ValueError("lumi_targets and sys_err_list must be supplied.")
    if analysis_range is not None and (target_mcut is not None or mcut_max is not None):
        raise ValueError(
            "Use either analysis_range=(min, max) or legacy target_mcut/mcut_max, not both."
        )
    if (target_mcut is None) != (mcut_max is None):
        raise ValueError("Legacy target_mcut and mcut_max must be supplied together.")
    legacy_range = (target_mcut, mcut_max) if target_mcut is not None else None

    rows = {}
    test_labels = list(dict.fromkeys(labels))
    if include_sm and "SM" not in test_labels:
        test_labels.append("SM")

    for lum in lumi_targets:
        if lum not in fitted_data_by_lumi:
            raise KeyError(f"No fitted data is available for luminosity {lum}.")
        if lum <= 0:
            raise ValueError("Luminosities must be positive.")

        for sys_err in map(float, sys_err_list):
            sys_key = _resolve_sys_key(fitted_data_by_lumi[lum], sys_err)
            data = fitted_data_by_lumi[lum][sys_key]
            bins = _as_1d_float("bins", data["bins"])

            stored_observable = str(data.get("observable", "m_tt"))
            if observable is not None and stored_observable != str(observable):
                raise ValueError(
                    f"Requested observable={observable!r}, but fitted data for L={lum} "
                    f"contains observable={stored_observable!r}."
                )
            active_observable = str(observable) if observable is not None else stored_observable

            if analysis_range is not None:
                range_to_use = analysis_range
            elif legacy_range is not None:
                range_to_use = legacy_range
            else:
                range_to_use = data.get("analysis_range", data.get("fit_window"))

            analysis_min, analysis_max = _resolve_analysis_range(
                active_observable, bins, analysis_range=range_to_use
            )
            mask = (bins[:-1] >= analysis_min) & (bins[:-1] < analysis_max)

            sm_xsec = np.asarray(data["hists"]["SM"], dtype=float)[mask].copy()
            if sm_cms:
                # Legacy overall correction retained from the original analysis.
                sm_xsec *= 1.7 * 0.287
            n_sm = sm_xsec * lum * PB_TO_FB
            if np.sum(n_sm) <= 0:
                raise ValueError("SM yield is zero in the requested analysis window.")

            model_labels = list(dict.fromkeys(test_labels + [fake_model]))
            signals = {
                label: _signal_histogram(data, label, mask) for label in model_labels
            }
            signals = {k: v for k, v in signals.items() if v is not None}
            if fake_model not in signals:
                raise KeyError(f"Fake model {fake_model!r} is missing from fitted histograms.")

            signal_yields = {
                label: signal * lum * PB_TO_FB for label, signal in signals.items()
            }
            reference_signal = signal_yields[fake_model]
            if sig_norm:
                for label in list(signal_yields):
                    if label == "SM":
                        continue
                    signal_yields[label] = _match_integral(
                        reference_signal, signal_yields[label]
                    )

            totals = {
                label: n_sm.copy() if label == "SM" else n_sm + signal
                for label, signal in signal_yields.items()
            }
            true_total = totals[fake_model]

            for label in test_labels:
                if label == fake_model or label not in totals:
                    continue
                if np.any(totals[label] <= 0) or np.any(true_total < 0):
                    raise ValueError(
                        f"Non-positive Poisson expectation encountered for {label} at L={lum}."
                    )

                z_falloff, z_shape = _compute_pair_significances(
                    true_total,
                    totals[label],
                    n_sm,
                    sys_err,
                    alpha=alpha,
                    allow_falloff=(label != "SM"),
                )
                key = (lum, f"{fake_model} vs {label}")
                rows.setdefault(
                    key,
                    {
                        "lumi": lum,
                        "pair": key[1],
                        "observable": active_observable,
                        "analysis_min": analysis_min,
                        "analysis_max": analysis_max,
                    },
                )
                rows[key][f"Z_fa_eps_{int(round(100 * sys_err)):02d}"] = z_falloff
                rows[key][f"Z_sh_eps_{int(round(100 * sys_err)):02d}"] = z_shape

    return pd.DataFrame(rows.values())


def run_fast_mcut_scan(
    fitted_data_dict,
    labels,
    mcuts,
    mcut_max,
    bin_width,
    L_target,
    sys_err_list,
    var="m_tt",
    alpha=1e-12,
    fake_model="FakeData",
    bin_offset=0.0,
    sig_norm=False,
):
    """Compute separation significances while varying a lower observable threshold.

    Unlike the original implementation, this function consumes the same
    pre-binned ``{sys_err: {'hists', 'bins', ...}}`` structure returned by
    :func:`fit_and_assemble_data`; it does not expect obsolete ``df_sm`` and
    ``df_bsm`` entries.

    Despite the historical name ``run_fast_mcut_scan``, the function can operate
    on any observable represented by the supplied workspace. ``bin_width``,
    ``var``, and ``bin_offset`` are retained in the signature for backward
    compatibility. ``bin_width`` is checked against the stored regular
    binning when possible, while ``var`` and ``bin_offset`` are otherwise not
    needed because no re-binning is performed.
    """
    del var, bin_offset
    mcuts = np.asarray(mcuts, dtype=float)
    if mcuts.ndim != 1 or len(mcuts) == 0:
        raise ValueError("mcuts must be a non-empty one-dimensional sequence.")
    if L_target <= 0:
        raise ValueError("L_target must be positive.")
    if np.any(mcuts >= mcut_max):
        raise ValueError("Every lower mass cut must be smaller than mcut_max.")

    rows = {}
    model_labels = list(dict.fromkeys(list(labels) + [fake_model]))

    for sys_err in map(float, sys_err_list):
        sys_key = _resolve_sys_key(fitted_data_dict, sys_err)
        data = fitted_data_dict[sys_key]
        if "hists" not in data or "bins" not in data:
            raise KeyError(
                "run_fast_mcut_scan now expects the pre-binned output of "
                "fit_and_assemble_data (keys 'hists' and 'bins')."
            )

        bins = _as_1d_float("bins", data["bins"])
        widths = np.diff(bins)
        if bin_width is not None and np.allclose(widths, widths[0]):
            if not np.isclose(widths[0], float(bin_width), rtol=0, atol=1e-9):
                raise ValueError(
                    f"bin_width={bin_width} does not match stored width {widths[0]}."
                )

        sm_full = np.asarray(data["hists"]["SM"], dtype=float)
        if len(sm_full) != len(bins) - 1:
            raise ValueError("SM histogram length does not match stored bins.")

        signals_full = {}
        full_mask = (bins[:-1] >= np.min(mcuts)) & (bins[:-1] < mcut_max)
        for label in model_labels:
            signals_full[label] = _signal_histogram(data, label, full_mask)
        signals_full = {k: v for k, v in signals_full.items() if v is not None}
        if fake_model not in signals_full:
            raise KeyError(f"Fake model {fake_model!r} is missing from fitted histograms.")

        n_sm_full = sm_full[full_mask] * L_target * PB_TO_FB
        signal_yields = {
            label: signal * L_target * PB_TO_FB
            for label, signal in signals_full.items()
        }
        reference_signal = signal_yields[fake_model]
        if sig_norm:
            for label in list(signal_yields):
                if label == "SM":
                    continue
                signal_yields[label] = _match_integral(
                    reference_signal, signal_yields[label]
                )

        left_edges = bins[:-1][full_mask]
        for mcut in mcuts:
            cut = left_edges >= mcut
            if not np.any(cut):
                continue
            n_sm = n_sm_full[cut]
            totals = {
                label: n_sm.copy() if label == "SM" else n_sm + signal[cut]
                for label, signal in signal_yields.items()
            }
            true_total = totals[fake_model]

            for label in labels:
                if label == fake_model or label not in totals:
                    continue
                if np.any(totals[label] <= 0) or np.any(true_total < 0):
                    raise ValueError(
                        f"Non-positive Poisson expectation for {label} at mcut={mcut}."
                    )

                z_falloff, z_shape = _compute_pair_significances(
                    true_total,
                    totals[label],
                    n_sm,
                    sys_err,
                    alpha=alpha,
                    allow_falloff=(label != "SM"),
                )
                key = (float(mcut), f"{fake_model} vs {label}")
                rows.setdefault(key, {"mcut": float(mcut), "pair": key[1]})
                rows[key][f"Z_fa_eps_{int(round(100 * sys_err)):02d}"] = z_falloff
                rows[key][f"Z_sh_eps_{int(round(100 * sys_err)):02d}"] = z_shape

    return pd.DataFrame(rows.values())


# ============================================================================
# Plotting functions
# ============================================================================


def _validate_plot_results(results, x_column):
    if results is None or results.empty:
        raise ValueError("results is empty; nothing can be plotted.")
    for column in ("pair", x_column):
        if column not in results.columns:
            raise KeyError(f"results is missing required column {column!r}.")


def plot_mcut_syst_grid(
    results,
    mcut_max,
    eps_values,
    metric="sh",
    outfile=None,
    excl_stats=False,
    fake_model="FakeData",
    best_fits=None,
    *,
    show=True,
):
    """Plot significance versus the lower invariant-mass cut for each model pair."""
    _validate_plot_results(results, "mcut")
    if metric not in {"sh", "fa"}:
        raise ValueError("metric must be 'sh' (shape) or 'fa' (falloff).")

    styles = {
        0.00: ("black", "-"),
        0.02: ("#1f77b4", "--"),
        0.05: ("#ff7f0e", "-."),
        0.10: ("#d62728", ":"),
    }
    pairs = list(results["pair"].dropna().unique())
    fig, axes = plt.subplots(
        1, len(pairs), figsize=(5.0 * len(pairs), 5.2), sharex=True, squeeze=False
    )
    axes = axes.ravel().tolist()
    method_name = "Profile-likelihood shape method" if metric == "sh" else "Normalized falloff method"
    eps_to_plot = list(eps_values)[1:] if excl_stats else list(eps_values)

    for index, pair in enumerate(pairs):
        ax = axes[index]
        subset = results[results["pair"] == pair].sort_values("mcut")
        for eps_syst in eps_to_plot:
            column = f"Z_{metric}_eps_{int(round(100 * eps_syst)):02d}"
            if column not in subset.columns:
                continue
            color, linestyle = styles.get(eps_syst, (None, "-"))
            label = "stat. only" if eps_syst == 0 else f"{100 * eps_syst:g}% syst."
            ax.plot(
                subset["mcut"],
                subset[column],
                marker="o",
                color=color,
                linestyle=linestyle,
                label=label,
            )

        ax.axhline(3.0, color="gray", linestyle="--", alpha=0.7, linewidth=1.5, label=r"$Z=3$")
        ax.axhline(5.0, color="gray", linestyle=":", alpha=0.7, linewidth=1.5, label=r"$Z=5$")
        bsm_name = pair.split(" vs ")[-1]
        title = format_model_label(pair)
        mass_text = get_mass_label_from_fits(bsm_name, best_fits)
        if mass_text:
            title += f"\n[{mass_text}]"
        ax.set_title(title)
        if index == 0:
            ax.set_ylabel(r"Separation significance $Z$")
        ax.set_xlabel(rf"$m_{{t\bar t}}^{{\min}}$ to {mcut_max:g} GeV")
        ax.set_ylim(bottom=0)
        beautify_axis(ax, grid=True)

    handles, legend_labels = axes[-1].get_legend_handles_labels()
    by_label = dict(zip(legend_labels, handles))
    fig.legend(
        by_label.values(),
        by_label.keys(),
        loc="upper center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.93),
    )
    fig.suptitle(
        f"{method_name} — synthetic baseline: {format_model_label(fake_model)}",
        fontsize=16,
        y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    if outfile:
        fig.savefig(outfile, bbox_inches="tight", dpi=300)
    if show:
        plt.show()
    return fig, axes


def plot_lumi_syst_grid(
    results,
    eps_values,
    metric="sh",
    outfile=None,
    excl_stats=False,
    shareY=True,
    fake_model="FakeData",
    best_fits=None,
    max_cols=4,
    *,
    ylim=None,
    show=True,
):
    """Plot significance versus luminosity in one panel per model pair."""
    _validate_plot_results(results, "lumi")
    if metric not in {"sh", "fa"}:
        raise ValueError("metric must be 'sh' or 'fa'.")

    styles = {
        0.00: ("black", "-"),
        0.02: ("#1f77b4", "--"),
        0.05: ("#ff7f0e", "-."),
        0.10: ("#d62728", ":"),
    }
    pairs = list(results["pair"].dropna().unique())
    n_plots = len(pairs)
    if n_plots == 0:
        raise ValueError("No model pairs are present in results.")

    if n_plots == 5:
        n_rows = 2
        fig = plt.figure(figsize=(15, 10.4))
        gs = gridspec.GridSpec(2, 6, figure=fig)
        ax0 = fig.add_subplot(gs[0, 0:2])
        ax1 = fig.add_subplot(gs[0, 2:4], sharex=ax0, sharey=ax0 if shareY else None)
        ax2 = fig.add_subplot(gs[0, 4:6], sharex=ax0, sharey=ax0 if shareY else None)
        ax3 = fig.add_subplot(gs[1, 1:3], sharex=ax0, sharey=ax0 if shareY else None)
        ax4 = fig.add_subplot(gs[1, 3:5], sharex=ax0, sharey=ax0 if shareY else None)
        axes = [ax0, ax1, ax2, ax3, ax4]
        if shareY:
            for ax in (ax1, ax2, ax4):
                ax.tick_params(labelleft=False)
    else:
        n_cols = min(n_plots, max_cols)
        n_rows = int(np.ceil(n_plots / n_cols))
        fig, array = plt.subplots(
            n_rows,
            n_cols,
            figsize=(5.0 * n_cols, 5.2 * n_rows),
            sharex=True,
            sharey=shareY,
            squeeze=False,
        )
        axes = array.ravel().tolist()
        for extra in axes[n_plots:]:
            fig.delaxes(extra)
        axes = axes[:n_plots]

    method_name = "Profile-likelihood shape method" if metric == "sh" else "Normalized falloff method"
    eps_to_plot = list(eps_values)[1:] if excl_stats else list(eps_values)

    for index, pair in enumerate(pairs):
        ax = axes[index]
        subset = results[results["pair"] == pair].sort_values("lumi")
        for eps_syst in eps_to_plot:
            column = f"Z_{metric}_eps_{int(round(100 * eps_syst)):02d}"
            if column not in subset.columns:
                continue
            color, linestyle = styles.get(eps_syst, (None, "-"))
            label = "stat. only" if eps_syst == 0 else f"{100 * eps_syst:g}% syst."
            ax.plot(
                subset["lumi"],
                subset[column],
                marker="o",
                color=color,
                linestyle=linestyle,
                label=label,
            )

        ax.axhline(3.0, color="gray", linestyle="--", alpha=0.7, linewidth=1.5, label=r"$Z=3$")
        ax.axhline(5.0, color="gray", linestyle=":", alpha=0.7, linewidth=1.5, label=r"$Z=5$")
        if ylim is not None:
            ax.set_ylim(ylim)
        else:
            ax.set_ylim(bottom=0)

        bsm_name = pair.split(" vs ")[-1]
        title = format_model_label(pair)
        if bsm_name != "SM":
            mass_text = get_mass_label_from_fits(bsm_name, best_fits)
            if mass_text:
                title += f"\n[{mass_text}]"
        ax.set_title(title)

        if n_plots == 5:
            is_left = index in (0, 3)
            is_bottom = index >= 3
        else:
            n_cols = min(n_plots, max_cols)
            is_left = index % n_cols == 0
            is_bottom = index + n_cols >= n_plots
        if is_left or not shareY:
            ax.set_ylabel(r"Separation significance $Z$")
        if is_bottom:
            ax.set_xlabel(r"Integrated luminosity $\mathcal{L}$ [fb$^{-1}$]")
        beautify_axis(ax, grid=True)

    handles, legend_labels = axes[0].get_legend_handles_labels()
    by_label = dict(zip(legend_labels, handles))
    top_rect = 1.0 - 0.14 / n_rows
    fig.legend(
        by_label.values(),
        by_label.keys(),
        loc="center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, top_rect + 0.02 / n_rows),
    )
    observable_suffix = ""
    if "observable" in results.columns and results["observable"].nunique() == 1:
        observable_suffix = (
            f" | observable: {format_observable_label(results['observable'].iloc[0])}"
        )
    fig.suptitle(
        f"{method_name} — synthetic baseline: {format_model_label(fake_model)}"
        + observable_suffix,
        fontsize=16,
        y=1.0 - 0.02 / n_rows,
    )
    fig.tight_layout(rect=[0, 0, 1, top_rect])
    if outfile:
        fig.savefig(outfile, bbox_inches="tight", dpi=300)
    if show:
        plt.show()
    return fig, axes


def plot_lumi_syst_combined(
    results,
    eps_values,
    metric="sh",
    outfile=None,
    excl_stats=False,
    fake_model="FakeData",
    best_fits=None,
    *,
    ylim=None,
    show=True,
):
    """Plot all model-pair luminosity scans on one axis.

    Model identity is encoded by color and systematic uncertainty by line style.
    Two separate legends make both encodings explicit.
    """
    del best_fits  # currently not shown in this compact combined plot
    _validate_plot_results(results, "lumi")
    if metric not in {"sh", "fa"}:
        raise ValueError("metric must be 'sh' or 'fa'.")

    colors_tab = plt.cm.tab20.colors
    color_map = {
        "SM": "gray",
        "VLF": colors_tab[4],
        "Scalar": colors_tab[0],
        "Zprime": colors_tab[6],
        "Zprime_20pc": colors_tab[7],
        "FakeData": "black",
    }
    syst_styles = {0.00: "-", 0.02: "--", 0.05: "-.", 0.10: ":"}
    eps_to_plot = list(eps_values)[1:] if excl_stats else list(eps_values)

    fig, ax = plt.subplots(figsize=(8, 6))
    pairs = list(results["pair"].dropna().unique())
    model_handles = {}

    for pair in pairs:
        subset = results[results["pair"] == pair].sort_values("lumi")
        model_name = pair.split(" vs ")[-1]
        display_name = format_model_label(model_name)
        color = color_map.get(model_name, None)
        for eps_syst in eps_to_plot:
            column = f"Z_{metric}_eps_{int(round(100 * eps_syst)):02d}"
            if column not in subset.columns:
                continue
            line = ax.plot(
                subset["lumi"],
                subset[column],
                marker="o",
                color=color,
                linestyle=syst_styles.get(eps_syst, "-"),
                label="_nolegend_",
            )[0]
            model_handles.setdefault(display_name, line)

    ax.axhline(3.0, color="gray", linestyle="--", alpha=0.5, linewidth=1.0)
    ax.axhline(5.0, color="gray", linestyle=":", alpha=0.5, linewidth=1.0)
    ax.set_ylabel(r"Asimov significance $Z$" if metric == "sh" else r"Falloff significance $Z$")
    ax.set_xlabel(r"Integrated luminosity $\mathcal{L}$ [fb$^{-1}$]")
    if ylim is not None:
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(bottom=0)
    beautify_axis(ax, grid=True)

    model_legend = ax.legend(
        model_handles.values(),
        model_handles.keys(),
        title="Test hypothesis",
        loc="upper left",
        frameon=False,
    )
    ax.add_artist(model_legend)

    style_handles = []
    style_labels = []
    for eps_syst in eps_to_plot:
        style_handles.append(
            Line2D([0], [0], color="black", linestyle=syst_styles.get(eps_syst, "-"))
        )
        style_labels.append(
            "stat. only" if eps_syst == 0 else f"{100 * eps_syst:g}% syst."
        )
    ax.legend(
        style_handles,
        style_labels,
        title="Uncertainty",
        loc="upper right",
        frameon=False,
    )

    method = "Profile-likelihood shape method" if metric == "sh" else "Normalized falloff method"
    observable_suffix = ""
    if "observable" in results.columns and results["observable"].nunique() == 1:
        observable_suffix = (
            f" | observable: {format_observable_label(results['observable'].iloc[0])}"
        )
    fig.suptitle(
        f"{method} — synthetic data: {format_model_label(fake_model)}"
        + observable_suffix
    )
    fig.tight_layout()
    if outfile:
        fig.savefig(outfile, bbox_inches="tight", dpi=300)
    if show:
        plt.show()
    return fig, ax
