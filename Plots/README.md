# Plots

Notebooks that produce the figures of the paper, together with the histogram files they read.

## Files

| File | Description |
|------|-------------|
| [helpers.py](./helpers.py) | Shared functions: reading LHE/Delphes files, building histograms and templates, fitting masses and couplings, Asimov significances with and without systematics, and plotting utilities. |
| [Differential_Distributions_paper_new.ipynb](./Differential_Distributions_paper_new.ipynb) | Differential distributions ($m_{t\bar{t}}$, $p_T(t)$, $\cos\theta^*$) for the SM and the benchmark points of each model, for the $q\bar{q}$ and $pp$ channels. |
| [Differential_distributions_histograms_13_6TeV.pkl.gz](./Differential_distributions_histograms_13_6TeV.pkl.gz) | Histograms read by the notebook above ($\sqrt{s} = 13.6$ TeV). |
| [AsimovDataset_plots_pT.ipynb](./AsimovDataset_plots_pT.ipynb) | Model discrimination with the top $p_T$ spectrum: fits each hypothesis to Asimov pseudo-data and shows the significance versus luminosity and systematics, plus summary plots. |
| [pT_mass_scan_13_6TeV_hists.pkl](./pT_mass_scan_13_6TeV_hists.pkl) | Histogram workspace (SM, pseudo-data, mass-scan templates, best-fit MC) read by the Asimov notebook. |
| [FormFactor_shape_new.ipynb](./FormFactor_shape_new.ipynb) | Shape of the $t\bar{t}g$ form factors for the Scalar and VLF models and of the $Z^\prime$ propagator, as a function of $s/M^2$. |
| [plotExclusion-SModelS-Scalar_new.ipynb](./plotExclusion-SModelS-Scalar_new.ipynb) | SModelS exclusion in the $(m_{\varphi}, \Delta m)$ plane for the Scalar model. Reads `../Recast/Scalar/Scalar_smodels.pcl`. |
| [plotExclusion-SModelS-VLF_new.ipynb](./plotExclusion-SModelS-VLF_new.ipynb) | Same for the VLF model. Reads `../Recast/VLF/VLF_smodels.pcl`. |
| [plotExclusion-SModelS-Zprime_new.ipynb](./plotExclusion-SModelS-Zprime_new.ipynb) | $Z^\prime$ limits from resonance searches, using the SModelS database directly. |
| [testShowering.ipynb](./testShowering.ipynb) | Validation: compares parton-level (LHE) and Delphes-level distributions for the benchmark LHEs in [../Benchmark_LHEs](../Benchmark_LHEs). |

## Notes

* Run the notebooks from this folder so the relative paths resolve.
* The SModelS exclusion notebooks need the `.pcl` files from [../Recast](../Recast). See [../Recast/README.md](../Recast/README.md) for how to make them.
* The $Z^\prime$ notebook imports `smodels` from `../../smodels`, and `testShowering.ipynb` needs ROOT and `../DelphesLLP`.
