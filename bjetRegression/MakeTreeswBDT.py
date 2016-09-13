
#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
from glob import glob
from array import array
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from evalBDT import *
#-------------------------------------------------------------------------------------#
#
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);
#
#-------------------------------------------------------------------------------------#
# Set Variables
outfilename = sys.argv[1]



evt_vars_noreg = ["Evt_blr_ETH_transformed",
                  "Evt_Deta_JetsAverage",
                  "Evt_H0",
                  "Evt_Dr_MinDeltaRLeptonJet",
                  "Evt_M_MinDeltaRUntaggedJets",
                  "Evt_Dr_MinDeltaRJets",
                  "Evt_TaggedJet_MaxDeta_Jets",
                  "Evt_M_Total",
                  "Evt_CSV_Average"]

evt_vars_reg = ["Evt_Reg_blr_ETH_transformed",
                "Evt_Deta_JetsAverage",
                "Evt_Reg_H0",
                "Evt_Reg_Dr_MinDeltaRLeptonJet",
                "Evt_Reg_M_MinDeltaRUntaggedJets",
                "Evt_Reg_Dr_MinDeltaRJets",
                "Evt_TaggedJet_MaxDeta_Jets",
                "Evt_Reg_M_Total",
                "Evt_CSV_Average"]

evt_vars_reg_init = ["Evt_Reg_blr_ETH_transformed",
                     "Evt_Reg_H0",
                     "Evt_Reg_Dr_MinDeltaRLeptonJet",
                     "Evt_Reg_M_MinDeltaRUntaggedJets",
                     "Evt_Reg_Dr_MinDeltaRJets",
                     "Evt_Reg_M_Total"]



common5_input = ["BDT_common5_input_avg_dr_tagged_jets",
                 "BDT_common5_input_tagged_dijet_mass_closest_to_125",
                 "BDT_common5_input_closest_tagged_dijet_mass",
                 "BDT_common5_input_fifth_highest_CSV",
                 "BDT_common5_input_best_higgs_mass",
                 "BDT_common5_input_sphericity",
                 "BDT_common5_input_M3",
                 "BDT_common5_input_all_sum_pt_with_met",
                 "BDT_common5_input_avg_btag_disc_btags",
                 "BDT_common5_input_dEta_fn",
                 "BDT_common5_input_aplanarity",
                 "BDT_common5_input_dev_from_avg_disc_btags",
                 "BDT_common5_input_Mlb",
                 "BDT_common5_input_min_dr_tagged_jets",
                 "BDT_common5_input_HT",
                 "BDT_common5_input_h3",
                 "BDT_common5_input_fourth_jet_pt",
                 "BDT_common5_input_pt_all_jets_over_E_all_jets",
                 "BDT_common5_input_h1",
                 "BDT_common5_input_fourth_highest_btag",
                 "BDT_common5_input_invariant_mass_of_everything",
                 "BDT_common5_input_fifth_highest_CSV",
                 "BDT_common5_input_h2",
                 "BDT_common5_input_dr_between_lep_and_closest_jet",
                 "BDT_common5_input_second_jet_pt"]

reg_common5_input = ["BDT_Reg_common5_input_avg_dr_tagged_jets",
                     "BDT_Reg_common5_input_tagged_dijet_mass_closest_to_125",
                     "BDT_Reg_common5_input_closest_tagged_dijet_mass",
                     "BDT_Reg_common5_input_fifth_highest_CSV",
                     "BDT_Reg_common5_input_best_higgs_mass",
                     "BDT_Reg_common5_input_sphericity",
                     "BDT_Reg_common5_input_M3",
                     "BDT_Reg_common5_input_all_sum_pt_with_met",
                     "BDT_Reg_common5_input_avg_btag_disc_btags",
                     "BDT_Reg_common5_input_dEta_fn",
                     "BDT_Reg_common5_input_aplanarity",
                     "BDT_Reg_common5_input_dev_from_avg_disc_btags",
                     "BDT_Reg_common5_input_Mlb",
                     "BDT_Reg_common5_input_min_dr_tagged_jets",
                     "BDT_Reg_common5_input_HT",
                     "BDT_Reg_common5_input_h3",
                     "BDT_Reg_common5_input_fourth_jet_pt",
                     "BDT_Reg_common5_input_pt_all_jets_over_E_all_jets",
                     "BDT_Reg_common5_input_h1",
                     "BDT_Reg_common5_input_fourth_highest_btag",
                     "BDT_Reg_common5_input_invariant_mass_of_everything",
                     "BDT_Reg_common5_input_fifth_highest_CSV",
                     "BDT_Reg_common5_input_h2",
                     "BDT_Reg_common5_input_dr_between_lep_and_closest_jet",
                     "BDT_Reg_common5_input_second_jet_pt"]

