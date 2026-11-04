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
    'input file' : '../processFolders/VLF_Slhas/VLF_250_240.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 92915.25,
        'upper limit (fb)' : 1211746000.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 250.0),
            ('psit~', 250.0),
            ('~sdm', 240.0)
        ],
        'AnalysisID' : 'CMS-PAS-SUS-16-052',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 7.66788e-05,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 4.417954e-16),
            ('psit~', 4.417954e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 90371.46,
        'upper limit (fb)' : 1214483000.0,
        'expected upper limit (fb)' : 873006000.0,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 250.0),
            ('psit~', 250.0),
            ('~sdm', 240.0)
        ],
        'AnalysisID' : 'CMS-SUS-17-005',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'upperLimit',
        'r' : 7.441144e-05,
        'r_expected' : 0.0001035176,
        'Width (GeV)' : [
            ('psit', 4.417954e-16),
            ('psit~', 4.417954e-16),
            ('~sdm', 'stable')
        ]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.0001731288,
        'upper limit (fb)' : 4.18392,
        'expected upper limit (fb)' : 1.745236,
        'TxNames' : ['T2bbWWoff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 250.0), ('~sdm', 240.0)],
        'AnalysisID' : 'CMS-PAS-SUS-16-052-agg',
        'DataSetID' : '(combined)',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 35.9,
        'dataType' : 'combined',
        'r' : 4.137956e-05,
        'r_expected' : 9.920078e-05,
        'Width (GeV)' : [('psit/psit~', 4.418e-16), ('~sdm', 'stable')],
        'nll' : 96.9669,
        'nll_min' : 93.17429,
        'nll_SM' : 96.96747
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 4.80717e-06,
        'upper limit (fb)' : 0.778,
        'expected upper limit (fb)' : 0.583,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [('psit/psit~', 250.0), ('~sdm', 240.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : 'bffN',
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.0,
        'dataType' : 'efficiencyMap',
        'r' : 6.178881e-06,
        'r_expected' : 8.245574e-06,
        'Width (GeV)' : [('psit/psit~', 4.418e-16), ('~sdm', 'stable')],
        'nll' : 6.209044,
        'nll_min' : 5.771604,
        'nll_SM' : 6.20906
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 90371.46,
        'upper limit (fb)' : 28331500000.0,
        'expected upper limit (fb)' : None,
        'TxNames' : ['T2bbffff'],
        'FinalStates' : ['PV > (b,jet,jet,MET),(b,nu,l,MET)'],
        'Mass (GeV)' : [
            ('psit', 250.0),
            ('psit~', 250.0),
            ('~sdm', 240.0)
        ],
        'AnalysisID' : 'ATLAS-SUSY-2016-16',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 36.1,
        'dataType' : 'upperLimit',
        'r' : 3.189787e-06,
        'r_expected' : None,
        'Width (GeV)' : [
            ('psit', 4.417954e-16),
            ('psit~', 4.417954e-16),
            ('~sdm', 'stable')
        ]
    }
],
'Total xsec for missing topologies (fb)' : 0.02443175,
'missing topologies' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.01740139,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.005871312,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.001159055,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with displaced decays (fb)' : 78219.76,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 39680.28,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 26776.64,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 5285.973,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 4517.284,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 1783.513,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 176.0415,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.01737145,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.005861212,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.001157061,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 2.993444e-05,
'missing topologies with prompt decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.993444e-05,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    }
],
'Total xsec for topologies outside the grid (fb)' : 0.0,
'topologies outside the grid' : []
}