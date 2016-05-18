#Setting configuration for testing regression configurations

#General stuff
cmsswpath='/nfs/dust/cms/user/kschweig/CMSSW_7_4_15'
program = 'Code/scriptcollection/regconfig/Regressiontraining.C'
nfsroot = "/nfs/dust/cms/user/kschweig/"
inputfiles = "JetRegression/trees0209/ttbarforbReg0211.root"
outputfilefolder = "JetRegression/trees0209/ttbarbReg0322_testing/"
outputfileprefix = ""
weightprefix = "0322_"
#variable definition
cuts = "Evt_Odd == 1 && abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5"
#NTrees
tree_list = [1200]
nTrees_start = 200
nTrees_end   = 1800
nTrees_steps = 400
#Shrinkage
shrink_list = [0.1,0.08,0.12,0.3]
shrink_start = 0.001
shrink_end   = 0.1
shrink_steps = 10
#MaxDepth
MaxD_start = 6
MaxD_end   = 10
MaxD_steps = 2
#nCuts
nCuts_start = 30
nCuts_end   = 40
nCuts_steps = 20
