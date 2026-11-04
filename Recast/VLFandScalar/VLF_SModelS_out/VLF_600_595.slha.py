smodelsOutput = {
'OutputStatus' : {
    'sigmacut' : 5e-06,
    'minmassgap' : 5.0,
    'maxcond' : 0.2,
    'ncpus' : -1,
    'model' : '/home/vinicius/EFT_ToyModel/processFolders/VLF/pp2psiTpsiTbar/Cards/param_card.dat',
    'promptwidth' : 1e-11,
    'stablewidth' : 1e-25,
    'checkinput' : True,
    'doinvisible' : True,
    'docompress' : True,
    'computestatistics' : True,
    'testcoverage' : True,
    'combinesrs' : True,
    'reportallsrs' : False,
    'experimentalfeatures' : False,
    'file status' : 1,
    'decomposition status' : 1,
    'warnings' : 'Input file ok',
    'input file' : '../processFolders/VLF_Slhas/VLF_600_595.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 692.65,
        'upper limit (fb)' : 1.45081,
        'expected upper limit (fb)' : None,
        'TxNames' : ['TRHadQM1'],
        'FinalStates' : ['PV > (RHadronQ),(RHadronQ)'],
        'Mass (GeV)' : [('psit~', 600.0), ('psit', 600.0)],
        'AnalysisID' : 'CMS-PAS-EXO-16-036',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 12.9,
        'dataType' : 'upperLimit',
        'r' : 477.4229,
        'r_expected' : None,
        'Width (GeV)' : [('psit~', 1.09511e-24), ('psit', 1.09511e-24)]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 692.65,
        'upper limit (fb)' : 2.352,
        'expected upper limit (fb)' : 1.218,
        'TxNames' : ['TRHadUM1'],
        'FinalStates' : ['PV > (RHadronU),(RHadronU)'],
        'Mass (GeV)' : [('psit~', 600.0), ('psit', 600.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-32',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 31.6,
        'dataType' : 'upperLimit',
        'r' : 294.494,
        'r_expected' : 568.6781,
        'Width (GeV)' : [('psit~', 1.09511e-24), ('psit', 1.09511e-24)]
    }
],
'Total xsec for missing topologies (fb)' : 4.026964e-05,
'missing topologies' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 4.026964e-05,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    }
],
'Total xsec for missing topologies with displaced decays (fb)' : 4.026522e-05,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 4.026522e-05,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}