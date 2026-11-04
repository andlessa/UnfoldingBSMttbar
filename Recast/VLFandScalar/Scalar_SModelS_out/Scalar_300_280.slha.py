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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_300_280.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5302.778,
        'upper limit (fb)' : 665.2136,
        'expected upper limit (fb)' : 767.87,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 300.0), ('~st', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 7.971543,
        'r_expected' : 6.905828,
        'Width (GeV)' : [
            ('~st~', 1.113916e-12),
            ('~st', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.2340572,
        'upper limit (fb)' : 0.042,
        'expected upper limit (fb)' : 0.055,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 300.0), ('~st', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD0',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 5.572792,
        'r_expected' : 4.255586,
        'Width (GeV)' : [
            ('~st~', 1.1139e-12),
            ('~st', 1.1139e-12),
            ('~chi', 'stable')
        ],
        'nll' : 26.38888,
        'nll_min' : 3.157096,
        'nll_SM' : 3.157096
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5690.147,
        'upper limit (fb)' : 1289.98,
        'expected upper limit (fb)' : 1289.98,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [('~st~', 300.0), ('~st', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'CMS-SUS-18-004',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 4.411034,
        'r_expected' : 4.411034,
        'Width (GeV)' : [
            ('~st~', 1.113916e-12),
            ('~st', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5247.062,
        'upper limit (fb)' : 1642.503,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [('~st~', 300.0), ('~st', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-08',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 3.194553,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 1.113916e-12),
            ('~st', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5423.324,
        'upper limit (fb)' : 1783.758,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 300.0), ('~st~', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 3.040392,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 1.113916e-12),
            ('~st~', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5274.847,
        'upper limit (fb)' : 1787.761,
        'expected upper limit (fb)' : 1841.656,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 300.0), ('~st~', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 2.950532,
        'r_expected' : 2.864187,
        'Width (GeV)' : [
            ('~st', 1.113916e-12),
            ('~st~', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 259.1142,
        'upper limit (fb)' : 174.6391,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,nu,l,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st~', 300.0), ('~st', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-17',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 1.483712,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 1.113916e-12),
            ('~st', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 9.394933,
        'upper limit (fb)' : 6.60437,
        'expected upper limit (fb)' : 4.340404,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 1.422533,
        'r_expected' : 2.16453,
        'Width (GeV)' : [('~st/~st~', 1.1139e-12), ('~chi', 'stable')],
        'nll' : 100.5974,
        'nll_min' : 96.19659,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.4394622,
        'upper limit (fb)' : 0.778,
        'expected upper limit (fb)' : 0.583,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : 'bffN',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.5648615,
        'r_expected' : 0.7537945,
        'Width (GeV)' : [('~st/~st~', 1.1139e-12), ('~chi', 'stable')],
        'nll' : 5.953207,
        'nll_min' : 5.771604,
        'nll_SM' : 6.20906
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5274.847,
        'upper limit (fb)' : 9793.319,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 300.0), ('~st~', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 0.5386168,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 1.113916e-12),
            ('~st~', 1.113916e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 5302.778,
        'upper limit (fb)' : 32900.35,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 300.0), ('~st', 300.0), ('~chi', 280.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-15',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 0.1611769,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 1.113916e-12),
            ('~st', 1.113916e-12),
            ('~chi', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 133.4774,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 60.98607,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 40.44322,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 18.03146,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 6.705032,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 5.978828,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.332819,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}