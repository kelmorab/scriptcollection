import ROOT
import array

class BDTEvaluator( ):
    
    def __init__(self, weightfiles, midfix=""):
        self.variables = {}
        self.classifier = {}
        
        self.variables["Evt_blr_ETH_transformed"] = array.array('f',[0])
        self.variables["Evt_Deta_JetsAverage"] = array.array('f',[0])
        self.variables["avg_dr_tagged_jets"] = array.array('f',[0])
        self.variables["tagged_dijet_mass_closest_to_125"] = array.array('f',[0])
        self.variables["closest_tagged_dijet_mass"] = array.array('f',[0])
        self.variables["fifth_highest_CSV"] = array.array('f',[0])
        self.variables["best_higgs_mass"] = array.array('f',[0])
        self.variables["sphericity"] = array.array('f',[0])
        self.variables["M3"] = array.array('f',[0])
        self.variables["all_sum_pt_with_met"] = array.array('f',[0])
        self.variables["avg_btag_disc_btags"] = array.array('f',[0])
        self.variables["dEta_fn"] = array.array('f',[0])
        self.variables["aplanarity"] = array.array('f',[0])
        self.variables["dev_from_avg_disc_btags"] = array.array('f',[0])
        self.variables["Evt_H0"] = array.array('f',[0])
        self.variables["Mlb"] = array.array('f',[0])
        self.variables["min_dr_tagged_jets"] = array.array('f',[0])
        self.variables["MinDeltaRLeptonJet"] = array.array('f',[0])
        self.variables["HT"] = array.array('f',[0])
        self.variables["Evt_M_MinDeltaRUntaggedJets"] = array.array('f',[0])
        self.variables["Evt_Dr_MinDeltaRJets"] = array.array('f',[0])
        self.variables["Evt_TaggedJet_MaxDeta_Jets"] = array.array('f',[0])
        self.variables["Evt_M_Total"] = array.array('f',[0])
        self.variables["h3"] = array.array('f',[0])
        self.variables["fourth_jet_pt"] = array.array('f',[0])
        self.variables["pt_all_jets_over_E_all_jets"] = array.array('f',[0])
        self.variables["h1"] = array.array('f',[0])
        self.variables["Evt_CSV_Average"] = array.array('f',[0])
        self.variables["fourth_highest_btag"] = array.array('f',[0])
        self.variables["h1"] = array.array('f',[0])
        self.variables["invariant_mass_of_everything"] = array.array('f',[0])
        self.variables["fifth_highest_CSV"] = array.array('f',[0])
        self.variables["h2"] = array.array('f',[0])
        self.variables["dr_between_lep_and_closest_jet"] = array.array('f',[0])
        self.variables["second_jet_pt"] = array.array('f',[0])


        self.classifier["6J4T"] =  ROOT.TMVA.Reader("Silent")
        self.classifier["6J3T"] =  ROOT.TMVA.Reader("Silent")
        self.classifier["6J2T"] =  ROOT.TMVA.Reader("Silent")
        self.classifier["5J4T"] =  ROOT.TMVA.Reader("Silent")
        self.classifier["5J3T"] =  ROOT.TMVA.Reader("Silent")
        self.classifier["4J4T"] =  ROOT.TMVA.Reader("Silent")
        self.classifier["4J3T"] =  ROOT.TMVA.Reader("Silent")

        
        prefix = "BDT_"+midfix+"common5_input_"

        print "   Initializing 64"
        self.classifier["6J4T"].AddVariable("Evt_"+midfix+"blr_ETH_transformed",self.variables["Evt_blr_ETH_transformed"])
        self.classifier["6J4T"].AddVariable("Evt_Deta_JetsAverage",self.variables["Evt_Deta_JetsAverage"])
        self.classifier["6J4T"].AddVariable(prefix+"avg_dr_tagged_jets",self.variables["avg_dr_tagged_jets"])
        self.classifier["6J4T"].AddVariable(prefix+"tagged_dijet_mass_closest_to_125",self.variables["tagged_dijet_mass_closest_to_125"])
        self.classifier["6J4T"].AddVariable(prefix+"closest_tagged_dijet_mass",self.variables["closest_tagged_dijet_mass"])
        self.classifier["6J4T"].AddVariable(prefix+"fifth_highest_CSV",self.variables["fifth_highest_CSV"])
        self.classifier["6J4T"].AddVariable(prefix+"best_higgs_mass",self.variables["best_higgs_mass"])
        self.classifier["6J4T"].AddVariable(prefix+"sphericity",self.variables["sphericity"])
        self.classifier["6J4T"].AddVariable(prefix+"M3",self.variables["M3"])

        print "   Initializing 63"
        self.classifier["6J3T"].AddVariable("Evt_"+midfix+"blr_ETH_transformed",self.variables["Evt_blr_ETH_transformed"])
        self.classifier["6J3T"].AddVariable(prefix+"all_sum_pt_with_met",self.variables["all_sum_pt_with_met"])
        self.classifier["6J3T"].AddVariable(prefix+"avg_btag_disc_btags",self.variables["avg_btag_disc_btags"])
        self.classifier["6J3T"].AddVariable(prefix+"dEta_fn",self.variables["dEta_fn"])
        self.classifier["6J3T"].AddVariable(prefix+"aplanarity",self.variables["aplanarity"])
        self.classifier["6J3T"].AddVariable(prefix+"avg_dr_tagged_jets",self.variables["avg_dr_tagged_jets"])
        self.classifier["6J3T"].AddVariable("Evt_Deta_JetsAverage",self.variables["Evt_Deta_JetsAverage"])
        self.classifier["6J3T"].AddVariable(prefix+"tagged_dijet_mass_closest_to_125",self.variables["tagged_dijet_mass_closest_to_125"])
        self.classifier["6J3T"].AddVariable(prefix+"dev_from_avg_disc_btags",self.variables["dev_from_avg_disc_btags"])


        print "   Initializing 62"
        self.classifier["6J2T"].AddVariable("Evt_"+midfix+"H0",self.variables["Evt_H0"])
        self.classifier["6J2T"].AddVariable("Evt_"+midfix+"blr_ETH_transformed",self.variables["Evt_blr_ETH_transformed"])
        self.classifier["6J2T"].AddVariable(prefix+"all_sum_pt_with_met",self.variables["all_sum_pt_with_met"])
        self.classifier["6J2T"].AddVariable("Evt_Deta_JetsAverage",self.variables["Evt_Deta_JetsAverage"])
        self.classifier["6J2T"].AddVariable(prefix+"Mlb",self.variables["Mlb"])
        self.classifier["6J2T"].AddVariable(prefix+"min_dr_tagged_jets",self.variables["min_dr_tagged_jets"])
        self.classifier["6J2T"].AddVariable("Evt_"+midfix+"Dr_MinDeltaRLeptonJet",self.variables["MinDeltaRLeptonJet"])
        self.classifier["6J2T"].AddVariable(prefix+"HT",self.variables["HT"])
        self.classifier["6J2T"].AddVariable("Evt_"+midfix+"M_MinDeltaRUntaggedJets",self.variables["Evt_M_MinDeltaRUntaggedJets"])
        self.classifier["6J2T"].AddVariable("Evt_"+midfix+"Dr_MinDeltaRJets",self.variables["Evt_Dr_MinDeltaRJets"])
        self.classifier["6J2T"].AddVariable("Evt_TaggedJet_MaxDeta_Jets",self.variables["Evt_TaggedJet_MaxDeta_Jets"])
        self.classifier["6J2T"].AddVariable("Evt_"+midfix+"M_Total",self.variables["Evt_M_Total"])
        self.classifier["6J2T"].AddVariable(prefix+"h3",self.variables["h3"])

        print "   Initializing 54"
        self.classifier["5J4T"].AddVariable("Evt_"+midfix+"blr_ETH_transformed",self.variables["Evt_blr_ETH_transformed"])
        self.classifier["5J4T"].AddVariable(prefix+"tagged_dijet_mass_closest_to_125",self.variables["tagged_dijet_mass_closest_to_125"])
        self.classifier["5J4T"].AddVariable(prefix+"closest_tagged_dijet_mass",self.variables["closest_tagged_dijet_mass"])
        self.classifier["5J4T"].AddVariable("Evt_Deta_JetsAverage",self.variables["Evt_Deta_JetsAverage"])
        self.classifier["5J4T"].AddVariable(prefix+"best_higgs_mass",self.variables["best_higgs_mass"])
        self.classifier["5J4T"].AddVariable(prefix+"avg_dr_tagged_jets",self.variables["avg_dr_tagged_jets"])
        self.classifier["5J4T"].AddVariable(prefix+"M3",self.variables["M3"])
        self.classifier["5J4T"].AddVariable(prefix+"fourth_jet_pt",self.variables["fourth_jet_pt"])
        self.classifier["5J4T"].AddVariable(prefix+"pt_all_jets_over_E_all_jets",self.variables["pt_all_jets_over_E_all_jets"])
        self.classifier["5J4T"].AddVariable(prefix+"h1",self.variables["h1"])

        print "   Initializing 53"
        self.classifier["5J3T"].AddVariable(prefix+"avg_btag_disc_btags",self.variables["avg_btag_disc_btags"])
        self.classifier["5J3T"].AddVariable("Evt_CSV_Average",self.variables["Evt_CSV_Average"])
        self.classifier["5J3T"].AddVariable(prefix+"fourth_highest_btag",self.variables["fourth_highest_btag"])
        self.classifier["5J3T"].AddVariable(prefix+"h1",self.variables["h1"])
        self.classifier["5J3T"].AddVariable(prefix+"avg_dr_tagged_jets",self.variables["avg_dr_tagged_jets"])
        self.classifier["5J3T"].AddVariable(prefix+"M3",self.variables["M3"])
        self.classifier["5J3T"].AddVariable(prefix+"all_sum_pt_with_met",self.variables["all_sum_pt_with_met"])
        self.classifier["5J3T"].AddVariable(prefix+"invariant_mass_of_everything",self.variables["invariant_mass_of_everything"])
        self.classifier["5J3T"].AddVariable(prefix+"fifth_highest_CSV",self.variables["fifth_highest_CSV"])
        self.classifier["5J3T"].AddVariable(prefix+"fourth_jet_pt",self.variables["fourth_jet_pt"])
        self.classifier["5J3T"].AddVariable(prefix+"pt_all_jets_over_E_all_jets",self.variables["pt_all_jets_over_E_all_jets"])
        self.classifier["5J3T"].AddVariable(prefix+"best_higgs_mass",self.variables["best_higgs_mass"])

        print "   Initializing 44"
        self.classifier["4J4T"].AddVariable(prefix+"avg_btag_disc_btags",self.variables["avg_btag_disc_btags"])
        self.classifier["4J4T"].AddVariable(prefix+"all_sum_pt_with_met",self.variables["all_sum_pt_with_met"])
        self.classifier["4J4T"].AddVariable("Evt_Deta_JetsAverage",self.variables["Evt_Deta_JetsAverage"])
        self.classifier["4J4T"].AddVariable(prefix+"avg_dr_tagged_jets",self.variables["avg_dr_tagged_jets"])
        self.classifier["4J4T"].AddVariable(prefix+"closest_tagged_dijet_mass",self.variables["closest_tagged_dijet_mass"])
        self.classifier["4J4T"].AddVariable(prefix+"h2",self.variables["h2"])
        self.classifier["4J4T"].AddVariable(prefix+"invariant_mass_of_everything",self.variables["invariant_mass_of_everything"])
        self.classifier["4J4T"].AddVariable(prefix+"M3",self.variables["M3"])

        print "   Initializing 43"
        self.classifier["4J3T"].AddVariable("Evt_"+midfix+"blr_ETH_transformed",self.variables["Evt_blr_ETH_transformed"])
        self.classifier["4J3T"].AddVariable(prefix+"M3",self.variables["M3"])
        self.classifier["4J3T"].AddVariable(prefix+"sphericity",self.variables["sphericity"])
        self.classifier["4J3T"].AddVariable("Evt_Deta_JetsAverage",self.variables["Evt_Deta_JetsAverage"])
        self.classifier["4J3T"].AddVariable(prefix+"all_sum_pt_with_met",self.variables["all_sum_pt_with_met"])
        self.classifier["4J3T"].AddVariable(prefix+"avg_btag_disc_btags",self.variables["avg_btag_disc_btags"])
        self.classifier["4J3T"].AddVariable(prefix+"closest_tagged_dijet_mass",self.variables["closest_tagged_dijet_mass"])
        self.classifier["4J3T"].AddVariable(prefix+"min_dr_tagged_jets",self.variables["min_dr_tagged_jets"])
        self.classifier["4J3T"].AddVariable(prefix+"dr_between_lep_and_closest_jet",self.variables["dr_between_lep_and_closest_jet"])
        self.classifier["4J3T"].AddVariable(prefix+"pt_all_jets_over_E_all_jets",self.variables["pt_all_jets_over_E_all_jets"])
        self.classifier["4J3T"].AddVariable(prefix+"second_jet_pt",self.variables["second_jet_pt"])
        self.classifier["4J3T"].AddVariable("Evt_CSV_Average",self.variables["Evt_CSV_Average"])

        print "   Booking 64"
        self.classifier["6J4T"].BookMVA( "BDT" , weightfiles["64"] )
        print "   Booking 63"
        self.classifier["6J3T"].BookMVA( "BDT" , weightfiles["63"] )
        print "   Booking 62"
        self.classifier["6J2T"].BookMVA( "BDT" , weightfiles["62"] )
        print "   Booking 54"
        self.classifier["5J4T"].BookMVA( "BDT" , weightfiles["54"] )
        print "   Booking 53"
        self.classifier["5J3T"].BookMVA( "BDT" , weightfiles["53"] )
        print "   Booking 44"
        self.classifier["4J4T"].BookMVA( "BDT" , weightfiles["44"] )
        print "   Booking 43"
        self.classifier["4J3T"].BookMVA( "BDT" , weightfiles["43"] )

    def evaluesBDT(self,inputdict, NJets, NBTags):

        self.variables["Evt_blr_ETH_transformed"][0] = inputdict["Evt_blr_ETH_transformed"]
        self.variables["Evt_Deta_JetsAverage"][0] = inputdict["Evt_Deta_JetsAverage"]
        self.variables["avg_dr_tagged_jets"][0] = inputdict["avg_dr_tagged_jets"]
        self.variables["tagged_dijet_mass_closest_to_125"][0] = inputdict["tagged_dijet_mass_closest_to_125"]
        self.variables["closest_tagged_dijet_mass"][0] = inputdict["closest_tagged_dijet_mass"]
        self.variables["fifth_highest_CSV"][0] = inputdict["fifth_highest_CSV"]
        self.variables["best_higgs_mass"][0] = inputdict["best_higgs_mass"]
        self.variables["sphericity"][0] = inputdict["sphericity"]
        self.variables["M3"][0] = inputdict["M3"]
        self.variables["all_sum_pt_with_met"][0] = inputdict["all_sum_pt_with_met"]
        self.variables["avg_btag_disc_btags"][0] = inputdict["avg_btag_disc_btags"]
        self.variables["dEta_fn"][0] = inputdict["dEta_fn"]
        self.variables["aplanarity"][0] = inputdict["aplanarity"]
        self.variables["dev_from_avg_disc_btags"][0] = inputdict["dev_from_avg_disc_btags"]
        self.variables["Evt_H0"][0] = inputdict["Evt_H0"]
        self.variables["Mlb"][0] = inputdict["Mlb"]
        self.variables["min_dr_tagged_jets"][0] = inputdict["min_dr_tagged_jets"]
        self.variables["MinDeltaRLeptonJet"][0] = inputdict["MinDeltaRLeptonJet"]
        self.variables["HT"][0] = inputdict["HT"]
        self.variables["Evt_M_MinDeltaRUntaggedJets"][0] = inputdict["Evt_M_MinDeltaRUntaggedJets"]
        self.variables["Evt_Dr_MinDeltaRJets"][0] = inputdict["Evt_Dr_MinDeltaRJets"]
        self.variables["Evt_TaggedJet_MaxDeta_Jets"][0] = inputdict["Evt_TaggedJet_MaxDeta_Jets"]
        self.variables["Evt_M_Total"][0] = inputdict["Evt_M_Total"]
        self.variables["h3"][0] = inputdict["h3"]
        self.variables["fourth_jet_pt"][0] = inputdict["fourth_jet_pt"]
        self.variables["pt_all_jets_over_E_all_jets"][0] = inputdict["pt_all_jets_over_E_all_jets"]
        self.variables["Evt_CSV_Average"][0] = inputdict["Evt_CSV_Average"]
        self.variables["fourth_highest_btag"][0] = inputdict["fourth_highest_btag"]
        self.variables["h1"][0] = inputdict["h1"]
        self.variables["invariant_mass_of_everything"][0] = inputdict["invariant_mass_of_everything"]
        self.variables["fifth_highest_CSV"][0] = inputdict["fifth_highest_CSV"]
        self.variables["h2"][0] = inputdict["h2"]
        self.variables["dr_between_lep_and_closest_jet"][0] = inputdict["dr_between_lep_and_closest_jet"]
        self.variables["second_jet_pt"][0] = inputdict["second_jet_pt"]

        BDTtoEval = None
        
        if (NJets >= 6 and NBTags >= 4):
            BDTtoEval = "6J4T" 
        elif (NJets >= 6 and NBTags == 3):
            BDTtoEval = "6J3T" 
        elif (NJets >= 6 and NBTags == 2):
            BDTtoEval = "6J2T" 
        elif (NJets == 5 and NBTags >= 4):
            BDTtoEval = "5J4T" 
        elif (NJets == 5 and NBTags == 3):
            BDTtoEval = "5J3T" 
        elif (NJets == 4 and NBTags >= 4):
            BDTtoEval = "4J4T" 
        elif (NJets == 4 and NBTags == 3):
            BDTtoEval = "4J3T" 

        if BDTtoEval is not None:
            return self.classifier[BDTtoEval].EvaluateMVA("BDT")
        else:
            return -1


