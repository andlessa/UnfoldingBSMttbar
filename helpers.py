"""
helpers.py

Core physics functions for High Energy Physics (HEP) phenomenology.
Includes LHE file parsing, kinematic derivations, template normalizations,
and rigorous Asimov significance calculations (Standard Shape and Falloff).
"""

import os
import gzip
import urllib.request
import glob
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

SQRT_S = 13000.0  # Center of mass energy in GeV

# ============================================================
# Data Acquisition & Management
# ============================================================

def download_data_files(base_url, files_dict, out_dir="data"):
    """Fetches LHE files from a remote repository if not found locally."""
    os.makedirs(out_dir, exist_ok=True)
    for name, url in files_dict.items():
        out = os.path.join(out_dir, f"{name}.lhe.gz")
        if not os.path.exists(out):
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(url, out)
        else:
            print(f"{out} already exists")

def load_model_data(base_path, model_name, rescale=1.0):
    """
    Finds all .npz files for a model (including qq and gg subprocesses),
    applies the rescale factor, and returns a single DataFrame.
    """
    file_pattern = f"{base_path}/*{model_name}*.npz"
    files = glob.glob(file_pattern)

    if not files:
        print(f"Warning: No files found for {model_name} at {base_path}")
        return pd.DataFrame(columns=['m_tt', 'weight', 'label'])

    mtt_list = []
    w_list = []

    for f in files:
        data = np.load(f, allow_pickle=True)
        mtt_list.append(data['mTT'])
        w_list.append(data['weights'] * rescale)

    df = pd.DataFrame({
        'm_tt': np.concatenate(mtt_list),
        'weight': np.concatenate(w_list)
    })
    df['label'] = model_name
    return df

# ============================================================
# Kinematics & Parsing
# ============================================================

def rapidity(E, pz, eps=1e-12):
    num = E + pz
    den = E - pz
    if num <= eps or den <= eps:
        return np.nan
    return 0.5 * np.log(num / den)

def pt(px, py):
    return np.hypot(px, py)

def phi(px, py):
    return np.arctan2(py, px)

def delta_phi(phi1, phi2):
    d = phi1 - phi2
    return (d + np.pi) % (2*np.pi) - np.pi

def mass(E, px, py, pz):
    """Calculates invariant mass from a 4-momentum vector."""
    m2 = E*E - px*px - py*py - pz*pz
    return np.sqrt(max(m2, 0.0))

def boost_to_rest_frame(p4, parent):
    """Boosts p4=(E,px,py,pz) into the rest frame of parent=(E,px,py,pz)."""
    E, px, py, pz = p4
    EP, Px, Py, Pz = parent
    bx, by, bz = Px/EP, Py/EP, Pz/EP
    b2 = bx*bx + by*by + bz*bz
    if b2 >= 1.0 or b2 < 1e-16:
        return np.array([E, px, py, pz], dtype=float)
    gamma = 1.0 / np.sqrt(1.0 - b2)
    bp = bx*px + by*py + bz*pz
    gamma2 = (gamma - 1.0) / b2
    pxp = px + (-gamma * E + gamma2 * bp) * bx
    pyp = py + (-gamma * E + gamma2 * bp) * by
    pzp = pz + (-gamma * E + gamma2 * bp) * bz
    Ep  = gamma * (E - bp)
    return np.array([Ep, pxp, pyp, pzp], dtype=float)

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
            "E":  float(cols[9]), "M": float(cols[10])
        })

    incoming = [p for p in particles if p["status"] == -1]
    final = [p for p in particles if p["status"] == 1]
    tops  = [p for p in final if p["pid"] == 6]
    tbars = [p for p in final if p["pid"] == -6]
    
    if not tops or not tbars:
        return None

    t, tb = tops[0], tbars[0]
    t4  = np.array([t["E"], t["px"], t["py"], t["pz"]], dtype=float)
    tb4 = np.array([tb["E"], tb["px"], tb["py"], tb["pz"]], dtype=float)
    tt4 = t4 + tb4

    mt  = mass(*t4)
    mtb = mass(*tb4)
    mtt = mass(*tt4)

    pt_t  = pt(t["px"], t["py"])
    pt_tb = pt(tb["px"], tb["py"])
    pt_tt = pt(tt4[1], tt4[2])

    y_t  = rapidity(t["E"],  t["pz"])
    y_tb = rapidity(tb["E"], tb["pz"])
    y_tt = rapidity(tt4[0], tt4[3])

    phi_t  = phi(t["px"],  t["py"])
    phi_tb = phi(tb["px"], tb["py"])

    t_star = boost_to_rest_frame(t4, tt4)
    p_star = np.sqrt(t_star[1]**2 + t_star[2]**2 + t_star[3]**2)
    cos_theta_star = np.nan if p_star < 1e-12 else t_star[3] / p_star

    x1, x2, qqbar_like = np.nan, np.nan, np.nan
    if len(incoming) >= 2:
        p1, p2 = incoming[0], incoming[1]
        x1 = (p1["E"] + p1["pz"]) / SQRT_S
        x2 = (p2["E"] - p2["pz"]) / SQRT_S
        pid1, pid2 = p1["pid"], p2["pid"]
        qqbar_like = int((abs(pid1) <= 5) and (abs(pid2) <= 5))

    extra = [p for p in final if abs(p["pid"]) in [1,2,3,4,5,21] and abs(p["pid"]) != 6]
    extra_pts = sorted([pt(p["px"], p["py"]) for p in extra], reverse=True)

    return {
        "weight": xwgtup,
        "m_t": mt, "m_tbar": mtb, "m_tt": mtt,
        "pt_t": pt_t, "pt_tbar": pt_tb, "pt_tt": pt_tt,
        "y_t": y_t, "y_tbar": y_tb, "y_tt": y_tt,
        "abs_y_t": abs(y_t) if np.isfinite(y_t) else np.nan,
        "abs_y_tbar": abs(y_tb) if np.isfinite(y_tb) else np.nan,
        "abs_y_tt": abs(y_tt) if np.isfinite(y_tt) else np.nan,
        "delta_y": y_t - y_tb if np.isfinite(y_t) and np.isfinite(y_tb) else np.nan,
        "abs_delta_y": abs(y_t - y_tb) if np.isfinite(y_t) and np.isfinite(y_tb) else np.nan,
        "delta_phi_tt": abs(delta_phi(phi_t, phi_tb)),
        "cos_theta_star": cos_theta_star,
        "abs_cos_theta_star": abs(cos_theta_star) if np.isfinite(cos_theta_star) else np.nan,
        "x1": x1, "x2": x2,
        "x_ratio": x1/x2 if (np.isfinite(x1) and np.isfinite(x2) and x2 > 0) else np.nan,
        "qqbar_like": qqbar_like,
        "n_extra_partons": len(extra),
        "ptj1": extra_pts[0] if len(extra_pts) > 0 else 0.0,
        "ht_extra": float(np.sum(extra_pts)) if len(extra_pts) > 0 else 0.0,
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
                    if max_events is not None and len(rows) >= max_events: break
                in_event = False
                continue
            if in_event:
                block.append(line)

    return pd.DataFrame(rows)

# ============================================================
# Histogram & Template Operations
# ============================================================

def class_normalized_weights(df, label_col="label", weight_col="weight"):
    w = df[weight_col].astype(float).copy()
    out = np.zeros(len(df), dtype=float)
    for lab in df[label_col].unique():
        mask = (df[label_col] == lab).values
        s = np.sum(np.abs(w[mask]))
        out[mask] = w[mask] / s if s > 0 else 0.0
    return out

def event_number_normalization(h_ref, h, lum=500.0):
    """Scales a template to match absolute expected event yields."""
    n_ref = lum * np.asarray(h_ref, dtype=float) * 1000.0
    n = lum * np.asarray(h, dtype=float) * 1000.0
    return n * sum(n_ref) / sum(n) if sum(n) != 0 else n

def weighted_hist(x, w, bins):
    """Generates a standard weighted histogram array."""
    h, _ = np.histogram(x, bins=bins, weights=np.abs(w))
    return h.astype(float)

def build_shape_template(h, alpha=1e-12):
    h_shape = h + alpha
    return h_shape / h_shape.sum()

def build_signed_delta(h_hyp, h_sm, alpha=1e-12):
    """Calculates the bin-by-bin fractional difference from the Standard Model."""
    return (h_hyp - h_sm) / (h_sm + alpha)

def normalize_signed_template(delta, alpha=1e-12):
    """Normalizes the signed difference array to isolate shape from overall rate."""
    norm = np.sum(np.abs(delta))
    return delta / norm if norm > alpha else None

def js_divergence(p, q, eps=1e-12):
    p = np.asarray(p, dtype=float) + eps
    q = np.asarray(q, dtype=float) + eps
    p /= p.sum()
    q /= q.sum()
    m = 0.5 * (p + q)
    return 0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m))

