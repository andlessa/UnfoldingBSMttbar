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
    'input file' : '../processFolders/VLF_Slhas/VLF_1300_1200.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.1257175,
        'upper limit (fb)' : 1.797921,
        'expected upper limit (fb)' : 2.256709,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W,b,MET),(W,b,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1300.0),
            ('psit', 1300.0),
            ('~sdm', 1200.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'combined',
        'r' : 0.06992381,
        'r_expected' : 0.05570834,
        'Width (GeV)' : [
            ('psit~', 2.2609e-06),
            ('psit', 2.2609e-06),
            ('~sdm', 'stable')
        ],
        'nll' : 249.5695,
        'nll_min' : 249.5166,
        'nll_SM' : 249.5166
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.04062015,
        'upper limit (fb)' : 4.1,
        'expected upper limit (fb)' : 3.72,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W,b,MET),(W,b,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1300.0),
            ('psit', 1300.0),
            ('~sdm', 1200.0)
        ],
        'AnalysisID' : 'CMS-SUS-16-033',
        'DataSetID' : 'SR3_Njet5_Nb0_HT500_MHT_500',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'efficiencyMap',
        'r' : 0.009907353,
        'r_expected' : 0.01091939,
        'Width (GeV)' : [
            ('psit~', 2.2609e-06),
            ('psit', 2.2609e-06),
            ('~sdm', 'stable')
        ],
        'nll' : 9.251451,
        'nll_min' : 9.235072,
        'nll_SM' : 9.255853
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 0.0,
'missing topologies with displaced decays' : [],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}