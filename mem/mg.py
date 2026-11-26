"""MadGraph matrix-element libraries: loading, param_card editing and evaluation workers.

IMPORTANT: load at most ONE MadGraph f2py library per Python process. The libraries
export identical Fortran symbols and COMMON blocks; a second library in the same
process silently uses the first one's. The workers below are meant to run in fresh
processes (ProcessPoolExecutor with max_tasks_per_child=1).
"""
import contextlib
import glob
import importlib.util
import os
import sys
import tempfile

import numpy as np

from . import config as cfg
from .io import partonic_momenta


@contextlib.contextmanager
def silence_fortran():
    """Redirect the process-level stdout/stderr (Fortran prints) to /dev/null."""
    sys.stdout.flush()
    sys.stderr.flush()
    devnull = os.open(os.devnull, os.O_WRONLY)
    old = os.dup(1), os.dup(2)
    try:
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        yield
    finally:
        os.dup2(old[0], 1)
        os.dup2(old[1], 2)
        for fd in (devnull, *old):
            os.close(fd)


def write_card(base, blocks=None, decays=None):
    """Copy a param_card replacing entries of the given blocks and DECAY widths.
    Raises if a requested entry is not found. Returns a short temporary path
    (the Fortran readers use fixed-length CHARACTER buffers)."""
    blocks = {k.upper(): dict(v) for k, v in (blocks or {}).items()}
    decays = dict(decays or {})
    found = set()
    fd, path = tempfile.mkstemp(suffix=".dat", prefix="mem_", dir="/tmp", text=True)
    cur = None
    with open(base) as fin, os.fdopen(fd, "w") as fout:
        for line in fin:
            tok = line.split()
            if tok and tok[0].upper() == "BLOCK":
                cur = tok[1].upper() if len(tok) > 1 else None
            elif tok and tok[0].upper() == "DECAY":
                cur = None
                try:
                    pid = int(tok[1])
                except (IndexError, ValueError):
                    pid = None
                if pid in decays:
                    line = f"DECAY {pid} {decays[pid]:.10e}\n"
                    found.add(("DECAY", pid))
            elif cur in blocks and len(tok) >= 2 and not tok[0].startswith("#"):
                try:
                    pid = int(tok[0])
                    float(tok[1])
                except ValueError:
                    pid = None
                if pid in blocks[cur]:
                    comment = line[line.index("#"):] if "#" in line else "\n"
                    line = f"    {pid} {blocks[cur][pid]:.10e} {comment}"
                    found.add((cur, pid))
            fout.write(line)
    wanted = {(b, p) for b, d in blocks.items() for p in d} | {("DECAY", p) for p in decays}
    missing = wanted - found
    if missing:
        os.remove(path)
        raise KeyError(f"param_card entries not found in {base}: {sorted(missing)}")
    if len(path) >= 128:
        raise RuntimeError(f"temporary card path too long for Fortran: {path}")
    return path


def load_library(subdir):
    """Import the f2py module of a MadGraph subprocess directory."""
    sos = sorted(glob.glob(os.path.join(subdir, "*.so")))
    if len(sos) != 1:
        raise FileNotFoundError(f"expected exactly one compiled .so in {subdir}, found {sos}")
    name = os.path.basename(sos[0]).split(".")[0]
    spec = importlib.util.spec_from_file_location(name, sos[0])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    attrs = dir(mod)

    def pick(suf):
        return next((getattr(mod, a) for a in attrs if a.lower().endswith(suf)), None)
    return dict(init=pick("initialisemodel") or pick("initialise"),
                get_me=pick("get_me"),            # MadLoop: (P, alphas, mu^2, nhel) -> (ans[4], rc)
                get_value=pick("get_value"))      # LO standalone: (P, alphas, nhel=0 summed) -> ans


def _fortran(P):
    return [np.asfortranarray(p.T) for p in P]


def _loop_ok(rc):
    return (rc % 100) // 10 == 1


# ====================================================================== one-loop models
def task_loop(model, ch, mtt, n, alphas0, mu0, masses, check_scales=None):
    """MadLoop library of `model`, channel ch in {gg, qq}.

    Returns the SM Born |M|^2 (first mass), rho[m, j] = finite one-loop interference /
    Born at y_DM = 1 for every mass, a quality flag per event, and a re-evaluation
    check of the first events (guards against first-call artefacts).
    check_scales: optional (alphas_lo, mu_lo, alphas_hi, mu_hi) arrays for a mu_R test
    at the first mass.
    """
    mcfg = cfg.LOOP_MODELS[model]
    subdir = os.path.join(mcfg["root"], "SubProcesses", mcfg["channels"][ch])
    base = os.path.join(mcfg["root"], "Cards", "param_card.dat")
    N = len(mtt)
    Pf = _fortran(partonic_momenta(mtt, n))
    born = np.full(N, np.nan)
    rho = np.full((len(masses), N), np.nan, dtype=np.float32)
    flag = np.zeros(N, dtype=bool)
    recheck = 0.0
    scale_test = None
    os.chdir(subdir)                       # MadLoop reads MadLoop5_resources from the cwd
    with silence_fortran():
        lib = load_library(subdir)
        get_me = lib["get_me"]

        def ev(j, a, s2):
            ans, rc = get_me(Pf[j], a, s2, -1)
            if not _loop_ok(rc):           # re-evaluate bypassing the wrapper cache (|M|^2 ~ alpha_s^2)
                a2 = a * (1 + 1e-9)
                ans2, rc = get_me(Pf[j], a2, s2, -1)
                ans = np.asarray(ans2) * (a / a2) ** 2
            return np.asarray(ans), _loop_ok(rc)

        for m, M in enumerate(masses):
            card = write_card(base, mcfg["card"](M))
            try:
                lib["init"](card)
                for k in range(5):                                   # warm-up, discarded
                    get_me(Pf[k % N], alphas0[k % N] * (1 + 1e-7 * (k + 1)), mu0[k % N] ** 2, -1)
                for j in range(N):
                    ans, ok = ev(j, alphas0[j], mu0[j] ** 2)
                    flag[j] |= not ok
                    if m == 0:
                        born[j] = ans[0]
                    rho[m, j] = ans[1] / ans[0]
                for j in range(min(3, N)):                           # stability re-check
                    ans, _ = ev(j, alphas0[j] * (1 + 3e-9), mu0[j] ** 2)
                    recheck = max(recheck, abs(ans[1] / ans[0] / rho[m, j] - 1))
                if m == 0 and check_scales is not None:
                    a_lo, mu_lo, a_hi, mu_hi = check_scales
                    rows = []
                    for j in range(min(len(a_lo), N)):
                        lo, _ = ev(j, a_lo[j], mu_lo[j] ** 2)
                        hi, _ = ev(j, a_hi[j], mu_hi[j] ** 2)
                        rows.append([lo[1] / lo[0], hi[1] / hi[0]])
                    scale_test = np.array(rows)
            finally:
                os.remove(card)
    return dict(born=born, rho=rho, flag=flag, recheck=recheck, scale_test=scale_test)


