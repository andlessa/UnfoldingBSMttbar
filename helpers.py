"""
helpers.py

A comprehensive module for Monte Carlo (MC) data management, kinematic calculations, 
statistical template analysis (Shape and Falloff methods), and significance plotting 
for Beyond the Standard Model (BSM) physics searches.
"""

import os
import gzip
import urllib.request
import glob
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import tempfile
import pylhe
import gc
import copy
from scipy.optimize import minimize
import matplotlib.gridspec as gridspec
import pickle

SQRT_S = 13000.0  # Center of mass energy in GeV

# ============================================================
# Data Acquisition & Management
# ============================================================

def download_data_files(base_url, files_dict, out_dir="data"):
    """
    Checks the local directory for the specified dataset files. 
    If a file is missing, it is downloaded from the designated remote repository.
    
    Args:
        base_url (str): The root URL for the remote repository.
        files_dict (dict): Dictionary mapping file names to their full download URLs.
        out_dir (str): Local directory path to save the downloaded .lhe.gz files.
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
    Aggregates all .npz simulation files corresponding to a specific physics model, 
    applies a universal weight rescaling factor, and returns a Pandas DataFrame.
    
    Args:
        base_path (str): The directory containing the .npz files.
        model_name (str): The specific model substring to search for in filenames.
        rescale (float): A universal multiplier applied to all event weights.
        
    Returns:
        pd.DataFrame: A consolidated DataFrame with 'm_tt', 'weight', and 'label' columns.
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
# Automated Configuration, Best Fit & Loading Module
# ============================================================


def fit_and_assemble_data(fake_data_key, workspace_file='lite_workspace.pkl', sys_err_list=None, lumi=500.0, zp_limit_csv='Safe_Limits_Zprime.csv'):
    """
    Fits models to fake data using the pre-binned workspace.
    fake_data_key should be one of: 'Zprime_3000', 'Scalar_1500', 'VLF_1500'
    """
    if sys_err_list is None or len(sys_err_list) == 0:
        sys_err_list = [0.0]

    with open(workspace_file, 'rb') as f:
        ws = pickle.load(f)
        
    bins = ws['bins']
    mass_mask = (bins[:-1] >= 1200) & (bins[:-1] <= 5000)


    # Prepare SM and Fake Data yields
    n_sm = ws['SM'] * lumi * 1000.0
    
    h_fake_pure = ws['FakeData'][fake_data_key]['pure']
    h_fake_int = ws['FakeData'][fake_data_key]['int']
    
    n_fake_pure = h_fake_pure * lumi * 1000.0
    n_fake_int = h_fake_int * lumi * 1000.0

    if fake_data_key == 'Scalar_1500':
            y_dm = 7.5
            n_fake = (n_fake_pure * (y_dm**2))
            sqrt_factor = y_dm 
    elif fake_data_key == 'VLF_1500':
            y_dm = 3.5
            n_fake = (n_fake_pure * (y_dm**2))
            sqrt_factor = y_dm 
    elif fake_data_key == 'Zprime_3000':
        gq_gt = -4.0
        sqrt_factor = -4.0 #*7.745886e-03*1.585365
        n_fake = (n_fake_pure * (gq_gt**2)) + (n_fake_int * gq_gt)
    else:
        print('Fake Data not available')
    print(f"Fake Data correctly normalized to yield: {np.sum(n_fake[mass_mask], dtype=np.float64):.2f} events in target window.")
    
    N_obs = n_sm + n_fake
    safe_N_obs = np.where(N_obs > 0, N_obs, 1e-10)

    # Helper to extract grid as matrices
    def extract_grid(model_pure, model_int=None):
        masses, grid1, grid2 = [], [], []
        for m, h in ws['Models'][model_pure].items():
            if np.sum(h) > 0:
                masses.append(m)
                grid1.append(h * lumi * 1000.0)
                if model_int: grid2.append(ws['Models'][model_int][m] * lumi * 1000.0)
        
        if not masses:
            return (None, None, None) if model_int else (None, None)
            
        if model_int:
            return np.array(masses), np.array(grid1), np.array(grid2)
        return np.array(masses), np.array(grid1), None

    vlf_m, vlf_grid, _ = extract_grid('VLF')
    scalar_m, scalar_grid, _ = extract_grid('Scalar')
    zp_m, zp_grid, zp_grid_int = extract_grid('Zprime', 'Zprime_int')
    zp20_m, zp20_grid, zp20_grid_int = extract_grid('Zprime_20pc', 'Zprime_20pc_int')

    # Original Fit Helper
    def fit_1d_parabolic(m_arr, grid_arr_1, denom, max_mu_sqrt, sys_err, grid_arr_2=None):
        if m_arr is None or len(m_arr) == 0: 
            return None, np.inf, 0.0
            
        chi2_vals, k_vals = [], []
        safe_denom = np.where(denom > 0, denom, 1e-10)
        
        for i, n_sig1 in enumerate(grid_arr_1):
            n_sig2 = grid_arr_2[i] if grid_arr_2 is not None else None
            max_k = max_mu_sqrt if max_mu_sqrt != np.inf else 100.0 
            k_min = -max_k if n_sig2 is not None else 0.0
            
            test_ks = np.linspace(k_min, max_k, 200)
            K_grid = test_ks[:, None]
            
            n_sig_tot_grid = (K_grid**2) * n_sig1
            if n_sig2 is not None:
                n_sig_tot_grid += K_grid * n_sig2
                
            if sys_err == 0.0:
                n_exp_grid = n_sm + n_sig_tot_grid
                safe_n_exp_grid = np.where(n_exp_grid > 0, n_exp_grid, 1e-10)
                chi2_tests = 2.0 * np.sum(safe_n_exp_grid - N_obs + N_obs * np.log(safe_N_obs / safe_n_exp_grid), axis=1)
            else:
                chi2_tests = np.sum(((n_sig_tot_grid - n_fake)**2) / safe_denom, axis=1)
                
            best_k_guess = test_ks[np.argmin(chi2_tests)]
            
            def objective(k_arr):
                k = k_arr[0]
                n_sig_tot = (k**2) * n_sig1
                if n_sig2 is not None: n_sig_tot += k * n_sig2
                
                if sys_err == 0.0:
                    n_exp = n_sm + n_sig_tot
                    safe_n_exp = np.where(n_exp > 0, n_exp, 1e-10)
                    return 2.0 * np.sum(safe_n_exp - N_obs + N_obs * np.log(safe_N_obs / safe_n_exp))
                else:
                    return np.sum(((n_sig_tot - n_fake)**2) / safe_denom)

            bound_tuple = (k_min, max_k) if max_mu_sqrt != np.inf else (None, None)
            res = minimize(objective, x0=[best_k_guess], bounds=[bound_tuple])
            
            chi2_vals.append(res.fun)
            k_vals.append(res.x[0])
            
        chi2_vals = np.array(chi2_vals)
        k_vals = np.array(k_vals)
        idx_min = np.argmin(chi2_vals)
        
        if len(m_arr) < 3 or chi2_vals[idx_min] < 1e-3:
            return m_arr[idx_min], chi2_vals[idx_min], k_vals[idx_min]
        
        window = [max(0, min(idx_min - 1, len(m_arr) - 3)), 
                  max(1, min(idx_min, len(m_arr) - 2)), 
                  max(2, min(idx_min + 1, len(m_arr) - 1))]
            
        m_window = m_arr[window]
        coeffs = np.polyfit(m_window, chi2_vals[window], 2)
        a, b, c = coeffs
        
        if a > 0:
            best_m = np.clip(-b / (2 * a), m_arr[0], m_arr[-1])
            best_chi2 = a * (best_m**2) + b * best_m + c
            best_k = np.polyval(np.polyfit(m_window, k_vals[window], 2), best_m)
            
            local_max_k = max_mu_sqrt if max_mu_sqrt != np.inf else np.inf
            local_k_min = -local_max_k if grid_arr_2 is not None else 0.0
            best_k = np.clip(best_k, local_k_min, local_max_k)
        else:
            best_m, best_chi2, best_k = m_arr[idx_min], chi2_vals[idx_min], k_vals[idx_min]
            
        return best_m, best_chi2, best_k

    def snap_to_grid(m, m_grid):
        if m is None or m_grid is None or len(m_grid) == 0: return 1000.0
        return m_grid[(np.abs(m_grid - m)).argmin()]

    output_dict = {}

    for sys_err in sys_err_list:
        print(f"\n============================================================")
        print(f" Fitting for Systematic Error: {sys_err*100:.1f}%")
        print(f"============================================================")
        
        chi2_denom_masked = (n_fake + n_sm) + (sys_err * n_sm)**2

        chi2_min = {
            'VLF': fit_1d_parabolic(vlf_m, vlf_grid, chi2_denom_masked, 7.0, sys_err),
            'Scalar': fit_1d_parabolic(scalar_m, scalar_grid, chi2_denom_masked, 10.1, sys_err),
            'Zprime': fit_1d_parabolic(zp_m, zp_grid, chi2_denom_masked, np.inf, sys_err, zp_grid_int),
            'Zprime_20pc': fit_1d_parabolic(zp20_m, zp20_grid, chi2_denom_masked, np.inf, sys_err, zp20_grid_int),
            'FakeData': (1500.0, 0.0, sqrt_factor)
        }

        print(f"--- Global Best Fit Results ---")
        best_fits = {}
        for model, fit in chi2_min.items():
            mass, chi2, best_mu = fit
            if mass is not None:
                print(f"{model:12}: Mass = {mass:.2f} GeV | Scaling factor = {best_mu:.6e} | Min Chi^2 = {chi2:.2f}")
                if model == 'FakeData': 
                    best_fits[model] = {'scale_factor': best_mu}
                else:
                    grid = vlf_m if model == 'VLF' else scalar_m if model == 'Scalar' else zp_m if model == 'Zprime' else zp20_m
                    snap_m = snap_to_grid(mass, grid)
                    best_fits[model] = {
                        'continuous_m': mass,
                        'scale_factor': best_mu,
                        'snap_m': snap_m
                    }

        # Build final Scaled Cross-Section Histograms
        fitted_hists = {'SM': np.copy(ws['SM'])}
        
        # Apply scaling to pure models (fac**2) and interference models (fac)
        fitted_hists['FakeData'] = h_fake_pure * best_fits['FakeData']['scale_factor']**2
        fitted_hists['FakeData_int'] = h_fake_int * best_fits['FakeData']['scale_factor']

        for m_name in ['VLF', 'Scalar', 'Zprime', 'Zprime_20pc']:
            if m_name in best_fits:
                fac = best_fits[m_name]['scale_factor']
                m_snap = best_fits[m_name]['snap_m']
                
                fitted_hists[m_name] = ws['Models'][m_name][m_snap] * (fac**2)
                
                int_key = f"{m_name}_int"
                if int_key in ws['Models']:
                    fitted_hists[int_key] = ws['Models'][int_key][m_snap] * fac

        output_dict[sys_err] = {'hists': fitted_hists, 'best_fits': best_fits, 'bins': bins}

    return output_dict


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
    data = {
        "weight": [], "m_t": [], "m_tbar": [], "m_tt": [],
        "pt_t": [], "pt_tbar": [], "pt_tt": [],
        "y_t": [], "y_tbar": [], "y_tt": [],
        "abs_delta_y": [], "cos_theta_star": [], "abs_cos_theta_star": [], "ptj1": []
    }
    if label: data["label"] = []

    block, in_event = [], False
    event_count = 0
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
                    for key, val in rec.items():
                        data[key].append(val)
                    if label:
                        data["label"].append(label)
                        
                    event_count += 1
                    if max_events and event_count >= max_events: break
                in_event = False
                continue
            if in_event: 
                block.append(line)

    return pd.DataFrame(data)

def get_run_metadata(filepath, is_nlo=False):
    """
    Extracts the true cross-section, LHE cross-section, and event count.
    - LO: Truth is strictly the LHE file.
    - NLO: Truth is strictly the summary.txt file.
    """
    run_dir = os.path.dirname(filepath)
    info = {'nevents': -1, 'xsec_lhe': -1.0, 'xsec_true': -1.0}
    
    fd, fixedFile = tempfile.mkstemp(suffix='.lhe')
    os.close(fd)
    try:
        with gzip.open(filepath, 'rt') as f_in, open(fixedFile, 'w') as f_out:
            for line in f_in:
                if 'generate' not in line:
                    f_out.write(line)
        
        initBlock = pylhe.read_lhe_init(fixedFile)
        info['xsec_lhe'] = initBlock['procInfo'][0]['xSection']
        info['nevents'] = pylhe.read_num_events(fixedFile)
        info['xsec_true'] = info['xsec_lhe'] 
        
    except Exception as e:
        print(f"Error parsing LHE header from {os.path.basename(filepath)}: {e}")
    finally:
        if os.path.exists(fixedFile):
            os.remove(fixedFile)

    if is_nlo:
        summary_path = os.path.join(run_dir, 'summary.txt')
        if os.path.isfile(summary_path):
            with open(summary_path, 'r') as f:
                lines = f.readlines()
                
            try:
                target_idx = [i for i, l in enumerate(lines) if 'Total cross section' in l][0]
                xsec_line = lines[target_idx]
                
                if 'DO NOT USE' in xsec_line:
                    scale_idx = [i for i, l in enumerate(lines) if 'Scale variation' in l][0]
                    xsec_line = lines[scale_idx + 2]
                    
                if 'Total cross section' in xsec_line:
                    xsec_line = xsec_line.split(':')[1].strip()
                    
                xsec_line = xsec_line.split(' +')[0].strip().replace('pb', '')
                info['xsec_true'] = float(xsec_line)
            except Exception:
                pass

    if info['nevents'] <= 0:
        banners = glob.glob(os.path.join(run_dir, '*banner*txt'))
        if banners:
            with open(banners[0], 'r') as f:
                banner_data = f.read()
            if '<MGGenerationInfo>' in banner_data:
                gen_info = banner_data.split('<MGGenerationInfo>')[1].split('</MGGenerationInfo>')[0]
                try:
                    info['nevents'] = eval(gen_info.split('\n')[1].split(':')[1].strip())
                except Exception:
                    pass
                    
    return info

def load_lhe_with_corrections(file_pattern, label=None, is_nlo=False, custom_rescale=1.0, max_events=None):
    """
    Finds LHE files and streams them into a DataFrame. 
    Guarantees that sum(weights) exactly equals the true cross section.
    """
    files = glob.glob(file_pattern)
    if not files:
        print(f"Warning: No files found for pattern {file_pattern}")
        return pd.DataFrame(columns=["weight", "m_t", "m_tbar", "m_tt", "pt_t", "pt_tbar", "pt_tt", "label"])
        
    print(f"Loading {label} from {len(files)} LHE files...")
    df_list = []
    
    for f in files:
        info = get_run_metadata(f, is_nlo=is_nlo)
        base_rescale = 1.0
        
        if not is_nlo and info['nevents'] > 0:
            base_rescale = 1.0 / info['nevents']
            
        elif is_nlo and info['xsec_lhe'] > 0 and info['xsec_true'] > 0:
            drift = abs(info['xsec_lhe'] - info['xsec_true']) / info['xsec_true']
            if drift > 0.01:
                bias_factor = info['xsec_true'] / info['xsec_lhe']
                base_rescale = bias_factor
                
                run_name = os.path.basename(os.path.dirname(f))
                print(f"  -> [BIAS DETECTED] {run_name}: Rescaled weights by {bias_factor:.5f} "
                      f"(True: {info['xsec_true']:.5e} pb, LHE: {info['xsec_lhe']:.5e} pb)")
        
        total_rescale = custom_rescale * base_rescale
        df = read_lhe_features(f, label=label, max_events=max_events, rescale_weight_by=total_rescale)
        
        if not df.empty:
            df_list.append(df)
        else:
            print(f"  -> Skipping {os.path.basename(f)} (No valid events)")
            
    if not df_list:
        return pd.DataFrame()
        
    return pd.concat(df_list, ignore_index=True)


# ============================================================
# Histogram & Template Operations
# ============================================================

def class_normalized_weights(df, label_col="label", weight_col="weight"):
    """Normalizes the weights inside a dataframe independently for each model class."""
    w = df[weight_col].astype(float).copy()
    out = np.zeros(len(df), dtype=float)
    for lab in df[label_col].unique():
        mask = (df[label_col] == lab).values
        s = np.sum(np.abs(w[mask]))
        out[mask] = w[mask] / s if s > 0 else 0.0
    return out

def event_number_normalization(h_ref, h, lum=500.0):
    """Rescales histogram yields to explicitly match a target expected luminosity yield."""
    n_ref, n = lum * np.asarray(h_ref, dtype=float) * 1000.0, lum * np.asarray(h, dtype=float) * 1000.0
    return n * sum(n_ref)/sum(n) if sum(n) != 0 else n

def weighted_hist(x, w, bins):
    """Computes a 1D histogram weighted by generated event parameters."""
    h, _ = np.histogram(x, bins=bins, weights=w)
    return h.astype(float)

def build_template(x, w, bins, alpha=1e-12, density=False):
    """Constructs a basic probability template preventing absolute 0 division errors."""
    h, _ = np.histogram(x, bins=bins, weights=w)
    h = h.astype(float) + alpha
    if density: h /= h.sum()
    return h

def build_shape_template(h, alpha=1e-12):
    """Returns a completely normalized unit-shape template from raw yields."""
    h_shape = h + alpha
    return h_shape / h_shape.sum()

def build_signed_delta(h_hyp, h_sm, alpha=1e-12):
    """Calculates the relative variance between a hypothesis template and SM."""
    return (h_hyp - h_sm) / (h_sm + alpha)

def normalize_signed_template(delta, alpha=1e-12):
    """Normalizes a signed delta distribution, maintaining its interference bounds."""
    norm = np.sum(np.abs(delta))
    return delta / norm if norm > alpha else None

def js_divergence(p, q, eps=1e-12):
    """Computes Jensen-Shannon divergence between two templates."""
    p, q = np.asarray(p, dtype=float) + eps, np.asarray(q, dtype=float) + eps
    p, q = p / p.sum(), q / q.sum()
    m = 0.5 * (p + q)
    return 0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m))

def kl_divergence(p, q, eps=1e-12):
    """Computes standard Kullback-Leibler divergence between two templates."""
    p, q = np.asarray(p, dtype=float) + eps, np.asarray(q, dtype=float) + eps
    p, q = p / p.sum(), q / q.sum()
    return np.sum(p * np.log(p / q))

def signed_l2_distance(d1, d2):
    """Computes L2 distance between shape differentials."""
    return np.sqrt(np.mean((d1 - d2)**2))

def asimov_shape_llr_stat_only(p_true, p_test, N=10000, eps=1e-12):
    """Calculates the asymptotic Log-Likelihood Ratio based entirely on statistical variations."""
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
    Computes the variance operator of the delta interference ratio incorporating 
    both statistical and systematic uncertainties in the denominator base.
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

def asimov_signed_Z_rigorous(dA, dB, hA, hB, n_sm, eps, mode="avg", alpha=1e-12):
    """
    Calculates the separation significance (Z) using the Normalized Falloff Method.
    This formulation accounts for signed (interference) distributions.
    """
    var_hat_A = calc_variance_hat_delta(hA, n_sm, eps, alpha=alpha)
    var_hat_B = calc_variance_hat_delta(hB, n_sm, eps, alpha=alpha)
    
    if mode =="test": var_n_ref = var_hat_B
    else: var_n_ref = (1/2)**2 * (var_hat_A + var_hat_B)
    num = (dA - dB)**2
    den = var_n_ref + alpha
    
    return np.sqrt(max(np.sum(num / den), 0.0)), num, den


def asimov_shape_Z_with_syst(p_true, p_test, frac_syst=0.05, eps=1e-12):
    """
    Calculates the separation significance (Z_A) using the exact profile 
    Poisson likelihood for an Asimov dataset with shape uncertainties.

    Parameters:
        p_true (array-like): Yields under the true hypothesis (Asimov data N_k^A).
        p_test (array-like): Yields under the test hypothesis (n_k^test).
        frac_syst (float): Uncorrelated fractional systematic uncertainty epsilon (e.g. 0.05 for 5%).
        eps (float): Numerical regulator to avoid log(0) or zero division.

    Returns:
        Z_A (float): Asimov median expected significance Z_A = sqrt(q_A).
        q_A (float): Total profile likelihood test statistic.
        theta_hat (ndarray): Profiled nuisance parameter per bin.
    """
    n_true = np.asarray(p_true, dtype=float) + eps
    n_test = np.asarray(p_test, dtype=float) + eps
    epsilon = float(frac_syst)

    if epsilon > 0:
        # Discriminant of the quadratic minimization condition
        A = 1.0 - n_test * (epsilon ** 2)
        disc = A**2 + 4.0 * (epsilon ** 2) * n_true
        
        # Profiled yield: y_k = n_k_test * (1 + epsilon * theta_k)
        y_test = 0.5 * n_test * (A + np.sqrt(disc))
        
        # Profiled nuisance parameters: theta_k = (y_k - n_k_test) / (epsilon * n_k_test)
        theta_hat = (y_test - n_test) / (n_test * epsilon)
    else:
        y_test = np.copy(n_test)
        theta_hat = np.zeros_like(n_test)

    # Bin-wise Poisson deviance
    poisson_terms = 2.0 * (y_test - n_true + n_true * np.log(n_true / y_test))
    
    # Total Asimov test statistic q_A = sum(Poisson deviance) + sum(theta_hat^2)
    q_k = poisson_terms + theta_hat**2
    q_A = float(np.sum(q_k))
    
    Z_A = float(np.sqrt(max(q_A, 0.0)))

    return Z_A, q_A, theta_hat


# ============================================================
# Plotting Utilities
# ============================================================

def beautify_axis(ax, grid=False):
    """Applies standard aesthetic adjustments to Matplotlib axes (despining)."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="in", top=False, right=False, length=5)
    if grid: ax.grid(True, alpha=0.22, linewidth=0.7)

