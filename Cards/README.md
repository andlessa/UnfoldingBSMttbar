# Cards

MadGraph, Pythia8 and Delphes cards used to generate the events for each model.

## Folders and files

| Path | Description |
|------|-------------|
| [sm](./sm) | SM $t\bar{t}$ production: proc, param and run cards. |
| [Scalar](./Scalar) | Scalar model at NLO (loop-induced). Separate proc cards for the $gg \to t\bar{t}$ (`proc_card_mg5_gg.dat`) and $q\bar{q} \to t\bar{t}$ (`proc_card_mg5_qq.dat`) channels, plus `FKS_params.dat` and `FO_analyse_card.dat` for fixed-order runs. |
| [VLF](./VLF) | VLF model at NLO, with the same structure as `Scalar`. |
| [z_prime/LO](./z_prime/LO), [z_prime/NLO](./z_prime/NLO) | $Z^\prime$ model at LO and NLO. |
| `*/Benchmark_banners` | MadGraph run banners of the benchmark points, i.e. the exact cards used for each benchmark. |
| `mtt_bias*.f` | Fortran bias modules that enhance event generation at high $m_{t\bar{t}}$ so the tails are well populated. Events are reweighted, so the distributions are unbiased. |

For the NLO runs, the bias function is passed to MadGraph through the `custom_fcts` option of the run card (e.g. `../Source/mtt_bias_NLO.f = custom_fcts`).
