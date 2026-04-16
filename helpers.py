"""
helpers.py

Helper module for High Energy Physics (HEP) phenomenology analysis.
Contains functions for kinematic variable derivation, LHE file parsing,
statistical separation metrics (JS/KL Divergence, Asimov Z), and plotting.
"""

import os
import gzip
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter
from tqdm.auto import tqdm
from itertools import combinations

SQRT_S = 13000.0  # Center of mass energy in GeV

# ============================================================
# File Management & Data Acquisition
# ============================================================

def download_data_files(base_url, files_dict, out_dir="data"):
    """
    Downloads LHE files from a remote repository if they do not exist locally.
    """
    os.makedirs(out_dir, exist_ok=True)
    for name, url in files_dict.items():
        out = os.path.join(out_dir, f"{name}.lhe.gz")
        if not os.path.exists(out):
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(url, out)
        else:
            print(f"{out} already exists.")

# ============================================================
# Kinematics & Reference Frames
# ============================================================

def rapidity(E, pz, eps=1e-12):
    """Calculates the rapidity of a particle."""
    num = E + pz
    den = E - pz
    if num <= eps or den <= eps:
        return np.nan
    return 0.5 * np.log(num / den)

def pt(px, py):
    """Calculates transverse momentum."""
    return np.hypot(px, py)

def phi(px, py):
    """Calculates the azimuthal angle phi."""
    return np.arctan2(py, px)

def delta_phi(phi1, phi2):
    """Calculates the difference in azimuthal angle between two particles."""
    d = phi1 - phi2
    return (d + np.pi) % (2 * np.pi) - np.pi

def mass(E, px, py, pz):
    """Calculates the invariant mass from a 4-momentum."""
    m2 = E*E - px*px - py*py - pz*pz
    return np.sqrt(max(m2, 0.0))

def boost_to_rest_frame(p4, parent):
    """
    Boosts a 4-momentum p4=(E, px, py, pz) into the rest frame of the parent.
    """
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

# ============================================================
# LHE Parsing Logic
# ============================================================

def parse_event_block(lines, rescale_weight_by=1.0):
    """
    Parses a single <event> block from an LHE file, extracting top quark
    kinematics and calculating specific event-level observables.
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
        if len(cols) < 13:
            continue
        particles.append({
            "pid": int(cols[0]),
            "status": int(cols[1]),
            "px": float(cols[6]),
            "py": float(cols[7]),
            "pz": float(cols[8]),
            "E":  float(cols[9]),
            "M":  float(cols[10]),
        })

    incoming = [p for p in particles if p["status"] == -1]
    final    = [p for p in particles if p["status"] == 1]
    tops  = [p for p in final if p["pid"] == 6]
    tbars = [p for p in final if p["pid"] == -6]
    
    if len(tops) == 0 or len(tbars) == 0:
        return None

    t, tb = tops[0], tbars[0]
    t4  = np.array([t["E"], t["px"], t["py"], t["pz"]], dtype=float)
    tb4 = np.array([tb["E"], tb["px"], tb["py"], tb["pz"]], dtype=float)
    tt4 = t4 + tb4

    y_t = rapidity(t["E"], t["pz"])
    y_tb = rapidity(tb["E"], tb["pz"])
    y_tt = rapidity(tt4[0], tt4[3])
    
    t_star = boost_to_rest_frame(t4, tt4)
    p_star = np.sqrt(t_star[1]**2 + t_star[2]**2 + t_star[3]**2)
    cos_theta_star = np.nan if p_star < 1e-12 else t_star[3] / p_star

    extra = [p for p in final if abs(p["pid"]) in [1,2,3,4,5,21] and abs(p["pid"]) != 6]
    extra_pts = sorted([pt(p["px"], p["py"]) for p in extra], reverse=True)

    return {
        "weight": xwgtup,
        "m_t": mass(*t4),
        "m_tbar": mass(*tb4),
        "m_tt": mass(*tt4),
        "pt_t": pt(t["px"], t["py"]),
        "pt_tbar": pt(tb["px"], tb["py"]),
        "pt_tt": pt(tt4[1], tt4[2]),
        "y_t": y_t,
        "y_tbar": y_tb,
        "y_tt": y_tt,
        "abs_delta_y": abs(y_t - y_tb) if np.isfinite(y_t) and np.isfinite(y_tb) else np.nan,
        "cos_theta_star": cos_theta_star,
        "ptj1": extra_pts[0] if len(extra_pts) > 0 else 0.0,
    }

def read_lhe_features(filepath, label=None, max_events=None, rescale_weight_by=1.0):
    """
    Iterates through an LHE file, sending events to the parser and compiling 
    the resulting features into a Pandas DataFrame.
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
                    if label is not None: rec["label"] = label
                    rows.append(rec)
                    if max_events and len(rows) >= max_events: break
                in_event = False
                continue
            if in_event:
                block.append(line)

    return pd.DataFrame(rows)

# ============================================================
# Statistics & Mathematics
# ============================================================

def class_normalized_weights(df, label_col="label", weight_col="weight"):
    """Normalizes weights so that each physical class sums to 1.0."""
    w = df[weight_col].astype(float).copy()
    out = np.zeros(len(df), dtype=float)
    for lab in df[label_col].unique():
        mask = (df[label_col] == lab).values
        s = np.sum(np.abs(w[mask]))
        out[mask] = w[mask] / s if s > 0 else 0.0
    return out

def event_number_normalization(h_ref, h, lum=500.0):
    """Scales a template to match absolute expected event yields based on luminosity."""
    n_ref = lum * np.asarray(h_ref, dtype=float) * 1000.0
    n = lum * np.asarray(h, dtype=float) * 1000.0
    return n * sum(n_ref) / sum(n) if sum(n) != 0 else n

