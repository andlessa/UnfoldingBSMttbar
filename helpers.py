"""
helpers.py

Core physics functions for High Energy Physics (HEP) phenomenology.
Includes LHE file parsing, kinematic derivations, template normalizations,
and rigorous Asimov significance calculations (Standard Shape and Falloff).
"""

import os
import gzip
import urllib.request
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

# ============================================================
# Data Acquisition & Management
# ============================================================

def download_data_files(base_url, files_dict, out_dir="data"):
    """Fetches LHE files from a remote repository if not found locally."""
    os.makedirs(out_dir, exist_ok=True)
    for name, url in files_dict.items():
        out = os.path.join(out_dir, f"{name}.lhe.gz")
        if not os.path.exists(out):
            urllib.request.urlretrieve(url, out)

# ============================================================
# Kinematics & Parsing
# ============================================================

def mass(E, px, py, pz):
    """Calculates invariant mass from a 4-momentum vector."""
    m2 = E*E - px*px - py*py - pz*pz
    return np.sqrt(max(m2, 0.0))

def parse_event_block(lines, rescale_weight_by=1.0):
    """
    Parses a single <event> block from an LHE file to extract top and 
    anti-top kinematics, returning an event-level dictionary.
    """
    content = [ln.strip() for ln in lines if ln.strip()]
    if not content:
        return None

    header = content[0].split()
    nup = int(header[0])
    xwgtup = float(header[2]) * rescale_weight_by

    particles = []
    for ln in content[1:1+nup]:
        cols = ln.split()
        if len(cols) < 13: continue
        particles.append({
            "pid": int(cols[0]), "status": int(cols[1]),
            "px": float(cols[6]), "py": float(cols[7]), "pz": float(cols[8]),
            "E":  float(cols[9])
        })

    final = [p for p in particles if p["status"] == 1]
    tops  = [p for p in final if p["pid"] == 6]
    tbars = [p for p in final if p["pid"] == -6]
    
    if not tops or not tbars:
        return None

    t, tb = tops[0], tbars[0]
    t4  = np.array([t["E"], t["px"], t["py"], t["pz"]], dtype=float)
    tb4 = np.array([tb["E"], tb["px"], tb["py"], tb["pz"]], dtype=float)
    tt4 = t4 + tb4

    return {
        "weight": xwgtup,
        "m_tt": mass(*tt4)
    }

def read_lhe_features(filepath, label=None, max_events=None, rescale_weight_by=1.0):
    """Iterates through an LHE file compiling event features into a DataFrame."""
    rows, block, in_event = [], [], False
    opener = gzip.open if filepath.endswith(".gz") else open
    
    with opener(filepath, "rt", encoding="utf-8", errors="ignore") as f:
        for line in tqdm(f, desc=f"Reading {os.path.basename(filepath)}"):
            if "<event>" in line:
                in_event = True
                block = []
                continue
            if "</event>" in line:
                rec = parse_event_block(block, rescale_weight_by)
                if rec is not None:
                    if label is not None: rec["label"] = label
                    rows.append(rec)
                    if max_events and len(rows) >= max_events: break
                in_event = False
                continue
            if in_event:
                block.append(line)

    return pd.DataFrame(rows)

# ============================================================
# Histogram & Template Operations
# ============================================================

def weighted_hist(x, w, bins):
    """Generates a standard weighted histogram array."""
    h, _ = np.histogram(x, bins=bins, weights=np.abs(w))
    return h.astype(float)

def event_number_normalization(h_ref, h, lum=500.0):
    """Scales a template to match absolute expected event yields."""
    n_ref = lum * np.asarray(h_ref, dtype=float) * 1000.0
    n = lum * np.asarray(h, dtype=float) * 1000.0
    return n * sum(n_ref) / sum(n) if sum(n) != 0 else n

def build_signed_delta(h_hyp, h_sm, alpha=1e-12):
    """Calculates the bin-by-bin fractional difference from the Standard Model."""
    return (h_hyp - h_sm) / (h_sm + alpha)

def normalize_signed_template(delta, alpha=1e-12):
    """Normalizes the signed difference array to isolate shape from overall rate."""
    norm = np.sum(np.abs(delta))
    return delta / norm if norm > alpha else None

# ============================================================
# Variance and Significance Calculations
# ============================================================

def calc_variance_hat_delta(h_hyp, h_sm, eps, alpha=1e-12):
    """
    Computes the rigorous propagated variance for the normalized signed difference.
    Includes both the local per-bin variance term and the global leakage term.
    """
    n_hyp = h_hyp
    n_sm = h_sm
    delta = (n_hyp - n_sm) / (n_sm + alpha)
    S = np.sum(np.abs(delta)) + alpha
    
    sigma2_delta = (n_hyp / (n_sm**2 + alpha)) + (n_hyp**2 * eps**2) / (n_sm**2 + alpha)
    bracket_i = (1.0 / S**2) - (2.0 * np.abs(delta) / S**3) + (delta**2 / S**4)
    term_same = bracket_i * sigma2_delta
    
    sum_sigma2_j_neq_i = np.sum(sigma2_delta) - sigma2_delta
    term_diff = (delta**2 / S**4) * sum_sigma2_j_neq_i
    
    return term_same + term_diff

def asimov_signed_Z_rigorous(dA, dB, hA, hB, n_sm, eps, alpha=1e-12):
    """
    Calculates the separation significance using the Normalized Falloff Method.
    Returns the total Z score, along with the raw numerator and denominator arrays.
    """
    var_hat_A = calc_variance_hat_delta(hA, n_sm, eps, alpha=alpha)
    var_hat_B = calc_variance_hat_delta(hB, n_sm, eps, alpha=alpha)
    
    var_n_ref = (1/2)**2 * (var_hat_A + var_hat_B)
    num = (dA - dB)**2
    den = var_n_ref + alpha
    
    return np.sqrt(max(np.sum(num / den), 0.0)), num, den

def asimov_shape_Z_with_syst(n_true, n_test, frac_syst=0.05, eps=1e-12):
    """
    Calculates the separation significance using the Standard Shape Method.
    Returns the total Z score, along with the raw numerator and denominator arrays.
    """
    n_true = np.asarray(n_true, dtype=float) + eps
    n_test = np.asarray(n_test, dtype=float) + eps

    n_ref = 0.5 * (n_true + n_test)
    var = n_ref + (frac_syst * n_ref)**2
    num = (n_true - n_test)**2
    
    return np.sqrt(max(np.sum(num / var), 0.0)), num, var

# ============================================================
# Plotting Utilities
# ============================================================

def beautify_axis(ax, grid=False):
    """Applies a clean, scientific styling to matplotlib axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="in", top=False, right=False, length=5)
    if grid:
        ax.grid(True, alpha=0.22, linewidth=0.7)