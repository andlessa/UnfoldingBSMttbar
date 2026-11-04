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
    'input file' : '../processFolders/Scalar_SLHAs/Scalar_1400_1390.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.20074,
        'upper limit (fb)' : 170058.5,
        'expected upper limit (fb)' : None,
        'TxNames' : ['TRHadQM1'],
        'FinalStates' : ['PV > (RHadronQ),(RHadronQ)'],
        'Mass (GeV)' : [('~st~', 1400.0), ('~st', 1400.0)],
        'AnalysisID' : 'CMS-PAS-EXO-16-036',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 12.9,
        'dataType' : 'upperLimit',
        'r' : 1.180417e-06,
        'r_expected' : None,
        'Width (GeV)' : [('~st~', 1.614514e-16), ('~st', 1.614514e-16)]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 0.20074,
        'upper limit (fb)' : 213200900.0,
        'expected upper limit (fb)' : 180478600.0,
        'TxNames' : ['TRHadUM1'],
        'FinalStates' : ['PV > (RHadronU),(RHadronU)'],
        'Mass (GeV)' : [('~st~', 1400.0), ('~st', 1400.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-32',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 31.6,
        'dataType' : 'upperLimit',
        'r' : 9.415533e-10,
        'r_expected' : 1.112265e-09,
        'Width (GeV)' : [('~st~', 1.614514e-16), ('~st', 1.614514e-16)]
    }
],
'Total xsec for missing topologies (fb)' : 0.001302847,
'missing topologies' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0009309154,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0003099853,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 6.194622e-05,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with displaced decays (fb)' : 0.200737,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.1018204,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.06781033,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.01355095,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.01129007,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.004512326,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.000930328,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0004508626,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0003097897,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 6.190713e-05,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0,
'missing topologies with prompt decays' : [],
'Total xsec for topologies outside the grid (fb)' : 0.1994351,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.1018205,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.06781036,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.01355095,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.01129008,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.004512328,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0004508628,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}