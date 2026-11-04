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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_650_625.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.01941661,
        'upper limit (fb)' : 0.042,
        'expected upper limit (fb)' : 0.055,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 650.0), ('~st', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD0',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.4623002,
        'r_expected' : 0.3530292,
        'Width (GeV)' : [
            ('~st~', 4.0856e-12),
            ('~st', 4.0856e-12),
            ('~chi', 'stable')
        ],
        'nll' : 4.082593,
        'nll_min' : 3.157096,
        'nll_SM' : 3.157096
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 62.26821,
        'upper limit (fb)' : 144.0,
        'expected upper limit (fb)' : 173.5,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 650.0), ('~st', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.4324181,
        'r_expected' : 0.3588945,
        'Width (GeV)' : [
            ('~st~', 4.085623e-12),
            ('~st', 4.085623e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 61.71472,
        'upper limit (fb)' : 160.492,
        'expected upper limit (fb)' : 123.392,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 650.0), ('~st', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.3845345,
        'r_expected' : 0.5001516,
        'Width (GeV)' : [
            ('~st~', 4.085623e-12),
            ('~st', 4.085623e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 64.83585,
        'upper limit (fb)' : 289.8701,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 650.0), ('~st~', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.2236721,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 4.085623e-12),
            ('~st~', 4.085623e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.429897,
        'upper limit (fb)' : 1.963651,
        'expected upper limit (fb)' : 2.28355,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.2189274,
        'r_expected' : 0.1882581,
        'Width (GeV)' : [('~st/~st~', 4.0856e-12), ('~chi', 'stable')],
        'nll' : 97.21169,
        'nll_min' : 96.96747,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 63.06081,
        'upper limit (fb)' : 290.4501,
        'expected upper limit (fb)' : 313.8301,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 650.0), ('~st~', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.2171141,
        'r_expected' : 0.2009393,
        'Width (GeV)' : [
            ('~st', 4.085623e-12),
            ('~st~', 4.085623e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 69.25641,
        'upper limit (fb)' : 332.5351,
        'expected upper limit (fb)' : 332.5351,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [('~st~', 650.0), ('~st', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'CMS-SUS-18-004',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.208268,
        'r_expected' : 0.208268,
        'Width (GeV)' : [
            ('~st~', 4.085623e-12),
            ('~st', 4.085623e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 3.153753,
        'upper limit (fb)' : 147.29,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,nu,l,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st~', 650.0), ('~st', 650.0), ('~chi', 625.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-17',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 0.02141185,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 4.085623e-12),
            ('~st', 4.085623e-12),
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
'Total xsec for topologies outside the grid (fb)' : 12.3698,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 8.73287,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.94801,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.6889221,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}