"""
inputdict["Evt_blr_ETH_transformed"]
inputdict["Evt_Deta_JetsAverage"]
inputdict["avg_dr_tagged_jets"]
inputdict["tagged_dijet_mass_closest_to_125"]
inputdict["closest_tagged_dijet_mass"]
inputdict["fifth_highest_CSV"]
inputdict["best_higgs_mass"]
inputdict["sphericity"]
inputdict["M3"]
inputdict["all_sum_pt_with_met"]
inputdict["avg_btag_disc_btags"]
inputdict["dEta_fn"]
inputdict["aplanarity"]
inputdict["dev_from_avg_disc_btags"]
inputdict["Evt_H0"]
inputdict["Mlb"]
inputdict["min_dr_tagged_jets"]
inputdict["MinDeltaRLeptonJet"]
inputdict["HT"]
inputdict["Evt_M_MinDeltaRUntaggedJets"]
inputdict["Evt_Dr_MinDeltaRJets"]
inputdict["Evt_TaggedJet_MaxDeta_Jets"]
inputdict["Evt_M_Total"]
inputdict["h3"]
inputdict["fourth_jet_pt"]
inputdict["pt_all_jets_over_E_all_jets"]
inputdict["h1"]
inputdict["Evt_CSV_Average"]
inputdict["fourth_highest_btag"]
inputdict["invariant_mass_of_everything"]
inputdict["fifth_highest_CSV"]
inputdict["h2"]
inputdict["dr_between_lep_and_closest_jet"]
inputdict["second_jet_pt"]
"""
