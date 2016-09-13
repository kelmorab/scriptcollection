#At first try with 6 Jet 4 Tag Cat
#usage: python training.py /path/to/signalfiles/ /path/to/bkgfiles/ outputname regressedvars[True/Flase] category[6j4t || 5j4t || ....]

from ROOT import TMVA, TFile, TTree, TCut, TChain
import sys
from glob import glob
################################################
cats = ["6j4t","5j4t","5j3t","4j4t","4j3t","6j3t","6j2t"]
regressedvars = [False,True]
# Set static variables 
weight = 1
#Set used MVA-Method for Regression
useBDT = True


if len(sys.argv) == 6:
    if str(sys.argv[4]) == "True":
        sys.argv[4]=True
    elif str(sys.argv[4]) == "False":
        sys.argv[4]=False
    else:
        print "Argument 4 must be True or False"
        exit()


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


    regressedvars = [sys.argv[4]]
    cats = [str(sys.argv[5])]
    
elif len(sys.argv) == 4:
    print "Beginning loop with all training."
    if raw_input("Type y if this is correct. Be aware of possible overwrite of previous training") != "y":
        print "Okay. You're the boss...."
    print "Please verify settings:"
    print "Signalpath:",sys.argv[1]
    print "Backgroundpath:",sys.argv[2]
    print "Outputnameprefix:",sys.argv[3]
    raw_input("Press Ret if correct")
    
else:
    print "Somethings wrong with the number of arguments!"
    exit()
    
