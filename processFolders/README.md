# processFolders

MadGraph5_aMC@NLO process folders for every model of the analysis.

| folder | content |
|---|---|
| `sm/pp2ttbar_gs4` | SM sample used by the analysis (section 0) |
| `Scalar/`, `VLF/`, `z_prime/` | event-generation folders (`pp2ttbar*`) and the cards used to produce the signal samples |
| `Scalar/MatrixElements` | MadLoop library: one-loop Scalar interference, used by the MEM |
| `VLF/MatrixElements` | MadLoop library: one-loop VLF interference, used by the MEM |
| `z_prime/MatrixElements/Zprime_{A,B}` | tree-level Z' libraries, used by the MEM |
| `build_matrix_elements.py` | generates and compiles the three `MatrixElements` folders |

## 0. Generating the SM sample

The SM sample of the analysis is an aMC@NLO fixed-order run of the **Scalar UFO with the new-physics
coupling switched off**. Only the $g_s^4$ (pure QCD Born) contribution is selected, and the events are
generated with an $m_{t\bar t}$ bias. Everything needed is in `sm/`:

| file | role |
|---|---|
| `sm/pp2ttbar_gs4.mg5` | MG5 commands that create the folder (`generate p p > t t~ [QCD NP]`, UFO `../../UFO_Models/SMS-stop_NLO-UFO`) |
| `sm/pp2ttbar_gs4/Cards/param_card.dat` | `ydm = 0`; `mst = 1500`, used only by the bias function |
| `sm/pp2ttbar_gs4/Cards/FKS_params.dat` | `#SelectedCouplingOrders` = `0 4 0`, so only $g_s^4$. The columns follow `SubProcesses/P*/orders.inc`, here `NP, QCD, QED` |
| `sm/pp2ttbar_gs4/Cards/run_card.dat` | 13.6 TeV, LHAPDF 244800, $\mu = H_T/2$ (`dynamical_scale_choice = -1`), `req_acc_FO = 0.0009`, top $p_T \in [0.5, 3.5]$ TeV (`pt_min_pdg`, `pt_max_pdg`), `event_norm = bias`, `custom_fcts = ../Source/mtt_bias_NLO.f` |
| `sm/pp2ttbar_gs4/Cards/FO_analyse_card.dat` | `FO_ANALYSIS_FORMAT = LHE`: the fixed-order run writes weighted events |
| `sm/pp2ttbar_gs4/Source/mtt_bias_NLO.f` | the $m_{t\bar t}$ bias, peaked at $2.05\,m_{st}$ |

Requirements: MG5_aMC v3.6.3 **with the bias patch** (`../mg5_bias_patch/README.md`). Without it, the
weights of each channel are normalised to the biased cross section.

```bash
cd processFolders/sm
cp -r pp2ttbar_gs4/Cards pp2ttbar_gs4/Source /tmp/sm_cards       # keep the tracked cards
rm -rf pp2ttbar_gs4                                              # only if the folder must be recreated
<MG5>/bin/mg5_aMC pp2ttbar_gs4.mg5                               # creates pp2ttbar_gs4 (default cards)
cp /tmp/sm_cards/Cards/*.dat pp2ttbar_gs4/Cards/
cp /tmp/sm_cards/Source/mtt_bias_NLO.f pp2ttbar_gs4/Source/
cd pp2ttbar_gs4/bin
printf "order=NLO\nfixed_order=ON\nshower=OFF\ndone\ndone\n" | ./generate_events -n bias_sm_13_6TeV_fiducial_pT
```

The run takes about 10 minutes on 16 cores and writes
`Events/bias_sm_13_6TeV_fiducial_pT/events.lhe.gz` (about 2.4M weighted events), which is the input
of `../scripts/prepare_events.py` (`SM_RUN` in `../mem/config.py`). The summary should read
`Total cross section, bias removed: 1.424e+00 pb` (the line is added by the bias patch). A new run is
statistically equivalent to the original, not identical, because the events come from MINT's
random sampling.

The same recipe gives the Scalar signal (SM + interference) sample with `ydm = 7.5` and two selected
lines in `#SelectedCouplingOrders`, `2 4 0` (Born x one-loop NP interference) and `0 4 0` (SM Born). **Check the column order in `orders.inc` for every
UFO:** for the VLF it is `NP2, NP1, NP3, QCD, QED`, so its interference is `0 2 0 4 0`.

---

The rest of this file is about the `MatrixElements` folders: how to generate them, and how the
MEM pipeline (`../mem`, `../scripts`) uses them to compute the matrix elements of each event.

---

## 1. What the libraries compute

