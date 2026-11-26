# Correct event weights for biased generation in MadGraph5_aMC@NLO

A patch for **MadGraph5_aMC@NLO v3.6.3** that fixes the normalization of event weights and the reported
cross sections when events are generated with a **bias** (to populate the tails of a distribution).

| mode | problem in v3.6.3 | after the patch |
|---|---|---|
| **Fixed-order NLO** (`fixed_order = ON`, `FO_ANALYSIS_FORMAT = LHE`, `event_norm = bias`) | Within each integration channel the LHE weights have the right shape, but each channel is normalized to its **biased** cross section. Weights of different channels (e.g. `gg` vs `qq~`) are therefore inconsistent, so a single rescaling factor cannot fix them. The `<init>` block holds the biased total, and its error is wrong. | Weights sum to the **true** cross section in every channel. `<init>` holds the true total with a correct error. `summary.txt` gets a new line `Total cross section, bias removed`. |
| **LO** (MadEvent, `bias_module`) | Weights and `<init>` are correct, but the banner's `Integrated weight (pb)` (in the LHE header and in `<run>_<tag>_banner.txt`) keeps the **biased** integral, and the error is reported as exactly `0`. | Banner and run summary hold the bias-corrected cross section with its Monte Carlo error. |

Runs without a bias are not affected: every change reduces to the original behaviour when the bias weight is 1.

---

## Contents

```
mg5_bias_patch.diff   unified diff against a clean MG5_aMC v3.6.3 (4 files, 19 hunks)
README.md             this file
```

## Requirements

- MadGraph5_aMC@NLO **v3.6.3** (`VERSION`: `version = 3.6.3`, `date = 2025-06-12`). Other versions may need
  small adjustments; `patch` reports it if a hunk does not apply.
- The standard `patch` utility and Python 3.

---

## Step by step, from a clean installation

### 1. Install MadGraph5_aMC@NLO v3.6.3

Download `MG5_aMC_v3.6.3.tar.gz` from https://launchpad.net/mg5amcnlo and unpack it:

```bash
tar xzf MG5_aMC_v3.6.3.tar.gz
cd MG5_aMC_v3_6_3
```

(Install LHAPDF and any other tools as usual, e.g. `./bin/mg5_aMC` and then `install lhapdf6`.)

### 2. Back up the four files that will change (optional, `patch -R` also works)

```bash
mkdir -p .backup_bias_patch
cp Template/NLO/SubProcesses/fks_singular.f \
   Template/NLO/SubProcesses/analysis_lhe.f \
   madgraph/interface/amcatnlo_run_interface.py \
   madgraph/interface/madevent_interface.py  .backup_bias_patch/
```

### 3. Apply the patch

From the top directory of the installation:

```bash
patch -p1 --dry-run < /path/to/mg5_bias_patch.diff     # check first
patch -p1 < /path/to/mg5_bias_patch.diff
```

Expected output:

```
patching file Template/NLO/SubProcesses/fks_singular.f
patching file Template/NLO/SubProcesses/analysis_lhe.f
patching file madgraph/interface/amcatnlo_run_interface.py
patching file madgraph/interface/madevent_interface.py
```

Every process folder created **after** this step (`output ...`) contains the fix: `output` copies these
files into the new folder (`SubProcesses/fks_singular.f`, `SubProcesses/analysis_lhe.f`,
`bin/internal/amcatnlo_run_interface.py`, `bin/internal/madevent_interface.py`). Process folders created
**before** patching keep their own unpatched copies; generate them again to get the fix.

### 4. Run as usual

Nothing changes in the cards. For a fixed-order run with a bias:

```
# run_card.dat
  bias = event_norm
  <path>/my_bias.f = custom_fcts      # contains subroutine bias_weight_function
# FO_analyse_card.dat
FO_ANALYSIS_FORMAT = LHE
```

`custom_fcts` is resolved relative to the directory you launch from: `../Source/my_bias.f` only works when
running from `bin/`. Use an absolute path to launch from anywhere. Note that a copied process folder then
still compiles the original folder's file.

The final summary of a biased fixed-order run now reads, for example:

```
      Total cross section, incl. bias (DO NOT USE): 1.502e-01 +- 1.1e-04 pb
      Total cross section, bias removed: 1.424e+00 +- 1.1e-03 pb
   --------------------------------------------------------------
      Scale variation (computed from histogram information):
          Dynamical_scale_choice -1 (envelope of 9 values):
              1.424e+00 pb  +33.1% -23.3%
```

The first line is the integral of the biased integrand and has no physical meaning (unchanged). The second
line is new. Summing the weights in `Events/<run>/events.lhe.gz` reproduces it, separately for every
channel, without any rescaling.

### Reverting

```bash
patch -p1 -R < /path/to/mg5_bias_patch.diff
```

---

## What was wrong

### Fixed order (NLO mode)

With `event_norm = bias`, MINT integrates the biased integrand `b(x) dsigma`, so each integration job ends
with a **biased** cross section `cross_j`. The events are written through the same routine that fills the
histograms (`fill_plots` in `fks_singular.f`), which divides the bias out (`www = plot_wgts/bias_wgt`):
the event weights `w_i` are unbiased, up to an overall MINT normalization `N_j`. Each job's `events.lhe`
ends with the line `nevents  sum_i w_i  cross_j`.

