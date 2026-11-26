#!/usr/bin/env python3
"""Generate and compile the matrix-element libraries used by the MEM pipeline (mem/, scripts/ at the repository root).

    python3 build_matrix_elements.py                 # all models
    python3 build_matrix_elements.py Scalar VLF      # some models
    python3 build_matrix_elements.py Zprime --force  # regenerate an existing folder

Output (relative to this directory):
    Scalar/MatrixElements             MadLoop standalone, SMS-stop_NLO-UFO          (1-loop interference)
    VLF/MatrixElements                MadLoop standalone, UV_BSM_ToyModel_NLO-UFO   (1-loop interference)
    z_prime/MatrixElements/Zprime_A   LO standalone, DMsimp_s_spin1, 2 Re(M_EW^* M_Z')
    z_prime/MatrixElements/Zprime_B   LO standalone, DMsimp_s_spin1, |M_Z'|^2

Each step (MG5 output, patch, f2py build) is described in README.md.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MG5_DIR = os.environ.get("MG5_DIR", os.path.expanduser("~/MG5"))
ZP_UFO = os.environ.get("ZP_UFO", os.path.expanduser("~/EFT_ToyModel/UFOandFAModels/DMsimp_s_spin1"))

HEADER = """set automatic_html_opening False --no_save
import model sm
define p = g u c d s u~ c~ d~ s~
"""

# MadLoop: Born x one-loop interference, only the new-physics loops (virt=NP).
# card: values written into Cards/param_card.dat, the base card of the MEM pipeline. The pipeline
# overrides the masses and y_DM for every evaluation; the new-particle width (0: no width in the
# loop propagators) and the VLF scalar couplings lamHs, lamS (0) are taken from this card.
LOOP_MODELS = {
    "Scalar": dict(out="Scalar/MatrixElements", ufo=f"{MG5_DIR}/models/SMS-stop_NLO-UFO",
                   generate="generate p p > t t~ QCD^2<=4 NP^2<=4 QED^2<=0 [virt=NP]",
                   card={"FRBLOCK": {1: 1.0}, "MASS": {5000002: 1000.0, 5000012: 900.0},
                         "DECAY": {5000002: 0.0}}),
    "VLF": dict(out="VLF/MatrixElements", ufo=f"{MG5_DIR}/models/UV_BSM_ToyModel_NLO-UFO",
                generate="generate p p > t t~ QCD^2<=4 NP1^2<=4 QED^2<=0 NP2^2<=0 NP3^2<=0 [virt=NP1]",
                card={"FRBLOCK": {1: 1.0, 2: 0.0, 3: 0.0}, "MASS": {5000006: 1500.0, 5000022: 1400.0},
                      "DECAY": {5000006: 0.0}}),
}

# Z': tree level, two separate outputs so that each coupling structure is its own library
ZP_LIBS = {
    "Zprime_B": dict(tag="ZpB", orders="DMV^2==4 QCD^2==0 QED^2==0"),           # |M_Z'|^2
    "Zprime_A": dict(tag="ZpA", orders="DMV^2==2 QED^2==2 QCD^2==0"),           # 2 Re(M_EW^* M_Z')
}
ZP_OUT = "z_prime/MatrixElements"
ZP_FLAVOURS = {"P1_uux_ttx": "uu", "P2_ddx_ttx": "dd"}


def run(cmd, cwd, log):
    print(f"  $ {cmd}   (log: {os.path.relpath(log, HERE)})", flush=True)
    with open(log, "a") as f:
        f.write(f"\n$ {cmd}\n")
        f.flush()
        r = subprocess.run(cmd, shell=True, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                           stdin=subprocess.DEVNULL)
    if r.returncode:
        sys.exit(f"FAILED ({r.returncode}): {cmd}\nsee {log}")


def mg5(script_text, script_path, log):
    with open(script_path, "w") as f:
        f.write(script_text)
    run(f"{MG5_DIR}/bin/mg5_aMC {script_path}", os.path.dirname(script_path), log)


def replace_once(text, old, new, what):
    if text.count(old) != 1:
        raise RuntimeError(f"patch '{what}': expected the original text exactly once, found {text.count(old)}")
    return text.replace(old, new)


def set_card(path, values):
    """Set entries of an SLHA param_card: {block: {id: value}}, block 'DECAY' for widths."""
    out, cur, done = [], None, set()
    for line in open(path):
        tok = line.split()
        if tok and tok[0].upper() == "BLOCK":
            cur = tok[1].upper()
        elif tok and tok[0].upper() == "DECAY":
            cur = None
            pid = int(tok[1])
            if pid in values.get("DECAY", {}):
                line = f"DECAY {pid} {values['DECAY'][pid]:.6e} {line[line.index('#'):] if '#' in line else chr(10)}"
                done.add(("DECAY", pid))
        elif cur in values and tok and not tok[0].startswith("#"):
            pid = int(tok[0])
            if pid in values[cur]:
                line = f"  {pid} {values[cur][pid]:.6e} {line[line.index('#'):] if '#' in line else chr(10)}"
                done.add((cur, pid))
        out.append(line)
    missing = {(b, i) for b, d in values.items() for i in d} - done
    if missing:
        raise KeyError(f"param_card entries not found in {path}: {sorted(missing)}")
    open(path, "w").writelines(out)


def check_fresh(path, force):
    if os.path.exists(path):
        if not force:
            sys.exit(f"{path} exists; use --force to regenerate it")
        shutil.rmtree(path)


# ------------------------------------------------------------------ MadLoop patches
# The f2py wrapper written by MG5 returns only MATELEM(1,0). We need the Born too
# (rho = finite interference / Born), so GET_ME returns ANS(4) = (Born, finite, 1/eps, 1/eps^2).
WRAPPER_PATCH = [
    ("      DOUBLE PRECISION ANS\n", "      DOUBLE PRECISION ANS(4)\n"),
    ("CF2PY INTENT(OUT) :: ANS\n", "CF2PY INTENT(OUT) :: ANS(4)\n"),
    ("      DOUBLE PRECISION OLD_ME(BUFFER_SIZE)\n", "      DOUBLE PRECISION OLD_ME(4, BUFFER_SIZE)\n"),
    ("              ANS = OLD_ME(I)\n", "              ANS(:) = OLD_ME(:,I)\n"),
    ("C     loop induce -> only finite part \n      ANS =  MATELEM(1,0)\n",
     "C     Export Full Matrix Element Array to Python\n"
     "      ANS(1) = MATELEM(0,0) ! Born (|M0|^2)\n"
     "      ANS(2) = MATELEM(1,0) ! Finite 1-loop\n"
     "      ANS(3) = MATELEM(2,0) ! Single Pole (1/eps)\n"
     "      ANS(4) = MATELEM(3,0) ! Double Pole (1/eps^2)\n"),
    ("      OLD_ME(BUFFER_POSITION) = ANS\n", "      OLD_ME(:, BUFFER_POSITION) = ANS(:)\n"),
]

# f2py target appended to each P*/makefile: a module named matrix_<model>_<Pdir>, linked
# with -Bsymbolic so that the library resolves its own Fortran symbols first.
MAKEFILE_BLOCK = """
# ---- added by build_matrix_elements.py: python module for the MEM pipeline (make so)
MODEL_NAME = {model}
PROCNAME   = $(notdir $(CURDIR))
PY_MOD     = matrix_$(MODEL_NAME)_$(PROCNAME)
HEP_LIB    = {mg5}/HEPTools/lib
F2PY_ENV   = LDFLAGS="-lstdc++ -Wl,-Bsymbolic $$LDFLAGS"
F2PY_FLAGS = --f77exec=$(FC) -I$(CURDIR)
F2PY_LIBS  = -L$(HEP_LIB) -ldhelas -lmodel $(LINK_LOOP_LIBS) -lMadLoop

