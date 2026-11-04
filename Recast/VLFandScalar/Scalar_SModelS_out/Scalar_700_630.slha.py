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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_700_630.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 38.22473,
        'upper limit (fb)' : 150.33,
        'expected upper limit (fb)' : 117.872,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [('~st~', 700.0), ('~st', 700.0), ('~chi', 630.0)],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 0.2542722,
        'r_expected' : 0.3242902,
        'Width (GeV)' : [
            ('~st~', 3.437368e-08),
            ('~st', 3.437368e-08),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 39.68549,
        'upper limit (fb)' : 443.29,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 700.0), ('~st~', 700.0), ('~chi', 630.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.0895249,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 3.437368e-08),
            ('~st~', 3.437368e-08),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 38.599,
        'upper limit (fb)' : 443.13,
        'expected upper limit (fb)' : 281.45,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 700.0), ('~st~', 700.0), ('~chi', 630.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.08710537,
        'r_expected' : 0.1371434,
        'Width (GeV)' : [
            ('~st', 3.437368e-08),
            ('~st~', 3.437368e-08),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.2371204,
        'upper limit (fb)' : 3.668873,
        'expected upper limit (fb)' : 4.013874,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 700.0), ('~chi', 630.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.0646303,
        'r_expected' : 0.05907519,
        'Width (GeV)' : [('~st/~st~', 3.4374e-08), ('~chi', 'stable')],
        'nll' : 97.01998,
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
'Total xsec for topologies outside the grid (fb)' : 9.863113,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 5.619949,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.907678,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.874843,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.4606436,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}