###############################################
TMVA.Tools.Instance()
for regressedvar in regressedvars:
    for cat in cats:
        if regressedvar:
            prefix = "BDT_Reg_common5_input_"
            midfix = "Reg_"
            outputpostfix = "reg"
        else:
            prefix = "BDT_common5_input_"
            midfix = ""
            outputpostfix = "noreg"

        print "Training the BDT for",cat,"with",outputpostfix,"variables"

        outputFile = TFile(str(sys.argv[3])+"_"+cat+"_"+outputpostfix+".root","RECREATE")

        factory = TMVA.Factory( "weights_"+str(sys.argv[3])+"_"+cat+"_"+outputpostfix, outputFile,"V:!Silent:Color:DrawProgressBar:AnalysisType=Classification" )

        weightexpression = "Weight_XS*Weight_ElectronSFID*Weight_MuonSFID*Weight_MuonSFIso*Weight_ElectronSFGFS*Weight_MuonSFHIP*Weight_pu69p2*Weight_CSV"
        #Add Variables

        if cat == "6j4t":
            
            factory.AddVariable("Evt_"+midfix+"blr_ETH_transformed","Evt_"+midfix+"blr_ETH_transformed","units",'F')
            #factory.AddVariable(prefix+"Evt_blr_ETH_transformed",prefix+"Evt_blr_ETH_transformed","units",'F')
            factory.AddVariable("Evt_Deta_JetsAverage","Evt_Deta_JetsAverage","units",'F')
            factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
            factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
            factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')
            factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
            factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            
            # 76X Inputvariables
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')
            #factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
            #factory.AddVariable(prefix+"Evt_Deta_JetsAverage",prefix+"Evt_Deta_JetsAverage","units",'F')
            #factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')
            #factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            #factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
            #factory.AddVariable(prefix+"second_highest_btag",prefix+"second_highest_btag","units",'F')
            #factory.AddVariable(prefix+"third_jet_pt",prefix+"third_jet_pt","units",'F')
            #factory.AddVariable(prefix+"dr_between_lep_and_closest_jet",prefix+"dr_between_lep_and_closest_jet","units",'F')


            cut = TCut("Evt_Odd == 1 && N_Jets >= 6 && N_BTagsM >= 4")

        if cat == "6j3t":
            factory.AddVariable("Evt_"+midfix+"blr_ETH_transformed","Evt_"+midfix+"blr_ETH_transformed","units",'F')
            #factory.AddVariable(prefix+"Evt_blr_ETH_transformed",prefix+"Evt_blr_ETH_transformed","units",'F')
            factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            factory.AddVariable(prefix+"dEta_fn",prefix+"dEta_fn","units",'F')
            factory.AddVariable(prefix+"aplanarity",prefix+"aplanarity","units",'F')
            factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            factory.AddVariable("Evt_Deta_JetsAverage","Evt_Deta_JetsAverage","units",'F')
            factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
            factory.AddVariable(prefix+"dev_from_avg_disc_btags",prefix+"dev_from_avg_disc_btags","units",'F')
            
            # 76X Inputvariables
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
            #factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')
            #factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            #factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            #factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
            #factory.AddVariable(prefix+"Evt_Deta_JetsAverage",prefix+"Evt_Deta_JetsAverage","units",'F')
            #factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"dEta_fn",prefix+"dEta_fn","units",'F')
            #factory.AddVariable(prefix+"aplanarity",prefix+"aplanarity","units",'F')
            #factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')

            cut = TCut("Evt_Odd == 1  && N_Jets >= 6 && N_BTagsM == 3")

        if cat == "6j2t":

            factory.AddVariable("Evt_"+midfix+"H0","Evt_"+midfix+"H0","units",'F')
            #factory.AddVariable(prefix+"h0",prefix+"h0","units",'F')
            factory.AddVariable("Evt_"+midfix+"blr_ETH_transformed","Evt_"+midfix+"blr_ETH_transformed","units",'F')
            factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            factory.AddVariable("Evt_Deta_JetsAverage","Evt_Deta_JetsAverage","units",'F')
            factory.AddVariable(prefix+"Mlb",prefix+"Mlb","units",'F')
            factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
            factory.AddVariable("Evt_"+midfix+"Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet","units",'F')
            factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
            factory.AddVariable("Evt_"+midfix+"M_MinDeltaRUntaggedJets","Evt_M_MinDeltaRUntaggedJets","units",'F')
            factory.AddVariable("Evt_"+midfix+"Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets","units",'F')
            factory.AddVariable("Evt_TaggedJet_MaxDeta_Jets","Evt_TaggedJet_MaxDeta_Jets","units",'F')
            factory.AddVariable("Evt_"+midfix+"M_Total","Evt_"+midfix+"M_Total","units",'F')
            factory.AddVariable(prefix+"h3",prefix+"h3","units",'F')
            
            # 76X Inputvariables
            #factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
            #factory.AddVariable(prefix+"third_highest_btag",prefix+"third_highest_btag","units",'F')
            #factory.AddVariable(prefix+"h3",prefix+"h3","units",'F')
            #factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
            #factory.AddVariable(prefix+"Mlb",prefix+"Mlb","units",'F')
            #factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
            #factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')

            cut = TCut("Evt_Odd == 1  && N_Jets >= 6 && N_BTagsM == 2")



        if cat == "5j4t":

            factory.AddVariable("Evt_"+midfix+"blr_ETH_transformed","Evt_"+midfix+"blr_ETH_transformed","units",'F')
            factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
            factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            factory.AddVariable("Evt_Deta_JetsAverage","Evt_Deta_JetsAverage","units",'F')
            factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')
            factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            factory.AddVariable(prefix+"fourth_jet_pt",prefix+"fourth_jet_pt","units",'F')
            factory.AddVariable(prefix+"pt_all_jets_over_E_all_jets",prefix+"pt_all_jets_over_E_all_jets","units",'F')
            factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')

            # 76X Inputvariables
            #factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            #factory.AddVariable(prefix+"pt_all_jets_over_E_all_jets",prefix+"pt_all_jets_over_E_all_jets","units",'F')
            #factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            #factory.AddVariable(prefix+"tagged_dijet_mass_closest_to_125",prefix+"tagged_dijet_mass_closest_to_125","units",'F')
            #factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            #factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
            #factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')

            cut = TCut("Evt_Odd == 1 && N_Jets == 5 && N_BTagsM >= 4")


        if cat == "5j3t":

            factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            factory.AddVariable("Evt_CSV_Average","Evt_CSV_Average","units",'F')
            factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')
            factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
            factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            factory.AddVariable(prefix+"invariant_mass_of_everything",prefix+"invariant_mass_of_everything","units",'F')
            factory.AddVariable(prefix+"fifth_highest_CSV",prefix+"fifth_highest_CSV","units",'F')
            factory.AddVariable(prefix+"fourth_jet_pt",prefix+"fourth_jet_pt","units",'F')
            factory.AddVariable(prefix+"pt_all_jets_over_E_all_jets",prefix+"pt_all_jets_over_E_all_jets","units",'F')
            factory.AddVariable(prefix+"best_higgs_mass",prefix+"best_higgs_mass","units",'F')

            # 76X Inputvariables
            #factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
            #factory.AddVariable(prefix+"third_highest_btag",prefix+"third_highest_btag","units",'F')
            #factory.AddVariable(prefix+"h3",prefix+"h3","units",'F')
            #factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
            #factory.AddVariable(prefix+"dev_from_avg_disc_btags",prefix+"dev_from_avg_disc_btags","units",'F')
            #factory.AddVariable(prefix+"fourth_highest_btag",prefix+"fourth_highest_btag","units",'F')


            cut = TCut("Evt_Odd == 1 && N_Jets == 5 && N_BTagsM == 3")


        if cat == "4j4t":

            factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            factory.AddVariable("Evt_Deta_JetsAverage","Evt_Deta_JetsAverage","units",'F')
            factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            factory.AddVariable(prefix+"h2",prefix+"h2","units",'F')
            factory.AddVariable(prefix+"invariant_mass_of_everything",prefix+"invariant_mass_of_everything","units",'F')
            factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')

            # 76X Inputvariables
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            #factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            #factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            #factory.AddVariable(prefix+"Evt_Deta_JetsAverage",prefix+"Evt_Deta_JetsAverage","units",'F')
            #factory.AddVariable(prefix+"maxeta_jet_tag",prefix+"maxeta_jet_tag","units",'F')
            #factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            #factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')

            cut = TCut("Evt_Odd == 1 &&  N_Jets == 4 && N_BTagsM >= 4")

        if cat == "4j3t":
            factory.AddVariable("Evt_"+midfix+"blr_ETH_transformed","Evt_"+midfix+"blr_ETH_transformed","units",'F')
            factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
            factory.AddVariable("Evt_Deta_JetsAverage","Evt_Deta_JetsAverage","units",'F')
            factory.AddVariable(prefix+"all_sum_pt_with_met",prefix+"all_sum_pt_with_met","units",'F')
            factory.AddVariable(prefix+"avg_btag_disc_btags",prefix+"avg_btag_disc_btags","units",'F')
            factory.AddVariable(prefix+"closest_tagged_dijet_mass",prefix+"closest_tagged_dijet_mass","units",'F')
            factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
            factory.AddVariable(prefix+"dr_between_lep_and_closest_jet",prefix+"dr_between_lep_and_closest_jet","units",'F')
            factory.AddVariable(prefix+"pt_all_jets_over_E_all_jets",prefix+"pt_all_jets_over_E_all_jets","units",'F')
            factory.AddVariable(prefix+"second_jet_pt",prefix+"second_jet_pt","units",'F')
            factory.AddVariable("Evt_CSV_Average","Evt_CSV_Average","units",'F')

            #factory.AddVariable(prefix+"h1",prefix+"h1","units",'F')
            #factory.AddVariable(prefix+"avg_dr_tagged_jets",prefix+"avg_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"sphericity",prefix+"sphericity","units",'F')
            #factory.AddVariable(prefix+"third_highest_btag",prefix+"third_highest_btag","units",'F')
            #factory.AddVariable(prefix+"HT",prefix+"HT","units",'F')
            #factory.AddVariable(prefix+"dev_from_avg_disc_btags",prefix+"dev_from_avg_disc_btags","units",'F')
            #factory.AddVariable(prefix+"M3",prefix+"M3","units",'F')
            #factory.AddVariable(prefix+"min_dr_tagged_jets",prefix+"min_dr_tagged_jets","units",'F')
            #factory.AddVariable(prefix+"Evt_CSV_Average",prefix+"Evt_CSV_Average","units",'F')

            cut = TCut("Evt_Odd == 1 && N_Jets == 4 && N_BTagsM == 3")



        #Get and Add Signal and Background Tree
        signal = TChain("MVATree")
        for infile in glob(sys.argv[1]+"/*nominal*.root"):
            signal.Add(infile)

        background = TChain("MVATree")
        for infile in glob(sys.argv[2]+"/*nominal*.root"):
            background.Add(infile)

        factory.AddSignalTree(signal)
        factory.AddBackgroundTree(background)




        factory.PrepareTrainingAndTestTree( cut, cut, "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

        #Book all methods
        if useBDT:
            if cat == "6j4t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=446:BoostType=Grad:Shrinkage=0.0326705861892:UseBaggedBoost:GradBaggingFraction=0.314676051777:nCuts=58:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining");
            if cat == "6j3t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=578:BoostType=Grad:Shrinkage=0.029627156969:UseBaggedBoost:GradBaggingFraction=0.331776656252:nCuts=60:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining");
            if cat == "6j2t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=351:BoostType=Grad:Shrinkage=0.0317973455362:UseBaggedBoost:GradBaggingFraction=0.241198201225:nCuts=32:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining");
            if cat == "5j4t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=914:BoostType=Grad:Shrinkage=0.00856744794334:UseBaggedBoost:GradBaggingFraction=0.301119706383:nCuts=29:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining" );
            if cat == "5j3t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=549:BoostType=Grad:Shrinkage=0.0272562089345:UseBaggedBoost:GradBaggingFraction=0.219329696948:nCuts=40:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining" );
            if cat == "4j4t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=708:BoostType=Grad:Shrinkage=0.00926433342788:UseBaggedBoost:GradBaggingFraction=0.15:nCuts=10:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining" );
            if cat == "4j3t":
                factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                                    "!H:!V:NTrees=1047:BoostType=Grad:Shrinkage=0.0358977146231:UseBaggedBoost:GradBaggingFraction=0.263999436985:nCuts=34:MaxDepth=2:NegWeightTreatment=IgnoreNegWeightsInTraining" );


        print "Training all Methods"
        factory.TrainAllMethods();
        print "Testing all Methods"
        factory.TestAllMethods();
        print "Evaluating all Methods"
        factory.EvaluateAllMethods(); 

        outputFile.Close()
