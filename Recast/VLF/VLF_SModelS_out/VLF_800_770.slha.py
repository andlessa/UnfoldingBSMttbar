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
    'input file' : '../processFolders/VLF_SLHAs/VLF_800_770.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 118.2317,
        'upper limit (fb)' : 115.681,
        'expected upper limit (fb)' : 88.1641,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 800.0),
            ('psit', 800.0),
            ('~sdm', 770.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 1.022049,
        'r_expected' : 1.341041,
        'Width (GeV)' : [
            ('psit~', 8.596371e-12),
            ('psit', 8.596371e-12),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 119.292,
        'upper limit (fb)' : 158.333,
        'expected upper limit (fb)' : 188.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 800.0),
            ('psit', 800.0),
            ('~sdm', 770.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 0.753425,
        'r_expected' : 0.6345322,
        'Width (GeV)' : [
            ('psit~', 8.596371e-12),
            ('psit', 8.596371e-12),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 123.0162,
        'upper limit (fb)' : 201.26,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 800.0),
            ('psit~', 800.0),
            ('~sdm', 770.0)
        ],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.6112301,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 8.596371e-12),
            ('psit~', 8.596371e-12),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 119.6483,
        'upper limit (fb)' : 201.43,
        'expected upper limit (fb)' : 206.91,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 800.0),
            ('psit~', 800.0),
            ('~sdm', 770.0)
        ],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.5939944,
        'r_expected' : 0.5782624,
        'Width (GeV)' : [
            ('psit', 8.596371e-12),
            ('psit~', 8.596371e-12),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 1.103873,
        'upper limit (fb)' : 1.915034,
        'expected upper limit (fb)' : 2.470178,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 800.0), ('~sdm', 770.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.576425,
        'r_expected' : 0.44688,
        'Width (GeV)' : [('psit/psit~', 8.5964e-12), ('~sdm', 'stable')],
        'nll' : 97.99424,
        'nll_min' : 96.96747,
        'nll_SM' : 96.96747
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 0.0,
'missing topologies with displaced decays' : [],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 29.86998,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 16.93138,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 5.926202,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 5.660649,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.351749,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}