| model | folder | MG5 process | returned quantity |
|---|---|---|---|
| Scalar | `Scalar/MatrixElements` | `p p > t t~ QCD^2<=4 NP^2<=4 QED^2<=0 [virt=NP]` (UFO `SMS-stop_NLO-UFO`) | SM Born $\|M_0\|^2$ and the finite one-loop interference $2\,\mathrm{Re}(M_0^* M_1^{NP})$ |
| VLF | `VLF/MatrixElements` | `p p > t t~ QCD^2<=4 NP1^2<=4 QED^2<=0 NP2^2<=0 NP3^2<=0 [virt=NP1]` (UFO `UV_BSM_ToyModel_NLO-UFO`) | same, with NP1 loops only |
| Z' (B) | `z_prime/MatrixElements/Zprime_B` | `q q~ > t t~ DMV^2==4 QCD^2==0 QED^2==0`, q = u, d (UFO `DMsimp_s_spin1`) | $\|M_{Z'}\|^2$ |
| Z' (A) | `z_prime/MatrixElements/Zprime_A` | `q q~ > t t~ DMV^2==2 QED^2==2 QCD^2==0`, q = u, d | $2\,\mathrm{Re}(M_{EW}^* M_{Z'})$, $\gamma$ + Z |

Subprocesses: the one-loop folders contain `P2_gg_ttx` and `P0_uux_ttx`. `P0_uux_ttx` is used for
every light quark: the new physics couples to the top only, so the matrix element does not depend
on the light-quark flavour. The Z' libraries contain `P1_uux_ttx` and `P2_ddx_ttx`.

## 2. Requirements

- MadGraph5_aMC@NLO **v3.6.3** in `~/MG5` (or set `MG5_DIR`), with the loop tools that MadLoop
  installs in `HEPTools` (CutTools, IREGI, Ninja, OneLOop, COLLIER).
- The UFO models: `SMS-stop_NLO-UFO` and `UV_BSM_ToyModel_NLO-UFO` in `$MG5_DIR/models`, and
  `DMsimp_s_spin1` in `~/EFT_ToyModel/UFOandFAModels` (or set `ZP_UFO` to its path).
- `gfortran`, Python 3 with `numpy` (`f2py`, which uses `meson` and `ninja` to compile).

The bias patch of MG5 (`../mg5_bias_patch`) changes only the NLO event-generation code, so it
has no effect on these libraries.

## 3. Generating the folders

```bash
cd processFolders
python3 build_matrix_elements.py                  # all models, about 2 minutes
python3 build_matrix_elements.py Scalar VLF       # only some models
python3 build_matrix_elements.py VLF --force      # delete and regenerate an existing folder
```

Logs: `Scalar/build_MatrixElements.log`, `VLF/build_MatrixElements.log`,
`z_prime/build_MatrixElements.log`. The MG5 commands that were run are saved next to each folder
(`Scalar/MatrixElements.mg5`, `VLF/MatrixElements.mg5`, `z_prime/MatrixElements/MatrixElements.mg5`).

The script does the following. Each step can also be done by hand.

### 3.1 One-loop models (Scalar, VLF)

1. **MG5 output.**
   ```
   set automatic_html_opening False --no_save
   import model sm
   define p = g u c d s u~ c~ d~ s~
   import model <UFO>
   generate <process of section 1>
   output Scalar/MatrixElements            # MadLoop standalone output
   ```
2. **Base `param_card.dat`.** `Cards/param_card.dat` is the card the pipeline copies before every
   evaluation. The pipeline sets the masses and $y_{DM}$ itself (`mem/config.py`), but every other
   entry comes from this card. The script sets:

   | model | entries |
   |---|---|
   | Scalar | `yDM = 1`, `mST = 1000`, `mChi = 900`, `DECAY 5000002 (wST) = 0` |
   | VLF | `yDM = 1`, `lamHs = 0`, `lamS = 0`, `mPsiT = 1500`, `mSDM = 1400`, `DECAY 5000006 (WPsiT) = 0` |

   The UFO defaults are a width of 1 GeV for the new coloured particle and, for the VLF,
   `lamHs = lamS = 1`. The analysis uses zero widths in the loop and no scalar self-couplings.
3. **Patch `SubProcesses/P*/f2py_wrapper.f`.** MG5 writes a `GET_ME` that returns only the finite
   part, `ANS = MATELEM(1,0)`. The pipeline also needs the Born, so `ANS` becomes an array of four
   values (the original is kept as `f2py_wrapper.f.orig`):
   ```fortran
         DOUBLE PRECISION ANS(4)
   CF2PY INTENT(OUT) :: ANS(4)
         DOUBLE PRECISION OLD_ME(4, BUFFER_SIZE)        ! internal cache of the last 5 points
         ...
               ANS(:) = OLD_ME(:,I)
         ...
         ANS(1) = MATELEM(0,0) ! Born (|M0|^2)
         ANS(2) = MATELEM(1,0) ! Finite 1-loop
         ANS(3) = MATELEM(2,0) ! Single Pole (1/eps)
         ANS(4) = MATELEM(3,0) ! Double Pole (1/eps^2)
         ...
         OLD_ME(:, BUFFER_POSITION) = ANS(:)
   ```
