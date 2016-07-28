from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = ?
config.General.workArea = 'carb_test'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/nfs/dust/cms/user/kschweig/CMSSW_8_0_10/src/BoostedTTH/BoostedProducer/test/boostedProducer_cfg.py'
config.JobType.outputFiles = ?
config.JobType.pyCfgParams = ?

config.section_("Data")
config.Data.inputDataset = ?
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = False
#config.Data.totalUnits = 1
#config.Data.publishDbsUrl = 'phys03'
config.Data.outputDatasetTag = ?

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