def signed_l2_distance(d1, d2):
    return np.sqrt(np.mean((d1 - d2)**2))

# ============================================================
# Variance and Significance Calculations
# ============================================================

def calc_variance_hat_delta(h_hyp, h_sm, eps, lum=500.0, alpha=1e-12):
    """
    Computes the rigorous propagated variance for the normalized signed difference.
    Includes both the local per-bin variance term and the global leakage term.
    """
    n_hyp = h_hyp * lum * 1000.0
    n_sm = h_sm * lum * 1000.0
    delta = (n_hyp - n_sm) / (n_sm + alpha)
    S = np.sum(np.abs(delta)) + alpha
    
    sigma2_delta = (n_hyp / (n_sm**2 + alpha)) + (n_hyp**2 * eps**2) / (n_sm**2 + alpha)
    bracket_i = (1.0 / S**2) - (2.0 * np.abs(delta) / S**3) + (delta**2 / S**4)
    term_same = bracket_i * sigma2_delta
    
    sum_sigma2_j_neq_i = np.sum(sigma2_delta) - sigma2_delta
    term_diff = (delta**2 / S**4) * sum_sigma2_j_neq_i
    
    return term_same + term_diff

def asimov_signed_Z_rigorous(dA, dB, hA, hB, h_sm, eps, alpha=1e-12):
    """
    Calculates the separation significance using the Normalized Falloff Method.
    Returns the total Z score, along with the raw numerator and denominator arrays.
    """
    var_hat_A = calc_variance_hat_delta(hA, h_sm, eps, alpha=alpha)
    var_hat_B = calc_variance_hat_delta(hB, h_sm, eps, alpha=alpha)
    
    var_n_ref = (1/2)**2 * (var_hat_A + var_hat_B)
    num = (dA - dB)**2
    den = var_n_ref + alpha
    
    return np.sqrt(max(np.sum(num / den), 0.0)), num, den

def asimov_shape_Z_with_syst(p_true, p_test, frac_syst=0.05, mode="avg", eps=1e-12, lum=500.0):
    """
    Calculates the separation significance using the Standard Shape Method.
    Returns the total Z score, along with the raw numerator and denominator arrays.
    """
    p_true = np.asarray(p_true, dtype=float) + eps
    p_test = np.asarray(p_test, dtype=float) + eps
    n_true = lum * 1000.0 * p_true
    n_test = lum * 1000.0 * p_test

    if mode == "test": n_ref = n_test
    else: n_ref = 0.5 * (n_true + n_test)

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