def get_best_pair_and_cut(df, N=100000):
    """Extracts the specific mass cut value that yields the maximum separation Z-score."""
    col = df.columns[-1]
    for c in [f"Z_{N}_a_true", f"Z_{N}_eps_00", f"Z_{N}_eps_02", "Z_eps_00", "Z_eps_02", "Z_shape"]:
        if c in df.columns:
            col = c
            break
    row = df.loc[df[col].idxmax()]
    return row["pair"], int(row["mcut"])

def format_model_label(model_name):
    """Formats raw model dataset names into presentation-ready LaTeX strings."""
    formatted = model_name.replace("Zprime", r"$Z^\prime$")
    formatted = formatted.replace("_20pcW", r" $(\Gamma_{Z^\prime}/m_{Z^\prime} = 0.2)$")
    formatted = formatted.replace("_20pc", r" $(\Gamma_{Z^\prime}/m_{Z^\prime} = 0.2)$")
    formatted = formatted.replace("FakeData", "Fake Data")
    return formatted

def get_mass_label_from_fits(model_name, best_fits):
    """
    Parses the best_fits dictionary and returns the properly formatted LaTeX 
    string containing the respective internal masses for the requested model.
    """
    if not best_fits or model_name not in best_fits:
        return ""
    
    fits = best_fits[model_name]
    if model_name == "VLF":
        return rf"$m_{{\psi_T}} = {fits.get('mPsiT', 0):.0f}$ GeV, $m_{{\phi}} = {fits.get('mSDM', 0):.0f}$ GeV"
    elif model_name == "Scalar":
        return rf"$m_{{\varphi_T}} = {fits.get('mST', 0):.0f}$ GeV, $m_{{\chi}} = {fits.get('mChi', 0):.0f}$ GeV"
    elif "Zprime" in model_name:
        return rf"$m_{{Z^\prime}} = {fits.get('mZp', 0):.0f}$ GeV"
    
    return ""