4. **Add a `so` target to `SubProcesses/P*/makefile` and run `make so`.** This builds the static
   MadLoop library (`lib/libMadLoop.a`) and the Python module
   `matrix_<model>_<Pdir>.cpython-*.so`:
   ```make
   MODEL_NAME = Scalar
   PROCNAME   = $(notdir $(CURDIR))
   PY_MOD     = matrix_$(MODEL_NAME)_$(PROCNAME)
   HEP_LIB    = $(HOME)/MG5/HEPTools/lib
   F2PY_ENV   = LDFLAGS="-lstdc++ -Wl,-Bsymbolic $$LDFLAGS"
   F2PY_FLAGS = --f77exec=$(FC) -I$(CURDIR)
   F2PY_LIBS  = -L$(HEP_LIB) -ldhelas -lmodel $(LINK_LOOP_LIBS) -lMadLoop

   so: $(PY_MOD).so

   $(PY_MOD).so: ../$(OLP)_static f2py_wrapper.f
   	touch __init__.py
   	$(F2PY_ENV) $(F2PY) -m $(PY_MOD) -c f2py_wrapper.f $(F2PY_FLAGS) -L$(CURDIR)/../../lib/ $(F2PY_LIBS)
   ```
   `-Wl,-Bsymbolic` makes each module resolve its own Fortran symbols first.
5. **Initialise MadLoop:** `make check && ./check` in each `P*` directory. The first evaluation in
   a new folder writes the helicity filter (`SubProcesses/MadLoop5_resources/ML5_*_HelFilter.dat`).
   While that file is missing, MadLoop is in its initialisation stage. Some points then return a
   code the pipeline treats as unstable, and the parallel workers would all initialise at the same
   time. The script stops if the filter files are missing.

### 3.2 Z'

1. **MG5 output**, one LO standalone folder per coupling structure:
   ```
   set automatic_html_opening False --no_save
   import model ~/EFT_ToyModel/UFOandFAModels/DMsimp_s_spin1
   generate u u~ > t t~ DMV^2==4 QCD^2==0 QED^2==0
   add process d d~ > t t~ DMV^2==4 QCD^2==0 QED^2==0
   output standalone z_prime/MatrixElements/Zprime_B
   generate u u~ > t t~ DMV^2==2 QED^2==2 QCD^2==0
   add process d d~ > t t~ DMV^2==2 QED^2==2 QCD^2==0
   output standalone z_prime/MatrixElements/Zprime_A
   ```
2. **Patch `SubProcesses/P*/matrix.f`.** With split orders, MG5 3.6.3 assigns only the colour
   flows (`JAMP`) of the requested orders and leaves the others uninitialised, which gives random
   results. The script zeroes the array before the first assignment (the original is kept as
   `matrix.f.orig`):
   ```fortran
   C     JAMPs contributing to orders QCD=0 DMV=2 QED=0
   C     Patched (MEM): zero all colour flows; MG5 leaves unset JAMPs uninitialised
         JAMP = (0D0,0D0)
         JAMP(1,1) = ...
   ```
3. **Compile** with MG5's own f2py target, one module per subprocess:
   ```bash
   cd z_prime/MatrixElements/Zprime_A/SubProcesses/P1_uux_ttx
   make matrix_ZpA_uupy.so MENUM=_ZpA_uu        # ZpA/ZpB x uu/dd
   ```

### 3.3 Result

```
Scalar/MatrixElements/SubProcesses/P0_uux_ttx/matrix_Scalar_P0_uux_ttx.cpython-*.so
Scalar/MatrixElements/SubProcesses/P2_gg_ttx/matrix_Scalar_P2_gg_ttx.cpython-*.so
VLF/MatrixElements/SubProcesses/P0_uux_ttx/matrix_VLF_P0_uux_ttx.cpython-*.so
VLF/MatrixElements/SubProcesses/P2_gg_ttx/matrix_VLF_P2_gg_ttx.cpython-*.so
z_prime/MatrixElements/Zprime_{A,B}/SubProcesses/P1_uux_ttx/matrix_Zp{A,B}_uupy.cpython-*.so
z_prime/MatrixElements/Zprime_{A,B}/SubProcesses/P2_ddx_ttx/matrix_Zp{A,B}_ddpy.cpython-*.so
```

