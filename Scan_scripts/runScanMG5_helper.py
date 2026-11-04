#!/usr/bin/env python3

# 1) Run MadGraph using the options set in the input file 
# (the proc_card.dat, parameter_card.dat and run_card.dat...).

from __future__ import print_function
import os,glob
import secrets
import re
import json
import signal
from pathlib import Path
import logging,shutil
import subprocess
import tempfile
import time,sys,datetime
from configParserWrapper import ConfigParserExt
from typing import Dict,Set,Union, NamedTuple
from collections import namedtuple
folderTuple = namedtuple('folderTuple', ['inputFolder', 'outputFolder'])

FORMAT = '%(levelname)s: %(message)s at %(asctime)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("MG5Scan")



# Accept both the historical randomly-named scratch folders and the fixed-name
# directories used in v2-v4, so old interrupted jobs can still be cleaned.
SCRATCH_NAME_RE = re.compile(r'(?:tmp[0-9A-Za-z_-]+_run_\d+|\.work_run_\d+)')

def is_scan_scratch_name(name):
    return SCRATCH_NAME_RE.fullmatch(name) is not None


def cleanup_abandoned_workdirs(input_folder, output_folder, *, enabled=True):
    """Clean abandoned random-name (and legacy .work_run) scratch folders.

    Refuse to change anything if HTCondor still lists jobs submitted from this
    scan_inputFiles directory. Completed run_N output is never touched. A
    canceled job may not execute worker-side signal cleanup (e.g. SIGKILL),
    making this the recovery path on the next setup invocation.
    """
    input_folder, output_folder = Path(input_folder).resolve(), Path(output_folder).resolve()
    if shutil.which('condor_q'):
        try:
            query = subprocess.run(['condor_q', '-json'], capture_output=True,
                                   text=True, timeout=20, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError('Could not check active Condor jobs; refusing to replace scan inputs') from exc
        if query.returncode:
            raise RuntimeError('condor_q failed; refusing to replace scan inputs: ' + query.stderr.strip()[:500])
        try:
            jobs = json.loads(query.stdout) if query.stdout.strip() else []
        except json.JSONDecodeError as exc:
            raise RuntimeError('Could not parse condor_q -json; refusing scan cleanup') from exc
        active = [f"{j.get('ClusterId', '?')}.{j.get('ProcId', '?')}"
                  for j in jobs if str(input_folder) in str(j.get('Args', j.get('Arguments', '')))
                  or str(input_folder) == str(j.get('Iwd', ''))]
        if active:
            raise RuntimeError('Condor still has jobs for this scan (' + ', '.join(active[:8]) +
                               '). Cancel or finish them before regenerating scan_inputFiles.')
    else:
        if enabled and output_folder.is_dir() and any(
                is_scan_scratch_name(p.name) for p in output_folder.iterdir()):
            raise RuntimeError('condor_q unavailable: cannot verify whether old jobs still use '
                               'the temporary directories. Run setup on the Condor submit host.')
    if not enabled or not output_folder.is_dir():
        return []
    cleaned = []
    for folder in sorted(output_folder.iterdir()):
        if is_scan_scratch_name(folder.name) and folder.is_dir() and not folder.is_symlink():
            logger.warning('Removing abandoned temporary scan directory %s', folder)
            shutil.rmtree(folder)
            cleaned.append(folder)
    return cleaned


_ACTIVE_MG5_PROCESS = None


def terminate_active_mg5_process():
    """Stop the running MG5 process group on worker SIGTERM/SIGINT."""
    global _ACTIVE_MG5_PROCESS
    child = _ACTIVE_MG5_PROCESS
    if child is None or child.poll() is not None:
        return
    try:
        os.killpg(child.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    # Do not call child.wait() here: this signal handler can interrupt an
    # ongoing Popen.wait(), whose internal lock makes a recursive wait hang.
    # Stop the whole group before deleting its shared scratch directory.
    time.sleep(0.2)
    try: os.killpg(child.pid, signal.SIGKILL)
    except ProcessLookupError: pass

def generateInputFiles(parfile, overwrite_inputs=True, cleanup_workdirs=True) -> Set[folderTuple]:
    """Generate fresh scan inputs by default; never erase completed results.

    ``overwrite_inputs=True`` recreates scan_inputFiles once per process,
    removing outdated INIs and job logs. It NEVER removes completed run_N
    directories. Abandoned random-name scratch directories are removed by default
    only after confirming no matching Condor jobs remain queued or running.
    """
    parser = ConfigParserExt(inline_comment_prefixes="#")
    if not parser.read(parfile):
        raise FileNotFoundError(parfile)
    parserList = parser.expandLoops()
    scanFolders = set()
    next_number = {}
    for irun, newParser in enumerate(parserList):
        processFolder = os.path.abspath(str(newParser.get('MadGraphPars','processFolder')))
        inputFolder = os.path.join(processFolder, 'scan_inputFiles')
        outputFolder = os.path.join(processFolder, 'scan_results')
        group = folderTuple(inputFolder, outputFolder)
        if not os.path.isdir(processFolder):
            generateProcess(newParser)

        if group not in next_number:
            # The output directory may contain completed runs from earlier
            # submissions; it must NEVER be overwritten or removed here.
            os.makedirs(outputFolder, exist_ok=True)
            # Check live jobs and remove abandoned scratch BEFORE deleting INIs.
            cleanup_abandoned_workdirs(inputFolder, outputFolder, enabled=cleanup_workdirs)
            if overwrite_inputs and os.path.isdir(inputFolder):
                logger.warning('Overwriting scan input folder %s (scan_results is preserved)', inputFolder)
                shutil.rmtree(inputFolder)
            os.makedirs(inputFolder, exist_ok=True)

            existing = []
            for root in (os.path.join(processFolder,'Events'),outputFolder):
                for path in glob.glob(os.path.join(root,'run_*')):
                    match = re.fullmatch(r'run_(\d+)',os.path.basename(path))
                    if match: existing.append(int(match.group(1)))
            next_number[group] = max(existing, default=0) + 1
        run_number = next_number[group]
        next_number[group] += 1
        # Original tempfile-style naming: each submission receives a fresh
        # random path, even if an earlier canceled run left scratch behind.
        # Reserve the path atomically, then remove the empty placeholder;
        # runMG5 will copy the process template into that path on the worker.
        runFolder = tempfile.mkdtemp(prefix='tmp',suffix=f'_run_{run_number:02d}',dir=outputFolder)
        os.rmdir(runFolder)
        if os.path.exists(os.path.join(outputFolder,f'run_{run_number:02d}')):
            raise FileExistsError(f'Output run already exists: run_{run_number:02d}')
        newParser.set('MadGraphPars','runFolder',runFolder)
        newParser.set('MadGraphPars','runNumber',str(run_number))
        newParser.set('MadGraphPars','resultsFolder',outputFolder)
        parserDict = newParser.toDict(raw=False,abspath_existing=True)
        # Materialize the resolved seed in each generated job INI as well.
        # This makes per-job seed independence visible before submission and
        # avoids relying solely on late seed selection inside the worker.
        parserDict.setdefault('MadGraphSet', {})['iseed'] = str(_choose_seed(parserDict))
        outfile = os.path.join(inputFolder,f'job_{run_number:05d}.ini')
        if os.path.exists(outfile):
            raise FileExistsError(f'Input config already exists: {outfile}. Rename/archive old files before resubmitting.')
        parserOut = ConfigParserExt()
        parserOut.read_dict(parserDict)
        with open(outfile,'w') as stream:
            parserOut.write(stream)
        scanFolders.add(group)
    logger.info('Created %i input files',len(parserList))
    return scanFolders

def generateProcess(parser):
    """
    Runs the madgraph process generation.
    This step just need to be performed once for a given
    model, since it is independent of the 
    numerical values of the model parameters.
    
    :param parser: Dictionary with parser sections.
    
    :return: True if successful. Otherwise False.
    """
    
    
    #Get run folder:    
    pars = parser["MadGraphPars"]
    processCard = os.path.abspath(pars["proccard"])    
    if not os.path.isfile(processCard):
        logger.error("Process card %s not found" %processCard)
        raise ValueError()

    processFolder = os.path.abspath(pars["processFolder"])
    if os.path.isdir(processFolder):
        logger.warning("Process folder %s found. Skipping process generation." %processFolder)
        return False

    logger.info('Generating process using %s' %processCard)

    # Create copy of process card to replace output folder
    procCard = tempfile.mkstemp(suffix='.dat', prefix='procCard_')
    os.close(procCard[0])
    procCard = procCard[1]
    shutil.copy(processCard,procCard)
    with open(procCard,'r') as f:
        lines = f.readlines()
    lines = [l for l in lines[:] if l.strip()[:6] != 'output']
    lines.append('output %s\n' %processFolder)
    with open(procCard,'w') as f:
        for l in lines:
            f.write(l)
    
    #Generate process
    mg5Folder = os.path.abspath('./MG5')
    run = subprocess.Popen('./bin/mg5_aMC -f %s' %procCard,shell=True,
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                cwd=mg5Folder)
         
    output,errorMsg = run.communicate()
    logger.debug('MG5 process error:\n %s \n' %errorMsg)
    logger.debug('MG5 process output:\n %s \n' %output)
    if run.returncode != 0:
        raise RuntimeError(f'MG5 process generation failed ({run.returncode}): {errorMsg.decode(errors="replace")[-2000:]}')
    logger.info("Finished process generation")

    os.remove(procCard)
        
    return True

_NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eEdD][+-]?\d+)?'