# ============================================================
# Optimized Mass & Luminosity Scans (Adapted for Dictionary Routing)
# ============================================================

def run_fast_lumi_scan(fitted_data_by_lumi, labels, target_mcut, mcut_max, bin_width, lumi_targets, 
                       sys_err_list, var="m_tt", alpha=1e-12, fake_model='FakeData', 
                       bin_offset=0.0, sig_norm=False, sm_cms=False, include_sm=True):
    """
    Computes Standard Shape and Normalized Falloff method separation significances 
    using the dictionaries output by fit_and_assemble_data_lite.
    """
    rows_dict = {} 

    test_labels = list(labels)
    if include_sm and 'SM' not in test_labels:
        test_labels.append('SM')

    for lum in lumi_targets:
        if lum not in fitted_data_by_lumi:
            continue
            
        for sys_err in sys_err_list:
            active_sys_key = sys_err if sys_err in fitted_data_by_lumi[lum] else 0.0
            data = fitted_data_by_lumi[lum][active_sys_key]
            
            bins = data['bins']
            
            # Identify which bins fall in the analysis range
            mask = (bins[:-1] >= target_mcut) & (bins[:-1] < mcut_max)
            
            h_sm_xsec = data['hists']['SM'][mask]
            if sm_cms: 
                h_sm_xsec = h_sm_xsec * 1.7 * 0.287
                
            h_sm_raw = h_sm_xsec * lum * 1000.0  # Convert pb to Yield
            
            if np.sum(h_sm_raw) == 0:
                print(f"Warning: 0 SM events found above {target_mcut} GeV for sys {sys_err} at lumi {lum}.")
                continue
            
            raw_templates = {}
            all_models = test_labels + [fake_model]
            
            for lab in all_models:
                if lab == 'SM':
                    raw_templates['SM'] = np.zeros_like(h_sm_raw)
                else:
                    if lab in data['hists']:
                        # Add interference to pure if it exists, convert to Yield
                        base_h = data['hists'][lab][mask]
                        if f"{lab}_int" in data['hists']:
                            base_h += data['hists'][f"{lab}_int"][mask]
                            
                        raw_templates[lab] = base_h * lum * 1000.0

            if fake_model not in raw_templates: 
                continue
            ref_template = raw_templates[fake_model].copy()
            n_sm = h_sm_raw.copy()
            
            scaled_templates = {}
            norm_templates = {}
            for lab in all_models:
                if lab not in raw_templates: 
                    continue
                
                if lab == 'SM':
                    scaled_templates['SM'] = h_sm_raw.copy()
                    norm_templates['SM'] = np.zeros_like(h_sm_raw)
                else:
                    if sig_norm:
                        aligned_sig = event_number_normalization(ref_template, raw_templates[lab], lum=1e-3)
                        scaled_templates[lab] = aligned_sig + h_sm_raw
                    else:
                        scaled_templates[lab] = raw_templates[lab] + h_sm_raw
                    
                    delta = build_signed_delta(scaled_templates[lab], h_sm_raw, alpha=alpha)
                    norm_templates[lab] = normalize_signed_template(delta, alpha=alpha)

            for lab in test_labels:
                if lab not in raw_templates or lab == fake_model: 
                    continue
                
                a, b = fake_model, lab
    
                hA, hB = scaled_templates[a], scaled_templates[b]
                dA, dB = norm_templates[a], norm_templates[b]
                
                Z_fa, _, _ = asimov_signed_Z_rigorous(dA, dB, hA, hB, n_sm, sys_err, mode="test", alpha=alpha)
                Z_sh, _, _ = asimov_shape_Z_with_syst(hA, hB, frac_syst=sys_err, eps=alpha)
                
                key = (lum, f"{a} vs {b}")
                if key not in rows_dict:
                    rows_dict[key] = {"lumi": lum, "pair": f"{a} vs {b}"}
                
                rows_dict[key][f"Z_fa_eps_{int(100*sys_err):02d}"] = Z_fa
                rows_dict[key][f"Z_sh_eps_{int(100*sys_err):02d}"] = Z_sh

    return pd.DataFrame(list(rows_dict.values()))


