"""
helpers.py

Useful functions for calculations and plotting
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
    """
    Checks the local directory for the specified dataset files. 
    If a file is missing, it is downloaded from the designated remote 
    repository (e.g., GitHub raw content).
    """
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
    Aggregates all .npz simulation files corresponding to a specific 
    physics model, applies a universal weight rescaling factor (for 
    coupling adjustments), and returns a consolidated Pandas DataFrame.
    """
    file_pattern = f"{base_path}/*{model_name}*.npz"
    files = glob.glob(file_pattern)

    if not files:
        print(f"Warning: No files found for {model_name} at {base_path}")
        return pd.DataFrame(columns=['m_tt', 'weight', 'label'])

    mtt_list, w_list = [], []
    for f in files:
        data = np.load(f, allow_pickle=True)
        mtt_list.append(data['mTT'])
        w_list.append(data['weights'] * rescale)

    df = pd.DataFrame({'m_tt': np.concatenate(mtt_list), 'weight': np.concatenate(w_list)})
    df['label'] = model_name
    return df

# ============================================================
# Kinematics & Parsing
# ============================================================

def rapidity(E, pz, eps=1e-12):
    """Calculates the momentum-dependent rapidity of a particle."""
    num, den = E + pz, E - pz
    if num <= eps or den <= eps: return np.nan
    return 0.5 * np.log(num / den)

def pt(px, py):
    """Calculates the transverse momentum (pT)."""
    return np.hypot(px, py)

def phi(px, py):
    """Calculates the azimuthal angle phi."""
    return np.arctan2(py, px)

def delta_phi(phi1, phi2):
    """Calculates the difference in azimuthal angle between two particles."""
    d = phi1 - phi2
    return (d + np.pi) % (2 * np.pi) - np.pi

def mass(E, px, py, pz):
    """Calculates the invariant mass from a 4-momentum vector."""
    m2 = E*E - px*px - py*py - pz*pz
    return np.sqrt(max(m2, 0.0))