rootdir = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/classificationtrain/weights/"
print "Init BDT without regression:"
BDTs_noreg = BDTEvaluator( { "64" : rootdir+"weights_retrainedBDTs_0908_6j4t_noreg_BDTG.weights.xml",
                             "63" : rootdir+"weights_retrainedBDTs_0908_6j3t_noreg_BDTG.weights.xml",
                             "62" : rootdir+"weights_retrainedBDTs_0908_6j2t_noreg_BDTG.weights.xml",
                             "54" : rootdir+"weights_retrainedBDTs_0908_5j4t_noreg_BDTG.weights.xml",
                             "53" : rootdir+"weights_retrainedBDTs_0908_5j3t_noreg_BDTG.weights.xml",
                             "44" : rootdir+"weights_retrainedBDTs_0908_4j4t_noreg_BDTG.weights.xml",
                             "43" : rootdir+"weights_retrainedBDTs_0908_4j3t_noreg_BDTG.weights.xml" })
print "Init BDT with regression:"
BDTs_reg = BDTEvaluator( { "64" : rootdir+"weights_retrainedBDTs_0908_6j4t_reg_BDTG.weights.xml",
                           "63" : rootdir+"weights_retrainedBDTs_0908_6j3t_reg_BDTG.weights.xml",
                           "62" : rootdir+"weights_retrainedBDTs_0908_6j2t_reg_BDTG.weights.xml",
                           "54" : rootdir+"weights_retrainedBDTs_0908_5j4t_reg_BDTG.weights.xml",
                           "53" : rootdir+"weights_retrainedBDTs_0908_5j3t_reg_BDTG.weights.xml",
                           "44" : rootdir+"weights_retrainedBDTs_0908_4j4t_reg_BDTG.weights.xml",
                           "43" : rootdir+"weights_retrainedBDTs_0908_4j3t_reg_BDTG.weights.xml" }, "Reg_")

outputfile = ROOT.TFile( outfilename, "RECREATE" );


path = "/nfs/dust/cms/user/kschweig/JetRegression/trees0908/BDTTraining/ttHbb/*_1_*nominal*.root"

inputtree = ROOT.TChain("MVATree")

for f in sys.argv[2:]:
    inputtree.Add(f)

BDTvars_input = {}

initialized = []
for variable in evt_vars_noreg + evt_vars_reg + common5_input + reg_common5_input:
    if variable not in initialized:
        #print variable
        BDTvars_input.update( { variable : array.array('f',[0] ) } )
        inputtree.SetBranchAddress( variable , BDTvars_input[variable] )
        initialized.append(variable)

outputfile.cd()
    
OutputTree =  ROOT.TTree("MVATree","MVATree");

E_Odd = array.array('f',[0])
E_Weight = array.array('f',[0])
P_Weight = array.array('f',[0])
P69_Weight = array.array('f',[0])
C_Weight = array.array('f',[0])
LSF = array.array('f',[0])

eSFGFS = array.array('f',[0])
eSFID = array.array('f',[0])
eSFIso = array.array('f',[0])
eSFTrigger = array.array('f',[0])
mSFID = array.array('f',[0])
mSFTrigger = array.array('f',[0])
mSFIso = array.array('f',[0])
mSFHIP = array.array('f',[0])

njets = array.array('f',[0])
nbtags = array.array('f',[0])

bdtout_noreg = array.array('f',[0])
bdtout_reg  = array.array('f',[0])

BDTvars = {}
initialized = []
for variable in evt_vars_noreg + evt_vars_reg + common5_input + reg_common5_input:
    if variable not in initialized:
        BDTvars.update( { variable : array.array('f',[0] ) } )
        OutputTree.Branch(variable,BDTvars[variable],variable+"/f")
        initialized.append(variable)


