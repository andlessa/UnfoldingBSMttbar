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
    'input file' : '../processFolders/VLF_SLHAs/VLF_750_675.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 175.4738,
        'upper limit (fb)' : 153.94,
        'expected upper limit (fb)' : 113.109,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 750.0),
            ('psit', 750.0),
            ('~sdm', 675.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 1.139884,
        'r_expected' : 1.551369,
        'Width (GeV)' : [
            ('psit~', 3.458914e-08),
            ('psit', 3.458914e-08),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 183.4462,
        'upper limit (fb)' : 462.83,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 750.0),
            ('psit~', 750.0),
            ('~sdm', 675.0)
        ],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.3963576,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 3.458914e-08),
            ('psit~', 3.458914e-08),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 178.4239,
        'upper limit (fb)' : 462.18,
        'expected upper limit (fb)' : 276.72,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 750.0),
            ('psit~', 750.0),
            ('~sdm', 675.0)
        ],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.3860485,
        'r_expected' : 0.6447814,
        'Width (GeV)' : [
            ('psit', 3.458914e-08),
            ('psit~', 3.458914e-08),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 1.105715,
        'upper limit (fb)' : 3.668522,
        'expected upper limit (fb)' : 4.001729,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 750.0), ('~sdm', 675.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.3014061,
        'r_expected' : 0.2763093,
        'Width (GeV)' : [('psit/psit~', 3.4589e-08), ('~sdm', 'stable')],
        'nll' : 97.31655,
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
'Total xsec for topologies outside the grid (fb)' : 46.08591,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 26.21613,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 8.879554,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 8.806643,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.183583,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}