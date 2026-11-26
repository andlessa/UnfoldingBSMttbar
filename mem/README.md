# `mem`: extended Matrix Element Method

Python package for the unbinned (extended) matrix-element analysis of the Scalar, VLF and $Z'$
top-philic hypotheses in $pp \to t\bar t$. The method and the notation follow
`~/TeXProjects/MatrixElementMethod/ExtendedMEM.tex`; section numbers below refer to that document.

## 1. The idea in one paragraph

There is **one** Monte Carlo sample, the SM ($q\bar q, gg \to t\bar t$ at LO, weighted events). Every
hypothesis $H$ is obtained by **reweighting** each event $j$ with the density ratio

$$r_H(x_j) = \frac{d\sigma_H}{d\sigma_{SM}}(x_j) = 1 + \theta\, a_H(x_j; M) + \theta^2\, b_H(x_j; M),$$

where $\theta$ is the coupling ($\theta = y_{DM}^2$ for the loop models, $\theta = g_q g_t$ for the $Z'$),
$M$ the mediator mass, and $a_H$, $b_H$ are built from per-event matrix elements and parton
luminosities. Since $a_H$ and $b_H$ do not depend on $\theta$, all the expensive work (MadGraph matrix
elements) is done **once per event**. Every fit afterwards is fast array algebra.
With $r_H$, the expected yield in any region is $n(r_H) = L \sum_j w_j\, r_H(x_j)$. The analysis is an
Asimov likelihood-ratio test built from these yields.

## 2. Data flow

```
 SM LHE (aMC@NLO FO, biased)                         MadGraph libraries
 processFolders/sm/pp2ttbar_gs4/Events/...           processFolders/*/MatrixElements
          |                                                     |
          v                                                     |
 scripts/prepare_events.py  ── mem.io, mem.validation           |
          |                                                     |
          v                                                     v
 data/events.h5  ──────────────────────>  scripts/compute_me.py ── mem.mg (one library per process)
 (weights, kinematics, PDF fluxes,                  |
  alpha_s, scale variations)                        v
          |                            data/me_Scalar.h5, me_VLF.h5, me_Zprime.h5
          |                            (Born, rho(M) per event / Z' kinematic functions)
          v                                         |
 mem.analysis.Sample  <─────────────────────────────┘
          |   builds r_H(x_j; theta, M) for every hypothesis
          v
 mem.analysis.run_analysis / run_truths   (Step A: best fits, Step B: q_A, Z_A)
          |
          v
 MEM_Asimov.ipynb   (checks, binned reproduction of the paper, unbinned results)
```

The two scripts are the only steps that take time: about 3 min and about 1 h on 15 cores for the
2.4M-event sample. Everything in `mem.analysis` runs in seconds to minutes.
All files in `data/` are aligned **event by event**: row $j$ of `me_*.h5` belongs to row $j$ of `events.h5`.
A file name suffix ties them together: `events_s40.h5` goes with `me_Scalar_s40.h5`, and so on.

## 3. Modules

### `config.py`: single source of truth for paths and physics settings

| name | meaning |
|---|---|
| `REPO_ROOT`, `DATA_DIR`, `PROC_DIR` | repository root, `data/`, `processFolders/` |
| `SM_RUN` | aMC@NLO run directory of the SM sample (input of `prepare_events.py`) |
| `LHAPDF_PY` | location of the LHAPDF Python bindings (added to `sys.path`) |
| `SQRT_S`, `MT`, `LHAID` | 13.6 TeV, $m_t = 172$ GeV, NNPDF2.3 NLO QED (244800). They must match the generation and the libraries |
| `MUF_FACTORS`, `MUR_FACTORS` | $(0.5, 1, 2)\,\mu_0$, with $\mu_0 = H_T/2$ |
| `QUARKS`, `FLUX_GROUPS` | the proton content (`g u c d s`, no b) and the ordered parton-pair groups: `gg`, `u_fw`, `u_bw`, ..., where `fw` means the quark comes from beam 1 (+z) |
| `LOOP_MODELS` | Scalar and VLF: library folder, mass grid (100 GeV steps), subprocesses, and the param_card entries for a mass $M$ ($m_{DM} = M - 100$ GeV, $y_{DM} = 1$) |
| `ZP_LIBS`, `ZP_SUBDIRS`, `ZP_COUPLINGS`, `ZP_REF_POINTS` | $Z'$ libraries and the reference points used to extract the kinematic functions (section 4) |
| `ZP_WIDTHS`, `ZP_MASSES` | the two $Z'$ benchmarks ($\Gamma/M$ = 1% and 20%) and the fit mass grid |
| `BENCHMARKS` | truth points of the paper (Table 1): model, $M$, $\theta$ |

The loop-model mass windows are $\pm 300$ GeV around every best fit found in a wide scan. If a best
fit lands on the edge of a window, `fit_hypothesis` prints a warning: extend `masses` and rerun
`compute_me.py`.

### `io.py`: events, kinematics, PDFs

- **`read_lhe(path)`**: fast parser (pipes `.gz` through `zcat`). It returns the weights, top and
  antitop four-momenta, the incoming PDG ids and the `<rwgt>` scale weights. Events that are not
  exactly $2 \to t\bar t$ are counted and skipped.
- **`channel_labels(init)`**: the generation channel of each event: 0 = $gg$, 1 = quark from beam 1,
  2 = quark from beam 2.
- **`read_summary_xsec(run_dir)`**: the physical cross section of a biased run. It ignores the
  "incl. bias (DO NOT USE)" line and takes the bias-removed value.
- **`kinematics(t, tb)`**: the event variables. An LO $2\to2$ event is fully described by
  $(m_{t\bar t}, y_{t\bar t}, \hat n)$, with $\hat n$ the top direction in the $t\bar t$ rest frame. The
  function also returns $x_{1,2}$, $p_T$, $\cos\theta^*$ and $\mu_0 = \sqrt{m_t^2 + p_T^2}$.
- **`partonic_momenta(mtt, n, swap)`**: rebuilds exactly on-shell momenta in the partonic CM frame,
  in MadGraph's particle order (parton 1, parton 2, $t$, $\bar t$). `swap=True` exchanges the incoming
  partons. The matrix elements are always evaluated on these momenta, never on the rounded LHE ones.
- **`get_pdf`, `fluxes(x1, x2, Q)`, `alphas(Q)`**: LHAPDF wrappers. `fluxes` returns **signed**
  parton luminosities per ordered pair (`FLUX_GROUPS`). NNPDF2.3 densities can be negative at large
  $x$, so the sign is kept, and `analysis.Sample` decides on the convention.
- **`H5_COMP`**: the compression settings of all HDF5 datasets.

### `mg.py`: MadGraph libraries (used only by `scripts/compute_me.py`)

- **Rule: one library per Python process.** All MadGraph f2py modules export the same Fortran
  symbols and COMMON blocks. A second library loaded in the same process silently uses the first
  one's. `compute_me.py` therefore runs every task in a new process.
- **`load_library(subdir)`**: imports the single `.so` of a subprocess folder and returns its
  `init` / `get_me` (MadLoop) or `get_value` (LO) functions.
- **`write_card(base, blocks, decays)`**: writes a temporary param_card with some entries replaced.
  It fails if an entry does not exist, so a misspelled parameter can't pass silently. The path is
  kept short because Fortran reads it into a fixed-length string.
- **`silence_fortran()`**: redirects the Fortran stdout/stderr at the file-descriptor level.
- **`task_loop(model, ch, ...)`**: one channel ($gg$ or $q\bar q$) of a loop model for a chunk of
  events. For every mass of the grid it returns the SM Born $|M_0|^2$ and
  $\rho_c = 2\mathrm{Re}(M_0^* M_1)/|M_0|^2$ at $y_{DM}=1$.
  - **Stability:** MadLoop's return code is checked. Unstable points are re-evaluated with
    $\alpha_s$ shifted by $10^{-9}$ (to bypass the wrapper's cache) and rescaled, and points that
    stay unstable are flagged.
  - **Checks:** a re-evaluation of the first events, and an optional $\mu_R$ test.
- **`task_loop_swap`**: checks that the $q\bar q$ interference is symmetric under exchange of the
  beams, so one orientation is enough for the loop models.
- **`task_zprime(piece, q, ...)`**: the $Z'$ libraries for flavour $q$, in both beam orientations
  (here the interference is **not** symmetric).
  - **`B` piece:** $|M_{Z'}|^2$ is evaluated at one reference point $(M, \Gamma)$ and multiplied by the
    Breit-Wigner denominator, which gives the mass-independent function $K$.
  - **`A` piece:** the interference is evaluated at two reference points (with and without width),
    which gives $R$ and $I$.
  - **Validation:** with `validate`, a few events are recomputed at other $(M, \Gamma)$ and compared
    with the Breit-Wigner formula; the logged deviation is about $10^{-15}$.

### `validation.py`: independent cross-checks (no MadGraph)

- **`born_lo(mtt, cost, alphas)`**: analytic LO $|M|^2$ for $gg$ and $q\bar q \to t\bar t$. It checks
  the MadLoop Born.
- **`lo_integration(n_points, pt_range, mtt_max)`**: a direct Monte Carlo integration of the LO SM
  cross section in the generation region. It gives $\sigma_{gg}$ and $\sigma_{q\bar q}$ separately,
  which is what `prepare_events.py` uses to normalise the weights (section 4).
- **`hist_with_err`**: weighted histogram with errors.

### `analysis.py`: density ratios and the statistical analysis

**`Sample(events_path, flux_mode="abs", muF_index=1, xcut=None)`** loads `events.h5` and the Born
column of `me_Scalar*.h5`, and holds the per-event ingredients:

- $F_{gg}$, $F_{q\bar q}$: parton luminosities at the chosen $\mu_F$;
- $B_{gg}$, $B_{q\bar q}$: SM Born;
- the SM density $D = F_{gg} B_{gg} + F_{q\bar q} B_{q\bar q}$;
- the weights $w_j$ in pb.

**PDF convention (`flux_mode`):**
- **`"abs"` (default):** MadEvent's $|f_a f_b|$ per ordered pair. The generator sampled the
  *signed* density, so each weight is multiplied by $|F|/F$ of **its own generation channel**
  (gg, quark from beam 1 or quark from beam 2).
- **`"signed"`:** a variation only. Where the negative large-$x$ gluon nearly cancels the $q\bar q$
  term, $D \to 0$ and $r_H$ becomes unphysically large.

`xcut` optionally removes events with $\max(x_1, x_2) \ge$ `xcut`, and `muF_index` selects the factorisation scale.

`Sample.hypothesis(name)` returns, and caches, one object per hypothesis with
`coeffs(M) -> (a, b)`. `Sample.r(name, theta, M)` assembles $r_H$:

| class | hypotheses | $a_H$ | $b_H$ | dependence on $M$ |
|---|---|---|---|---|
| `SMHyp` | `SM` | 0 | none | none |
| `LoopHyp` | `Scalar`, `VLF` | $\dfrac{F_{gg}B_{gg}\rho_{gg}(M) + F_{q\bar q}B_{q\bar q}\rho_{q\bar q}(M)}{D}$ | none ($r$ is linear in $\theta = y_{DM}^2$) | linear interpolation between grid masses (exact for linearly interpolated $\rho$) |
| `ZpHyp` (via `ZpKin`) | `Zp01`, `Zp20` ($\Gamma = 0.01M$, $0.2M$) | $\dfrac{(s-M^2)\,\tilde R + M\Gamma\,\tilde I}{(s-M^2)^2 + M^2\Gamma^2}$ | $\dfrac{\tilde K}{(s-M^2)^2 + M^2\Gamma^2}$ | **exact** for any $M$ |

Here $\tilde K = \sum_{q,\,o} F_{q,o} K_{q,o} / D$ (and likewise $\tilde R$, $\tilde I$). `ZpKin` precomputes
these sums over flavours and orientations once, so changing $M$ or $\Gamma$ is pure arithmetic.

**`Cells(sample, bins=None, var="pt")`** turns per-event quantities into yields. With `bins=None`
every event is its own cell, which is the unbinned analysis. With bins, events are grouped, for
example in $p_T$ bins, which reproduces the published binned analysis. Both use the same code:
- `agg(x)` gives $\sum_{j\in k} w_j x_j$;
- `template(name, M)` gives $(W, W_A, W_B)$ such that $n_k(\theta)/L = W_k + \theta W_{A,k} + \theta^2 W_{B,k}$.

**Statistics** (Secs. 5-6):

- **Deviance:** $\mathrm{dev}(H\,|\,T) = 2\sum_k [\,n_k^H - n_k^T + n_k^T \ln(n_k^T/n_k^H)\,]$, with
  $n = L\,[\mathrm{fb}^{-1}] \times 1000 \times$ (cell sums in pb). Computed by `deviance`; `deviance_terms`
  gives the per-cell contributions.
- **Step A, best fit of each hypothesis to the Asimov data of the truth** (`fit_hypothesis`):
  - **Profile over the mass grid:** for each $M$, `fit_theta` minimises over $\theta$ with the exact
    gradient and Hessian (`_ThetaProblem`, projected Newton in `_newton`).
  - **Loop models:** $\chi^2(\theta)$ is convex, so Newton starts from a linearised estimate. The
    upper bound keeps every $n_k^H > 0$, and $\theta \le (4\pi)^2$ for perturbativity (`theta_range`).
  - **$Z'$:** $\chi^2(\theta)$ is a quartic with possibly several minima. Candidates come from a scan
    on a stride of about 100k events (`SEED_EVENTS`). Each is refined on all events, and the best is kept.
  - **Final fit:** a parabola through the three lowest grid points gives $\hat M$, and $\theta$ is
    refitted there. The fit is independent of $L$.
- **Step B, separation** (`q_asimov`): the best fits are frozen, and
  $q_A = \mathrm{dev}(\hat H_0\,|\,\hat H_1)$ with $H_1$ the truth model gives $Z_A = \sqrt{q_A}$.
  $q_A$ is proportional to $L$.
- **`bootstrap_q`:** the Monte Carlo-statistics uncertainty of $q_A$, from Poisson(1) resampling of
  the events (unbinned only).
- **`run_analysis(sample, truth, hypotheses, lumi, bins)`:** Step A and Step B for one truth benchmark.
  `step_a_cells` lets the fits use a different binning from $q_A$.
- **`run_truths(...)`:** the same for several truths in parallel. The hypothesis coefficients are
  computed once and shared with forked workers (copy-on-write). Avoid BLAS threads inside the
  workers.

## 4. Conventions and pitfalls (why some code looks the way it does)

- **Weight normalisation (`prepare_events.py`).** In a biased aMC@NLO fixed-order run, the LHE weights
  have the right shape *within* each integration channel, but each channel sums to its **biased**
  cross section. A single normalisation would mis-weight $gg$ against $q\bar q$ by 7.5%. The weights
  are therefore normalised per channel to $\sigma_{gg}$ and $\sigma_{q\bar q}$ from
  `validation.lo_integration`, and the total is checked against `summary.txt`. With the MG5 bias patch
  (`mg5_bias_patch/`) the raw weights are already correct, and the normalisation becomes a check.
- **Scales.** $\mu_R = \mu_F = \mu_0 = H_T/2$ (aMC@NLO's `dynamical_scale_choice = -1` for $2\to2$).
  `events.h5` stores fluxes at three $\mu_F$ and $\alpha_s$ at three $\mu_R$ for the systematics.
  PDF replicas are not stored: recompute them with `io.fluxes(..., get_pdf(member=k))`.
- **$\rho$ is stored, not the interference.** $\rho_c = I_c/B_c$ at $y_{DM} = 1$ is dimensionless and
  smooth in $M$, so linear interpolation on a 100 GeV grid is accurate. It also makes
  $r_H = 1 + y_{DM}^2\, a_H$ exact in the coupling.
- **Loop-model channels.** `P0_uux_ttx` is used for all light quarks: the new states couple only to
  the top, so the matrix element does not depend on the light-quark flavour, and it is symmetric
  under beam exchange (`task_loop_swap` checks this). The $Z'$ couples to $u$ and $d$ differently and
  its interference is forward-backward asymmetric, so it is stored per flavour and orientation.
- **The $Z'$ libraries** are LO standalone outputs with a patched `matrix.f`: MG5 leaves colour
  flows of unselected orders uninitialised (see `processFolders/README.md`).
- **Coupling-order columns.** When generating with aMC@NLO, the `#SelectedCouplingOrders` columns of
  `FKS_params.dat` follow `orders.inc`, and their order differs between UFOs.

## 5. Minimal example

```python
from mem import analysis as A

S = A.Sample("data/events.h5")                       # flux_mode="abs", nominal muF
print(S.sigma, S.n_eff)                              # sigma_SM [pb] in the sample region, effective N
r = S.r("VLF", theta=3.8**2, M=1500.0)               # per-event density ratio of the VLF benchmark
print((S.w * r).sum() - S.sigma)                     # BSM contribution [pb]

res = A.run_analysis(S, truth="VLF", hypotheses=["SM", "Scalar", "VLF", "Zp01", "Zp20"], lumi=500.0)
print(res["Z"])                                      # Z_A of each H0 against the VLF truth at 500 fb^-1

import numpy as np
pt_bins = np.arange(500, 3501, 100)                  # binned version (paper binning): same call with bins
res_b = A.run_analysis(S, truth="VLF", hypotheses=["SM", "VLF"], lumi=500.0, bins=pt_bins)
```
