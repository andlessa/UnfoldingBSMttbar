# $Z^\prime$ benchmarks ($m_{Z^\prime} = 3000$ GeV)

MadGraph5_aMC@NLO (v3.6.3) banners for the narrow and broad $Z^\prime$ benchmarks used in the analysis, generated with the `DMsimp_s_spin1` model (the $Z^\prime$ is the `Y1` particle, PDG 5000001).
All values below are for $pp$ collisions at $\sqrt{s} = 13$ TeV (`ebeam1 = ebeam2 = 6500 GeV`).

## Files

Each benchmark (`narrow`, `broad`) has one banner per process:

| File | Process (`generate` line) | Content |
|---|---|---|
| `*_pp2Z_bench_3000_banner.txt` | `p p > y1` | Inclusive $Z^\prime$ production |
| `narrow_qqbar_channel_3000_banner.txt`, `broad_qq_channel_3000_banner.txt` | `p p > y1 > q q DMV^2==4 QCD^2==0 QED^2==0` | Dijet channel through an $s$-channel $Z^\prime$ |
| `*_ttbar_channel_3000_banner.txt` | `p p > t t~ QCD^2==0 DMV^2==4 QED^2==0` | Pure BSM $t\bar{t}$ ($\lvert\mathcal{M}_{Z^\prime}\rvert^2$) |
| `*_ttbar_interference_3000_banner.txt` | `p p > t t~ QCD^2==0 DMV^2==2 QED^2==2` | $Z^\prime$–$\gamma/Z$ interference in $t\bar{t}$ |

## Model parameters

All other couplings are negligible: $g^V_{u22} = g^V_{d22} = g^V_{d33} = 10^{-6}$, and all axial couplings are zero. The $d$-quark coupling is equal to the $u$-quark one ($g^V_{d11} = g^V_{u11}$).

| Parameter | Param card name | Narrow | Broad |
|---|---|---|---|
| $Z^\prime$ mass | `my1` | 3000 GeV | 3000 GeV |
| $Z^\prime$ width | `wy1` | 30.008 GeV ($\Gamma/M \simeq 1\%$) | 600.016 GeV ($\Gamma/M \simeq 20\%$) |
| Light-quark vector coupling | `gvu11` (= `gvd11`) | $-1.16702 \times 10^{-2}$ | $-3.41116 \times 10^{-2}$ |
| Top vector coupling | `gvu33` | $3.54165 \times 10^{-1}$ | $1.584669$ |
| BR($Z^\prime \to t\bar{t}$) | — | $0.99783$ | $0.99907$ |
| BR($Z^\prime \to u\bar{u}$) = BR($Z^\prime \to d\bar{d}$) | — | $1.0835 \times 10^{-3}$ | $4.6297 \times 10^{-4}$ |

## Cross sections

The values are the `Integrated weight (pb)` written in each banner. The banners do not include the uncertainty of the cross section, so no errors are quoted.

| Process | Narrow $\sigma$ (pb) | Broad $\sigma$ (pb) |
|---|---|---|
| $p p \to Z^\prime$ | $1.3259 \times 10^{-4}$ | $1.1321 \times 10^{-3}$ |
| $p p \to Z^\prime \to q \bar{q}$ | $3.6415 \times 10^{-7}$ | $2.5329 \times 10^{-6}$ |
| $p p \to t \bar{t}$, pure BSM | $1.6506 \times 10^{-4}$ | $2.3926 \times 10^{-3}$ |
| $p p \to t \bar{t}$, interference | $7.8143 \times 10^{-4}$ | $9.7060 \times 10^{-3}$ |
| **Sum** $t \bar{t}$ (pure BSM + interference) | $9.4649 \times 10^{-4}$ | $1.2099 \times 10^{-2}$ |


## Main run settings

* PDF: `nn23nlo` (NNPDF2.3 NLO), leading order
* Dynamical scale choice: `-1` for $p p \to Z^\prime$, `3` for the dijet and $t\bar{t}$ processes
* Dijet channel: $q = u, c, d, s$ (and antiquarks), with $p_T^j > 20$ GeV
* `set gauge unitary`; see the full banners for all settings.