def run_fast_mcut_scan(fitted_data_dict, labels, mcuts, mcut_max, bin_width, L_target, sys_err_list, var="m_tt", alpha=1e-12, fake_model='FakeData', bin_offset=0.0, sig_norm=False):
    """
    Computes Standard Shape and Normalized Falloff method separation significances 
    by varying the minimum mass cut using the correctly fitted baseline per systematic error.
    """
    rows_dict = {}
    mcut_base = mcuts[0]
    bins = np.arange(mcut_base + bin_offset, mcut_max + bin_width, bin_width)
    bin_edges = bins[:-1] 

    for sys_err in sys_err_list:
        active_sys_key = sys_err if sys_err in fitted_data_dict else 0.0
        
        df_sm = fitted_data_dict[active_sys_key]['df_sm']
        df_bsm = fitted_data_dict[active_sys_key]['df_bsm']
        
        sm_x, sm_w = df_sm[var].values, df_sm['weight'].values
        sm_mask = (sm_x > mcut_base) & (sm_x <= mcut_max)
        h_sm_raw = weighted_hist(sm_x[sm_mask], sm_w[sm_mask], bins)
        n_sm = h_sm_raw * L_target * 1000.0

        raw_templates = {}
        for lab in labels + [fake_model]:
            sub = df_bsm[df_bsm['label'] == lab]
            if sub.empty: continue
            
            lab_x, lab_w = sub[var].values, sub['weight'].values
            hyp_mask = (lab_x > mcut_base) & (lab_x <= mcut_max)
            if np.sum(hyp_mask) > 0:
                raw_templates[lab] = weighted_hist(lab_x[hyp_mask], lab_w[hyp_mask], bins)
        
        if fake_model not in raw_templates: continue
        ref_template = raw_templates[fake_model].copy()
        
        for lab in labels + [fake_model]:
            if lab not in raw_templates: continue
            if sig_norm:
                aligned_sig = event_number_normalization(ref_template, raw_templates[lab], lum=L_target)
                raw_templates[lab] = aligned_sig + n_sm
            else:
                raw_templates[lab] = raw_templates[lab] * L_target * 1000.0 + n_sm

        for mcut in mcuts:
            cut_mask = (bin_edges >= mcut) & (bin_edges < mcut_max)
            if not np.any(cut_mask): continue
            
            n_sm_cut = n_sm[cut_mask]
            
            norm_templates = {}
            for lab in labels + [fake_model]:
                if lab not in raw_templates: continue
                h_combined_cut = raw_templates[lab][cut_mask]
                delta = build_signed_delta(h_combined_cut, n_sm_cut, alpha=alpha)
                norm_templates[lab] = normalize_signed_template(delta, alpha=alpha)

            for lab in labels:
                if lab not in raw_templates or lab == fake_model: continue
                
                a, b = fake_model, lab
                hA, hB = raw_templates[a][cut_mask], raw_templates[b][cut_mask]
                dA, dB = norm_templates[a], norm_templates[b]
                
                Z_fa, _, _ = asimov_signed_Z_rigorous(dA, dB, hA, hB, n_sm_cut, sys_err, mode="test", alpha=alpha)
                Z_sh, _, _ = asimov_shape_Z_with_syst(hA, hB, frac_syst=sys_err, mode="test", eps=alpha)
                
                key = (mcut, f"{a} vs {b}")
                if key not in rows_dict:
                    rows_dict[key] = {"mcut": mcut, "pair": f"{a} vs {b}"}
                
                rows_dict[key][f"Z_fa_eps_{int(100*sys_err):02d}"] = Z_fa
                rows_dict[key][f"Z_sh_eps_{int(100*sys_err):02d}"] = Z_sh

    return pd.DataFrame(list(rows_dict.values()))