def getInfoFromOutput(outputStr):
    """Best-effort extraction for LO and NLO, never eval untrusted text.

    Information in MG5 stdout is advisory: fixed-order NLO may not print the
    LO `Results Summary` or any `Nb of events` line. Preserve the full stdout.
    """
    if isinstance(outputStr, bytes): outputStr = outputStr.decode(errors='replace')
    result = {'run number':None,'run tag':None,'cross-section (pb)':None,
              'cross-section error (pb)':None,'Number of events':None}
    pattern = re.compile(r'cross[ -]?section\s*:?\s*('+_NUMBER+r')(?:\s*\+[-/]\s*('+_NUMBER+'))?', re.I)
    matches = list(pattern.finditer(outputStr))
    if matches:
        match = matches[-1]
        result['cross-section (pb)'] = float(match.group(1).replace('D','E'))
        if match.group(2): result['cross-section error (pb)'] = float(match.group(2).replace('D','E'))
    match = list(re.finditer(r'Nb of events\s*:\s*(\d+)',outputStr,re.I))
    if match: result['Number of events'] = int(match[-1].group(1))
    match = list(re.finditer(r'Results Summary for run\s*:?\s*(run_\d+)(?:\s+tag\s*:\s*(\S+))?',outputStr,re.I))
    if match:
        result['run number'],result['run tag'] = match[-1].groups()
    return result

