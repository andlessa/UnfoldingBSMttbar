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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_250_230.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 13804.36,
        'upper limit (fb)' : 2541.3,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 250.0), ('~st~', 250.0), ('~chi', 230.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 5.432008,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 1.31281e-12),
            ('~st~', 1.31281e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 13426.43,
        'upper limit (fb)' : 2548.79,
        'expected upper limit (fb)' : 2830.965,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 250.0), ('~st~', 250.0), ('~chi', 230.0)],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 5.267769,
        'r_expected' : 4.742706,
        'Width (GeV)' : [
            ('~st', 1.31281e-12),
            ('~st~', 1.31281e-12),
            ('~chi', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 16.65948,
        'upper limit (fb)' : 7.961435,
        'expected upper limit (fb)' : 5.025245,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 250.0), ('~chi', 230.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 2.092523,
        'r_expected' : 3.315158,
        'Width (GeV)' : [('~st/~st~', 1.3128e-12), ('~chi', 'stable')],
        'nll' : 108.3255,
        'nll_min' : 96.00925,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.8731466,
        'upper limit (fb)' : 0.778,
        'expected upper limit (fb)' : 0.583,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st/~st~', 250.0), ('~chi', 230.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : 'bffN',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.0,
        'dataType' : 'efficiencyMap',
        'r' : 1.122296,
        'r_expected' : 1.497678,
        'Width (GeV)' : [('~st/~st~', 1.3128e-12), ('~chi', 'stable')],
        'nll' : 7.825286,
        'nll_min' : 5.771604,
        'nll_SM' : 6.20906
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 13426.43,
        'upper limit (fb)' : 13394.23,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('~st', 250.0), ('~st~', 250.0), ('~chi', 230.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 1.002405,
        'r_expected' : None,
        'Width (GeV)' : [
            ('~st', 1.31281e-12),
            ('~st~', 1.31281e-12),
            ('~chi', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 155.7262,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 70.92608,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 47.58878,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 20.74995,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 7.982577,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 6.961225,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1.517638,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}