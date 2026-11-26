"""Asimov analysis of the extended MEM (ExtendedMEM.tex, Secs. 3-6).

Notation (all per Monte Carlo event j of the SM sample):
    w_j        normalised weight [pb]                         (sum_j w_j = sigma_SM in the sample region)
    r_H(x_j)   = dsigma_H/dsigma_SM = 1 + theta a_H + theta^2 b_H
    a_H, b_H   = sum_c F_c |M_SM,c|^2 rho^H_c / sum_c F_c |M_SM,c|^2

Every likelihood quantity is a sum over "cells" k of
    n_k(r) = L * sum_{j in k} w_j r(x_j)
The unbinned analysis uses one cell per event; the binned analysis groups the
events in p_T bins (the published analysis). The same code serves both:
    deviance(H | T) = 2 sum_k [n_k(r_H) - n_k(r_T) + n_k(r_T) ln(n_k(r_T)/n_k(r_H))]
Step A: (theta_hat, M_hat) = argmin deviance(H | truth)       [luminosity independent]
Step B: q_A = deviance(H0_hat | H1_hat),  Z_A = sqrt(q_A)      [proportional to L]
"""
import json
import os

import h5py
import numpy as np
from scipy.optimize import minimize_scalar

from . import config as cfg

FB = 1000.0      # pb -> fb: n = L[fb^-1] * 1000 * sigma[pb]


# ====================================================================== sample
class Sample:
    """SM Monte Carlo sample with the per-event ingredients of the density ratios.

    flux_mode : 'abs' (default) -- MadEvent convention |f_a f_b| per ordered flavour pair
                (ExtendedMEM.tex, Eq. lumi). The aMC@NLO generator sampled the SIGNED density,
                so the weights are corrected by D_abs/D_signed (all weights become positive).
                'signed' -- signed PDF products. Where the negative large-x gluon nearly cancels
                the q qbar term, D_SM -> 0 and r_H blows up (up to ~8 for the Scalar benchmark):
                a PDF artefact; kept only as a variation.
    muF_index : 0, 1, 2 for mu_F = (0.5, 1, 2) mu0 (systematics; 1 = nominal)
    xcut      : optional max(x1, x2) < xcut acceptance
    """

    def __init__(self, events_path, flux_mode="abs", muF_index=1, xcut=None):
        self.path = os.path.abspath(events_path)
        d, b = os.path.split(self.path)
        self.suffix = b[len("events"):]
        self.dir = d
        with h5py.File(self.path, "r") as h:
            self.meta = json.loads(h.attrs["meta"])
            w = h["w"][:]
            pt = h["pt"][:].astype(np.float64)
            mtt = h["mtt"][:]
            x1, x2 = h["x1"][:], h["x2"][:]
            F = h["flux"][:, muF_index, :].astype(np.float64)
            self.gen_scale = h["gen_scale"][:] if "gen_scale" in h else None
            chan = h["channel"][:]
        with h5py.File(self.me_file("Scalar"), "r") as h:
            born = h["born"][:]
        mask = np.ones(len(w), dtype=bool)
        if xcut is not None:
            mask &= np.maximum(x1, x2) < xcut
        self.mask = mask
        self.flux_mode, self.xcut, self.muF_index = flux_mode, xcut, muF_index
        g = {name: i for i, name in enumerate(cfg.FLUX_GROUPS)}
        self.groups = g
        Fs = F[mask]
        Fe = np.abs(Fs) if flux_mode == "abs" else Fs
        self.Bgg, self.Bqq = born[mask, 0], born[mask, 1]
        self.Fgg = Fe[:, g["gg"]]
        self.Fqq = sum(Fe[:, g[f"{q}_{o}"]] for q in cfg.QUARKS for o in ("fw", "bw"))
        self.Fq = {f"{q}_{o}": Fe[:, g[f"{q}_{o}"]] for q in cfg.QUARKS for o in ("fw", "bw")}
        self.D = self.Fgg * self.Bgg + self.Fqq * self.Bqq
        if flux_mode == "abs":
            # Each generated event comes from ONE integration channel and its weight follows that
            # channel's signed density, so the conversion |f f| / f f is applied channel by channel.
            # The q qbar channels are oriented (uux: quark from beam 1, uxu: quark from beam 2).
            def orient(F_, o):
                return sum(F_[:, g[f"{q}_{o}"]] for q in cfg.QUARKS)
            c = chan[mask]
            corr = np.where(c == 0, self.Fgg / Fs[:, g["gg"]],
                            np.where(c == 1, orient(Fe, "fw") / orient(Fs, "fw"), orient(Fe, "bw") / orient(Fs, "bw")))
            self.w = w[mask] * corr
        else:
            self.w = w[mask]
        self.pt, self.mtt = pt[mask], mtt[mask]
        self.x1, self.x2 = x1[mask], x2[mask]
        self.s = self.mtt ** 2
        self.omega_gg = self.Fgg * self.Bgg / self.D           # SM fraction of the gg channel
        self._hyp = {}

    def me_file(self, model):
        return os.path.join(self.dir, f"me_{model}{self.suffix}")

    @property
    def sigma(self):
        return float(self.w.sum())

    @property
    def n_eff(self):
        return float(self.w.sum() ** 2 / np.sum(self.w ** 2))

    def hypothesis(self, name):
        """name in {'SM', 'Scalar', 'VLF', 'Zp01', 'Zp20'}."""
        if name not in self._hyp:
            if name == "SM":
                self._hyp[name] = SMHyp(self)
            elif name in cfg.LOOP_MODELS:
                self._hyp[name] = LoopHyp(self, name)
            elif name in cfg.ZP_WIDTHS:
                if "Zprime" not in self._hyp:
                    self._hyp["Zprime"] = ZpKin(self)
                self._hyp[name] = ZpHyp(self._hyp["Zprime"], name, cfg.ZP_WIDTHS[name])
            else:
                raise KeyError(name)
        return self._hyp[name]

    def r(self, name, theta, M):
        a, b = self.hypothesis(name).coeffs(M)
        return 1.0 + theta * a + (theta ** 2 * b if b is not None else 0.0)

    def r_benchmark(self, key):
        bm = cfg.BENCHMARKS[key]
        return self.r(bm["model"], bm["theta"], bm["M"])