def _get_bool(value):
    if isinstance(value,bool): return value
    return str(value).strip().lower() in ('true','yes','1','on')


def _choose_seed(parser):
    """Choose a random positive seed when iseed is omitted or zero.

    For independent cloned MG5 jobs, iseed=0 can resolve to the same seed.
    With seedMode=unique (the default), a random positive integer is selected
    once when each job INI is generated and recorded in that INI for reuse.
    Positive explicit seeds are respected; seedMode=auto preserves MG5's
    original zero-seed behavior. Random collisions are very unlikely but not
    mathematically impossible.
    """
    comms = parser.get('MadGraphSet', {})
    explicit = next((val for key, val in comms.items() if key.lower() == 'iseed'), None)
    if explicit is not None and str(explicit).strip():
        specified = int(explicit)
        if specified < 0:
            raise ValueError('iseed must be nonnegative')
        if specified > 0:
            return specified

    mode = str(parser.get('options', {}).get('seedMode', 'unique')).strip().lower()
    if mode == 'auto':
        return 0
    if mode == 'unique':
        # Generate a positive random seed once per job at scan-input creation.
        # Its value is saved in the job INI for reproducibility.
        return secrets.randbelow(30081**2 - 1) + 1
    raise ValueError(f'Invalid seedMode={mode!r}; expected auto or unique')


