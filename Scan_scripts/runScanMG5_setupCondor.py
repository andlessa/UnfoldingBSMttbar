#!/usr/bin/env python3
"""Generate HTCondor submit files using the original transfer settings.

The worker separately accesses MG5 process and scan_results absolute paths,
which must remain accessible on eligible execute nodes. HTCondor sandbox
transfer does not replace the Python collection of MG5 output files.
"""
from __future__ import annotations
import argparse
import logging
from pathlib import Path
from configParserWrapper import ConfigParserExt
from runScanMG5_helper import generateInputFiles,logger


def generateCondorFile(configFolder,resultsFolder,subFile,worker_file='runScanMG5_worker.py',
                       verbose='info',request_cpus=1,request_memory='5GB',requirements=None):
    worker=Path(worker_file).resolve()
    if not worker.is_file(): raise FileNotFoundError(worker)
    configFolder=Path(configFolder).resolve()
    submitFile=(configFolder/subFile).resolve()
    # Preserve the original Condor behavior: the queue dynamically matches
    # ALL .ini files currently present in scan_inputFiles when submitted.
    # Usually they are freshly generated because inputs are overwritten by
    # default; --keep-input-files deliberately permits reusing old INIs.
    if not list(configFolder.glob('*.ini')):
        raise ValueError(f'No .ini job files found in {configFolder}')
    if any(ch in str(configFolder) for ch in (' ', '\n')):
        raise ValueError('Spaces/newlines in scan_inputFiles path are not supported by the submit template')
    # Paths in job arguments are shared paths, NOT HTCondor's transfer sandbox.
    with submitFile.open('w') as f:
        f.write('universe = vanilla\n')
        f.write('executable = /usr/bin/python3\n')
        f.write(f'arguments = {worker} -c $(config) -v {verbose}\n')
        f.write('getenv = True\n')
        f.write(f'request_memory = {request_memory}\n')
        f.write(f'request_cpus = {int(request_cpus)}\n')
        if requirements: f.write(f'requirements = {requirements}\n')
        f.write(f'output = {configFolder}/job.$(Cluster).$(Process).out\n')
        f.write(f'error = {configFolder}/job.$(Cluster).$(Process).err\n')
        f.write(f'log = {configFolder}/job.$(Cluster).$(Process).log\n')
        # Restore the original HTCondor sandbox transfer behavior. This avoids
        # the implicit FileSystemDomain matchmaking restriction introduced by NO.
        # NLO output collection remains the responsibility of the Python worker.
        f.write('should_transfer_files = YES\n')
        f.write('when_to_transfer_output = ON_EXIT\n')
        # Revert to the original queue syntax: all INIs in scan_inputFiles.
        f.write(f'queue config matching {configFolder}/*.ini\n')
    return str(submitFile)


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-o','--outputFile',default='runScanMG5_condor.sub')
    ap.add_argument('-w','--workerFile',default='runScanMG5_worker.py')
    ap.add_argument('-p','--parfile',default='scan_parameters.ini')
    ap.add_argument('-v','--verbose',default='info')
    ap.add_argument('--requirements',default=None,help='Optional ClassAd expression; no host restriction by default')
    ap.add_argument('--request-memory',default='5GB')
    ap.add_argument('--keep-input-files',action='store_true',
                    help='Do not delete previous scan_inputFiles (default: recreate it)')
    args=ap.parse_args(argv)
    logger.setLevel(getattr(logging,args.verbose.upper(),logging.INFO))
    par=ConfigParserExt(inline_comment_prefixes='#')
    if not par.read(args.parfile): raise FileNotFoundError(args.parfile)
    ncore=int(par.get('options','ncore')) if par.has_option('options','ncore') else 1
    # Regenerate scan_inputFiles by default while leaving scan_results intact.
    folders=generateInputFiles(args.parfile,overwrite_inputs=not args.keep_input_files)
    for group in folders:
        sub=generateCondorFile(group.inputFolder,group.outputFolder,args.outputFile,
            args.workerFile,args.verbose,ncore,args.request_memory,args.requirements)
        n_configs=len(list(Path(group.inputFolder).glob('*.ini')))
        logger.info('Submit file %s queues ALL %i INI files in %s',sub,n_configs,group.inputFolder)
    return len(folders)

if __name__=='__main__':
    main()
