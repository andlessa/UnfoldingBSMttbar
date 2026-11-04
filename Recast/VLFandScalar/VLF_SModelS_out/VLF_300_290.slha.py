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
    'input file' : '../processFolders/VLF_Slhas/VLF_300_290.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 6.446109e-06,
        'upper limit (fb)' : 0.042,
        'expected upper limit (fb)' : 0.055,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 300.0),
            ('psit', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD0',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.0001534788,
        'r_expected' : 0.000117202,
        'Width (GeV)' : [
            ('psit~', 3.7015e-16),
            ('psit', 3.7015e-16),
            ('~sdm', 'stable')
        ],
        'nll' : 3.157304,
        'nll_min' : 3.157096,
        'nll_SM' : 3.157096
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 35642.96,
        'upper limit (fb)' : 265664800.0,
        'expected upper limit (fb)' : 333043600.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 300.0),
            ('psit', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.0001341651,
        'r_expected' : 0.0001070219,
        'Width (GeV)' : [
            ('psit~', 3.701484e-16),
            ('psit', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 37024.5,
        'upper limit (fb)' : 1350415000.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 300.0),
            ('psit~', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 2.741713e-05,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 3.701484e-16),
            ('psit~', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 36010.86,
        'upper limit (fb)' : 1351810000.0,
        'expected upper limit (fb)' : 886415700.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 300.0),
            ('psit~', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 2.663899e-05,
        'r_expected' : 4.062525e-05,
        'Width (GeV)' : [
            ('psit', 3.701484e-16),
            ('psit~', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 6.021478e-05,
        'upper limit (fb)' : 3.332166,
        'expected upper limit (fb)' : 1.363504,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 300.0), ('~sdm', 290.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 1.807077e-05,
        'r_expected' : 4.416181e-05,
        'Width (GeV)' : [('psit/psit~', 3.7015e-16), ('~sdm', 'stable')],
        'nll' : 96.96722,
        'nll_min' : 93.11055,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 39454.86,
        'upper limit (fb)' : 6356705000.0,
        'expected upper limit (fb)' : 6356705000.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [
            ('psit~', 300.0),
            ('psit', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'CMS-SUS-18-004',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 6.206811e-06,
        'r_expected' : 6.206811e-06,
        'Width (GeV)' : [
            ('psit~', 3.701484e-16),
            ('psit', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 1.643964e-06,
        'upper limit (fb)' : 0.778,
        'expected upper limit (fb)' : 0.583,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 300.0), ('~sdm', 290.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : 'bffN',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.0,
        'dataType' : 'efficiencyMap',
        'r' : 2.113064e-06,
        'r_expected' : 2.819835e-06,
        'Width (GeV)' : [('psit/psit~', 3.7015e-16), ('~sdm', 'stable')],
        'nll' : 6.209055,
        'nll_min' : 5.771604,
        'nll_SM' : 6.20906
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 1796.67,
        'upper limit (fb)' : 1511643000.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,nu,l,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit~', 300.0),
            ('psit', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2016-17',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 1.188555e-06,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit~', 3.701484e-16),
            ('psit', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 36382.56,
        'upper limit (fb)' : 42221750000.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,nu,l-,MET),(b,l+,nu,MET)'],
        'Mass (GeV)' : [
            ('psit~', 300.0),
            ('psit', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2018-08',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 8.617019e-07,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit~', 3.701484e-16),
            ('psit', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 36010.86,
        'upper limit (fb)' : 65132160000.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 300.0),
            ('psit~', 300.0),
            ('~sdm', 290.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 5.528891e-07,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 3.701484e-16),
            ('psit~', 3.701484e-16),
            ('~sdm', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.1237417,
'missing topologies' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.08818119,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.02969713,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.005863337,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with displaced decays (fb)' : 31193.94,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 15841.22,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 10669.82,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2106.626,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1796.659,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 709.4568,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 70.03681,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.08805408,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.02965432,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.005854885,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0001699172,
'missing topologies with prompt decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0001271099,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 4.28073e-05,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    }
],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}