#Setting configuration for testing regression configurations

#General stuff
cmsswpath='/nfs/dust/cms/user/kschweig/CMSSW_7_4_15'
program = 'Code/scriptcollection/regconfig/Regressiontraining.C'
nfsroot = "/nfs/dust/cms/user/kschweig/"
inputfiles = "JetRegression/trees0209/ttbarforbReg0211.root"
outputfilefolder = "JetRegression/trees0209/ttbarbReg0211_testing/"
outputfileprefix = ""
weightprefix = ""
#variable definition
cuts = "Evt_Odd == 1 && abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5"
#NTrees
nTrees_start = 200
nTrees_end   = 1500
nTrees_steps = 400
#Shrinkage
shrink_start = 0.1
shrink_end   = 0.8
shrink_steps = 0.4
#MaxDepth
MaxD_start = 2
MaxD_end   = 3
MaxD_steps = 1
#nCuts
nCuts_start = 20
nCuts_end   = 20
nCuts_steps = 1