class SMHyp:
    kind = "SM"
    masses = np.array([0.0])

    def __init__(self, sample):
        self.zero = np.zeros_like(sample.w)

    def coeffs(self, M):
        return self.zero, None


class LoopHyp:
    """Scalar / VLF: r = 1 + theta a(M), a linear in rho -> linear interpolation in M is exact
    for linearly interpolated rho (ExtendedMEM.tex, Sec. 5)."""
    kind = "loop"

    def __init__(self, sample, model):
        self.name = model
        with h5py.File(sample.me_file(model), "r") as h:
            self.masses = np.asarray(h.attrs["masses"], dtype=float)
            if not (h["done_gg"][:].all() and h["done_qq"][:].all()):
                raise RuntimeError(f"{sample.me_file(model)} is incomplete")
            m = sample.mask
            cgg = (sample.Fgg * sample.Bgg / sample.D).astype(np.float64)
            cqq = (sample.Fqq * sample.Bqq / sample.D).astype(np.float64)
            self.a = np.empty((len(self.masses), m.sum()), dtype=np.float32)
            for i in range(len(self.masses)):
                self.a[i] = cgg * h["rho_gg"][i][m] + cqq * h["rho_qq"][i][m]
        if not np.all(np.isfinite(self.a)):
            raise RuntimeError(f"non-finite coefficients for {model}")

    def coeffs(self, M):
        Ms = self.masses
        if not Ms[0] <= M <= Ms[-1]:
            raise ValueError(f"M = {M} outside the grid [{Ms[0]}, {Ms[-1]}]")
        i = min(np.searchsorted(Ms, M, side="right") - 1, len(Ms) - 2)
        t = (M - Ms[i]) / (Ms[i + 1] - Ms[i])
        if t == 0.0:
            return self.a[i].astype(np.float64), None
        return ((1 - t) * self.a[i] + t * self.a[i + 1]).astype(np.float64), None


