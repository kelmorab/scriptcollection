###################################################################################################################
#-----------------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------------# 
#         Script for training of TMVA multivariate regression for morphed gaussian distributions                  # 
#-----------------------------------------------------------------------------------------------------------------# 
#          >>>>>>>> usage: python PyRegTraining.py outputname nTree Shrinkage nCuts minNodeSize Depth <<<<<<<<                     #
#-----------------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------------#
###################################################################################################################

# usage: python PyRegTraining.py outpuname BDTString 
from ROOT import TMVA, TFile, TTree, TCut
import sys
################################################
# Set static variables 
weight = 1
#Set used MVA-Method for Regression
useBDT = True
useANN = False

if len(sys.argv) < 2:
    BDTString = "NTrees=750::BoostType=Grad:Shrinkage=0.09:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3:PruneMethod=costcomplexity:PruneStrength=30:VarTransform=U(Jet_leptonDeltaR):MinNodeSize=0.6"
else:
    BDTString = "NTrees="+str(sys.argv[2])+"::BoostType=Grad:Shrinkage="+str(sys.argv[3])+":UseBaggedBoost:BaggedSampleFraction=0.5:nCuts="+str(sys.argv[4])+":MaxDepth="+str(sys.argv[6])+":PruneMethod=costcomplexity:PruneStrength=30:VarTransform=U(Jet_leptonDeltaR):MinNodeSize="+str(sys.argv[5])
################################################
TMVA.Tools.Instance()

outputFile = TFile(str(sys.argv[1])+".root","RECREATE")

factory = TMVA.Factory( str(sys.argv[1])+"_", outputFile,"V:!Silent:Color:DrawProgressBar" )
factory.AddVariable("Jet_Pt","Jet_pt","units", 'F');
factory.AddVariable("Jet_corr","Jet_corr","units", 'F');
factory.AddVariable("N_PrimaryVertices","N_PrimaryVertices","units", 'F');
   
factory.AddVariable("Jet_Eta","Jet_eta","units", 'F');
factory.AddVariable("Jet_Mt","Jet_mt","units", 'F');
factory.AddVariable("Jet_leadTrackPt","Jet_leadTrackPt","units", 'F');
factory.AddVariable("Jet_leptonPtRel","Jet_leptonPtRel","units", 'F');
factory.AddVariable("Jet_leptonPt","Jet_leptonPt","units", 'F');
factory.AddVariable("Jet_leptonDeltaR","Jet_leptonDeltaR","units", 'F');
factory.AddVariable("Jet_totHEFrac","Jet_totHEFrac","units", 'F');
factory.AddVariable("Jet_nEmEFrac","Jet_neEmEF","units", 'F');
factory.AddVariable("Jet_vtxPt","Jet_vtxPt","units", 'F');
factory.AddVariable("Jet_vtxMass","Jet_vtxMass","units", 'F');
factory.AddVariable("Jet_vtx3DVal","Jet_vtx3dL","units", 'F');
factory.AddVariable("Jet_vtxNtracks","Jet_vtxNtrk","units", 'F');
factory.AddVariable("Jet_vtx3DSig","Jet_vtx3deL","units", 'F');

#factory.AddTarget( "Jet_MatchedPartonPt / Jet_Pt" );
factory.AddTarget( "Jet_MatchedGenJetwNuPt / Jet_Pt" );



inputfile = TFile.Open("/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TreeforbReg_nominal_0906.root")
tree = inputfile.Get("bRegTree")

factory.AddRegressionTree( tree, 1.0 )

factory.SetWeightExpression("Weight_PU * Weight_CSV * Weight_ElectronSFID * Weight_ElectronSFIso * Weight_MuonSFID * Weight_MuonSFTrigger * Weight_MuonSFIso * Weight_ElectronSFGFS * Weight_ElectronSFTrigger","Regression");

cut = TCut("Evt_Odd == 1 && abs(Jet_Flav) == 5 && Jet_Pt > 25 && Jet_Pt < 600  && Jet_Eta <= 2.4 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600 && abs(Jet_MatchedPartonFlav) == 5")
#cut = TCut("")

factory.PrepareTrainingAndTestTree( cut, "V:VerboseLevel=Debug:nTrain_Regression=200000:nTest_Regression=250000:SplitMode=Random:NormMode=NumEvents:!V" );
#Book all methods
if useBDT:
    factory.BookMethod( TMVA.Types.kBDT, "BDTG","!H:V:VerbosityLevel=Debug:"+BDTString+":GradBaggingFraction=0.5:UseBaggedBoost=True" );

print "Training all Methods"
factory.TrainAllMethods();
print "Testing all Methods"
factory.TestAllMethods();
print "Evaluating all Methods"
factory.EvaluateAllMethods(); 

outputFile.Close()
