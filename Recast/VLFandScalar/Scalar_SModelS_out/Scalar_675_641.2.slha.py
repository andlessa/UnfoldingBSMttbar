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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_675_641.2.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 49.13457,
        'upper limit (fb)' : 126.24,
        'expected upper limit (fb)' : 149.887,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 675.0), ('~st', 675.0), ('~chi', 641.2)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.3892155,
        'r_expected' : 0.3278107,
        'Width (GeV)' : [
            ('~st~', 5.573887e-11),
            ('~st', 5.573887e-11),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.01426549,
        'upper limit (fb)' : 0.042,
        'expected upper limit (fb)' : 0.055,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 675.0), ('~st', 675.0), ('~chi', 641.2)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD0',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.3396545,
        'r_expected' : 0.2593725,
        'Width (GeV)' : [
            ('~st~', 5.5739e-11),
            ('~st', 5.5739e-11),
            ('~chi', 'stable')
        ],
        'nll' : 3.785955,
        'nll_min' : 3.157096,
        'nll_SM' : 3.157096
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 48.69781,
        'upper limit (fb)' : 145.44,
        'expected upper limit (fb)' : 106.455,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 675.0), ('~st', 675.0), ('~chi', 641.2)],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.334831,
        'r_expected' : 0.4574498,
        'Width (GeV)' : [
            ('~st~', 5.573887e-11),
            ('~st', 5.573887e-11),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 50.22281,
        'upper limit (fb)' : 260.657,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 675.0), ('~st~', 675.0), ('~chi', 641.2)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.1926778,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 5.573887e-11),
            ('~st~', 5.573887e-11),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.3937105,
        'upper limit (fb)' : 2.077806,
        'expected upper limit (fb)' : 2.771586,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 675.0), ('~chi', 641.2)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.1894837,
        'r_expected' : 0.1420524,
        'Width (GeV)' : [('~st/~st~', 5.5739e-11), ('~chi', 'stable')],
        'nll' : 97.24578,
        'nll_min' : 96.96747,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 48.84783,
        'upper limit (fb)' : 261.132,
        'expected upper limit (fb)' : 241.567,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 675.0), ('~st~', 675.0), ('~chi', 641.2)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.1870618,
        'r_expected' : 0.2022123,
        'Width (GeV)' : [
            ('~st', 5.573887e-11),
            ('~st~', 5.573887e-11),
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
'Total xsec for topologies outside the grid (fb)' : 12.36499,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 7.057731,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.398161,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.338848,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.5702504,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}