#At first try with 6 Jet 4 Tag Cat
#usage: python training.py /path/to/signalfiles/ /path/to/bkgfiles/ outputname regressedvars[True/Flase] category[6j4t || 5j4t || ....]

from ROOT import TMVA, TFile, TTree, TCut, TChain
import sys
from glob import glob
################################################
if str(sys.argv[4]) == "True":
    sys.argv[4]=True
elif str(sys.argv[4]) == "False":
    sys.argv[4]=False
else:
    print "Argument 4 must be True or False"
    exit()

cats = ["6j4t","5j4t","5j3t","4j4t","4j3t","6j3t","6j2t"]
if str(sys.argv[5]) not in cats:
    print "Argument 5 must be an element of",cats
    exit()

print "Please verify settings:"
print "Signalpath:",sys.argv[1]
print "Backgroundpath:",sys.argv[2]
print "Outputnameprefix:",sys.argv[3]
print "Use regressed input variables:",sys.argv[4]
print "Jet/Tag Category:",sys.argv[5]
raw_input("Press Ret if correct")

# Set static variables 
weight = 1
#Set used MVA-Method for Regression
useBDT = True

regressedvars = sys.argv[4]
cat = str(sys.argv[5])

###############################################
TMVA.Tools.Instance()

outputFile = TFile(str(sys.argv[3])+".root","RECREATE")

factory = TMVA.Factory( "weights_"+str(sys.argv[3]), outputFile,"V:!Silent:Color:DrawProgressBar:AnalysisType=Classification" )

#Add Variables
if regressedvars:
    prefix = "BDT_reg_common5_input_"
else:
    prefix = "BDT_common5_input_"

if cat == "6j4t":
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')
    factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
    factory.AddVariable(prefix+"Evt_Deta_JetsAverage",prefix+"Evt_Deta_JetsAverage","units",'F')
    factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')
    factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
    factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
    factory.AddVariable(prefix+"second_highest_btag",prefix+"second_highest_btag","units",'F')
    factory.AddVariable(prefix+"dr_between_lep_and_closest_jet",prefix+"dr_between_lep_and_closest_jet","units",'F')
    factory.AddVariable(prefix+"third_jet_pt",prefix+"third_jet_pt","units",'F')

    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 6 && N_BTagsM >= 4")

if cat == "6j3t":
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
    factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')
    factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
    factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
    factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
    factory.AddVariable(prefix+"Evt_Deta_JetsAverage",prefix+"Evt_Deta_JetsAverage","units",'F')
    factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"dEta_fn",prefix+"dEta_fn","units",'F')
    factory.AddVariable(prefix+"aplanarity",prefix+"aplanarity","units",'F')
    factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')

    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 6 && N_BTagsM >= 3")

if cat == "6j2t":
    factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
    factory.AddVariable(prefix+"third_highest_btag",prefix+"third_highest_btag","units",'F')
    factory.AddVariable(prefix+"h3",prefix+"h3","units",'F')
    factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
    factory.AddVariable(prefix+"Mlb",prefix+"Mlb","units",'F')
    factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
    factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')

    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 6 && N_BTagsM >= 2")


    
if cat == "5j4t":
    factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
    factory.AddVariable(prefix+"pt_all_jets_over_E_all_jets",prefix+"pt_all_jets_over_E_all_jets","units",'F')
    factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
    factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
    factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
    factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
    factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')

    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 5 && N_BTagsM >= 4")


if cat == "5j3t":
    factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
    factory.AddVariable(prefix+"third_highest_btag",prefix+"third_highest_btag","units",'F')
    factory.AddVariable(prefix+"h3",prefix+"h3","units",'F')
    factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
    factory.AddVariable(prefix+"dev_from_avg_disc_btags",prefix+"dev_from_avg_disc_btags","units",'F')
    factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')


    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 5 && N_BTagsM >= 3")


if cat == "4j4t":
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
    factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
    factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
    factory.AddVariable(prefix+"Evt_Deta_JetsAverage",prefix+"Evt_Deta_JetsAverage","units",'F')
    factory.AddVariable(prefix+"maxeta_jet_tag",prefix+"maxeta_jet_tag","units",'F')
    factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
    factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')

    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 4 && N_BTagsM >= 4")

if cat == "4j3t":
    factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
    factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
    factory.AddVariable(prefix+"third_highest_btag",prefix+"third_highest_btag","units",'F')
    factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
    factory.AddVariable(prefix+"dev_from_avg_disc_btags",prefix+"dev_from_avg_disc_btags","units",'F')
    factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
    factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
    factory.AddVariable(prefix+"Evt_CSV_Average",prefix+"Evt_CSV_Average","units",'F')

    cut = TCut("Evt_Odd == 1 && Weight && Weight_PU  && N_Jets >= 4 && N_BTagsM >= 3")

    

#Get and Add Signal and Background Tree
signal = TChain("MVATree")
for infile in glob(sys.argv[1]+"/*.root"):
    signal.Add(infile)

background = TChain("MVATree")
for infile in glob(sys.argv[2]+"/*.root"):
    background.Add(infile)

factory.AddSignalTree(signal)
factory.AddBackgroundTree(background)




factory.PrepareTrainingAndTestTree( cut, cut, "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

#Book all methods
if useBDT:
    if cat == "6j4t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=1218::BoostType=Grad:Shrinkage=8.641517e-03:UseBaggedBoost=True:nCuts=21:MaxDepth=2:GradBaggingFraction=6.673016e-01:NegWeightTreatment=ignorenegweightsintraining" );
    if cat == "6j3t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=454::BoostType=Grad:Shrinkage=3.284414e-02:UseBaggedBoost=True:nCuts=38:MaxDepth=2:GradBaggingFraction=2.589974e-01:NegWeightTreatment=ignorenegweightsintraining" );
    if cat == "6j2t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=1244::BoostType=Grad:Shrinkage=2.809529e-02:UseBaggedBoost=True:nCuts=63:MaxDepth=2:GradBaggingFraction=6.295185e-01:NegWeightTreatment=ignorenegweightsintraining" );
    if cat == "5j4t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=711::BoostType=Grad:Shrinkage=2.144398e-02:UseBaggedBoost=True:nCuts=18:MaxDepth=2:GradBaggingFraction=2.312831e-01:NegWeightTreatment=ignorenegweightsintraining" );
    if cat == "5j3t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=924::BoostType=Grad:Shrinkage=3.886864e-02:UseBaggedBoost=True:nCuts=59:MaxDepth=2:GradBaggingFraction=4.053659e-01:NegWeightTreatment=ignorenegweightsintraining" );
    if cat == "4j4t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=1025::BoostType=Grad:Shrinkage=9.330372e-03:UseBaggedBoost=True:nCuts=24:MaxDepth=2:GradBaggingFraction=4.894101e-01:NegWeightTreatment=ignorenegweightsintraining" );
    if cat == "4j3t":
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "NTrees=1113::BoostType=Grad:Shrinkage=1.968542e-02:UseBaggedBoost=True:nCuts=76:MaxDepth=2:GradBaggingFraction=6.232292e-01:NegWeightTreatment=ignorenegweightsintraining" );

        
print "Training all Methods"
factory.TrainAllMethods();
print "Testing all Methods"
factory.TestAllMethods();
print "Evaluating all Methods"
factory.EvaluateAllMethods(); 

outputFile.Close()