When the jobs are merged (`combine_FO_lhe`), the weights of each job are rescaled by `cross_j / sum_i w_i`,
to fix `N_j`. With a bias this divides a biased number by an unbiased one, so each job is normalized to
its biased cross section. Jobs of the same channel are distorted by the same factor, which a global
rescaling would hide. Jobs of different channels are not: the bias enhances channels with different
kinematic distributions differently (in `pp -> t t~` with an `m_tt` bias, `gg` and `qq~` differed by 9%).

The correct normalization uses one more number per job. Since

```
cross_j = N_j * sum_i w_i b_i      and      sigma_j(true) = N_j * sum_i w_i ,
```

the right factor is `N_j = cross_j / sum_i w_i b_i`. The partial unweighting of the FO LHE output does not
spoil this, because it preserves the expectation of `w` and `b` is a function of the momenta.

The header error was also wrong, independently of the bias. Each job's `error` is an absolute error, but
the merge computed `sqrt(sum(error))` instead of `sqrt(sum(error**2))`. In the example above this printed
16% instead of 0.07%.

The run summary is printed before the merge and shows the biased integral ("DO NOT USE"). The physical
value appears only as the central value of the scale-variation block, without a statistical error.

### LO (MadEvent)

LO handles the bias correctly for the weights. Each event carries its bias weight (`<wgt id='bias'>`), and
`correct_bias` divides it out and rebuilds `<init>`. But:

1. The banner's `<MGGenerationInfo>` (`Integrated weight (pb)`) is written in `do_combine_events` before
   `correct_bias` runs, and is never updated. Both the LHE header and `<run>_<tag>_banner.txt` keep the
   biased integral.
2. `correct_bias` sets `results.current['error'] = 0`, so the run reports the cross section with zero error.

---

## The changes, file by file

The exact changes are in `mg5_bias_patch.diff`. Every addition is marked with a comment containing `PATCH`.

### 1. `Template/NLO/SubProcesses/fks_singular.f` (2 hunks)

In `subroutine fill_plots`, which divides out the bias and calls the analysis for every phase-space point:

- **Declaration** (after `implicit none`): a new common block that hands the bias weight of the current
  point to the analysis routines.
  ```fortran
  c PATCH (bias normalisation of FO LHE events)
        double precision cur_bias_wgt
        common /c_fo_lhe_bias/cur_bias_wgt
  ```
- **Before `call outfun(...)`**: store the bias weight of contribution `i`.
  ```fortran
  c PATCH (bias normalisation of FO LHE events): bias weight of this point
              cur_bias_wgt=bias_wgt(i)
              call outfun(momenta(0,1,i),y_bst(i),www,pdg(1,i),plot_id(i))
  ```
  Without a bias, `bias_wgt(i) = 1`.

### 2. `Template/NLO/SubProcesses/analysis_lhe.f` (6 hunks)

The LHE "analysis" used when `FO_ANALYSIS_FORMAT = LHE`.

- **Common block `/to_lhe_analysis/`** (in `analysis_begin`, `analysis_end`, `analysis_fill`,
  `HwU_add_points`): new accumulator `sum_of_bwgts`.
  ```fortran
        double precision sum_of_wgts,sum_of_bwgts
        common/to_lhe_analysis/sum_of_wgts,sum_of_bwgts,nwgts,nevents,
       &     passed_unwgt
  ```
- **`analysis_begin`**: `sum_of_bwgts=0d0`.
- **`analysis_fill`**: declares `/c_fo_lhe_bias/` and accumulates the weight times the bias weight next to
  the existing sum.
  ```fortran
        sum_of_wgts=sum_of_wgts+wwgts(1)
        sum_of_bwgts=sum_of_bwgts+wwgts(1)*cur_bias_wgt
  ```
- **`analysis_end`**: the last line of each job's `events.lhe` gets a 4th number.
  ```fortran
           write (41,*) nevents,sum_of_wgts,cross_section,sum_of_bwgts
  ```

### 3. `madgraph/interface/amcatnlo_run_interface.py` (6 hunks)

- **New method `fo_lhe_unbiased_total(jobs)`**: reads the last line of every job's `events.lhe`; if the 4th
  number is present and `event_norm == 'bias'`, returns
  `sum_j cross_j * sum_w_j / sum_(w b)_j` and its error
  `sqrt(sum_j (error_j * sigma_j / cross_j)^2)`. Otherwise returns `None`.
- **`collect_the_results`** (final fixed-order summary): calls `fo_lhe_unbiased_total(jobs_to_collect)` and
  stores the result in `cross_sect_dict['xsect_unbiased']` and `['errt_unbiased']`.
- **`print_summary`**: if present, prints
  `Total cross section, bias removed: <value> +- <error> pb` under the existing total. Written to the screen
  and to `summary.txt`.