# ============================================================
# Grid Plotting Functions (Shape vs Falloff Comparisons)
# ============================================================

def plot_mcut_syst_grid(results, mcut_max, eps_values, metric="sh", outfile=None, excl_stats=False, fake_model='FakeData', best_fits=None):
    """Generates a grid of plots displaying significance Z-scores as a function of the minimum mass cut."""
    syst_styles = {0.00: ("black", "-"), 0.02: ("#1f77b4", "--"), 0.05: ("#ff7f0e", "-."), 0.10: ("#d62728", ":")}
    
    pairs = list(results["pair"].unique())
    fig, axes = plt.subplots(1, len(pairs), figsize=(5.0*len(pairs), 5.2), sharex=True)
    if len(pairs) == 1: axes = [axes]
    
    method_name = "Standard Shape Method" if metric == "sh" else "Normalized Falloff Method"

    for j, pair in enumerate(pairs):
        ax = axes[j]
        sub = results[results["pair"] == pair].sort_values("mcut")
        eps_v = eps_values[1:] if excl_stats else eps_values

        for eps_syst in eps_v:
            col = f"Z_{metric}_eps_{int(100*eps_syst):02d}" 
            if col not in sub.columns: continue
                
            color, ls = syst_styles.get(eps_syst, ("black", "-"))
            label = "stat. only" if eps_syst == 0 else rf"{int(100*eps_syst)}\% syst."
            ax.plot(sub["mcut"], sub[col], marker="o", color=color, linestyle=ls, label=label)

        ax.axhline(3.0, color='gray', linestyle='--', alpha=0.7, linewidth=1.5, label=r"$Z = 3\sigma$")
        ax.axhline(5.0, color='gray', linestyle=':', alpha=0.7, linewidth=1.5, label=r"$Z = 5\sigma$")

        bsm_name = pair.split(" vs ")[-1] if " vs " in pair else pair
        title_str = format_model_label(pair)
        
        mass_str = get_mass_label_from_fits(bsm_name, best_fits)
        if mass_str:
            title_str += f"\n[{mass_str}]"
        
        ax.set_title(title_str)
        if j == 0:
            ax.set_ylabel(r"Separation Significance $Z$")

        upper_label = f"{mcut_max}" if mcut_max is not None else r"\infty"
        ax.set_xlabel(rf"$m_{{t\bar t}}^{{\min}}$ up to {upper_label} [GeV]")
        ax.set_ylim(bottom=0) 
        beautify_axis(ax, grid=True) 

    plt.tight_layout(rect=[0, 0, 1, 0.86])

    handles, labels_ = axes[-1].get_legend_handles_labels()
    by_label = dict(zip(labels_, handles))
    

    fig.legend(by_label.values(), by_label.keys(), loc="center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.88))
    fig.suptitle(method_name + f' [Fake Data Baseline: {format_model_label(fake_model)}]' , fontsize=16, y=0.98)

    if outfile:
        fig.savefig(outfile, bbox_inches="tight", dpi=300)
    plt.show()


def plot_lumi_syst_grid(results, eps_values, metric="sh", outfile=None, excl_stats=False, shareY=True, fake_model='FakeData', best_fits=None, max_cols=4):
    """Generates a grid of plots displaying significance Z-scores as a function of projected luminosity."""
    syst_styles = {0.00: ("black", "-"), 0.02: ("#1f77b4", "--"), 0.05: ("#ff7f0e", "-."), 0.10: ("#d62728", ":")}
    
    pairs = list(results["pair"].unique())
    n_plots = len(pairs)
    
    # --- Custom Grid Layout ---
    if n_plots == 5:
        n_rows = 2
        fig = plt.figure(figsize=(5.0 * 3, 5.2 * 2))
        gs = gridspec.GridSpec(2, 6, figure=fig)
        
        ax0 = fig.add_subplot(gs[0, 0:2])
        ax1 = fig.add_subplot(gs[0, 2:4], sharex=ax0, sharey=ax0 if shareY else None)
        ax2 = fig.add_subplot(gs[0, 4:6], sharex=ax0, sharey=ax0 if shareY else None)
        ax3 = fig.add_subplot(gs[1, 1:3], sharex=ax0, sharey=ax0 if shareY else None)
        ax4 = fig.add_subplot(gs[1, 3:5], sharex=ax0, sharey=ax0 if shareY else None)
        
        axes_flat = [ax0, ax1, ax2, ax3, ax4]
        
        # Hide Y-ticks for inner plots to match sharey=True behavior
        if shareY:
            for ax in [ax1, ax2, ax4]:
                ax.tick_params(labelleft=False)
                
        # Force X-ticks to remain visible on all due to the staggered overhang
        for ax in axes_flat:
            ax.tick_params(labelbottom=True)
            
    else:
        n_cols = min(n_plots, max_cols)
        n_rows = int(np.ceil(n_plots / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.0 * n_cols, 5.2 * n_rows), sharex=True, sharey=shareY)
        
        axes_flat = [axes] if n_plots == 1 else axes.flatten().tolist()
        
        for k in range(n_plots, len(axes_flat)):
            fig.delaxes(axes_flat[k])
            
    # --- Plotting ---
    method_name = "Standard Shape Method" if metric == "sh" else "Normalized Falloff Method"

    for j, pair in enumerate(pairs):
        ax = axes_flat[j]
        sub = results[results["pair"] == pair].sort_values("lumi")
        eps_v = eps_values[1:] if excl_stats else eps_values

        for eps_syst in eps_v:
            col = f"Z_{metric}_eps_{int(100*eps_syst):02d}" 
            if col not in sub.columns: continue

            color, ls = syst_styles.get(eps_syst, ("black", "-"))
            label = "stat. only" if eps_syst == 0 else rf"{int(100*eps_syst)}\% syst."
            ax.plot(sub["lumi"], sub[col], marker="o", color=color, linestyle=ls, label=label)
            ax.set_ylim([0,8])

        ax.axhline(3.0, color='gray', linestyle='--', alpha=0.7, linewidth=1.5, label=r"$Z = 3\sigma$")
        ax.axhline(5.0, color='gray', linestyle=':', alpha=0.7, linewidth=1.5, label=r"$Z = 5\sigma$")

        bsm_name = pair.split(" vs ")[-1] if " vs " in pair else pair
        title_str = format_model_label(pair)
        
        if bsm_name != "SM" and best_fits is not None:
            mass_str = get_mass_label_from_fits(bsm_name, best_fits)
            if mass_str:
                title_str += f"\n[{mass_str}]"
            
        ax.set_title(title_str)
        
        # --- Edge Detection for Labels ---
        if n_plots == 5:
            is_left = (j == 0 or j == 3)
            is_bottom = (j >= 3)
        else:
            is_left = (j % min(n_plots, max_cols) == 0)
            is_bottom = (j + min(n_plots, max_cols) >= n_plots)
            
        if is_left or not shareY:
            ax.set_ylabel(r"Separation Significance $Z$")
        if is_bottom:
            ax.set_xlabel(rf"Integrated Luminosity $\mathcal{{L}}$ [fb$^{{-1}}$]")
        
        beautify_axis(ax, grid=True) 

    top_rect = 1.0 - (0.14 / n_rows)
    plt.tight_layout(rect=[0, 0, 1, top_rect])

    handles, labels_ = axes_flat[0].get_legend_handles_labels()
    by_label = dict(zip(labels_, handles))
    
    fig.legend(by_label.values(), by_label.keys(), loc="center", ncol=3, frameon=False, 
               bbox_to_anchor=(0.5, top_rect + (0.02 / n_rows)))
    fig.suptitle(method_name + f' [Fake Data Baseline: {format_model_label(fake_model)}]' , 
                 fontsize=16, y=1.0 - (0.02 / n_rows))

    if outfile is not None:
        fig.savefig(outfile, bbox_inches="tight", dpi=300)
    plt.show()



def plot_lumi_syst_combined(results, eps_values, metric="sh", outfile=None, excl_stats=False, fake_model='FakeData', best_fits=None):
    """Generates a single combined plot displaying significance Z-scores as a function of projected luminosity for all models."""
    
    # --- Color and Style Mapping ---
    colors_tab = plt.cm.tab20.colors
    color_map = {
        'SM': 'gray',
        'VLF': colors_tab[4],
        'Scalar': colors_tab[0],
        'Zprime': colors_tab[6],
        'Zprime_20pc': colors_tab[7],
        'FakeData': 'black',
        '$Z^\prime$ $(\Gamma_{Z^\prime}/M_{Z^\prime} = 0.2)$': colors_tab[7],
        '$Z^\prime$ $(\Gamma_{Z^\prime}/M_{Z^\prime} = 0.01)$': colors_tab[6],
        'Pseudo Dataset': 'black'
    }
    
    # Use line styles for systematics since color is used for models
    syst_ls = {0.00: "-", 0.02: "--", 0.05: "-.", 0.10: ":"}
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    pairs = list(results["pair"].unique())
    method_name = "Standard Shape Method" if metric == "sh" else "Normalized Falloff Method"

    for pair in pairs:
        sub = results[results["pair"] == pair].sort_values("lumi")
        eps_v = eps_values[1:] if excl_stats else eps_values
        
        
        bsm_name = pair.split(" vs ")[-1] if " vs " in pair else pair
        
       
        display_name = format_model_label(bsm_name) if 'format_model_label' in globals() else bsm_name
        
        if display_name == r'$Z^\prime$': display_name = r'$Z^\prime$ $(\Gamma_{Z^\prime}/M_{Z^\prime} = 0.01)$'
        
        model_color = color_map.get(bsm_name, color_map.get(display_name, "tab:purple"))

        for eps_syst in eps_v:
            col = f"Z_{metric}_eps_{int(100*eps_syst):02d}" 
            if col not in sub.columns: continue

            ls = syst_ls.get(eps_syst, "-")
            syst_label = "stat. only" if eps_syst == 0 else rf"{int(100*eps_syst)}\% syst."
            
            
            label_str = f"{display_name}"
            
            ax.plot(sub["lumi"], sub[col], marker="o", color=model_color, linestyle=ls, label=label_str)

    # --- Formatting the Single Axis ---
    ax.set_ylim([0, 8])
    ax.axhline(3.0, color='gray', linestyle='--', alpha=0.7, linewidth=1.5, label=r"$Z = 3\sigma$")
    ax.axhline(5.0, color='gray', linestyle=':', alpha=0.7, linewidth=1.5, label=r"$Z = 5\sigma$")

    ax.set_ylabel(r"Asimov Significance $Z$")
    ax.set_xlabel(rf"Integrated Luminosity $\mathcal{{L}}$ [fb$^{{-1}}$]")
    
    if 'beautify_axis' in globals():
        beautify_axis(ax, grid=True)
    else:
        ax.grid(True, linestyle=":", alpha=0.6)

    # --- Legend and Titles ---
    
    handles, labels_ = ax.get_legend_handles_labels()
    by_label = dict(zip(labels_, handles))
    
    
    ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(0.5, 1.01),loc="lower center", frameon=False, fontsize = 20, ncols=2)
    
    fake_model_str = format_model_label(fake_model) if 'format_model_label' in globals() else fake_model
    fig.suptitle(f"Synthetic data underlying model: {fake_model_str}")

    plt.tight_layout()

    if outfile is not None:
        fig.savefig(outfile, bbox_inches="tight", dpi=300)
    plt.show()


