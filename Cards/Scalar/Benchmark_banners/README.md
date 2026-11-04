# Scalar model benchmark ($m_{\tilde{s}_t} = 1500$ GeV, $m_\chi = 1400$ GeV)

MadGraph5_aMC@NLO (v3.6.3) banners and run summaries for the 1-loop Scalar benchmark used in the analysis.
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
| Scalar top partner mass | `mst` (PDG 5000002) | 1500 GeV |
| Dark matter mass | `mchi` (PDG 5000012) | 1400 GeV |
| Dark matter Yukawa coupling | `ydm` | 7.5 |

## Cross sections

Processes (fixed-order NLO):

* `q q > t t~ QCD^2<=4 NP^2<=4 QED^2<=0 [QCD NP]`
* `g g > t t~ QCD^2<=4 NP^2<=4 QED^2<=0 [QCD NP]`

| Channel | $\sigma$ (pb) | MC error (pb) | Scale variation |
|---|---|---|---|
| $q q \to t \bar{t}$ | $6.511 \times 10^{-2}$ | $\pm 4.2 \times 10^{-4}$ | $+23.2\%$ / $-17.7\%$ |
| $g g \to t \bar{t}$ | $-5.035 \times 10^{-1}$ | $\pm 2.2 \times 10^{-3}$ | $+22.8\%$ / $-30.2\%$ |
| **Sum** ($p p \to t \bar{t}$) | $-4.384 \times 10^{-1}$ | $\pm 2.2 \times 10^{-3}$ | — |

* The MC error of the sum is the two channel errors added in quadrature.
* The scale variation is the envelope of the 9 $(\mu_R, \mu_F)$ variations given in the summary files. It is not combined for the sum, because the variations of the two channels are correlated.
* The $g g$ cross section is negative, so its scale variation is quoted exactly as MadGraph reports it (`+-22.8% --30.2%`).

## Main run settings

* PDF: `nn23nlo` (NNPDF2.3 NLO)
* Dynamical scale choice: `-1` (MadGraph default)
* $m_t = 172$ GeV
* Events generated with an $m_{t\bar{t}}$ bias (`mtt_bias_NLO.f`); see the full banners for all settings.