OutputTree.Branch("Evt_Odd",E_Odd,"Evt_Odd/f");
OutputTree.Branch("Weight",E_Weight,"Weight/f");
OutputTree.Branch("Weight_PU",P_Weight,"Weight_PU/f");
OutputTree.Branch("Weight_pu69p2",P69_Weight,"Weight_pu69p2/f");
OutputTree.Branch("Weight_CSV",C_Weight,"Weight_CSV/f");

OutputTree.Branch("Weight_ElectronSFGFS",eSFGFS,"Weight_ElectronSFGFS/f");
OutputTree.Branch("Weight_ElectronSFID",eSFID,"Weight_ElectronSFID/f");
OutputTree.Branch("Weight_ElectronSFIso",eSFIso,"Weight_ElectronSFIso/f");
OutputTree.Branch("Weight_ElectronSFTrigger",eSFTrigger,"Weight_ElectronSFTrigger/f");
OutputTree.Branch("Weight_MuonSFID",mSFID,"Weight_MuonSFID/f");
OutputTree.Branch("Weight_MuonSFTrigger",mSFTrigger,"Weight_MuonSFTrigger/f");
OutputTree.Branch("Weight_MuonSFIso",mSFIso,"Weight_MuonSFIso/f");
OutputTree.Branch("Weight_MuonSFHIP",mSFHIP,"Weight_MuonSFHIP/f");

OutputTree.Branch("N_Jets",njets,"N_Jets/f")
OutputTree.Branch("N_BTagsM",nbtags,"N_BTagsM/f")

OutputTree.Branch("BDTOutput_noreg",bdtout_noreg,"BDTOutput_noreg/f");
OutputTree.Branch("BDTOutput_reg",bdtout_reg,"BDTOutput_reg/f");


nEvents = inputtree.GetEntries()