_RUN_CARD_SEED = re.compile(r'^(?P<indent>\s*)(?P<value>[-+]?\d+)(?P<suffix>\s*=\s*iseed\b.*)$', re.I)

def set_run_card_seed(card_path, seed):
    """Set iseed in cloned run_card.dat, in addition to the MG5 set command.

    This avoids inheriting `21 = iseed` silently from the template. The
    original process-folder run card is never modified.
    """
    card_path = Path(card_path)
    if not card_path.is_file():
        raise FileNotFoundError(card_path)
    lines = card_path.read_text().splitlines(keepends=True)
    count = 0
    new = []
    for line in lines:
        match = _RUN_CARD_SEED.match(line)
        if match:
            line = f"{match.group('indent')}{seed}{match.group('suffix').rstrip()}\n"
            count += 1
        new.append(line)
    if count > 1:
        raise ValueError(f'Multiple iseed entries in {card_path}')
    if count == 0:
        new.append(f' {seed} = iseed ! RNG seed assigned by scan helper\n')
    card_path.write_text(''.join(new))


def verify_banner_seed(run_folder, expected):
    """Verify seed from an available MG5 run banner. NLO banners may be absent."""
    event_dir = Path(run_folder) / 'Events'
    banners = sorted(event_dir.glob('run_*/*banner*.txt')) if event_dir.exists() else []
    if not banners:
        logger.info('No MG5 event banner available for iseed verification; requested %s', expected)
        return None
    for banner in banners:
        txt = banner.read_text(errors='replace')
        section = re.search(r'<mgruncard\b[^>]*>(.*?)</mgruncard>', txt, re.I | re.S)
        if section is None:
            continue
        match = re.search(r'^\s*(\d+)\s*=\s*iseed\b', section.group(1), re.I | re.M)
        if match:
            observed = int(match.group(1))
            if expected != 0 and observed != expected:
                raise RuntimeError(f'MG5 banner {banner} recorded iseed={observed}, expected {expected}; scratch preserved')
            logger.info('Confirmed iseed=%s in %s', observed, banner)
            return observed
    logger.warning('Could not read iseed from MG5 banner(s) for %s', run_folder)
    return None


