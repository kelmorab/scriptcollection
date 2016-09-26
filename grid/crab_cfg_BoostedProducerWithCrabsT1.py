from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = ?
config.General.workArea = 'crab_BoostedMiniAODICHEPv2'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/nfs/dust/cms/user/kelmorab/newCMSSW8019/CMSSW_8_0_19/src/BoostedTTH/BoostedProducer/test/boostedProducer_cfg.py'
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
config.Data.outLFNDirBase='dcms/disk-only/store/user/kelmorab/'

config.section_("Site")
config.Site.storageSite = 'T1_DE_KIT'
config.Site.ignoreGlobalBlacklist=True

config.section_("User")
config.User.voGroup = "dcms"