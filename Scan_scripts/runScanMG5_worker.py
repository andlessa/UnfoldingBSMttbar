#!/usr/bin/env python3
"""Execute one scan job and safely collect both LO and NLO MG5 results."""
from __future__ import annotations
import argparse
import logging
import os
from pathlib import Path
import shutil
import sys
import time
from configParserWrapper import ConfigParserExt
from runScanMG5_helper import generateEvents, logger, moveFolders


def compressOutputFolder(output, *, delete_original=False):
    """Create a verified recovery tarball; never delete before archiving."""
    folder = Path(output['runFolder']).resolve()
    if not folder.is_dir(): raise FileNotFoundError(folder)
    archive = Path(shutil.make_archive(str(folder), 'gztar', root_dir=str(folder.parent), base_dir=folder.name))
    if not archive.is_file() or archive.stat().st_size == 0:
        raise IOError(f'Archive was not created successfully: {archive}')
    if delete_original: shutil.rmtree(folder)
    logger.info('Recovery archive: %s',archive)
    return archive


def runSingleJob(configFile: str, verbose: str='info', archive_failed=False):
    logger.setLevel(getattr(logging,verbose.upper(),logging.INFO))
    parser = ConfigParserExt(inline_comment_prefixes='#')
    if not parser.read(configFile): raise FileNotFoundError(configFile)
    config = parser.toDict(raw=False,abspath_existing=True)
    # HTCondor may set OMP_NUM_THREADS; do not ignore configured ncore.
    available = os.environ.get('OMP_NUM_THREADS')
    if available and available.isdigit():
        config['options']['ncore'] = min(int(config['options'].get('ncore',1)),int(available))
    runFolder = Path(config['MadGraphPars']['runFolder'])
    resultFolder = Path(config['MadGraphPars']['resultsFolder'])
    start = time.time()
    try:
        logger.info('Starting scan job %s',configFile)
        info = generateEvents(config)
        destination = moveFolders(info)
        logger.info('Completed %s in %.2f min',destination,(time.time()-start)/60)
        return str(destination)
    except Exception:
        logger.exception('MG5 scan job failed: %s',configFile)
        # On both generation and collection failures, do not destroy output.
        # If collection failed, an additional .staging_run_* directory may exist.
        resultFolder.mkdir(parents=True,exist_ok=True)
        failure_file = resultFolder/(runFolder.name+'.FAILED.txt')
        import traceback
        failure_file.write_text(f'Input: {configFile}\nScratch folder: {runFolder}\n'
                                +traceback.format_exc())
        if archive_failed and runFolder.exists():
            try: compressOutputFolder({'runFolder':str(runFolder)},delete_original=False)
            except Exception: logger.exception('Recovery archive failed; scratch retained')
        raise


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-c','--configfile',required=True)
    ap.add_argument('-v','--verbose',default='info')
    ap.add_argument('--archive-failed',action='store_true',help='Also archive failed scratch; never delete it')
    args=ap.parse_args()
    try: runSingleJob(args.configfile,args.verbose,args.archive_failed)
    except Exception: sys.exit(1)