def runMG5(parser, runPythia=False, runMadSpin=False) -> Dict:
    """Run MadGraph and preserve its raw output for both LO and NLO.

    Never assume an NLO fixed-order computation writes an LO-style event
    summary or an `unweighted_events.lhe.gz` file.
    """
    pars = parser['MadGraphPars']
    runFolder = os.path.abspath(str(pars['runFolder']))
    processFolder = os.path.abspath(str(pars['processFolder']))
    if not os.path.isdir(processFolder): raise FileNotFoundError(processFolder)
    if not os.path.isdir(runFolder):
        # Create directly at the named scratch path, while avoiding a recursive
        # copy of scan_results and Events from the source process directory.
        shutil.copytree(processFolder,runFolder,ignore=shutil.ignore_patterns(
            'Events','HTML','scan_inputFiles','scan_results','*.lhe','*.lhe.gz','*.root','*.hepmc'),symlinks=True)
        os.makedirs(os.path.join(runFolder,'Events'),exist_ok=True)
        os.makedirs(os.path.join(runFolder,'HTML'),exist_ok=True)
    card_dir = os.path.join(runFolder,'Cards')
    os.makedirs(card_dir,exist_ok=True)
    for key,destination in [('runcard','run_card.dat'),('paramcard','param_card.dat')]:
        if key in pars:
            if not os.path.isfile(pars[key]): raise FileNotFoundError(pars[key])
            shutil.copyfile(pars[key],os.path.join(card_dir,destination))
    for enabled,key,destination in [(runPythia,'pythia8card','pythia8_card.dat'),
                                     (runMadSpin,'madspincard','madspin_card.dat')]:
        if enabled and key in pars:
            shutil.copyfile(pars[key],os.path.join(card_dir,destination))

    seed = _choose_seed(parser)
    set_run_card_seed(os.path.join(card_dir, 'run_card.dat'), seed)
    commands = ['shower=Pythia8' if runPythia else 'shower=OFF',
                'detector=OFF','madspin=ON' if runMadSpin else 'madspin=OFF','done']
    for key,val in parser.get('MadGraphSet',{}).items():
        if key.lower() == 'iseed': continue
        commands.append(f'set {key} {val}')
    commands.extend([f'set iseed {seed}','done','done'])
    commandsFile = os.path.join(runFolder,'MG5_scan_commands.txt')
    with open(commandsFile,'w') as stream: stream.write('\n'.join(commands)+'\n')

    ncore = int(parser['options'].get('ncore',1))
    if ncore < 1: raise ValueError('ncore must be positive')
    command = ['./bin/generate_events','--multicore',f'--nb_core={ncore}']
    stdout_path, stderr_path = [os.path.join(runFolder,name) for name in ('MG5_scan_stdout.log','MG5_scan_stderr.log')]
    logger.info('MG5 run=%s seed=%s ncore=%s',pars.get('runNumber'),seed,ncore)
    global _ACTIVE_MG5_PROCESS
    with open(commandsFile,'r') as inp, open(stdout_path,'w') as out, open(stderr_path,'w') as err:
        # An independent process group lets the worker stop MG5's subprocesses
        # when Condor sends SIGTERM to the Python worker.
        child = subprocess.Popen(command,stdin=inp,stdout=out,stderr=err,
                                 cwd=runFolder,start_new_session=True)
        _ACTIVE_MG5_PROCESS = child
        try:
            returncode = child.wait()
        finally:
            _ACTIVE_MG5_PROCESS = None
    output = Path(stdout_path).read_text(errors='replace')
    runInfo = dict(pars)
    runInfo.update(getInfoFromOutput(output))
    runInfo.update({'seed_requested':seed,'mg_returncode':returncode,
                    'mg_stdout':stdout_path,'mg_stderr':stderr_path})
    if returncode != 0:
        raise RuntimeError(f'MG5 exited with code {returncode}; logs preserved in {runFolder}')
    runInfo['seed_banner'] = verify_banner_seed(runFolder, seed)
    return runInfo