def build_template(x, w, bins, alpha=1e-12, density=False):
    """Constructs a weighted histogram template, optionally converting to a PDF."""
    h, _ = np.histogram(x, bins=bins, weights=np.abs(w))
    h = h.astype(float) + alpha
    if density:
        h /= h.sum()
    return h

def js_divergence(p, q, eps=1e-12):
    """Calculates the symmetric Jensen-Shannon divergence between two distributions."""
    p, q = np.asarray(p, dtype=float) + eps, np.asarray(q, dtype=float) + eps
    p, q = p / p.sum(), q / q.sum()
    m = 0.5 * (p + q)
    return 0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m))

def kl_divergence(p, q, eps=1e-12):
    """Calculates the directed Kullback-Leibler divergence."""
    p, q = np.asarray(p, dtype=float) + eps, np.asarray(q, dtype=float) + eps
    p, q = p / p.sum(), q / q.sum()
    return np.sum(p * np.log(p / q))

def asimov_shape_llr(p_true, p_test, N=10000, eps=1e-12):
    """Calculates standard shape-only Asimov significance without systematics."""
    p_true, p_test = np.asarray(p_true, dtype=float) + eps, np.asarray(p_test, dtype=float) + eps
    p_true, p_test = p_true / p_true.sum(), p_test / p_test.sum()
    n = N * p_true
    q = 2.0 * np.sum(n * np.log(p_true / p_test))
    return q, np.sqrt(max(q, 0.0))

def asimov_shape_Z_with_syst(n_true, n_test, frac_syst=0.05, mode="avg", eps=1e-12):
    """Calculates sample-level separation including diagonal fractional shape systematics."""
    n_true, n_test = np.asarray(n_true, dtype=float) + eps, np.asarray(n_test, dtype=float) + eps
    n_ref = n_test if mode == "test" else 0.5 * (n_true + n_test)
    var = n_ref + (frac_syst * n_ref)**2
    num = (n_true - n_test)**2
    q = np.sum(num / var)
    return q, np.sqrt(max(q, 0.0)), num, var

# ============================================================
# Plotting Utilities
# ============================================================

def beautify_axis(ax, grid=False):
    """Applies clean, paper-ready styling to a matplotlib axis."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="in", top=False, right=False, length=5)
    if grid:
        ax.grid(True, alpha=0.22, linewidth=0.7)

def add_panel_label(ax, label):
    """Adds a bold alphabetical label to the top-left of a subplot panel."""
    ax.text(0.02, 0.98, label, transform=ax.transAxes, ha="left", va="top", fontsize=14, fontweight="bold")

def get_best_pair_cut(results_syst, N=100000, eps_syst=0.02):
    """Finds the model pair and cut threshold that maximizes separation."""
    col = f"Z_{N}_eps_{int(100*eps_syst):02d}"
    idx = results_syst[col].idxmax()
    row = results_syst.loc[idx]
    return row["pair"], int(row["mcut"])

def weighted_hist_by_label(df, var, bins=60, rng=None, weight_col="w_norm", density=False):
    """Plots superimposed 1D distributions for all specific labels in a dataframe."""
    labels = ["Scalar", "VLF", "Zprime"]
    plt.figure(figsize=(7,5))
    for lab in labels:
        sub = df[df["label"] == lab]
        x = sub[var].replace([np.inf, -np.inf], np.nan).dropna()
        w = sub.loc[x.index, weight_col]
        plt.hist(x, bins=bins, range=rng, weights=w, histtype="step", linewidth=2, label=lab, density=density)
    plt.xlabel(var)
    plt.ylabel("Density" if density else "Weighted Counts")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_syst_grid(results_syst, eps_values, syst_styles, pair_latex, mcut_max, outfile=None, excl_stats=False):
    """Plots a multi-panel grid showing Z-score vs tail cut across different systematic levels."""
    pairs = list(results_syst["pair"].unique())
    fig, axes = plt.subplots(1, len(pairs), figsize=(5.0*len(pairs), 3.9), sharex=True)
    if len(pairs) == 1: axes = np.array([axes]).reshape(1, 1)

    for j, pair in enumerate(pairs):
        ax = axes[j] if len(pairs) > 1 else axes[0,0]
        sub = results_syst[results_syst["pair"] == pair].sort_values("mcut")
        eps_v = eps_values[1:] if excl_stats else eps_values

        for eps_syst in eps_v:
            # Assumes columns are constructed correctly in the main notebook loop
            col_matches = [c for c in sub.columns if f"eps_{int(100*eps_syst):02d}" in c]
            if not col_matches: continue
            col = col_matches[0]
            
            color, ls = syst_styles[eps_syst]
            label = "Stat. Only" if eps_syst == 0 else rf"{int(100*eps_syst)}\%"
            ax.plot(sub["mcut"], sub[col], marker="o", color=color, linestyle=ls, label=label)

        ax.set_title(pair_latex.get(pair, pair))
        if j == 0: ax.set_ylabel(r"Asimov $Z$")
        upper_label = f"{mcut_max}" if mcut_max is not None else r"\infty"
        ax.set_xlabel(rf"$m_{{t\bar t}}^{{\min}}$ up to {upper_label} [GeV]")
        beautify_axis(ax, grid=True)

    handles, labels_ = axes[-1].get_legend_handles_labels() if len(pairs) > 1 else axes[0,0].get_legend_handles_labels()
    fig.legend(handles, labels_, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.02))
    
    if outfile: fig.savefig(outfile)
    plt.show()