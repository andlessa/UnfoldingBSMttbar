# Plots

Notebooks that produce the figures of the paper, together with the histogram files they read.

## Files

| File | Description |
|------|-------------|
| [helpers.py](./helpers.py) | Shared functions: reading LHE/Delphes files, building histograms and templates, fitting masses and couplings, Asimov significances with and without systematics, and plotting utilities. |
| [Differential_Distributions.ipynb](./Differential_Distributions.ipynb) | Differential distributions ($m_{t\bar{t}}$, $p_T(t)$, $\cos\theta^*$) for the SM and the benchmark points of each model, for the $q\bar{q}$ and $pp$ channels. |
| [Differential_distributions_histograms_13_6TeV.pkl.gz](./Differential_distributions_histograms_13_6TeV.pkl.gz) | Histograms read by the notebook above ($\sqrt{s} = 13.6$ TeV). |
| [pT_distribution_bestFits.ipynb](./pT_distribution_bestFits.ipynb) | Fits each model hypothesis (mass and coupling) to Asimov pseudo-data in the top $p_T$ spectrum and plots the SM, pseudo-data and best-fit distributions for a chosen luminosity. |
| [significance_vs_lumi.ipynb](./significance_vs_lumi.ipynb) | Asimov significance for discriminating each pair of hypotheses as a function of luminosity (300–3000 fb$^{-1}$), one plot per true hypothesis. |
| [significance_summary.ipynb](./significance_summary.ipynb) | Summary heatmap of the significances at $\mathcal{L} = 3$ ab$^{-1}$: fitted hypothesis (rows) versus true benchmark (columns). |
| [pT_mass_scan_13_6TeV_hists.pkl](./pT_mass_scan_13_6TeV_hists.pkl) | Histogram workspace (SM, pseudo-data, mass-scan templates, best-fit MC) read by the three $p_T$ notebooks above. |
| [FormFactor_shape.ipynb](./FormFactor_shape.ipynb) | Shape of the $t\bar{t}g$ form factors for the Scalar and VLF models and of the $Z^\prime$ propagator, as a function of $s/M^2$. |
| [plotExclusion-SModelS-Scalar.ipynb](./plotExclusion-SModelS-Scalar.ipynb) | SModelS exclusion in the $(m_{\varphi}, \Delta m)$ plane for the Scalar model. Reads `../Recast/Scalar/Scalar_smodels.pcl`. |
| [plotExclusion-SModelS-VLF.ipynb](./plotExclusion-SModelS-VLF.ipynb) | Same for the VLF model. Reads `../Recast/VLF/VLF_smodels.pcl`. |
| [plotExclusion-SModelS-Zprime.ipynb](./plotExclusion-SModelS-Zprime.ipynb) | $Z^\prime$ limits from resonance searches, using the SModelS database directly. |

## Notes

* Run the notebooks from this folder so the relative paths resolve.
* The SModelS exclusion notebooks need the `.pcl` files from [../Recast](../Recast). See [../Recast/README.md](../Recast/README.md) for how to make them.
* The $p_T$ notebooks save their figures to [../paper_plots](../paper_plots).
* The $Z^\prime$ notebook imports `smodels` from `../../smodels`.
