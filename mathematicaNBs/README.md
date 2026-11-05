# Mathematica Notebooks

Mathematica notebooks that turn the FeynRules models into UFO and FeynArts models, and compute the one-loop $t\bar{t}g$ form factors.

## loadModels

Load the FeynRules models in [../feynrules_models](../feynrules_models) and export them:

| Notebook | Output |
|----------|--------|
| [Scalar.nb](./loadModels/Scalar.nb), [VLF.nb](./loadModels/VLF.nb), [Zprime.nb](./loadModels/Zprime.nb) | Tree-level UFO (`WriteUFO`) and FeynArts (`WriteFeynArtsOutput`) models. |
| [Scalar_NLO.nb](./loadModels/Scalar_NLO.nb), [VLF_NLO.nb](./loadModels/VLF_NLO.nb) | NLO models: UV counterterms (NLOCT, `OnShellRenormalization`) and $R_2$ terms, exported as UFO for MadGraph5_aMC@NLO loop-induced generation. |

The generated models go to [../UFO_Models](../UFO_Models) and [../FA_models](../FA_models).

## FormFactors

| Notebook | Description |
|----------|-------------|
| [Scalar_ttGTriangle-loop.nb](./FormFactors/Scalar_ttGTriangle-loop.nb) | One-loop $t\bar{t}g$ vertex (triangle diagrams) in the Scalar model. |
| [VLF_ttGTriangle-loop.nb](./FormFactors/VLF_ttGTriangle-loop.nb) | Same for the VLF model. |

The diagrams are generated with FeynArts from the FA models. The amplitudes are reduced with FeynCalc, and the loop integrals are evaluated analytically with Package-X through FeynHelpers (`PaXEvaluate`). The resulting form factors are used in [../Plots/FormFactor_shape.ipynb](../Plots/FormFactor_shape.ipynb).

## Requirements

Mathematica with FeynRules, FeynArts, NLOCT (for the NLO notebooks), FeynCalc and FeynHelpers (with Package-X).