- **`combine_FO_lhe`**:
  - a helper `_fo_lhe_norm(dirname)` returns, per job, `(nb_event, ratio, sigma_true, cross_biased)` with
    `ratio = cross / sum(w*b)` when the 4th number exists, and the original `cross / sum(w)` otherwise
    (unpatched Fortran, or files from older runs);
  - the `<init>` cross section is the sum of the true job cross sections, and the error is combined in
    quadrature with each job's error scaled to the unbiased normalization;
  - both merging branches (`fo_lhe_postprocessing` with and without `norandom`) use `ratio` and
    `sigma_true` instead of `cross/sumwgt` and `cross`.

The error assigns each job the relative error of its biased integral. This is an approximation, but of the
right size, unlike the original value.

### 4. `madgraph/interface/madevent_interface.py` (5 hunks)

In `correct_bias`, which divides out the bias of LO events:

- accumulates `sum_w2` (sum of squared corrected weights) and computes the Monte Carlo error of the
  corrected estimate: `sqrt(sum_w2 - (sum_w)^2/N)` for `event_norm = sum`, the same divided by `N` for
  `average` (0 for other normalizations);
- after `banner.modify_init_cross(cross)`: replaces the generation info (`Number of Events`,
  `Integrated weight (pb)`) with the corrected values, in the banner written to the LHE file and in
  `self.banner`. Banners read from file store the tag in lower case, so every variant of
  `MGGenerationInfo` is removed first to avoid a duplicate block. It then rewrites
  `Events/<run>/<run>_<tag>_banner.txt`, which was written before the correction;
- `self.results.current['error'] = total_error` instead of `0`.

The error column of the `<init>` block is not changed. It still comes from the biased integration.

---

## Validation

All tests with MG5_aMC v3.6.3, LHAPDF 6.5.5, `NNPDF23_nlo_as_0119_qed`, `sqrt(s) = 13.6 TeV`,
`mu_R = mu_F = H_T/2`, `m_t = 172 GeV`.

### Fixed order: `p p > t t~` (Born only), `0.5 < pT(t) < 3.5 TeV`, `m_tt` bias, 2.4M events

Reference: an independent LO integration (analytic Born matrix elements, LHAPDF, plain Monte Carlo,
16M points), whose total agrees with MadGraph's own histogram-based value.

| | unpatched (sum of LHE weights) | patched (sum of LHE weights, no rescaling) | independent LO |
|---|---|---|---|
| `gg` | 0.0999 pb (biased) | 0.97618 pb | 0.97649 pb |
| `qq~` | 0.0505 pb (biased) | 0.44965 pb | 0.44963 pb |
| total, `<init>` | 0.1463 pb, error 0.023 | 1.4258 pb, error 0.0011 | 1.4255 pb |

- `p_T` spectrum of the patched weights vs the independent LO: chi2/ndf = 4.6/12 (12 bins up to 3.5 TeV).
  With the unpatched weights and one global rescaling factor, the `qq~` events are 9% too heavy relative to
  `gg`. That distorts the spectrum by up to +4% at `pT > 1.2 TeV`.
- Summary: `Total cross section, bias removed: 1.424e+00 +- 1.1e-03 pb`, equal to the scale-variation
  central value (1.424 pb).

### LO: `p p > t t~` via an s-channel Z' (DMsimp_s_spin1), `mtt_bias`

- Weights per flavour (13 TeV, `M = 3 TeV`, `Gamma = 600 GeV`) against a direct integration of the LO
  matrix element: `uu~` 1.593 vs 1.574 fb, `dd~` 0.807 vs 0.805 fb, within the ~1% PDF-set difference of
  that comparison. The weights were already correct at LO.
- After the patch (10k events): LHE header, `<init>`, sum of weights, run banner and printed result agree.
  For example, `0.0001505 +- 1.23e-05 pb` everywhere, where previously the banner said 5.615 pb and the
  error was 0. Two independent runs (1.86 ± 0.14 and 1.51 ± 0.12, ×1e-4 pb) combine to 1.66 ± 0.09,
  against 1.642 from direct integration, so the new error is realistic.

---

## Notes and limitations

- **Old samples are not fixed by the patch.** Events generated before patching still carry the per-channel
  normalization of the biased cross sections. They can be corrected by normalizing each channel separately,
  `w -> w * sigma_c / sum_(i in c) w_i`, with an independent `sigma_c` (e.g. from separate `gg` and `qq~`
  runs, or an LO integration). For `pp -> t t~` the channel of each event is given by the incoming parton
  IDs.
- **Only the LHE output of fixed-order runs is changed.** The HwU/ROOT histograms were already correct, and
  MC@NLO event generation (`fixed_order = OFF`) uses a different path (`driver_mintMC.f`, not touched).
- **The error in the summary and in the header** assumes each job's relative error is the same for the
  biased and the unbiased integral. This is an approximation.
- **Generating processes separately** (`g g > t t~` and `q q~ > t t~` in different runs) avoided the
  fixed-order problem even without the patch, since all jobs of a run then belong to one channel type.
- The issue is worth reporting upstream (https://bugs.launchpad.net/mg5amcnlo).
