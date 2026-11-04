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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_750_680.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 24.31666,
        'upper limit (fb)' : 138.836,
        'expected upper limit (fb)' : 107.162,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 750.0), ('~st', 750.0), ('~chi', 680.0)],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.1751466,
        'r_expected' : 0.2269149,
        'Width (GeV)' : [
            ('~st~', 3.260158e-08),
            ('~st', 3.260158e-08),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 24.91619,
        'upper limit (fb)' : 405.66,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 750.0), ('~st~', 750.0), ('~chi', 680.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.06142137,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 3.260158e-08),
            ('~st~', 3.260158e-08),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 24.23405,
        'upper limit (fb)' : 405.32,
        'expected upper limit (fb)' : 252.46,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 750.0), ('~st~', 750.0), ('~chi', 680.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.05978992,
        'r_expected' : 0.09599165,
        'Width (GeV)' : [
            ('~st', 3.260158e-08),
            ('~st~', 3.260158e-08),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.1650967,
        'upper limit (fb)' : 3.532873,
        'expected upper limit (fb)' : 4.213127,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 750.0), ('~chi', 680.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.04673158,
        'r_expected' : 0.03918627,
        'Width (GeV)' : [('~st/~st~', 3.2602e-08), ('~chi', 'stable')],
        'nll' : 97.01701,
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
'Total xsec for topologies outside the grid (fb)' : 6.26521,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 3.600476,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.18545,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.182076,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.2972082,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}