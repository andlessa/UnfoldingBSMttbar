# Recast

Recasting of LHC searches with [SModelS](https://smodels.github.io/) to find the regions of parameter space that are already excluded for each model.

## Files

| Path | Description |
|------|-------------|
| [smodels_parameters.ini](./smodels_parameters.ini) | SModelS parameter file used for all models. |
| [getSModelSData.ipynb](./getSModelSData.ipynb) | Reads the SLHA inputs and the SModelS outputs and stores them in a pandas DataFrame (`.pcl`). |
| [convert2SLHA.py](./convert2SLHA.py) | Converts MadGraph LHE files into SLHA files with `XSECTION` blocks (SModelS input). Detects Scalar/VLF/Zprime automatically. |
| [auxPlots.py](./auxPlots.py) | Helper functions (reading LHE files, ATLAS cuts, interpolation and contours). |
| [Scalar](./Scalar) | `SModelS_results_Scalar.tar.gz` (SLHA inputs + SModelS outputs) and `Scalar_smodels.pcl`. |
| [VLF](./VLF) | `SModelS_results_VLF.tar.gz` and `VLF_smodels.pcl`. |
| [Zprime](./Zprime) | `Zp_SModelS_results.tar.gz`, `Safe_Limits_Zprime.csv` and benchmark banners. |

## 1. Install SModelS

```bash
pip install smodels
```

or clone it from [GitHub](https://github.com/SModelS/smodels) next to this repository (the $Z^\prime$ plotting notebook imports it from `../../smodels`).

## 2. Prepare the SLHA input files

SModelS needs one SLHA file per scan point, with the masses, widths and production cross sections (`XSECTION` blocks) of the BSM particles. [convert2SLHA.py](./convert2SLHA.py) builds them from the MadGraph LHE files of the BSM pair-production scans ($pp \to \varphi_T \varphi_T^*$, $pp \to \psi_T \bar{\psi}_T$, $pp \to Z^\prime$):

```bash
python convert2SLHA.py -d <processFolder>/Events -o ./VLF/VLF_SLHAs --mg5 ~/MG5
```

The script searches `-d` recursively for `*events.lhe*` files and writes one SLHA file per LHE into `-o`. The model is detected from the PDG codes in the MASS block:

| Model | Final state in `XSECTION` | Output name |
|-------|---------------------------|-------------|
| Scalar | `-5000002 5000002` | `Scalar_<mST>_<mChi>.slha` |
| VLF | `-5000006 5000006` | `VLF_<mPsiT>_<mSDM>.slha` |
| Zprime | `5000001` | `Zprime_<mY1>_w<Γ/M in %>.slha` |

Options:

* `-m {Scalar,VLF,Zprime}` forces the model instead of detecting it.
* `-pids ...` overrides the final-state PDGs. Pass `-pids` with no values to read them from the process card.
* `--mg5` is the MadGraph installation, used for its banner reader. It defaults to `$MG5_PATH` or `~/MG5`.

Subprocesses with the same final state are summed into a single `XSECTION` block. To add a new model, add an entry to the `MODELS` dictionary at the top of the script.

## 3. Run SModelS

Edit `smodels_parameters.ini` to point to your model. In the `[particles]` section, set `model` to an SLHA file with `QNUMBERS` blocks. Then run:

```bash
runSModelS.py -p smodels_parameters.ini -f ./Scalar/Scalar_SLHAs/ -o ./Scalar/Scalar_SModelS_out/ -v warning
```

* `-f` is a single SLHA file or a folder of them.
* `-o` is the output folder. With `outputType = summary, python, xml, slha`, SModelS writes a `.py` file (used in the next step) and other files for each input.
* `ncpus = -1` in the `.ini` uses all available cores.
* The first run downloads the official database (`path = official`).

## 4. Collect the results with getSModelSData

[getSModelSData.ipynb](./getSModelSData.ipynb) combines the SLHA inputs (masses, widths, parameters, cross sections) and the SModelS results (`r` values and analysis IDs) into one DataFrame:

1. Extract the results if you are using the stored ones:
   ```bash
   cd Scalar && tar xzf SModelS_results_Scalar.tar.gz && cd ..
   ```
2. In the notebook, set `slhaFolder` and `smodelsFolder` for the model, e.g.
   ```python
   slhaFolder    = './Scalar/Scalar_SLHAs/'
   smodelsFolder = './Scalar/Scalar_SModelS_out/'
   ```
3. Run all cells. The last cell saves the DataFrame:
   ```python
   dataDF.to_pickle('./Scalar/Scalar_smodels.pcl', protocol=4)
   ```
   Change the output name for the other models (`./VLF/VLF_smodels.pcl`, ...).

The `.pcl` files are read by the exclusion notebooks in [../Plots](../Plots) (`plotExclusion-SModelS-*_new.ipynb`). A point is excluded if `ExptRes.result0.r > 1`.