so: $(PY_MOD).so

$(PY_MOD).so: ../$(OLP)_static f2py_wrapper.f
\ttouch __init__.py
\t$(F2PY_ENV) $(F2PY) -m $(PY_MOD) -c f2py_wrapper.f $(F2PY_FLAGS) -L$(CURDIR)/../../lib/ $(F2PY_LIBS)
"""


def build_loop(model, force):
    m = LOOP_MODELS[model]
    out = os.path.join(HERE, m["out"])
    check_fresh(out, force)
    log = os.path.join(HERE, f"{m['out'].split('/')[0]}/build_MatrixElements.log")
    open(log, "w").close()
    print(f"[{model}] MG5 output -> {m['out']}")
    mg5(HEADER + f"import model {m['ufo']}\n{m['generate']}\noutput {out}\n",
        os.path.join(os.path.dirname(out), "MatrixElements.mg5"), log)
    set_card(os.path.join(out, "Cards", "param_card.dat"), m["card"])
    pdirs = sorted(glob.glob(os.path.join(out, "SubProcesses", "P*_*")))
    pdirs = [p for p in pdirs if os.path.isfile(os.path.join(p, "f2py_wrapper.f"))]
    if not pdirs:
        sys.exit(f"no subprocess with f2py_wrapper.f in {out}")
    for p in pdirs:
        name = os.path.basename(p)
        print(f"[{model}] patch + compile {name}")
        w = os.path.join(p, "f2py_wrapper.f")
        shutil.copy(w, w + ".orig")
        s = open(w).read()
        for old, new in WRAPPER_PATCH:
            s = replace_once(s, old, new, f"{name}/f2py_wrapper.f")
        open(w, "w").write(s)
        mk = os.path.join(p, "makefile")
        with open(mk, "a") as f:
            f.write(MAKEFILE_BLOCK.format(model=model, mg5=MG5_DIR))
        run("make so", p, log)
        if len(glob.glob(os.path.join(p, f"matrix_{model}_{name}*.so"))) != 1:
            sys.exit(f"compiled module not found in {p}")
        # One standalone evaluation writes the helicity filter to SubProcesses/MadLoop5_resources.
        # Without it the first evaluations of a fresh folder run MadLoop's initialisation (some
        # of them return 'unstable'), and parallel workers would all initialise at once.
        print(f"[{model}] initialise MadLoop filters ({name})")
        run("make check && ./check", p, log)
    res = os.path.join(out, "SubProcesses", "MadLoop5_resources")
    if len(glob.glob(os.path.join(res, "ML5_*_HelFilter.dat"))) != len(pdirs):
        sys.exit(f"MadLoop helicity filters missing in {res}")


# ------------------------------------------------------------------ Z' patch
# MG5 3.6.3 standalone with split orders only assigns the JAMPs of the requested orders and
# leaves the others uninitialised (random results). Zero the whole array first.
JAMP_ANCHOR = "C     JAMPs contributing to orders"
JAMP_PATCH = ("C     Patched (MEM): zero all colour flows; MG5 leaves unset JAMPs uninitialised\n"
              "      JAMP = (0D0,0D0)\n")


def build_zprime(force):
    base = os.path.join(HERE, ZP_OUT)
    check_fresh(base, force)
    os.makedirs(base)
    log = os.path.join(HERE, "z_prime/build_MatrixElements.log")
    open(log, "w").close()
    text = "set automatic_html_opening False --no_save\n" + f"import model {ZP_UFO}\n"
    for lib, z in ZP_LIBS.items():
        text += (f"generate u u~ > t t~ {z['orders']}\n"
                 f"add process d d~ > t t~ {z['orders']}\n"
                 f"output standalone {os.path.join(base, lib)}\n")
    print(f"[Zprime] MG5 output -> {ZP_OUT}/{{{','.join(ZP_LIBS)}}}")
    mg5(text, os.path.join(base, "MatrixElements.mg5"), log)
    for lib, z in ZP_LIBS.items():
        for pdir, q in ZP_FLAVOURS.items():
            p = os.path.join(base, lib, "SubProcesses", pdir)
            print(f"[Zprime] patch + compile {lib}/{pdir}")
            mf = os.path.join(p, "matrix.f")
            shutil.copy(mf, mf + ".orig")
            s = open(mf).read()
            i = s.index(JAMP_ANCHOR)                    # first JAMP assignment block of MATRIX
            j = s.index("\n", i) + 1
            s = s[:j] + JAMP_PATCH + s[j:]
            open(mf, "w").write(s)
            menum = f"_{z['tag']}_{q}"
            run(f"make matrix{menum}py.so MENUM={menum}", p, log)
            if not glob.glob(os.path.join(p, f"matrix{menum}py*.so")):
                sys.exit(f"compiled module not found in {p}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("models", nargs="*", default=["Scalar", "VLF", "Zprime"],
                    choices=["Scalar", "VLF", "Zprime"])
    ap.add_argument("--force", action="store_true", help="delete and regenerate existing folders")
    a = ap.parse_args()
    for m in a.models:
        if m == "Zprime":
            build_zprime(a.force)
        else:
            build_loop(m, a.force)
    print("done")


if __name__ == "__main__":
    main()
