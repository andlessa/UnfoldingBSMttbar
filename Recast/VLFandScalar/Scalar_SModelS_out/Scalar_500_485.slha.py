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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_500_485.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.001807431,
        'upper limit (fb)' : 0.042,
        'expected upper limit (fb)' : 0.055,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 500.0), ('~st', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD0',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.04303407,
        'r_expected' : 0.03286238,
        'Width (GeV)' : [
            ('~st~', 4.3453e-14),
            ('~st', 4.3453e-14),
            ('~chi', 'stable')
        ],
        'nll' : 3.218372,
        'nll_min' : 3.157096,
        'nll_SM' : 3.157096
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 323.2074,
        'upper limit (fb)' : 8618.383,
        'expected upper limit (fb)' : 10667.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 500.0), ('~st', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.03750209,
        'r_expected' : 0.03029974,
        'Width (GeV)' : [
            ('~st~', 4.345323e-14),
            ('~st', 4.345323e-14),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 320.3344,
        'upper limit (fb)' : 9473.368,
        'expected upper limit (fb)' : 7473.004,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 500.0), ('~st', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.03381421,
        'r_expected' : 0.04286555,
        'Width (GeV)' : [
            ('~st~', 4.345323e-14),
            ('~st', 4.345323e-14),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 354.4243,
        'upper limit (fb)' : 41657.26,
        'expected upper limit (fb)' : 41657.26,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [('~st~', 500.0), ('~st', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'CMS-SUS-18-004',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.008508105,
        'r_expected' : 0.008508105,
        'Width (GeV)' : [
            ('~st~', 4.345323e-14),
            ('~st', 4.345323e-14),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 334.16,
        'upper limit (fb)' : 40177.47,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 500.0), ('~st~', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.008317098,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 4.345323e-14),
            ('~st~', 4.345323e-14),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 325.0115,
        'upper limit (fb)' : 40213.32,
        'expected upper limit (fb)' : 31314.03,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 500.0), ('~st~', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.008082184,
        'r_expected' : 0.0103791,
        'Width (GeV)' : [
            ('~st', 4.345323e-14),
            ('~st~', 4.345323e-14),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 326.8257,
        'upper limit (fb)' : 43165.47,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [('~st~', 500.0), ('~st', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'ATLAS-SUSY-2018-08',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.007571461,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 4.345323e-14),
            ('~st', 4.345323e-14),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.02145392,
        'upper limit (fb)' : 4.076979,
        'expected upper limit (fb)' : 2.422619,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.005262211,
        'r_expected' : 0.008855672,
        'Width (GeV)' : [('~st/~st~', 4.3453e-14), ('~chi', 'stable')],
        'nll' : 96.93898,
        'nll_min' : 95.75687,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 16.13954,
        'upper limit (fb)' : 342951.4,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,nu,l,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st~', 500.0), ('~st', 500.0), ('~chi', 485.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-17',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 4.706072e-05,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st~', 4.345323e-14),
            ('~st', 4.345323e-14),
            ('~chi', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 300.3989,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 140.1618,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 93.96279,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 36.10101,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 15.74788,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 12.10084,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.324604,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}