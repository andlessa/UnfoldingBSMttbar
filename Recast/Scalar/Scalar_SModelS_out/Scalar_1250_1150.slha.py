smodelsOutput = {
'OutputStatus' : {
    'sigmacut' : 5e-06,
    'minmassgap' : 5.0,
    'maxcond' : 0.2,
    'ncpus' : -1,
    'model' : '/home/vinicius/EFT_ToyModel/processFolders/Scalar/pp2sTsTbar/Cards/param_card.dat',
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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_1250_1150.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.01592199,
        'upper limit (fb)' : 1.7199,
        'expected upper limit (fb)' : 2.263983,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W,b,MET),(W,b,MET)'],
        'Mass (GeV)' : [
            ('~st~', 1250.0),
            ('~st', 1250.0),
            ('~chi', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'combined',
        'r' : 0.009257511,
        'r_expected' : 0.007032736,
        'Width (GeV)' : [
            ('~st~', 4.401e-06),
            ('~st', 4.401e-06),
            ('~chi', 'stable')
        ],
        'nll' : 249.5252,
        'nll_min' : 249.5166,
        'nll_SM' : 249.5166
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.53666,
        'upper limit (fb)' : 81.1,
        'expected upper limit (fb)' : 44.8,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W-,b,MET),(W+,b,MET)'],
        'Mass (GeV)' : [
            ('~st~', 1250.0),
            ('~st', 1250.0),
            ('~chi', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-20-002',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.006617263,
        'r_expected' : 0.01197902,
        'Width (GeV)' : [
            ('~st~', 4.401e-06),
            ('~st', 4.401e-06),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.001415591,
        'upper limit (fb)' : 0.887,
        'expected upper limit (fb)' : 0.704,
        'TxNames' : ['T2ttoff'],
        'FinalStates' : ['PV > (W,b,MET),(W,b,MET)'],
        'Mass (GeV)' : [
            ('~st~', 1250.0),
            ('~st', 1250.0),
            ('~chi', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-16-033',
        'DataSetID' : 'SR12_Njet5_Nb1_HT750_MHT750',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'efficiencyMap',
        'r' : 0.001595931,
        'r_expected' : 0.002010783,
        'Width (GeV)' : [
            ('~st~', 4.401e-06),
            ('~st', 4.401e-06),
            ('~chi', 'stable')
        ],
        'nll' : 6.164699,
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