def runDelphes(parser,runInfo,runDelphesPythia=True) -> Dict:
    """
    Runs Delphes on a hepmc file or directly (bypassing hepmc generation)
    on the LHE file.
    
    :param parser: Dictionary with parser sections.
    :param runInfo: Dictionary with MadGraph run information.
    :param runDelphesPythia: If True, run DelphesPythia8 on an input LHE file, otherwise run DelphesHepMC2 on an input HEPMC file.
    
    :return: Dictionary with run info. False if failed.
    """

    cleanOutput = parser['options']['cleanOutput']
    pars = parser["DelphesPars"]

    runFolder = os.path.abspath(parser['MadGraphPars']['runFolder'])
    nevts = parser["MadGraphSet"]["nevents"]
    rootFile = os.path.join(runFolder,'Events',runInfo['run number'], '%s_delphes_events.root'  %runInfo['run tag'])
    delphesFile = os.path.join(runFolder,'Events',runInfo['run number'],'delphes_card.dat')
    delphescard = os.path.abspath(pars['delphescard'])
    shutil.copyfile(delphescard,delphesFile)
    delphesDir = os.path.abspath(pars['delphesDir'])

    if not os.path.isdir(runFolder):
        logger.error(f'Run folder {runFolder} not found. Cannot run Delphes.')
        return runInfo
    if not os.path.isdir(delphesDir):
        logger.error(f'Delphes directory {delphesDir} not found. Cannot run Delphes.')
        return runInfo
    
    
    
    # Get possible input files:
    eventsFolder = os.path.join(runFolder,'Events',runInfo['run number'])
    lheFile = os.path.join(eventsFolder,'unweighted_events.lhe.gz')        
    hepmcFiles = list(glob.glob(os.path.join(eventsFolder,'*hepmc*')))
    if not os.path.isdir(eventsFolder):
        logger.error(f'Events folder {eventsFolder} not found. Cannot run Delphes.')
        return runInfo


    if runDelphesPythia:
        if not os.path.isfile(lheFile):
            logger.error(f'LHE file {lheFile} not found.')
            return runInfo
        pythiaCard = os.path.abspath(pars['pythia8card'])
        pythiaFile = os.path.join(runFolder,'Events',runInfo['run number'],'pythia8_card.dat')
        shutil.copyfile(pythiaCard,pythiaFile)    
        #Generate pythia card with additional info
        with open(pythiaFile,'a') as f:
            f.write('\n\n')
            f.write('### Added lines:\n')
            f.write('Beams:frameType = 4\n')
            f.write('Beams:LHEF = %s\n' %lheFile)
            f.write('Beams:setProductionScalesFromLHEF=on\n')
            f.write('Main:numberOfEvents   = %i\n' %nevts)
            f.write('Main:timesAllowErrors   = %i\n' %int(1e-2*nevts)) # Allow at most 1% of failures
            # Matching specific parameters:
            if 'matching' in pars and pars['matching']:
                qcut = 1.5*parser["MadGraphSet"]['xqcut']
                njet = pars['njetmax']
                f.write('JetMatching:merge=on \n')
                f.write('JetMatching:qCut         = %1.2f \n' %qcut)
                f.write('JetMatching:nJetMax      = %i \n' %njet)

        logger.debug("Running DelphesPythia8 with config files %s and %s" %(pythiaFile,delphesFile))
        run = subprocess.Popen('./DelphesPythia8 %s %s %s' %(delphesFile,pythiaFile,rootFile),shell=True,
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                                cwd=delphesDir)
    else:   
        if len(hepmcFiles) > 1:
            logger.warning(f'Found {len(hepmcFiles)} candidate files for the HEPMC file. Using {hepmcFiles[0]}.')
        elif not hepmcFiles:
            logger.error(f'HEPMC file not found in {eventsFolder}. Cannot run Delphes.')
            return runInfo
        
        hepmcFile = hepmcFiles[0]
        logger.debug(f"Running ./DelphesHepMC2 {delphesFile} {rootFile} {hepmcFile} at {delphesDir}")
        run = subprocess.Popen(f'./DelphesHepMC2 {delphesFile} {rootFile} {hepmcFile}',shell=True,
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                                cwd=delphesDir)

    output,errorMsg = run.communicate()
    logger.debug('Delphes error:\n %s \n' %errorMsg)
    logger.debug('Delphes output:\n %s \n' %output)

    runInfo.update({'DelphesOutput' : output, 'DelphesError' : errorMsg})

    #Generate pythia log file
    if runDelphesPythia:
        pythia_log = rootFile.replace('_delphes_events.root','_pythia_delphes.log')
        with open(pythia_log,'w') as f:
            f.write(output)

    if cleanOutput:
        for f in hepmcFiles + [lheFile]:
            if os.path.isfile(f):
                os.remove(f)
        

    return runInfo

