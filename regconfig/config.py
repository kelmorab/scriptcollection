#Setting configuration for testing regression configurations

#General stuff
cmsswpath='/nfs/dust/cms/user/kschweig/CMSSW_7_6_3'
program = 'Code/scriptcollection/regconfig/Regressiontraining.C'
nfsroot = "/nfs/dust/cms/user/kschweig/"
inputfiles = "JetRegression/trees0413/ttbarforbReg.root"
outputfilefolder = "JetRegression/Settingtesting/0601/inputsets_noratio/"
outputfileprefix = ""
weightprefix = "0601_"
#variable definition
cuts = "Evt_Odd == 1 && abs(Jet_Flav) == 5 && abs(Jet_MatchedPartonFlav) == 5 && Jet_Eta <= 2.4"
weightexp = "Weight * Weight_PU"
#NTrees
tree_list = [1200]
nTrees_start = 200
nTrees_end   = 1800
nTrees_steps = 400
#Shrinkage
shrink_list = [0.1]
shrink_start = 0.001
shrink_end   = 0.1
shrink_steps = 10
#MaxDepth
MaxD_start = 4
MaxD_end   = 5
MaxD_steps = 2
#nCuts
nCuts_start = 30
nCuts_end   = 40
nCuts_steps = 20
#baggedsf
bsf_list = [0.6]


#inputsets
allinputsets= [ ["True","True","True","True","True","True","True","True","True","True","True","True","True","True","True","True"],
                ["True","False","True","True","True","True","True","True","True","True","True","True","True","True","True","True"],
                ["True","True","False","True","True","True","True","True","True","True","True","True","True","True","True","True"],
                ["True","True","True","False","True","True","True","True","True","True","True","True","True","True","True","True"],
                ["True","True","True","True","False","True","True","True","True","True","True","True","True","True","True","True"],
                ["True","True","True","True","True","False","True","True","True","True","True","True","True","True","True","True"],
                ["True","True","True","True","True","True","False","True","True","True","True","True","True","True","True","True"],
                ["True","True","True","True","True","True","True","False","True","True","True","True","True","True","True","True"],
                ["True","True","True","True","True","True","True","True","False","True","True","True","True","True","True","True"],
                ["True","True","True","True","True","True","True","True","True","False","True","True","True","True","True","True"],
                ["True","True","True","True","True","True","True","True","True","True","False","True","True","True","True","True"],
                ["True","True","True","True","True","True","True","True","True","True","True","False","True","True","True","True"],
                ["True","True","True","True","True","True","True","True","True","True","True","True","False","True","True","True"],
                ["True","True","True","True","True","True","True","True","True","True","True","True","True","False","True","True"],
                ["True","True","True","True","True","True","True","True","True","True","True","True","True","True","False","True"],
                ["True","True","True","True","True","True","True","True","True","True","True","True","True","True","True","False"],
                ["True","True","True","True","True","True","True","True","True","False","False","False","True","True","True","True"],
]
namelist = ["All","NoVar1","NoVar2","NoVar3","NoVar4","NoVar5","NoVar6","NoVar7","NoVar8","NoVar9","NoVar10","NoVar11","NoVar12","NoVar13","NoVar14","NoVar15","NoVar9_10_11"]
#namelist = []
