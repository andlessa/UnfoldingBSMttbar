# MadGraph Scan Scripts

Scripts for running MadGraph5_aMC@NLO parameter scans, either locally (multiprocessing) or on an HTCondor cluster.

## Files

| File | Description |
|------|-------------|
| [runScanMG5.py](./runScanMG5.py) | Main script: reads a scan `.ini` file, expands the scanned parameters into one job per point and runs the jobs in parallel. |
| [runScanMG5_helper.py](./runScanMG5_helper.py) | Helper functions: generates the per-job input files, runs MadGraph and collects the output. |
| [runScanMG5_setupCondor.py](./runScanMG5_setupCondor.py) | Generates the per-job input files and an HTCondor submit file. |
| [runScanMG5_worker.py](./runScanMG5_worker.py) | Worker executed by each HTCondor job. |
| [configParserWrapper.py](./configParserWrapper.py) | Extended `ConfigParser` that understands the `$loop{...}` and `${section:option}` syntax used in the `.ini` files. |
| [scan_parameters_Scalar.ini](./scan_parameters_Scalar.ini), [scan_parameters_VLF.ini](./scan_parameters_VLF.ini), [scan_parameters_Zprime.ini](./scan_parameters_Zprime.ini) | Scan configurations for each model. |
| [setenv.sh](./setenv.sh) | Sets the library paths (LHAPDF, Pythia8, Collier, Ninja, Delphes) needed by MadGraph. |

## Configuration file

Each `.ini` file has four sections:

* `[options]`: which steps to run (`runMadGraph`, `runPythia`, `runDelphes`, ...) and the number of parallel jobs (`ncpu`) and cores per job (`ncore`).
* `[AuxPars]`: auxiliary scan variables. `$loop{[...]}` creates one job for each value, e.g. a list of `(mST, mChi)` mass pairs.
* `[MadGraphPars]`: paths to the process folder and to the default proc, param and run cards.
* `[MadGraphSet]`: values written to the cards for each job (masses, couplings, `order = NLO`, `run_tag`, ...). Values can refer to `[AuxPars]`, e.g. `mST = ${AuxPars:massPairs}[0]`.

For each process folder, the per-job input files are written to `scan_inputFiles/` and the results to `scan_results/`.

## Usage

Set up the environment from the directory that contains the `MG5` installation (see [../installer.sh](../installer.sh)):

```bash
source setenv.sh
```

Run locally:

```bash
python runScanMG5.py -p scan_parameters_Scalar.ini -v info
```

Run on HTCondor:

```bash
python runScanMG5_setupCondor.py -p scan_parameters_Scalar.ini -o runScanMG5_condor.sub
condor_submit <processFolder>/scan_inputFiles/runScanMG5_condor.sub
```

The process folder and the `scan_results` folder must be on a filesystem that the execute nodes can access. Run `python runScanMG5_setupCondor.py -h` for the other options (`--request-memory`, `--requirements`, `--keep-input-files`).
