from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = ?
config.General.workArea = 'crab_BoostedMiniAODICHEPv1'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/afs/cern.ch/user/k/koschwei/private/CMSSW_8_0_12/src/BoostedTTH/BoostedProducer/test/boostedProducer_cfg.py'
config.JobType.outputFiles = ?


config.section_("Data")
config.Data.inputDataset = ?
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = True
#config.Data.totalUnits = 1
config.Data.publishDBS = 'phys03'
config.Data.outputDatasetTag = ?

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
