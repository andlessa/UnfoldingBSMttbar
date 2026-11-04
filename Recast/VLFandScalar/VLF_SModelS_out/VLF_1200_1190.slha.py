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
    'input file' : '../processFolders/VLF_Slhas/VLF_1200_1190.slha',
    'database version' : '3.1.1',
    'smodels version' : '3.1.1'
},
'ExptRes' : [
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 7.1684,
        'upper limit (fb)' : 1264.333,
        'expected upper limit (fb)' : None,
        'TxNames' : ['TRHadQM1'],
        'FinalStates' : ['PV > (RHadronQ),(RHadronQ)'],
        'Mass (GeV)' : [('psit~', 1200.0), ('psit', 1200.0)],
        'AnalysisID' : 'CMS-PAS-EXO-16-036',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 12.9,
        'dataType' : 'upperLimit',
        'r' : 0.005669707,
        'r_expected' : None,
        'Width (GeV)' : [('psit~', 9.399359e-17), ('psit', 9.399359e-17)]
    },
    {
        'maxcond' : 0.0,
        'theory prediction (fb)' : 7.1684,
        'upper limit (fb)' : 61885.03,
        'expected upper limit (fb)' : 53861.19,
        'TxNames' : ['TRHadUM1'],
        'FinalStates' : ['PV > (RHadronU),(RHadronU)'],
        'Mass (GeV)' : [('psit~', 1200.0), ('psit', 1200.0)],
        'AnalysisID' : 'ATLAS-SUSY-2016-32',
        'DataSetID' : None,
        'AnalysisSqrts (TeV)' : 13.0,
        'lumi (fb-1)' : 31.6,
        'dataType' : 'upperLimit',
        'r' : 0.0001158342,
        'r_expected' : 0.0001330903,
        'Width (GeV)' : [('psit~', 9.399359e-17), ('psit', 9.399359e-17)]
    }
],
'Total xsec for missing topologies (fb)' : 0.4927279,
'missing topologies' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.3516734,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.1175026,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0235519,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with displaced decays (fb)' : 7.159106,
'missing topologies with displaced decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 3.395993,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.269368,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.4548659,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.3791254,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.3515398,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.1519817,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.117458,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.02354296,
        'SMS' : 'PV > (RHadronQ),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0152314,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
],
'Total xsec for missing topologies with prompt decays (fb)' : 0.0001781781,
'missing topologies with prompt decays' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0001335543,
        'SMS' : 'PV > (RHadronQ),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 4.462374e-05,
        'SMS' : 'PV > (RHadronQ),(b,nu,l,MET)'
    }
],
'Total xsec for topologies outside the grid (fb)' : 6.666566,
'topologies outside the grid' : [
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 3.395994,
        'SMS' : 'PV > (b,jet,jet,MET),(b,jet,jet,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 2.269368,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.4548659,
        'SMS' : 'PV > (b,jet,jet,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.3791254,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,l,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.1519817,
        'SMS' : 'PV > (b,nu,l,MET),(b,nu,ta,MET)'
    },
    {
        'sqrts (TeV)' : 13.0,
        'weight (fb)' : 0.0152314,
        'SMS' : 'PV > (b,nu,ta,MET),(b,nu,ta,MET)'
    }
]
}