class ZpKin:
    """PDF-weighted Z' kinematic functions (sum over u, d and both orientations) / D_SM."""

    def __init__(self, sample):
        self.s = sample.s
        m = sample.mask
        K = R = I = 0.0
        with h5py.File(sample.me_file("Zprime"), "r") as h:
            if not all(h[k][:].all() for k in h if k.startswith("done")):
                raise RuntimeError(f"{sample.me_file('Zprime')} is incomplete")
            for q in cfg.ZP_SUBDIRS:
                for o in ("fw", "bw"):
                    F = sample.Fq[f"{q}_{o}"]
                    K = K + F * h[f"{q}_{o}/K"][:][m]
                    R = R + F * h[f"{q}_{o}/R"][:][m]
                    I = I + F * h[f"{q}_{o}/I"][:][m]
        self.K, self.R, self.I = K / sample.D, R / sample.D, I / sample.D


class ZpHyp:
    """Z' with Gamma = frac * M: r = 1 + theta a(M) + theta^2 b(M), exact in M."""
    kind = "zp"

    def __init__(self, kin, name, frac):
        self.kin, self.name, self.frac = kin, name, frac
        self.masses = np.asarray(cfg.ZP_MASSES, dtype=float)

    def coeffs(self, M):
        G = self.frac * M
        s = self.kin.s
        D = (s - M ** 2) ** 2 + (M * G) ** 2
        return ((s - M ** 2) * self.kin.R + M * G * self.kin.I) / D, self.kin.K / D


# ====================================================================== cells (binned / unbinned)
class Cells:
    """Aggregation of per-event quantities: one cell per event (bins=None) or p_T bins."""

    def __init__(self, sample, bins=None, var="pt"):
        self.sample = sample
        self.w = sample.w
        self.bins = None if bins is None else np.asarray(bins, dtype=float)
        if self.bins is None:
            self.idx = None
            self.keep = np.ones(len(self.w), dtype=bool)
        else:
            x = getattr(sample, var)
            k = np.digitize(x, self.bins) - 1
            self.keep = (k >= 0) & (k < len(self.bins) - 1)
            self.idx = k[self.keep]
            self.nb = len(self.bins) - 1

    def agg(self, x):
        """sum_{j in cell} w_j x_j  (x may be None -> 1)."""
        v = self.w if x is None else self.w * x
        if self.idx is None:
            return v
        return np.bincount(self.idx, weights=v[self.keep], minlength=self.nb)

    def template(self, name, M):
        """(W, WA, WB) such that n(theta) / L = W + theta WA + theta^2 WB."""
        a, b = self.sample.hypothesis(name).coeffs(M)
        return self.agg(None), self.agg(a), (self.agg(b) if b is not None else None)

    def counts(self, r):
        return self.agg(r)


def deviance(nH, nT, lumi):
    """2 sum [nH - nT + nT ln(nT/nH)] with n = lumi * 1000 * (cell sums). Cells with nT = nH = 0
    are ignored; nH must have the sign of nT wherever nT != 0."""
    ok = (nT != 0) | (nH != 0)
    nH, nT = nH[ok], nT[ok]
    ratio = nT / nH
    if np.any(ratio <= 0) or not np.all(np.isfinite(ratio)):
        return np.inf
    return 2.0 * lumi * FB * float(np.sum(nH - nT + nT * np.log(ratio)))


def deviance_terms(nH, nT):
    """Per-cell deviance contributions (for L = 1 fb^-1 / 1000), used for the bootstrap."""
    with np.errstate(divide="ignore", invalid="ignore"):
        t = nH - nT + nT * np.log(nT / nH)
    return np.where((nT == 0) & (nH == 0), 0.0, t)