def generateEvents(parser : Union[str,Dict]) -> Dict:
    """Generate MG events (LO or NLO) with the resolved configuration."""
    t0 = time.time()
    if isinstance(parser,(str,os.PathLike)):
        filename = os.fspath(parser)
        cp = ConfigParserExt(inline_comment_prefixes='#')
        if not cp.read(filename): raise FileNotFoundError(filename)
        config = cp.toDict(raw=False,abspath_existing=True)
    elif isinstance(parser,dict):
        config = parser
    else:
        raise TypeError(f'Expected INI file or dict, got {type(parser).__name__}')
    opts = config['options']
    mg,pythia,delphes,dp,spin = [_get_bool(opts.get(k,False)) for k in (
        'runMadGraph','runPythia','runDelphes','runDelphesPythia','runMadSpin')]
    if not mg:
        raise ValueError('runMadGraph=False; no new MG5 results to collect')
    if pythia and dp:
        logger.warning('Both runPythia and runDelphesPythia requested; disabling latter')
        dp = False
    info = runMG5(config,runPythia=pythia,runMadSpin=spin)
    if delphes or dp:
        if not info.get('run number') or info.get('Number of events') is None:
            raise RuntimeError('Delphes requested but MG5 did not report a standard LO event run; NLO fixed-order weighted runs require a separate downstream workflow')
        info = runDelphes(config,info,runDelphesPythia=dp)
    info['time (s)'] = time.time()-t0
    return info

def moveFolders(runInfo: Dict) -> Path:
    """Move ONLY the completed MadGraph Events/run_XX directory to scan_results.

    Each cloned MG5 process normally creates Events/run_01. The resulting
    scan_results/run_N uses the first unused positive integer, irrespective of
    runInfo['runNumber'] or Condor completion order.

    A single directory listing builds the set of used indices. Linux flock on
    a regular lock file in the *process folder* serializes the listing and the
    rename across simultaneous Condor workers. There is no metadata added to
    scan_results/run_N, and no extra file in scan_results itself.

    The temporary process directory is removed only after the source run has
    been moved successfully. If an error occurs, its files are preserved.
    """
    import fcntl

    run_folder = Path(runInfo['runFolder']).resolve()
    results_folder = Path(runInfo['resultsFolder']).resolve()
    process_folder = Path(runInfo['processFolder']).resolve()
    if run_folder == process_folder:
        raise ValueError('Refusing to move the original MG5 process folder')
    if run_folder.parent != results_folder or not is_scan_scratch_name(run_folder.name):
        raise ValueError(f'Expected a temporary scan directory inside {results_folder}: {run_folder}')
    if not run_folder.is_dir():
        raise FileNotFoundError(run_folder)

    events = run_folder / 'Events'
    preferred = events / 'run_01'
    if preferred.is_dir():
        source = preferred
    else:
        # Also handle MadGraph variants naming the sole event run differently.
        runs = sorted(p for p in events.glob('run_*') if p.is_dir() and
                      re.fullmatch(r'run_\d+',p.name)) if events.is_dir() else []
        if len(runs) != 1:
            raise RuntimeError(f'Expected exactly one Events/run_XX in {events}; '
                               f'found {[p.name for p in runs]} (scratch preserved)')
        source = runs[0]

    results_folder.mkdir(parents=True,exist_ok=True)
    # The lock resides in the common process folder, not in saved run output.
    lock_path = process_folder / '.scan_results.lock'
    with lock_path.open('a+b') as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            # One directory scan, followed by in-memory integer lookups; no
            # repeated filesystem checks run_01, run_02, ... for every job.
            occupied = set()
            with os.scandir(results_folder) as entries:
                for entry in entries:
                    match = re.fullmatch(r'run_(\d+)',entry.name)
                    if match:
                        occupied.add(int(match.group(1)))
            index = 1
            while index in occupied:
                index += 1
            destination = results_folder / f'run_{index:02d}'
            # Both paths are within scan_results and therefore on the same
            # filesystem; os.rename publishes the complete folder atomically.
            # Lock prevents the destination race among our scan workers.
            os.rename(source, destination)
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    # Remove the cloned process after a successful move. Even if cleanup fails,
    # the completed Events/run_XX has already been safely published.
    try:
        shutil.rmtree(run_folder)
    except OSError:
        logger.exception('Result saved at %s, but could not remove %s',destination,run_folder)
    logger.info('Moved %s to %s',source,destination)
    return destination
