# VLF model benchmark ($m_{\psi_T} = 1500$ GeV, $m_{S_{DM}} = 1400$ GeV)

MadGraph5_aMC@NLO (v3.6.3) banners and run summaries for the 1-loop VLF benchmark used in the analysis.
All values below are for $pp$ collisions at $\sqrt{s} = 13.6$ TeV (`ebeam1 = ebeam2 = 6800 GeV`).

## Files

| File | Content |
|---|---|
| [qq_13_6TeV_1500_1400_banner.txt](qq_13_6TeV_1500_1400_banner.txt) | Run card and param card for the $q q \to t \bar{t}$ channel |
| [qq_summary.txt](qq_summary.txt) | Cross section summary for the $q q \to t \bar{t}$ channel |
| [gg_13_6TeV_1500_1400_banner.txt](gg_13_6TeV_1500_1400_banner.txt) | Run card and param card for the $g g \to t \bar{t}$ channel |
| [gg_summary.txt](gg_summary.txt) | Cross section summary for the $g g \to t \bar{t}$ channel |

## Model parameters

| Parameter | Param card name | Value |
|---|---|---|
| Vector-like top partner mass | `mpsit` (PDG 5000006) | 1500 GeV |
| Scalar dark matter mass | `msdm` (PDG 5000022) | 1400 GeV |
| Dark matter Yukawa coupling | `ydm` | 3.8 |

## Cross sections

Processes (fixed-order NLO, as written in the summary files):

* `q q > t t~ QCD^2<=4 NP1^2<=4 QED^2<=0 NP2^2<=0 NP3^2<=0 [QCD ...]`
* `g g > t t~ QCD^2<=4 NP1^2<=4 QED^2<=0 NP2^2<=0 NP3^2<=0 [QCD ...]`

| Channel | $\sigma$ (pb) | MC error (pb) | Scale variation |
|---|---|---|---|
| $q q \to t \bar{t}$ | $1.203 \times 10^{-1}$ | $\pm 5.1 \times 10^{-4}$ | $+21.7\%$ / $-16.8\%$ |
| $g g \to t \bar{t}$ | $1.353 \times 10^{-1}$ | $\pm 6.5 \times 10^{-4}$ | $+30.4\%$ / $-22.8\%$ |
| **Sum** ($p p \to t \bar{t}$) | $2.556 \times 10^{-1}$ | $\pm 8.3 \times 10^{-4}$ | — |

* The MC error of the sum is the two channel errors added in quadrature.
* The scale variation is the envelope of the 9 $(\mu_R, \mu_F)$ variations given in the summary files. It is not combined for the sum, because the variations of the two channels are correlated.

## Main run settings

* PDF: `nn23nlo` (NNPDF2.3 NLO)
* Dynamical scale choice: `-1` (MadGraph default)
* $m_t = 172$ GeV
* Events generated with an $m_{t\bar{t}}$ bias (`mtt_bias_NLO.f`); see the full banners for all settings.
