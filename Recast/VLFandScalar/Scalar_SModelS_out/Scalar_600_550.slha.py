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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_600_550.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 101.7853,
        'upper limit (fb)' : 160.646,
        'expected upper limit (fb)' : 128.987,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 600.0), ('~st', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.6336,
        'r_expected' : 0.7891129,
        'Width (GeV)' : [
            ('~st~', 1.841421e-09),
            ('~st', 1.841421e-09),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 102.6982,
        'upper limit (fb)' : 203.0,
        'expected upper limit (fb)' : 235.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 600.0), ('~st', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.5059024,
        'r_expected' : 0.4370135,
        'Width (GeV)' : [
            ('~st~', 1.841421e-09),
            ('~st', 1.841421e-09),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.02341564,
        'upper limit (fb)' : 0.053,
        'expected upper limit (fb)' : 0.0647,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 600.0), ('~st', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD2',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.4418046,
        'r_expected' : 0.361911,
        'Width (GeV)' : [
            ('~st~', 1.8414e-09),
            ('~st', 1.8414e-09),
            ('~chi', 'stable')
        ],
        'nll' : 4.376686,
        'nll_min' : 3.582759,
        'nll_SM' : 3.582759
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 111.735,
        'upper limit (fb)' : 341.39,
        'expected upper limit (fb)' : 341.39,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [('~st~', 600.0), ('~st', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'CMS-SUS-18-004',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.3272943,
        'r_expected' : 0.3272943,
        'Width (GeV)' : [
            ('~st~', 1.841421e-09),
            ('~st', 1.841421e-09),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 105.7616,
        'upper limit (fb)' : 392.81,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 600.0), ('~st~', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.2692437,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 1.841421e-09),
            ('~st~', 1.841421e-09),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 102.8661,
        'upper limit (fb)' : 393.49,
        'expected upper limit (fb)' : 296.54,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 600.0), ('~st~', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.2614199,
        'r_expected' : 0.3468878,
        'Width (GeV)' : [
            ('~st', 1.841421e-09),
            ('~st~', 1.841421e-09),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.6867068,
        'upper limit (fb)' : 2.655434,
        'expected upper limit (fb)' : 3.968612,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.2586044,
        'r_expected' : 0.1730345,
        'Width (GeV)' : [('~st/~st~', 1.8414e-09), ('~chi', 'stable')],
        'nll' : 97.43142,
        'nll_min' : 96.96747,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5.088115,
        'upper limit (fb)' : 102.41,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,nu,l,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st~', 600.0), ('~st', 600.0), ('~chi', 550.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-17',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 0.04968377,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 1.841421e-09),
            ('~st', 1.841421e-09),
            ('~chi', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 0.0,
'missing topologies with displaced decays' : [],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 21.36937,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 15.08596,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 5.036876,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.246538,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}