# ====================================================================== Step A
def theta_range(name):
    if name in cfg.LOOP_MODELS:
        return 0.0, (4 * np.pi) ** 2                 # theta = y_DM^2, perturbativity y_DM < 4 pi
    return -2.0, 2.0                                 # theta = g_q g_t


class _ThetaProblem:
    """chi2(theta) = 2 L sum_k [nH - nT + nT ln(nT/nH)],  nH = W + theta WA + theta^2 WB  (per L),
    with its exact first and second derivatives (ExtendedMEM.tex, Sec. 5)."""

    def __init__(self, W, WA, WB, nT, lumi):
        ok = (nT != 0) | (W != 0)
        self.W, self.WA = W[ok], WA[ok]
        self.WB = WB[ok] if WB is not None else None
        self.nT = nT[ok]
        self.c = 2.0 * lumi * FB
        self.calls = 0

    def nH(self, th):
        n = self.W + th * self.WA
        return n + th * th * self.WB if self.WB is not None else n

    def value(self, th):
        self.calls += 1
        return deviance(self.nH(th), self.nT, 1.0) * self.c / (2.0 * FB)

    def derivs(self, th):
        """(chi2, d chi2/d theta, d2 chi2/d theta2); chi2 = inf outside the physical region."""
        self.calls += 1
        nH = self.nH(th)
        ratio = self.nT / nH
        if np.any(ratio < 0) or not np.all(np.isfinite(ratio)):
            return np.inf, 0.0, 0.0
        dn = self.WA + 2.0 * th * self.WB if self.WB is not None else self.WA
        one_m = 1.0 - ratio
        with np.errstate(divide="ignore", invalid="ignore"):
            lg = np.where(self.nT != 0, self.nT * np.log(np.where(ratio > 0, ratio, 1.0)), 0.0)
        f = self.c * float(np.sum(nH - self.nT + lg))
        # element-wise sums, not np.dot: dot uses multithreaded BLAS, which oversubscribes the cores
        # when several truths run in parallel
        d1 = self.c * float(np.sum(dn * one_m))
        d2 = self.c * float(np.sum(self.nT * (dn / nH) ** 2))
        if self.WB is not None:
            d2 += self.c * float(np.sum(2.0 * self.WB * one_m))
        return f, d1, d2


def _newton(prob, th0, lo, hi, tol=1e-10, maxit=60):
    """Projected Newton with backtracking on [lo, hi]. Returns (theta, chi2, converged)."""
    th = float(np.clip(th0, lo, hi))
    f, d1, d2 = prob.derivs(th)
    if not np.isfinite(f):
        return th, f, False
    for _ in range(maxit):
        if d2 <= 0:
            return th, f, False                                    # not locally convex: let the caller decide
        step = -d1 / d2
        if (th <= lo and step < 0) or (th >= hi and step > 0):
            return th, f, True                                     # minimum on the boundary
        t = 1.0
        while True:
            th_new = float(np.clip(th + t * step, lo, hi))
            f_new, d1_new, d2_new = prob.derivs(th_new)
            if np.isfinite(f_new) and f_new <= f + 1e-12 * abs(f):
                break
            t *= 0.5
            if t < 1e-8:
                return th, f, abs(d1) * abs(step) < 1e-9 * max(1.0, abs(f))
        converged = abs(th_new - th) <= tol * max(1.0, abs(th_new))
        th, f, d1, d2 = th_new, f_new, d1_new, d2_new
        if converged:
            return th, f, True
    return th, f, False


SEED_EVENTS = 100_000      # Z' starting points are searched on a stride of about this many events


