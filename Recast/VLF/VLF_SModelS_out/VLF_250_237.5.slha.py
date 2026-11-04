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
    'input file' : '../processFolders/VLF_SLHAs/VLF_250_237.5.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 86557.95,
        'upper limit (fb)' : 5441642.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 250.0),
            ('psit~', 250.0),
            ('~sdm', 237.5)
        ],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.01590659,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 6.29827e-15),
            ('psit~', 6.29827e-15),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 84188.21,
        'upper limit (fb)' : 5455080.0,
        'expected upper limit (fb)' : 4456652.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 250.0),
            ('psit~', 250.0),
            ('~sdm', 237.5)
        ],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.01543299,
        'r_expected' : 0.01889046,
        'Width (GeV)' : [
            ('psit', 6.29827e-15),
            ('psit~', 6.29827e-15),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.04003031,
        'upper limit (fb)' : 5.500421,
        'expected upper limit (fb)' : 2.468062,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 250.0), ('~sdm', 237.5)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 0.007277682,
        'r_expected' : 0.01621933,
        'Width (GeV)' : [('psit/psit~', 6.2983e-15), ('~sdm', 'stable')],
        'nll' : 96.8826,
        'nll_min' : 93.77506,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.001481624,
        'upper limit (fb)' : 0.778,
        'expected upper limit (fb)' : 0.583,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 250.0), ('~sdm', 237.5)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : 'bffN',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.0,
        'dataType' : 'efficiencyMap',
        'r' : 0.001904401,
        'r_expected' : 0.002541379,
        'Width (GeV)' : [('psit/psit~', 6.2983e-15), ('~sdm', 'stable')],
        'nll' : 6.204068,
        'nll_min' : 5.771604,
        'nll_SM' : 6.20906
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 84188.21,
        'upper limit (fb)' : 112587900.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 250.0),
            ('psit~', 250.0),
            ('~sdm', 237.5)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 0.0007477555,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 6.29827e-15),
            ('psit~', 6.29827e-15),
            ('~sdm', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 78174.01,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 38197.28,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 24929.99,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 7964.691,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 4067.727,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2599.134,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 415.1886,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}