for iev in range(nEvents):

    inputtree.GetEvent(iev)

    E_Odd[0] = inputtree.Evt_Odd
    E_Weight[0] = inputtree.Weight
    P_Weight[0] = inputtree.Weight_PU
    P69_Weight[0] = inputtree.Weight_pu69p2
    C_Weight[0] = inputtree.Weight_CSV
    
    eSFGFS[0] = inputtree.Weight_ElectronSFGFS
    eSFID[0] = inputtree.Weight_ElectronSFID
    eSFIso[0] = inputtree.Weight_ElectronSFIso
    eSFTrigger[0] = inputtree.Weight_ElectronSFTrigger
    mSFID[0] = inputtree.Weight_MuonSFID
    mSFTrigger[0] = inputtree.Weight_MuonSFTrigger
    mSFIso[0] = inputtree.Weight_MuonSFIso
    mSFHIP[0] = inputtree.Weight_MuonSFHIP
    njets[0] = inputtree.N_Jets
    nbtags [0] = inputtree.N_BTagsM

    written = []
    for variable in evt_vars_noreg + evt_vars_reg + common5_input + reg_common5_input:
        if variable not in written:
            #print variable
            BDTvars[variable][0] = BDTvars_input[variable][0]
            written.append(variable)
            
    input_noreg = {}
    input_noreg["Evt_blr_ETH_transformed"] = BDTvars_input[ "Evt_blr_ETH_transformed"  ][0]
    input_noreg["Evt_Deta_JetsAverage"] = BDTvars_input[ "Evt_Deta_JetsAverage" ][0]
    input_noreg["avg_dr_tagged_jets"] = BDTvars_input[ "BDT_common5_input_avg_dr_tagged_jets" ][0]
    input_noreg["tagged_dijet_mass_closest_to_125"] = BDTvars_input[ "BDT_common5_input_tagged_dijet_mass_closest_to_125" ][0]
    input_noreg["closest_tagged_dijet_mass"] = BDTvars_input[ "BDT_common5_input_closest_tagged_dijet_mass" ][0]
    input_noreg["fifth_highest_CSV"] = BDTvars_input[ "BDT_common5_input_fifth_highest_CSV" ][0]
    input_noreg["best_higgs_mass"] = BDTvars_input[ "BDT_common5_input_best_higgs_mass" ][0]
    input_noreg["sphericity"] = BDTvars_input[ "BDT_common5_input_sphericity"][0]
    input_noreg["M3"] = BDTvars_input[ "BDT_common5_input_M3" ][0]
    input_noreg["all_sum_pt_with_met"] = BDTvars_input[ "BDT_common5_input_all_sum_pt_with_met" ][0]
    input_noreg["avg_btag_disc_btags"] = BDTvars_input[ "BDT_common5_input_avg_btag_disc_btags" ][0]
    input_noreg["dEta_fn"] = BDTvars_input[ "BDT_common5_input_dEta_fn" ][0]
    input_noreg["aplanarity"] = BDTvars_input[ "BDT_common5_input_aplanarity" ][0]
    input_noreg["dev_from_avg_disc_btags"] = BDTvars_input[ "BDT_common5_input_dev_from_avg_disc_btags" ][0]
    input_noreg["Evt_H0"] = BDTvars_input[ "Evt_H0"  ][0]
    input_noreg["Mlb"] = BDTvars_input[ "BDT_common5_input_Mlb" ][0]
    input_noreg["min_dr_tagged_jets"] = BDTvars_input[ "BDT_common5_input_min_dr_tagged_jets" ][0]
    input_noreg["MinDeltaRLeptonJet"] = BDTvars_input[ "Evt_Dr_MinDeltaRLeptonJet"  ][0]
    input_noreg["HT"] = BDTvars_input[ "BDT_common5_input_HT" ][0]
    input_noreg["Evt_M_MinDeltaRUntaggedJets"] = BDTvars_input[ "Evt_M_MinDeltaRUntaggedJets"  ][0]
    input_noreg["Evt_Dr_MinDeltaRJets"] = BDTvars_input[ "Evt_Dr_MinDeltaRJets"  ][0]
    input_noreg["Evt_TaggedJet_MaxDeta_Jets"] = BDTvars_input[ "Evt_TaggedJet_MaxDeta_Jets"  ][0]
    input_noreg["Evt_M_Total"] = BDTvars_input[ "Evt_M_Total"  ][0]
    input_noreg["h3"] = BDTvars_input[ "BDT_common5_input_h3" ][0]
    input_noreg["fourth_jet_pt"] = BDTvars_input[ "BDT_common5_input_fourth_jet_pt" ][0]
    input_noreg["pt_all_jets_over_E_all_jets"] = BDTvars_input[ "BDT_common5_input_pt_all_jets_over_E_all_jets" ][0]
    input_noreg["h1"] = BDTvars_input[ "BDT_common5_input_h1" ][0]
    input_noreg["Evt_CSV_Average"] = BDTvars_input[ "Evt_CSV_Average"  ][0]
    input_noreg["fourth_highest_btag"] = BDTvars_input[ "BDT_common5_input_fourth_highest_btag" ][0]
    input_noreg["invariant_mass_of_everything"] = BDTvars_input[ "BDT_common5_input_invariant_mass_of_everything" ][0]
    input_noreg["fifth_highest_CSV"] = BDTvars_input[ "BDT_common5_input_fifth_highest_CSV" ][0]
    input_noreg["h2"] = BDTvars_input[ "BDT_common5_input_h2" ][0]
    input_noreg["dr_between_lep_and_closest_jet"] = BDTvars_input[ "BDT_common5_input_dr_between_lep_and_closest_jet" ][0]
    input_noreg["second_jet_pt"] = BDTvars_input[ "BDT_common5_input_second_jet_pt" ][0]
    
    input_reg = {}
    input_reg["Evt_blr_ETH_transformed"] = BDTvars_input[ "Evt_Reg_blr_ETH_transformed"  ][0]
    input_reg["Evt_Deta_JetsAverage"] = BDTvars_input[ "Evt_Deta_JetsAverage"  ][0]
    input_reg["avg_dr_tagged_jets"] = BDTvars_input[ "BDT_Reg_common5_input_avg_dr_tagged_jets" ][0]
    input_reg["tagged_dijet_mass_closest_to_125"] = BDTvars_input[ "BDT_Reg_common5_input_tagged_dijet_mass_closest_to_125" ][0]
    input_reg["closest_tagged_dijet_mass"] = BDTvars_input[ "BDT_Reg_common5_input_closest_tagged_dijet_mass" ][0]
    input_reg["fifth_highest_CSV"] = BDTvars_input[ "BDT_Reg_common5_input_fifth_highest_CSV" ][0]
    input_reg["best_higgs_mass"] = BDTvars_input[ "BDT_Reg_common5_input_best_higgs_mass" ][0]
    input_reg["sphericity"] = BDTvars_input[ "BDT_Reg_common5_input_sphericity"][0]
    input_reg["M3"] = BDTvars_input[ "BDT_Reg_common5_input_M3" ][0]
    input_reg["all_sum_pt_with_met"] = BDTvars_input[ "BDT_Reg_common5_input_all_sum_pt_with_met" ][0]
    input_reg["avg_btag_disc_btags"] = BDTvars_input[ "BDT_Reg_common5_input_avg_btag_disc_btags" ][0]
    input_reg["dEta_fn"] = BDTvars_input[ "BDT_Reg_common5_input_dEta_fn" ][0]
    input_reg["aplanarity"] = BDTvars_input[ "BDT_Reg_common5_input_aplanarity" ][0]
    input_reg["dev_from_avg_disc_btags"] = BDTvars_input[ "BDT_Reg_common5_input_dev_from_avg_disc_btags" ][0]
    input_reg["Evt_H0"] = BDTvars_input[ "Evt_Reg_H0"  ][0]
    input_reg["Mlb"] = BDTvars_input[ "BDT_Reg_common5_input_Mlb" ][0]
    input_reg["min_dr_tagged_jets"] = BDTvars_input[ "BDT_Reg_common5_input_min_dr_tagged_jets" ][0]
    input_reg["MinDeltaRLeptonJet"] = BDTvars_input[ "Evt_Reg_Dr_MinDeltaRLeptonJet"  ][0]
    input_reg["HT"] = BDTvars_input[ "BDT_Reg_common5_input_HT" ][0]
    input_reg["Evt_M_MinDeltaRUntaggedJets"] = BDTvars_input[ "Evt_Reg_M_MinDeltaRUntaggedJets"  ][0]
    input_reg["Evt_Dr_MinDeltaRJets"] = BDTvars_input[ "Evt_Reg_Dr_MinDeltaRJets"  ][0]
    input_reg["Evt_TaggedJet_MaxDeta_Jets"] = BDTvars_input[ "Evt_TaggedJet_MaxDeta_Jets"  ][0]
    input_reg["Evt_M_Total"] = BDTvars_input[ "Evt_Reg_M_Total"  ][0]
    input_reg["h3"] = BDTvars_input[ "BDT_Reg_common5_input_h3" ][0]
    input_reg["fourth_jet_pt"] = BDTvars_input[ "BDT_Reg_common5_input_fourth_jet_pt" ][0]
    input_reg["pt_all_jets_over_E_all_jets"] = BDTvars_input[ "BDT_Reg_common5_input_pt_all_jets_over_E_all_jets" ][0]
    input_reg["h1"] = BDTvars_input[ "BDT_Reg_common5_input_h1" ][0]
    input_reg["Evt_CSV_Average"] = BDTvars_input[ "Evt_CSV_Average"  ][0]
    input_reg["fourth_highest_btag"] = BDTvars_input[ "BDT_Reg_common5_input_fourth_highest_btag" ][0]
    input_reg["invariant_mass_of_everything"] = BDTvars_input[ "BDT_Reg_common5_input_invariant_mass_of_everything" ][0]
    input_reg["fifth_highest_CSV"] = BDTvars_input[ "BDT_Reg_common5_input_fifth_highest_CSV" ][0]
    input_reg["h2"] = BDTvars_input[ "BDT_Reg_common5_input_h2" ][0]
    input_reg["dr_between_lep_and_closest_jet"] = BDTvars_input[ "BDT_Reg_common5_input_dr_between_lep_and_closest_jet" ][0]
    input_reg["second_jet_pt"] = BDTvars_input[ "BDT_Reg_common5_input_second_jet_pt" ][0]

    #print BDTvars["Evt_Deta_JetsAverage"][0], type(BDTvars["Evt_Deta_JetsAverage"][0])
    
    bdtout_noreg[0] = BDTs_noreg.evaluesBDT(input_noreg, inputtree.N_Jets  , inputtree.N_BTagsM )
    bdtout_reg[0] = BDTs_reg.evaluesBDT(input_reg, inputtree.N_Jets , inputtree.N_BTagsM )

    OutputTree.Fill()

OutputTree.Write();