def boost_to_rest_frame(p4, parent):
    """
    Performs a Lorentz transformation, boosting a 4-momentum vector (p4) 
    into the rest frame of its parent particle/system.
    """
    E, px, py, pz = p4
    EP, Px, Py, Pz = parent
    bx, by, bz = Px/EP, Py/EP, Pz/EP
    b2 = bx*bx + by*by + bz*bz
    if b2 >= 1.0 or b2 < 1e-16: return np.array([E, px, py, pz], dtype=float)
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
    Parses a single <event> block from an LHE file, extracting top quark 
    kinematics and calculating macroscopic event-level observables like 
    invariant mass (m_tt) and transverse momentum (pT).
    """
    content = [ln.strip() for ln in lines if ln.strip()]
    if not content: return None

    header = content[0].split()
    nup, xwgtup = int(header[0]), float(header[2]) * rescale_weight_by

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
    tops, tbars = [p for p in final if p["pid"] == 6], [p for p in final if p["pid"] == -6]
    
    if not tops or not tbars: return None

    t, tb = tops[0], tbars[0]
    t4 = np.array([t["E"], t["px"], t["py"], t["pz"]], dtype=float)
    tb4 = np.array([tb["E"], tb["px"], tb["py"], tb["pz"]], dtype=float)
    tt4 = t4 + tb4

    t_star = boost_to_rest_frame(t4, tt4)
    p_star = np.sqrt(t_star[1]**2 + t_star[2]**2 + t_star[3]**2)
    cos_theta_star = np.nan if p_star < 1e-12 else t_star[3] / p_star

    extra = [p for p in final if abs(p["pid"]) in [1,2,3,4,5,21] and abs(p["pid"]) != 6]
    extra_pts = sorted([pt(p["px"], p["py"]) for p in extra], reverse=True)

    y_t, y_tb = rapidity(t["E"], t["pz"]), rapidity(tb["E"], tb["pz"])
    return {
        "weight": xwgtup,
        "m_t": mass(*t4), "m_tbar": mass(*tb4), "m_tt": mass(*tt4),
        "pt_t": pt(t["px"], t["py"]), "pt_tbar": pt(tb["px"], tb["py"]), "pt_tt": pt(tt4[1], tt4[2]),
        "y_t": y_t, "y_tbar": y_tb, "y_tt": rapidity(tt4[0], tt4[3]),
        "abs_delta_y": abs(y_t - y_tb) if np.isfinite(y_t) and np.isfinite(y_tb) else np.nan,
        "cos_theta_star": cos_theta_star,
        "abs_cos_theta_star": abs(cos_theta_star) if np.isfinite(cos_theta_star) else np.nan,
        "ptj1": extra_pts[0] if len(extra_pts) > 0 else 0.0,
    }

def read_lhe_features(filepath, label=None, max_events=None, rescale_weight_by=1.0):
    """
    Iterates through a compressed or raw LHE file, feeding events to the parser 
    and compiling the returned variables into an analysis-ready Pandas DataFrame.
    """
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
                    if label: rec["label"] = label
                    rows.append(rec)
                    if max_events and len(rows) >= max_events: break
                in_event = False
                continue
            if in_event: block.append(line)

    return pd.DataFrame(rows)

# ============================================================
# Histogram & Template Operations
# ============================================================

def class_normalized_weights(df, label_col="label", weight_col="weight"):
    """Normalizes the event weights so that each physical model class sums to 1.0."""
    w = df[weight_col].astype(float).copy()
    out = np.zeros(len(df), dtype=float)
    for lab in df[label_col].unique():
        mask = (df[label_col] == lab).values
        s = np.sum(np.abs(w[mask]))
        out[mask] = w[mask] / s if s > 0 else 0.0
    return out

def event_number_normalization(h_ref, h, lum=500.0):
    """
    Scales a histogram template to match the absolute expected physical event yields, 
    aligning cross-sections based on the provided detector luminosity.
    """
    n_ref, n = lum * np.asarray(h_ref, dtype=float) * 1000.0, lum * np.asarray(h, dtype=float) * 1000.0
    return n * sum(n_ref)/sum(n) if sum(n) != 0 else n

def weighted_hist(x, w, bins):
    """Generates a standard weighted 1D histogram array."""
    h, _ = np.histogram(x, bins=bins, weights=np.abs(w))
    return h.astype(float)

def build_template(x, w, bins, alpha=1e-12, density=False):
    """Generates a histogram template, applying a safety epsilon and optional PDF normalization."""
    h, _ = np.histogram(x, bins=bins, weights=np.abs(w))
    h = h.astype(float) + alpha
    if density: h /= h.sum()
    return h

def build_shape_template(h, alpha=1e-12):
    """Converts an absolute histogram array into a normalized probability distribution."""
    h_shape = h + alpha
    return h_shape / h_shape.sum()

def build_signed_delta(h_hyp, h_sm, alpha=1e-12):
    """Calculates the bin-by-bin fractional difference from the Standard Model background."""
    return (h_hyp - h_sm) / (h_sm + alpha)

def normalize_signed_template(delta, alpha=1e-12):
    """Normalizes the fractional difference array to isolate shape deformations from overall rate shifts."""
    norm = np.sum(np.abs(delta))
    return delta / norm if norm > alpha else None

def js_divergence(p, q, eps=1e-12):
    """Calculates the symmetric Jensen-Shannon divergence between two distributions."""
    p, q = np.asarray(p, dtype=float) + eps, np.asarray(q, dtype=float) + eps
    p, q = p / p.sum(), q / q.sum()
    m = 0.5 * (p + q)
    return 0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m))

def kl_divergence(p, q, eps=1e-12):
    """Calculates the directed Kullback-Leibler divergence between two distributions."""
    p, q = np.asarray(p, dtype=float) + eps, np.asarray(q, dtype=float) + eps
    p, q = p / p.sum(), q / q.sum()
    return np.sum(p * np.log(p / q))

def signed_l2_distance(d1, d2):
    """Calculates the root-mean-square Euclidean distance between two arrays."""
    return np.sqrt(np.mean((d1 - d2)**2))

def asimov_shape_llr_stat_only(p_true, p_test, N=10000, eps=1e-12):
    """Calculates standard shape-only Asimov significance assuming perfect detection (No Systematics)."""
    p_true, p_test = np.asarray(p_true, dtype=float) + eps, np.asarray(p_test, dtype=float) + eps
    p_true, p_test = p_true / p_true.sum(), p_test / p_test.sum()
    n = N * p_true
    q = 2.0 * np.sum(n * np.log(p_true / p_test))
    return q, np.sqrt(max(q, 0.0))

# ============================================================
# Variance and Significance Calculations
# ============================================================

def calc_variance_hat_delta(h_hyp, h_sm, eps, alpha=1e-12):
    """
    Computes the rigorous propagated variance for the Normalized Falloff Method.
    Includes both the local per-bin variance component and the global leakage component 
    created by the shape-isolation normalization.
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
    Calculates the statistical separation significance between two models utilizing 
    the Normalized Falloff Method, rigorously propagating systematic uncertainties.
    """
    var_hat_A = calc_variance_hat_delta(hA, n_sm, eps, alpha=alpha)
    var_hat_B = calc_variance_hat_delta(hB, n_sm, eps, alpha=alpha)
    
    var_n_ref = (1/2)**2 * (var_hat_A + var_hat_B)
    num = (dA - dB)**2
    den = var_n_ref + alpha
    
    return np.sqrt(max(np.sum(num / den), 0.0)), num, den

def asimov_shape_Z_with_syst(p_true, p_test, frac_syst=0.05, mode="avg", eps=1e-12):
    """
    Calculates the statistical separation significance using the traditional 
    Standard Shape Method, penalizing the baseline with fractional diagonal systematics.
    """
    p_true = np.asarray(p_true, dtype=float) + eps
    p_test = np.asarray(p_test, dtype=float) + eps

    if mode == "test": n_ref = p_test
    else: n_ref = 0.5 * (p_true + p_test)

    var = n_ref + (frac_syst * n_ref)**2
    num = (p_true - p_test)**2
    
    return np.sqrt(max(np.sum(num / var), 0.0)), num, var

# ============================================================
# Plotting Utilities
# ============================================================

def beautify_axis(ax, grid=False):
    """Applies a clean, scientific styling to matplotlib axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="in", top=False, right=False, length=5)
    if grid: ax.grid(True, alpha=0.22, linewidth=0.7)

def get_best_pair_and_cut(df, N=100000):
    """Searches the significance DataFrame to find the model pair and mass cut yielding the highest separation Z."""
    col = df.columns[-1]
    for c in [f"Z_{N}_a_true", f"Z_{N}_eps_00", f"Z_{N}_eps_02", "Z_eps_00", "Z_eps_02", "Z_shape"]:
        if c in df.columns:
            col = c
            break
    row = df.loc[df[col].idxmax()]
    return row["pair"], int(row["mcut"])

def split_pair(pair):
    """Splits a pair string (e.g. 'Scalar vs Zprime') into a tuple for component analysis."""
    return pair.split(" vs ")