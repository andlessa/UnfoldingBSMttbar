# Unfolding BSM @ ttbar

Code, model files and data for the study of top-philic new physics in top-pair production.

## About the project

Precision measurements can reveal more than the presence of new physics: they can also tell us about the dynamics that produced it. This project studies that question in $t\bar{t}$ production by comparing three top-philic scenarios:

* a **colored scalar top partner** (`Scalar`),
* a **colored vector-like fermion** (`VLF`),
* a **spin-one $Z^\prime$ mediator** (`Zprime`).

The scalar and vector-like fermion contribute through loop corrections. The $Z^\prime$ contributes at tree level.

At low energies, the scalar and vector-like fermion scenarios match onto the same effective operator structure, so an EFT approach cannot tell them apart. Near or above threshold, however, their full loop amplitudes develop distinct momentum-dependent interference patterns. Using the top transverse momentum ($p_T$) spectrum, we find that:

* resonant and loop-induced effects are relatively easy to distinguish;
* separating the scalar and vector-like hypotheses is much harder, but their different analytic structures still leave measurable information in the shape of the distribution.

These results show how precision differential measurements can probe the spin and dynamics of virtual new states even when those states are not directly reconstructed. They also motivate more powerful multidimensional analyses.

## Software

| Tool | Role in this project |
|------|----------------------|
| [MadGraph5_aMC@NLO](https://launchpad.net/mg5amcnlo) | Event generator. Computes the tree-level ($Z^\prime$) and loop-induced (Scalar, VLF) $t\bar{t}$ amplitudes from the UFO models and generates events and parameter scans. Installed by [installer.sh](installer.sh) together with LHAPDF6, HepMC, Pythia8 and Collier. |
| [FeynRules](https://feynrules.irmp.ucl.ac.be/) | Mathematica package that derives Feynman rules from a Lagrangian. Used to implement the three models ([feynrules_models](feynrules_models)) and export them as UFO models ([UFO_Models](UFO_Models)), including the NLO versions for the loop-induced scenarios. It also exports FeynArts model files ([FA_models](FA_models)). |
| [FeynArts](http://www.feynarts.de/) | Mathematica package that generates Feynman diagrams and amplitudes. Used to build the one-loop diagrams for the new-physics contributions to $t\bar{t}$ production. |
| [FeynCalc](https://feyncalc.github.io/) | Mathematica package for symbolic QFT calculations (Dirac algebra, tensor reduction, Passarino–Veltman functions). Used to compute the one-loop amplitudes, e.g. the $t\bar{t}g$ form factors for the Scalar and VLF models ([mathematicaNBs/FormFactors](mathematicaNBs/FormFactors)). |
| [FeynHelpers](https://github.com/FeynCalc/feynhelpers) | FeynCalc add-on that connects it to Package-X and FIRE. Used to obtain analytic expressions for the loop integrals in the form factors. |
| [SModelS](https://smodels.github.io/) | Reinterprets LHC searches using simplified-model results. Used to derive the current exclusion limits on the parameter space of each model ([Recast](Recast)). |

## Repository layout

* [feynrules_models](feynrules_models): FeynRules model files (`Scalar.fr`, `VLF.fr`, `Zprime.fr`, ...).
* [mathematicaNBs](mathematicaNBs): Mathematica notebooks that load the models (`loadModels`) and compute the $t\bar{t}g$ form factors (`FormFactors`).
* [FA_models](FA_models): FeynArts model files generated from FeynRules.
* [UFO_Models](UFO_Models): UFO models used by MadGraph.
* [Cards](Cards): MadGraph, Pythia8 and Delphes cards for each model.
* [Scan_scripts](Scan_scripts): scripts and `.ini` files for running MadGraph parameter scans (locally or on HTCondor).
* [Benchmark_LHEs](Benchmark_LHEs): LHE files for the SM and benchmark points of each model.
* [Recast](Recast): SModelS inputs, outputs and exclusion limits.
* [Plots](Plots): notebooks and helper functions (`helpers.py`) that make the differential distributions, form-factor shapes, Asimov-significance and exclusion plots.
* [installer.sh](installer.sh) / [setenv.sh](setenv.sh): installation of the external tools and environment setup.
