###################################################################################################################
#-----------------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------------# 
#         Script for training of TMVA multivariate regression for morphed gaussian distributions                  # 
#-----------------------------------------------------------------------------------------------------------------# 
#          >>>>>>>> usage: python simpletraining.py inputfile.root outputname prefix <<<<<<<<                     #
#-----------------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------------#
###################################################################################################################

# usage: python simpletraining.py inputfile outpuname prefix 
from ROOT import TMVA, TFile, TTree, TCut
import sys
################################################
# Set static variables 
weight = 1
#Set used MVA-Method for Regression
useBDT = True
useANN = False

if len(sys.argv) < 4:
    prefix = ""
else:
    prefix = "_"+str(sys.argv[3])

################################################
TMVA.Tools.Instance()

outputFile = TFile(prefix+str(sys.argv[2])+".root","RECREATE")

factory = TMVA.Factory( "TMVARegression"+prefix, outputFile,"V:!Silent:Color:DrawProgressBar" )

#Add Variables
factory.AddVariable("var0","var0","units",'F')
#factory.AddVariable("var1","var1","units",'F')
factory.AddVariable("var2","var1","units",'F')
#factory.AddVariable("var3","var2","units",'F')
#Add Target
#factory.AddTarget("target_uni_up")
factory.AddTarget("target")

inputfile = TFile.Open(str(sys.argv[1]))
tree = inputfile.Get("MVATree")

factory.AddRegressionTree( tree, weight )

cut = TCut("Evt_Odd == 1")
#cut = TCut("")

factory.PrepareTrainingAndTestTree( cut, "V:VerboseLevel=Debug:nTrain_Regression=250000:nTest_Regression=250000:SplitMode=Random:NormMode=NumEvents:!V" )

#Book all methods
if useBDT:
    factory.BookMethod( TMVA.Types.kBDT, "BDTG","!H:V:VerbosityLevel=Debug:NTrees=750::BoostType=Grad:Shrinkage=0.09:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3:PruneMethod=costcomplexity:PruneStrength=30:GradBaggingFraction=0.5:UseBaggedBoost=True" );

print "Training all Methods"
factory.TrainAllMethods();
print "Testing all Methods"
factory.TestAllMethods();
print "Evaluating all Methods"
factory.EvaluateAllMethods(); 

outputFile.Close()
