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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_1400_1150.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.20074,
        'upper limit (fb)' : 8.67,
        'expected upper limit (fb)' : 12.7,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t-,MET),(t+,MET)'],
        'Mass (GeV)' : [
            ('~st~', 1400.0),
            ('~st', 1400.0),
            ('~chi', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-20-002',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.0231534,
        'r_expected' : 0.0158063,
        'Width (GeV)' : [
            ('~st~', 2.034432),
            ('~st', 2.034432),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.01521805,
        'upper limit (fb)' : 1.004051,
        'expected upper limit (fb)' : 2.081374,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t,MET),(t,MET)'],
        'Mass (GeV)' : [
            ('~st~', 1400.0),
            ('~st', 1400.0),
            ('~chi', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'combined',
        'r' : 0.01515665,
        'r_expected' : 0.007311538,
        'Width (GeV)' : [
            ('~st~', 2.034432),
            ('~st', 2.034432),
            ('~chi', 'stable')
        ],
        'nll' : 249.5427,
        'nll_min' : 249.5166,
        'nll_SM' : 249.5166
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.001377008,
        'upper limit (fb)' : 0.887,
        'expected upper limit (fb)' : 0.704,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t,MET),(t,MET)'],
        'Mass (GeV)' : [
            ('~st~', 1400.0),
            ('~st', 1400.0),
            ('~chi', 1150.0)
        ],
        'AnalysisID' : 'CMS-SUS-16-033',
        'DataSetID' : 'SR12_Njet5_Nb1_HT750_MHT750',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'efficiencyMap',
        'r' : 0.001552433,
        'r_expected' : 0.001955977,
        'Width (GeV)' : [
            ('~st~', 2.034432),
            ('~st', 2.034432),
            ('~chi', 'stable')
        ],
        'nll' : 6.164756,
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