def fit_theta(cells, name, M, nT, lumi, theta0=None):
    """Best theta at fixed mass. Loop models: chi2 is convex in theta (positive weights), so a few
    Newton steps from a linearised estimate suffice. Z': chi2 is a quartic and can have several
    minima; candidate starting points come from a scan on an event stride, each is refined with
    Newton on all cells, and the best is kept. Brent's method is the fallback."""
    W, WA, WB = cells.template(name, M)
    lo, hi = theta_range(name)
    prob = _ThetaProblem(W, WA, WB, nT, lumi)
    if WB is None:
        with np.errstate(divide="ignore", invalid="ignore"):
            neg = (prob.W != 0) & ((prob.WA / prob.W) < 0)
        if np.any(neg):
            hi = min(hi, 0.999 * np.min(-prob.W[neg] / prob.WA[neg]))
        if theta0 is None:            # linearised (Pearson) estimate
            pos = prob.nT > 0
            den = np.sum(prob.WA[pos] ** 2 / prob.nT[pos])
            theta0 = np.sum(prob.WA[pos] * (prob.nT[pos] - prob.W[pos]) / prob.nT[pos]) / den if den > 0 else lo
        th, f, ok = _newton(prob, theta0, lo, hi)
        if ok:
            return th, f
        res = minimize_scalar(prob.value, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6 * max(1.0, hi)))
        return float(res.x), float(res.fun)

    # ---- Z': candidate minima from a scan on a stride of the cells
    n = len(prob.W)
    k = max(1, n // SEED_EVENTS)
    seed = prob if k == 1 else _ThetaProblem(prob.W[::k] * k, prob.WA[::k] * k, prob.WB[::k] * k,
                                             prob.nT[::k] * k, lumi)
    grid = np.sinh(np.linspace(np.arcsinh(lo / 1e-4), np.arcsinh(hi / 1e-4), 101)) * 1e-4
    vals = np.array([seed.value(t) for t in grid])
    finite = np.isfinite(vals)
    is_min = finite & (vals <= np.r_[np.inf, vals[:-1]]) & (vals <= np.r_[vals[1:], np.inf])
    cand = np.where(is_min)[0]
    cand = cand[np.argsort(vals[cand])][:3] if len(cand) else np.array([int(np.nanargmin(np.where(finite, vals, np.nan)))])
    best = (None, np.inf)
    for i in cand:
        a, b = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
        th, f, ok = _newton(prob, grid[i], lo, hi)
        if not ok or not (a - abs(b - a) <= th <= b + abs(b - a)):
            res = minimize_scalar(prob.value, bounds=(a, b), method="bounded", options=dict(xatol=1e-9))
            th, f = float(res.x), float(res.fun)
        if f < best[1]:
            best = (th, f)
    return float(best[0]), float(best[1])


def fit_hypothesis(cells, name, nT, lumi, masses=None):
    """Profile over the mass grid, parabola through the three lowest points, theta refit at M_hat."""
    hyp = cells.sample.hypothesis(name)
    if name == "SM":
        return dict(model=name, M=np.nan, theta=0.0, chi2=deviance(cells.agg(None), nT, lumi),
                    grid=None, profile=None)
    Ms = np.asarray(masses if masses is not None else hyp.masses, dtype=float)
    prof, th_prev = [], None
    for M in Ms:                                  # loop models: start from the neighbouring mass
        th, c2 = fit_theta(cells, name, M, nT, lumi, theta0=th_prev if name in cfg.LOOP_MODELS else None)
        prof.append((th, c2))
        th_prev = th
    prof = np.array(prof)
    chi = prof[:, 1]
    i = int(np.argmin(chi))
    j = min(max(i - 1, 0), len(Ms) - 3)
    Mw, cw = Ms[j:j + 3], chi[j:j + 3]
    if name in cfg.LOOP_MODELS and i in (0, len(Ms) - 1):
        print(f"[warn] {name}: best grid mass {Ms[i]:.0f} GeV is on the edge of the computed window "
              f"[{Ms[0]:.0f}, {Ms[-1]:.0f}]: extend cfg.LOOP_MODELS['{name}']['masses']", flush=True)
    A = np.polyfit(Mw, cw, 2)
    best = dict(M=float(Ms[i]), theta=float(prof[i, 0]), chi2=float(chi[i]))
    if A[0] > 0:
        Mh = float(np.clip(-A[1] / (2 * A[0]), Ms[0], Ms[-1]))
        th, c2 = fit_theta(cells, name, Mh, nT, lumi)
        if c2 <= best["chi2"]:
            best = dict(M=Mh, theta=th, chi2=c2)
    return dict(model=name, **best, grid=Ms, profile=prof)


def r_of(sample, fit):
    return sample.r(fit["model"], fit["theta"], fit["M"]) if fit["model"] != "SM" else np.ones_like(sample.w)


# ====================================================================== Step B
def q_asimov(cells, r0, r1, lumi):
    """q_A = deviance(H0 | H1) for frozen hypotheses (Asimov data = H1)."""
    return deviance(cells.counts(r0), cells.counts(r1), lumi)


def bootstrap_q(cells, r0, r1, lumi, nboot=200, seed=1):
    """MC-statistics spread of q_A at fixed best fits: Poisson(1) resampling of the events."""
    if cells.idx is not None:
        raise ValueError("bootstrap implemented for unbinned cells")
    terms = deviance_terms(cells.w * r0, cells.w * r1)
    rng = np.random.default_rng(seed)
    q = np.array([2.0 * lumi * FB * np.dot(rng.poisson(1.0, len(terms)), terms) for _ in range(nboot)])
    return q


# ====================================================================== full analysis
def run_analysis(sample, truth, hypotheses, lumi=500.0, bins=None, step_a_cells=None, verbose=True):
    """Step A + Step B for one truth benchmark.

    bins=None -> unbinned; otherwise the binning (p_T) used in both steps unless
    step_a_cells is given (e.g. binned fits with unbinned q_A).
    Returns dict with best fits and Z_A at `lumi` for every (H0, H1 = truth model).
    """
    cells = Cells(sample, bins)
    cells_a = step_a_cells or cells
    rT = sample.r_benchmark(truth)
    nT_a = cells_a.counts(rT)
    fits = {}
    for h in hypotheses:
        fits[h] = fit_hypothesis(cells_a, h, nT_a, lumi)
        if verbose:
            f = fits[h]
            print(f"  [{truth} truth] {h:7s} M = {f['M']:8.1f}  theta = {f['theta']:+.5g}  chi2 = {f['chi2']:.4g}",
                  flush=True)
    h1 = cfg.BENCHMARKS[truth]["model"]
    r1 = r_of(sample, fits[h1]) if h1 in fits else rT
    Z = {}
    for h in hypotheses:
        if h == h1:
            continue
        q = q_asimov(cells, r_of(sample, fits[h]), r1, lumi)
        Z[h] = np.sqrt(max(q, 0.0))
    return dict(truth=truth, lumi=lumi, fits=fits, Z=Z, r1=r1, binned=bins is not None)


_SHARED = {}


def _truth_worker(args):
    truth, hyps, lumi, bins = args
    return run_analysis(_SHARED["sample"], truth, hyps, lumi=lumi, bins=bins, verbose=False)


def run_truths(sample, truths, hypotheses, lumi=500.0, bins=None, nproc=None):
    """run_analysis for several truths in parallel. The per-hypothesis coefficients are computed
    once in the parent and shared with the forked workers (copy-on-write, no pickling)."""
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    for h in hypotheses:
        sample.hypothesis(h)
    _SHARED["sample"] = sample
    nproc = min(len(truths), nproc or os.cpu_count() or 1)
    if nproc == 1:
        return {t: _truth_worker((t, hypotheses, lumi, bins)) for t in truths}
    with ProcessPoolExecutor(nproc, mp_context=mp.get_context("fork")) as ex:
        res = list(ex.map(_truth_worker, [(t, hypotheses, lumi, bins) for t in truths]))
    return dict(zip(truths, res))