def task_loop_swap(model, mtt, n, alphas0, mu0, mass):
    """Beam-swap symmetry check of the q qbar one-loop library: rho(p1,p2) and rho(p2,p1)."""
    mcfg = cfg.LOOP_MODELS[model]
    subdir = os.path.join(mcfg["root"], "SubProcesses", mcfg["channels"]["qq"])
    base = os.path.join(mcfg["root"], "Cards", "param_card.dat")
    out = np.zeros((2, 2, len(mtt)))                     # [orientation, (born, rho)]
    os.chdir(subdir)
    with silence_fortran():
        lib = load_library(subdir)
        card = write_card(base, mcfg["card"](mass))
        try:
            lib["init"](card)
            for o, swap in enumerate((False, True)):
                Pf = _fortran(partonic_momenta(mtt, n, swap=swap))
                for k in range(5):
                    lib["get_me"](Pf[0], alphas0[0] * (1 + 1e-7 * (k + 1)), mu0[0] ** 2, -1)
                for j in range(len(mtt)):
                    ans, _ = lib["get_me"](Pf[j], alphas0[j], mu0[j] ** 2, -1)
                    out[o, 0, j], out[o, 1, j] = ans[0], ans[1] / ans[0]
        finally:
            os.remove(card)
    return out


# ====================================================================== Z'
def _zp_eval(lib, base, Pf, M, G):
    card = write_card(base, {**cfg.ZP_COUPLINGS, "MASS": {5000001: M}}, decays={5000001: G})
    try:
        lib["init"](card)
        for k in range(5):
            lib["get_value"](Pf[k % len(Pf)], 0.118, 0)       # warm-up (helicity filter)
        return np.array([lib["get_value"](p, 0.118, 0) for p in Pf])
    finally:
        os.remove(card)


def task_zprime(piece, q, mtt, n, validate=0):
    """Kinematic functions of the Z' piece (A or B) for flavour q in {u, d}, both orientations.

    Returns {orientation: arrays}: piece B -> K; piece A -> R, I (see config). If
    validate > 0, the first `validate` events are also evaluated at two extra (M, Gamma)
    points and the maximal relative deviation from the Breit-Wigner form is returned.
    """
    root = cfg.ZP_LIBS[piece]
    subdir = os.path.join(root, "SubProcesses", cfg.ZP_SUBDIRS[q])
    base = os.path.join(root, "Cards", "param_card.dat")
    s = mtt ** 2
    D = lambda M, G: (s - M ** 2) ** 2 + M ** 2 * G ** 2
    out, dev = {}, 0.0
    os.chdir(subdir)                       # lha_read looks for ident_card.dat in the parent directories
    with silence_fortran():
        lib = load_library(subdir)
        for o, swap in (("fw", False), ("bw", True)):
            Pf = _fortran(partonic_momenta(mtt, n, swap=swap))
            if piece == "B":
                (M, G), = cfg.ZP_REF_POINTS["B"]
                K = _zp_eval(lib, base, Pf, M, G) * D(M, G)
                out[o] = dict(K=K)
                pred = lambda M, G, sl: K[sl] / D(M, G)[sl]
            else:
                (M1, G1), (M2, G2) = cfg.ZP_REF_POINTS["A"]
                R = _zp_eval(lib, base, Pf, M1, G1) * D(M1, G1) / (s - M1 ** 2)
                I = (_zp_eval(lib, base, Pf, M2, G2) * D(M2, G2) - (s - M2 ** 2) * R) / (M2 * G2)
                out[o] = dict(R=R, I=I)
                pred = lambda M, G, sl: ((s[sl] - M ** 2) * R[sl] + M * G * I[sl]) / D(M, G)[sl]
            if validate:
                sl = slice(0, min(validate, len(mtt)))
                for (M, G) in ((3000.0, 30.0), (2500.0, 500.0)):
                    direct = _zp_eval(lib, base, Pf[sl], M, G)
                    dev = max(dev, float(np.max(np.abs(pred(M, G, sl) - direct)) / np.max(np.abs(direct))))
    return dict(out=out, bw_dev=dev)
