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
    'input file' : '../processFolders/VLF_Slhas/VLF_1600_1100.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.68084,
        'upper limit (fb)' : 3.42167,
        'expected upper limit (fb)' : 4.80947,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t,MET),(t,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1600.0),
            ('psit', 1600.0),
            ('~sdm', 1100.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.1989789,
        'r_expected' : 0.1415624,
        'Width (GeV)' : [
            ('psit~', 4.237112),
            ('psit', 4.237112),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.1803187,
        'upper limit (fb)' : 0.989055,
        'expected upper limit (fb)' : 1.604008,
        'TxNames' : ['T2tt'],
        'FinalStates' : ['PV > (t,MET),(t,MET)'],
        'Mass (GeV)' : [
            ('psit~', 1600.0),
            ('psit', 1600.0),
            ('~sdm', 1100.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-006-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'combined',
        'r' : 0.1823141,
        'r_expected' : 0.1124176,
        'Width (GeV)' : [
            ('psit~', 4.237112),
            ('psit', 4.237112),
            ('~sdm', 'stable')
        ],
        'nll' : 249.7962,
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