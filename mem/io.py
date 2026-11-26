"""LHE reading, event kinematics, parton luminosities and HDF5 helpers."""
import glob
import gzip
import os
import re
import shutil
import subprocess

import numpy as np

from . import config as cfg

H5_COMP = dict(compression="gzip", compression_opts=4, shuffle=True)


# ====================================================================== LHE
def _open_text(path):
    """Fast line iterator: pipe through zcat for .gz files when available."""
    if path.endswith(".gz") and shutil.which("zcat"):
        proc = subprocess.Popen(["zcat", path], stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
        return proc.stdout, proc
    opener = gzip.open if path.endswith(".gz") else open
    return opener(path, "rt"), None


def read_lhe(path, nmax=None):
    """Read a parton-level t tbar LHE file.

    Returns dict with
        w      (N,)   XWGTUP
        t, tb  (N,4)  top / antitop four-momenta (E, px, py, pz)
        rwgt   (N,K)  values of the <rwgt> weights, in file order (K may be 0)
        rwgt_ids      list of the K weight ids
        rwgt_info     {id: description} from <initrwgt>
        init   (N,2)  PDG ids of the incoming partons from beam 1 (+z) and beam 2 (-z)
        n_skipped     events that are not exactly t tbar + 2 incoming partons
    """
    w, t, tb, rw, ini = [], [], [], [], []
    ids, info = [], {}
    n_skipped = 0
    f, proc = _open_text(path)
    try:
        in_ev = in_initrwgt = False
        block, cur_rw = [], []
        for line in f:
            s = line.strip()
            if in_initrwgt:
                if s.startswith("</initrwgt"):
                    in_initrwgt = False
                else:
                    m = re.match(r"<weight id=['\"]([^'\"]+)['\"]\s*>(.*?)</weight>", s)
                    if m:
                        info[m.group(1)] = m.group(2).strip()
                continue
            if s.startswith("<initrwgt"):
                in_initrwgt = True
                continue
            if s.startswith("<event"):
                in_ev, block, cur_rw = True, [], []
                continue
            if not in_ev:
                continue
            if s.startswith("<wgt"):
                m = re.match(r"<wgt id=['\"]([^'\"]+)['\"]\s*>\s*([^<\s]+)", s)
                cur_rw.append(float(m.group(2)))
                if len(w) == 0 and len(cur_rw) > len(ids):
                    ids.append(m.group(1))
                continue
            if s.startswith("</event"):
                in_ev = False
                nup = int(block[0].split()[0])
                pt_ = ptb_ = None
                n_in = n_out = 0
                b1 = b2 = 0
                for ln in block[1:1 + nup]:
                    c = ln.split()
                    if c[1] == "-1":
                        n_in += 1
                        if float(c[8]) > 0:
                            b1 = int(c[0])
                        else:
                            b2 = int(c[0])
                    elif c[1] == "1":
                        n_out += 1
                        v = (float(c[9]), float(c[6]), float(c[7]), float(c[8]))
                        if c[0] == "6":
                            pt_ = v
                        elif c[0] == "-6":
                            ptb_ = v
                if n_in != 2 or n_out != 2 or pt_ is None or ptb_ is None:
                    n_skipped += 1
                    continue
                w.append(float(block[0].split()[2]))
                t.append(pt_)
                tb.append(ptb_)
                rw.append(cur_rw)
                ini.append((b1, b2))
                if nmax and len(w) >= nmax:
                    break
                continue
            if s and not s.startswith("<") and not s.startswith("#"):
                block.append(s)
    finally:
        if proc is not None:
            proc.kill()
            proc.wait()
        else:
            f.close()
    rw = np.array(rw, dtype=np.float64) if rw and rw[0] else np.zeros((len(w), 0))
    return dict(w=np.array(w), t=np.array(t), tb=np.array(tb), rwgt=rw, rwgt_ids=ids, init=np.array(ini),
                rwgt_info=info, n_skipped=n_skipped)


def channel_labels(init):
    """0 = gg, 1 = quark from beam 1, 2 = quark from beam 2 (antiquark from beam 1)."""
    lab = np.zeros(len(init), dtype=np.uint8)
    lab[(init[:, 0] > 0) & (init[:, 0] < 21)] = 1
    lab[(init[:, 0] < 0)] = 2
    return lab


def read_summary_xsec(run_dir):
    """Correct total cross section [pb] of a biased aMC@NLO run (summary.txt).

    With a generation bias the 'Total cross section' line includes the bias
    ("DO NOT USE"); the physical value is the central value of the scale-variation block.
    Falls back to the 'Total cross section' line for unbiased runs.
    """
    path = os.path.join(run_dir, "summary.txt")
    txt = open(path).read()
    m = re.search(r"Scale variation.*?\n.*?\n\s*([0-9.eE+-]+)\s*pb", txt, re.S)
    if m:
        return float(m.group(1))
    m = re.search(r"Total cross section:\s*([0-9.eE+-]+)", txt)
    if m:
        return float(m.group(1))
    raise ValueError(f"no cross section found in {path}")


def find_lhe(run_dir):
    files = sorted(glob.glob(os.path.join(run_dir, "*events.lhe*")))
    if not files:
        raise FileNotFoundError(f"no LHE file in {run_dir}")
    return files[0]


# ====================================================================== kinematics
def boost_to_rest(p, P):
    """Boost four-vectors p (n,4) into the rest frame of P (n,4). Order (E, px, py, pz)."""
    b = P[:, 1:] / P[:, :1]
    b2 = np.sum(b * b, axis=1)
    gamma = 1.0 / np.sqrt(1.0 - b2)
    bp = np.sum(b * p[:, 1:], axis=1)
    g2 = np.where(b2 > 0, (gamma - 1.0) / np.where(b2 > 0, b2, 1.0), 0.0)
    p3 = p[:, 1:] + (g2 * bp - gamma * p[:, 0])[:, None] * b
    return np.column_stack([gamma * (p[:, 0] - bp), p3])


def kinematics(t, tb, sqrt_s=cfg.SQRT_S, mt=cfg.MT):
    """Observables and the variables needed to rebuild the partonic momenta.

    The event is (mtt, ytt, n), n = top direction in the t tbar rest frame (the
    t tbar system has no transverse momentum at LO). x1, x2 follow from mtt, ytt.
    mu0 = H_T/2 = sqrt(mt^2 + pT^2) (aMC@NLO dynamical_scale_choice = -1 for 2 -> 2).
    """
    tt = t + tb
    shat = tt[:, 0] ** 2 - np.sum(tt[:, 1:] ** 2, axis=1)
    mtt = np.sqrt(shat)
    ytt = 0.5 * np.log((tt[:, 0] + tt[:, 3]) / (tt[:, 0] - tt[:, 3]))
    tau = mtt / sqrt_s
    x1, x2 = tau * np.exp(ytt), tau * np.exp(-ytt)
    pt = np.hypot(t[:, 1], t[:, 2])
    mu0 = np.sqrt(mt ** 2 + pt ** 2)
    tstar = boost_to_rest(t, tt)
    n = tstar[:, 1:] / np.linalg.norm(tstar[:, 1:], axis=1)[:, None]
    return dict(x1=x1, x2=x2, mtt=mtt, ytt=ytt, n=n, pt=pt, mu0=mu0, cost=n[:, 2],
                pt_tt_max=float(np.max(np.hypot(tt[:, 1], tt[:, 2]))),
                mtop=np.sqrt(np.maximum(t[:, 0] ** 2 - np.sum(t[:, 1:] ** 2, axis=1), 0.0)))


def partonic_momenta(mtt, n, mt=cfg.MT, swap=False):
    """Exactly on-shell momenta in the partonic CM frame, shape (N, 4 particles, 4).

    Particle order of the MadGraph processes: (parton 1, parton 2, t, tbar), parton 1
    along +z (beam 1). swap=True exchanges the incoming momenta (parton 1 from beam 2).
    """
    eh = 0.5 * mtt
    pm = np.sqrt(np.maximum(eh ** 2 - mt ** 2, 0.0))
    z = np.zeros_like(eh)
    P = np.empty((len(mtt), 4, 4))
    P[:, 0] = np.column_stack([eh, z, z, eh])
    P[:, 1] = np.column_stack([eh, z, z, -eh])
    P[:, 2, 0], P[:, 2, 1:] = eh, pm[:, None] * n
    P[:, 3, 0], P[:, 3, 1:] = eh, -pm[:, None] * n
    if swap:
        P[:, [0, 1]] = P[:, [1, 0]]
    return P


# ====================================================================== PDFs
_PDF_CACHE = {}


def get_pdf(lhaid=cfg.LHAID, member=0):
    import lhapdf
    key = (lhaid, member)
    if key not in _PDF_CACHE:
        lhapdf.setVerbosity(0)
        if member == 0:
            _PDF_CACHE[key] = lhapdf.mkPDF(int(lhaid))
        else:
            _PDF_CACHE[key] = lhapdf.mkPDF(lhapdf.mkPDF(int(lhaid)).set().name, member)
    return _PDF_CACHE[key]


def fluxes(x1, x2, Q, pdf):
    """Signed parton luminosities per ordered flavour pair, shape (N, len(FLUX_GROUPS)).

    Order: cfg.FLUX_GROUPS. f = xfxQ/x. The sign is kept (NNPDF2.3 densities are
    negative at large x); the |.| convention of MadEvent is obtained element-wise.
    """
    def f(pid, x):
        return np.asarray(pdf.xfxQ(pid, x, Q)) / x
    out = np.empty((len(x1), len(cfg.FLUX_GROUPS)))
    out[:, 0] = f(21, x1) * f(21, x2)
    k = 1
    for q, pid in cfg.QUARKS.items():
        out[:, k] = f(pid, x1) * f(-pid, x2)
        out[:, k + 1] = f(-pid, x1) * f(pid, x2)
        k += 2
    return out


def alphas(Q, pdf):
    return np.array([pdf.alphasQ(float(q)) for q in Q])
