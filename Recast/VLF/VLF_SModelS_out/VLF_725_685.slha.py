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
    'input file' : '../processFolders/VLF_SLHAs/VLF_725_685.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 218.3391,
        'upper limit (fb)' : 125.29,
        'expected upper limit (fb)' : 97.1856,
        'TxNames' : ['T2ttC'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 725.0),
            ('psit', 725.0),
            ('~sdm', 685.0)
        ],
        'AnalysisID' : 'CMS-SUS-19-010',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 137.0,
        'dataType' : 'upperLimit',
        'r' : 1.74267,
        'r_expected' : 2.24662,
        'Width (GeV)' : [
            ('psit~', 1.169859e-10),
            ('psit', 1.169859e-10),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 220.2973,
        'upper limit (fb)' : 144.0,
        'expected upper limit (fb)' : 173.5,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 725.0),
            ('psit', 725.0),
            ('~sdm', 685.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'upperLimit',
        'r' : 1.529842,
        'r_expected' : 1.269725,
        'Width (GeV)' : [
            ('psit~', 1.169859e-10),
            ('psit', 1.169859e-10),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.05352343,
        'upper limit (fb)' : 0.042,
        'expected upper limit (fb)' : 0.055,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,jet,jet,MET)'],
        'Mass (GeV)' : [
            ('psit~', 725.0),
            ('psit', 725.0),
            ('~sdm', 685.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2018-12',
        'DataSetID' : 'SRD0',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 139.0,
        'dataType' : 'efficiencyMap',
        'r' : 1.274367,
        'r_expected' : 0.9731533,
        'Width (GeV)' : [
            ('psit~', 1.1699e-10),
            ('psit', 1.1699e-10),
            ('~sdm', 'stable')
        ],
        'nll' : 6.649762,
        'nll_min' : 3.157096,
        'nll_SM' : 3.157096
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 1.952893,
        'upper limit (fb)' : 1.786993,
        'expected upper limit (fb)' : 2.890514,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 725.0), ('~sdm', 685.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 1.092838,
        'r_expected' : 0.6756214,
        'Width (GeV)' : [('psit/psit~', 1.1699e-10), ('~sdm', 'stable')],
        'nll' : 99.6099,
        'nll_min' : 96.96747,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 226.7648,
        'upper limit (fb)' : 235.8,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 725.0),
            ('psit~', 725.0),
            ('~sdm', 685.0)
        ],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.9616828,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 1.169859e-10),
            ('psit~', 1.169859e-10),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 220.5565,
        'upper limit (fb)' : 236.07,
        'expected upper limit (fb)' : 204.82,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 725.0),
            ('psit~', 725.0),
            ('~sdm', 685.0)
        ],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 0.9342845,
        'r_expected' : 1.076831,
        'Width (GeV)' : [
            ('psit', 1.169859e-10),
            ('psit~', 1.169859e-10),
            ('~sdm', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.0,
'missing topologies' : [],
'Total xsec for missing topologies with displaced decays (fb)' : 0.0,
'missing topologies with displaced decays' : [],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 55.63001,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 31.62012,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 10.9045,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 10.55244,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.552939,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}