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
    'input file' : '../processFolders/VLF_Slhas/VLF_1300_1150.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.1496333,
        'upper limit (fb)' : 1.311084,
        'expected upper limit (fb)' : 1.983858,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W,b,MET),(W,b,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1300.0),
            ('psit', 1300.0),
            ('~sdm', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'combined',
        'r' : 0.1141295,
        'r_expected' : 0.07542542,
        'Width (GeV)' : [
            ('psit~', 0.00077595),
            ('psit', 0.00077595),
            ('~sdm', 'stable')
        ],
        'nll' : 249.6661,
        'nll_min' : 249.5166,
        'nll_SM' : 249.5166
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 3.8773,
        'upper limit (fb)' : 42.7,
        'expected upper limit (fb)' : 33.5,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W-,b,MET),(W+,b,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1300.0),
            ('psit', 1300.0),
            ('~sdm', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-20-002',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.09080328,
        'r_expected' : 0.1157403,
        'Width (GeV)' : [
            ('psit~', 0.00077595),
            ('psit', 0.00077595),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.02003409,
        'upper limit (fb)' : 0.887,
        'expected upper limit (fb)' : 0.704,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W,b,MET),(W,b,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1300.0),
            ('psit', 1300.0),
            ('~sdm', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-16-033',
        'DataSetID' : 'SR12_Njet5_Nb1_HT750_MHT750',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'efficiencyMap',
        'r' : 0.02258634,
        'r_expected' : 0.02845751,
        'Width (GeV)' : [
            ('psit~', 0.00077595),
            ('psit', 0.00077595),
            ('~sdm', 'stable')
        ],
        'nll' : 6.138902,
        'nll_min' : 6.04734,
        'nll_SM' : 6.166793
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