---

## 4. Computing the matrix elements (MEM pipeline)

The paths are set in `../mem/config.py` (`PROC_DIR`, `LOOP_MODELS[...]["root"]`, `ZP_LIBS`).
They point to these folders, so after a rebuild nothing else needs to change.

```bash
cd ../scripts
python3 prepare_events.py                                          # LHE -> ../data/events.h5
nohup python3 compute_me.py --nproc 15 > ../data/compute_me.log 2>&1 &   # -> ../data/me_{Scalar,VLF,Zprime}.h5
```

- `compute_me.py` is resumable: rerun the same command to continue an interrupted run.
- Test on the 1-in-40 subsample: `python3 prepare_events.py --stride 40 --out ../data/events_s40.h5`,
  then `python3 compute_me.py --events ../data/events_s40.h5 --chunk 2500`.
- `--models Scalar,VLF` computes only some models.

What is stored (see the header of `compute_me.py`):

| file | content |
|---|---|
| `me_Scalar.h5`, `me_VLF.h5` | `born[N, (gg, qq)]` and `rho_gg`, `rho_qq` [mass, N] = interference / Born at $y_{DM}=1$, for the masses in `config.LOOP_MODELS` ($m_{DM} = M - 100$ GeV); `flag` = MadLoop unstable after a re-evaluation |
| `me_Zprime.h5` | $K$ (from B) and $R$, $I$ (from A) per flavour and beam orientation, at $g_q=g_t=1$, so that $\|M_{Z'}\|^2 = K/D$ and $2\mathrm{Re}(M_{EW}^*M_{Z'}) = [(s-M^2)R + M\Gamma I]/D$ with $D=(s-M^2)^2+M^2\Gamma^2$, for any $(M,\Gamma)$ |

### Using a library directly

`../mem/mg.py` contains the loaders. The essentials:

```python
import os, numpy as np
from mem import mg                       # run from the repository root

sub = "<path>/processFolders/VLF/MatrixElements/SubProcesses/P0_uux_ttx"
base = "<path>/processFolders/VLF/MatrixElements/Cards/param_card.dat"
os.chdir(sub)                            # MadLoop reads ../MadLoop5_resources relative to the cwd
lib = mg.load_library(sub)               # imports the single .so of the directory
card = mg.write_card(base, {"MASS": {5000006: 1500.0, 5000022: 1400.0}, "FRBLOCK": {1: 1.0}})
lib["init"](card)                        # INITIALISE(path): reads the param_card
P = np.asfortranarray(p.T)               # p: (4 particles, 4) array (E, px, py, pz) in the partonic CM frame
ans, rc = lib["get_me"](P, alphas, muR**2, -1)   # -1: sum over helicities
born, interference = ans[0], ans[1]      # ans[2], ans[3]: 1/eps and 1/eps^2 poles (zero for a finite interference)
ok = (rc % 100) // 10 == 1               # tens digit 1: double precision, MadLoop not initialising
```

The Z' libraries have `INITIALISEMODEL(path)` and `GET_VALUE(P, alphas, nhel)`, with `nhel = 0`
for the helicity sum (`mg.task_zprime`). The couplings and the width are set in the card:
`DMINPUTS` and `DECAY 5000001`.

Rules:
- **Load at most one library per Python process.** All libraries export the same Fortran
  symbols and COMMON blocks. A second library in the same process silently uses the first
  one's. `compute_me.py` runs each task in a new process (`max_tasks_per_child=1`).
- The param_card path given to `init` must be shorter than 128 characters (fixed-length Fortran
  string). `mg.write_card` writes to `/tmp` and checks this.
- `GET_ME` caches the last 5 points. To re-evaluate the same point (for example after an unstable
  return code), change `alphas` by a relative 1e-9 and rescale by $(\alpha_s/\alpha_s')^2$, as
  `mg.task_loop` does.

## 5. Validation

These folders replace the libraries previously in `~/EFT_ToyModel/processFolders/{SMS_1_loop,UV_BSM}/MatrixElements`
and `MEM/libs/Zprime_{A,B}` (now `backup/Zprime_libs_old`). They were checked against them (2026-11-26):

- The generated Fortran is identical. The only exceptions are the patches above, and the order
  in which MG5 lists the zero coupling orders NP2/NP3 of the VLF, which appears only in comments
  and printouts.
- The base param_cards have the same values.
- `compute_me.py` on the first 300 events of `data/events.h5` gives `born`, `rho_gg`, `rho_qq`
  (all masses) and the Z' $K$, $R$, $I$ **identical** to the stored `me_*.h5` of the full run, with
  no flagged events.
