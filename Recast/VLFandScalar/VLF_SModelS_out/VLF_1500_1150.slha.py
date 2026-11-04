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
    'input file' : '../processFolders/VLF_Slhas/VLF_1500_1150.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 1.197,
        'upper limit (fb)' : 3.66,
        'expected upper limit (fb)' : 5.16,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t-,MET),(t+,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1500.0),
            ('psit', 1500.0),
            ('~sdm', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-20-002',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.3270492,
        'r_expected' : 0.2319767,
        'Width (GeV)' : [
            ('psit~', 2.272065),
            ('psit', 2.272065),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.1960375,
        'upper limit (fb)' : 1.218677,
        'expected upper limit (fb)' : 2.480623,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t,MET),(t,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1500.0),
            ('psit', 1500.0),
            ('~sdm', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'combined',
        'r' : 0.1608609,
        'r_expected' : 0.07902751,
        'Width (GeV)' : [
            ('psit~', 2.272065),
            ('psit', 2.272065),
            ('~sdm', 'stable')
        ],
        'nll' : 249.7985,
        'nll_min' : 249.5166,
        'nll_SM' : 249.5166
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