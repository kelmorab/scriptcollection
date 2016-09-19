
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
from plotting import *
from rootutils import PDFPrinting

sys.path.append("/nfs/dust/cms/user/kschweig/pyroot-plotscripts")
from plotutils import  getSepaTests2TextOnly

from evalBDT import *
#-------------------------------------------------------------------------------------#
#
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);
#
#-------------------------------------------------------------------------------------#
# Set Variables

path = "/nfs/dust/cms/user/kschweig/JetRegression/trees0908/BDTTraining/TreeswBDT0908output/"

inputtree_sig = ROOT.TChain("MVATree")
inputtree_bkg = ROOT.TChain("MVATree")

print "Adding inputfiles to signal chain"
for f in glob(path+"ttHbb*.root"):
    print "    Adding",f
    inputtree_sig.Add(f)
print "Adding inputfiles to background chain"
for f in glob(path+"ttbar*.root"):
    print "    Adding",f
    inputtree_bkg.Add(f)

#outputname = "ttHbb_commonbdt5_comp"
outputname = "BDT80xblrV1_comp_MA"
name = "0917"
Evt = "Evt_Odd == 0"
#weight = "(Weight_ElectronSFID*Weight_MuonSFID*Weight_MuonSFIso*Weight_ElectronSFGFS*Weight_MuonSFHIP*Weight_pu69p2*Weight_CSV)"
weight = "1"
#boosted="(BoostedTopHiggs_TopHadCandidate_TopMVAOutput>=-0.485&&BoostedTopHiggs_HiggsCandidate_HiggsTag>=0.8925)"                        
boosted= "0"
categoriesSELECTION=[Evt+"&&"+weight+"*((N_Jets>=6&&N_BTagsM>=4)&&!"+boosted+")",
                     Evt+"&&"+weight+"*((N_Jets>=6&&N_BTagsM==2)&&!"+boosted+")",
                     Evt+"&&"+weight+"*((N_Jets==4&&N_BTagsM==3)&&!"+boosted+")",
                     Evt+"&&"+weight+"*((N_Jets==5&&N_BTagsM==3)&&!"+boosted+")",
                     Evt+"&&"+weight+"*((N_Jets>=6&&N_BTagsM==3)&&!"+boosted+")",
                     Evt+"&&"+weight+"*((N_Jets==4&&N_BTagsM>=4)&&!"+boosted+")",
                     Evt+"&&"+weight+"*((N_Jets==5&&N_BTagsM>=4)&&!"+boosted+")",             
                     ]
                     #Evt+"&&"+weight+"*((N_Jets>=4&&N_BTagsM>=2)&&"+boosted+")"]



categorieslegend=["N_{Jets} #geq 6, N_{bTags} #geq 4",
                  "N_{Jets} #geq 6, N_{bTags} = 2",
                  "N_{Jets} = 4, N_{bTags} = 3",
                  "N_{Jets} = 5, N_{bTags} = 3",
                  "N_{Jets} #geq 6, N_{bTags} = 3",
                  "N_{Jets} = 4, N_{bTags} #geq 4",
                  "N_{Jets} = 5, N_{bTags} #geq 4",             
                  ]
                  #"boosted"]

binning = { "blr_ETH_transformed":[30,0,12],
            "Deta_JetsAverage":[20,0,4],
            "avg_dr_tagged_jets":[ 10,1.6,3.6],
            "tagged_dijet_mass_closest_to_125":[ 30,80,180],
            "closest_tagged_dijet_mass":[ 50,0,250],
            "fifth_highest_CSV":[20,-2,2],
            "best_higgs_mass": [30,0,600 ],
            "sphericity":[20,0,1],
            "M3":[30,0,600],
            "all_sum_pt_with_met":[10,0,1000],
            "avg_btag_disc_btags":[30,0.8,1.05],
            "dEta_fn":[ 20,0,5],
            "aplanarity":[20,0,0.4],
            "dev_from_avg_disc_btags":[ 25,0,0.008],
            "H0":[ 15,0.2,0.4],
            "Mlb":[15,0,250],
            "min_dr_tagged_jets":[12,0,2.4],
            "Dr_MinDeltaRLeptonJet":[60,0.4,3.4],
            "HT":[20,0,1000],
            "M_MinDeltaRUntaggedJets":[45,0.,450],
            "Dr_MinDeltaRJets":[50,0.,5.0],
            "TaggedJet_MaxDeta_Jets":[50,0.,5.0],
            "M_Total":[50,0.,2500],
            "h3":[15,-0.2,1.0],
            "fourth_jet_pt":[32,0,160],
            "pt_all_jets_over_E_all_jets":[10,0.2,1.2],
            "h1":[27,-.2,.34],
            "CSV_Average":[17,0.3,1],
            "fourth_highest_btag":[ 22,-.1,1],
            "invariant_mass_of_everything":[15,0,1500],
            "fifth_highest_CSV":[20,-2,2],
            "h2":[15,-0.2,0.4],
            "dr_between_lep_and_closest_jet":[25,0,4],
            "second_jet_pt":[ 40,0,300]
        }


#
#
#-------------------------------------------------------------------------------------#




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

plotnames = {}

plotnames["BDT_common5_input_avg_dr_tagged_jets"] = "Avg. #Delta R [tag,tag]"
plotnames["BDT_common5_input_tagged_dijet_mass_closest_to_125"] = "Tagged dijet mass closests to 125 GeV [GeV]"
plotnames["BDT_common5_input_closest_tagged_dijet_mass"] = "Closest tagged dijet mass [GeV]"
plotnames["BDT_common5_input_fifth_highest_CSV"] = "Fitht highes CSV"
plotnames["BDT_common5_input_best_higgs_mass"] = "Best Higgs mass [GeV]"
plotnames["BDT_common5_input_sphericity"] = "Spericity"
plotnames["BDT_common5_input_M3"] = "M3 [GeV]"
plotnames["BDT_common5_input_all_sum_pt_with_met"] = "sum of p_{T} [lepton,jet,met] [GeV]"
plotnames["BDT_common5_input_avg_btag_disc_btags"] = "Avg. CSV [tags]"
plotnames["BDT_common5_input_dEta_fn"] = "#sqrt{#Delta #eta (t^{lep}, bb) #times #Delta #eta(t^{had}, bb)}"
plotnames["BDT_common5_input_aplanarity"] = "Aplanarity"
plotnames["BDT_common5_input_dev_from_avg_disc_btags"] = "Dev. from avg CSV [tags]"
plotnames["BDT_common5_input_Mlb"] = "Mass [lepton,closest tagged jet] [GeV]"
plotnames["BDT_common5_input_min_dr_tagged_jets"] = "Min. #Delta R tagged jets"
plotnames["BDT_common5_input_HT"] = "HT [GeV]"
plotnames["BDT_common5_input_h3"] = "H_{3}"
plotnames["BDT_common5_input_fourth_jet_pt"] = "p_{T} of fouth jet [GeV]"
plotnames["BDT_common5_input_pt_all_jets_over_E_all_jets"] = "(sum of jet p_{T})/(sum of jet E))"
plotnames["BDT_common5_input_h1"] = "H_{1}"
plotnames["BDT_common5_input_fourth_highest_btag"] = "Fourth highest btag"
plotnames["BDT_common5_input_invariant_mass_of_everything"] = "Mass [jets,lepton,MET] [GeV]"
plotnames["BDT_common5_input_fifth_highest_CSV"] = "Fifth highest CSV"
plotnames["BDT_common5_input_h2"] = "H_{2}"
plotnames["BDT_common5_input_dr_between_lep_and_closest_jet"] = "Min. #Delta R [lepton,jet]"
plotnames["BDT_common5_input_second_jet_pt"] = "p_{T} of second jet [GeV]"
plotnames["Evt_blr_ETH_transformed"] = "B-tagging likelihood ratio"
plotnames["Evt_Deta_JetsAverage"] = "Avg. #Delta #eta (jet,jet)"
plotnames["Evt_H0"] = "H_{0}"
plotnames["Evt_Dr_MinDeltaRLeptonJet"] = "#Delta R of closest [#Delta R] jet-lepton"
plotnames["Evt_M_MinDeltaRUntaggedJets"] = "Mass of closest [#Delta R] untagged jets [GeV]"
plotnames["Evt_Dr_MinDeltaRJets"] = "#Delta R of closest [#Delta R] jets"
plotnames["Evt_TaggedJet_MaxDeta_Jets"] = "max #Delta #eta (tag,tag)"
plotnames["Evt_M_Total"] = "Total mass of event [GeV]"
plotnames["Evt_CSV_Average"] = "Avg CSV of event"


c1 = ROOT.TCanvas()

tree_sig = inputtree_sig
tree_bkg = inputtree_bkg

outputfile = ROOT.TFile(outputname+"_noregVreg"+name+".root","RECREATE")
outputfile.cd()

pdfout = PDFPrinting(outputname+"_noregVreg"+name)


for icat, cat in enumerate(categoriesSELECTION):
    print "Processing category:",categorieslegend[icat],"which is",icat+1,"of",len(categoriesSELECTION)
    plots = {}

    legend_all = ["No Regression t#bar{t}", "No Regression t#bar{t}H,  H #rightarrow b#bar{b}","Regression t#bar{t}", "Regression t#bar{t}H,  H #rightarrow b#bar{b}"]

    #for var in common5_input:
    #    var = var[len("BDT_common5_input_"):]
    #    plots.update(  {  var : normPlots(  var , True , 4,  legend_all , binning[var]  )  }  )
    #for var in evt_vars_noreg:
    #    plots.update(  {  var : normPlots(  var , True , 4,  legend_all , binning[var]  )  }  )


    output = normPlots(  "BDT Output" , True , 4 , legend_all , [10,-1,1]  )

    ROC = normPlots( "ROC Curve" , True , 2, ["No Regression","Regression"], [10,0,1] )
    
 
    # Generate arrays and connect them to branchadresses for all inputvariable for Signal and Background
    for variable in evt_vars_noreg:
        plots.update( { variable : normPlots(   plotnames[variable] , True , 4,  legend_all , binning[ variable[len("Evt_"):] ] )  } )
        plots[variable].changeColorlist([ROOT.kAzure-3,ROOT.kRed,ROOT.kAzure-3,ROOT.kRed])
        plots[variable].setmanualegendsize("right",0.55,0.55,0.88,0.88)
        plots[variable].addLabel(0.04,0.03,categorieslegend[icat],0,0.045)
    for variable in common5_input:
        plots.update( { variable : normPlots(  plotnames[variable] , True , 4,  legend_all , binning[ variable[len("BDT_common5_input_"):] ] ) } )
        plots[variable].changeColorlist([ROOT.kAzure-3,ROOT.kRed,ROOT.kAzure-3,ROOT.kRed])
        plots[variable].setLineStyle([0,1],2)
        plots[variable].setmanualegendsize("right",0.55,0.55,0.88,0.88)
        plots[variable].addLabel(0.04,0.03,categorieslegend[icat],0,0.045)

        

    #print arrays_sig.keys()
    #print arrays_bkg.keys()

    excllist = ["Evt_Deta_JetsAverage","Evt_TaggedJet_MaxDeta_Jets","Evt_CSV_Average"]
    
    for variable in common5_input:
        plots[variable].projecttoHisto(1, tree_sig, variable, cat)
        plots[variable].projecttoHisto(3, tree_sig, "BDT_Reg_common5_input_"+variable[len("BDT_common5_input_"):], cat)
        plots[variable].projecttoHisto(0, tree_bkg, variable, cat)
        plots[variable].projecttoHisto(2, tree_bkg, "BDT_Reg_common5_input_"+variable[len("BDT_common5_input_"):], cat)
        plots[variable].setLineStyle([0,1],2)
    for variable in evt_vars_noreg:
        plots[variable].projecttoHisto(1, tree_sig, variable, cat)
        plots[variable].projecttoHisto(0, tree_bkg, variable, cat)
        if variable in excllist:
            plots[variable].projecttoHisto(3, tree_sig, variable, cat)
            plots[variable].projecttoHisto(2, tree_bkg, variable, cat)
        else:
            plots[variable].projecttoHisto(3, tree_sig, "Evt_Reg_"+variable[len("Evt_"):], cat)
            plots[variable].projecttoHisto(2, tree_bkg, "Evt_Reg_"+variable[len("Evt_"):], cat)
        plots[variable].setLineStyle([0,1],2)

    for variable in common5_input + evt_vars_noreg:
        histos = plots[variable].getHistos()
        
        noreg_text = getSepaTests2TextOnly([histos[0]],histos[1])[0]
        reg_text = getSepaTests2TextOnly([histos[2]],histos[3])[0]
        
        plots[variable].addLabel(0.13,0.8, "No Regression: "+noreg_text,0,0.04)
        plots[variable].addLabel(0.13,0.75, "Regression: "+reg_text,0,0.04)
        print variable
        plots[variable].WriteHisto(c1, None, False, True, pdfout,False,None,False,False,0.3)
        
    output.projecttoHisto(0, tree_bkg,"BDTOutput_noreg" , cat)
    output.projecttoHisto(1, tree_sig,"BDTOutput_noreg" , cat)
    output.projecttoHisto(2, tree_bkg,"BDTOutput_reg" , cat)
    output.projecttoHisto(3, tree_sig,"BDTOutput_reg" , cat)
        
    output.changeColorlist([ROOT.kAzure-3,ROOT.kRed,ROOT.kAzure-3,ROOT.kRed])
    output.setLineStyle([0,1],2)

    histos = output.getHistos()
    
    noreg_text = getSepaTests2TextOnly([histos[0]],histos[1])[0]
    reg_text = getSepaTests2TextOnly([histos[2]],histos[3])[0]
        
    output.addLabel(0.13,0.8, "No Regression: "+noreg_text,0,0.04)
    output.addLabel(0.13,0.75, "Regression: "+reg_text,0,0.04)
    output.setmanualegendsize("right",0.50,0.60,0.88,0.88)
    output.addLabel(0.04,0.03,categorieslegend[icat],0,0.045)
    output.WriteHisto(c1,None, False, True, pdfout,False,None,False,False,0.525)

    ROC.converttoROC(0,tree_sig, tree_bkg, "BDTOutput_noreg","BDTOutput_noreg", cat, cat, [1000,-1,1])
    ROC.converttoROC(1,tree_sig, tree_bkg, "BDTOutput_reg","BDTOutput_reg", cat, cat, [1000,-1,1])
    
    ROC.changeColorlist([ROOT.kAzure-3,ROOT.kRed])
    
    ROC.addLabel(0.04,0.03,categorieslegend[icat],0,0.045)
    ROC.WriteHisto(c1 ,None, False, False, pdfout)

    del output, ROC, plots

    """
    for variable in common5_input:

        var = variable[len("BDT_common5_input_"):]
        var_reg = "BDT_reg"+name+"_common5_input_"+variable[len("BDT_common5_input_"):]

        #liste =  ["all_sum_pt_with_met","sphericity","invariant_mass_of_everything", "closest_tagged_dijet_mass","best_higgs_mass","M3","first_jet_pt","second_jet_pt","third_jet_pt"]
        #liste =  ["closest_tagged_dijet_mass","best_higgs_mass",'tagged_dijet_mass_closest_to_125']
        liste =  []


        #print var in liste
        if var in liste or len(liste) is 0:
            print "Processing: ",var

            plots[var].projecttoHisto(0, tree_bkg, variable, cat)
            plots[var].projecttoHisto(1, tree, variable, cat)
            plots[var].projecttoHisto(2, tree_bkg, var_reg, cat)
            plots[var].projecttoHisto(3, tree, var_reg, cat)

            histos = plots[var].getHistos()

            noreg_text = getSepaTests3([histos[0]],histos[1])[0]
            reg_text = getSepaTests3([histos[2]],histos[3])[0]

            print variable

            plots[var].addLabel(0.13,0.8, "No Regression: "+noreg_text,0,0.04)
            plots[var].addLabel(0.13,0.75, "Regression: "+reg_text,0,0.04)

            plots[var].changeColorlist([ROOT.kAzure-3,ROOT.kRed,ROOT.kAzure-3,ROOT.kRed])

            plots[var].addLabel(0.04,0.03,categorieslegend[icat],0,0.045)

            plots[var].setLineStyle([0,1],2)


            if var != "dr_between_lep_and_closest_jet":
                pass

            else:
                print "hallo"
            plots[var].WriteHisto(c1, None, False, True, pdfout,False,None,False,False,0.3)

            del histos 

    output.projecttoHisto(0, tree_bkg,"BDT_common5_output" , cat)
    output.projecttoHisto(1, tree,"BDT_common5_output" , cat)
    output.projecttoHisto(2, tree_bkg,"BDT_reg"+name+"_common5_output" , cat)
    output.projecttoHisto(3, tree,"BDT_reg"+name+"_common5_output" , cat)

    histos = output.getHistos()


    noreg_text = getSepaTests3([histos[0]],histos[1])[0]
    reg_text = getSepaTests3([histos[2]],histos[3])[0]

    #noreg_roc = getROClist(histos[1],histos[0])
    #reg_roc = getROClist(histos[3],histos[2])

    #rocnoreg = ROOT.TH1F("rocnoreg","rocnoreg",20,0,1)
    #rocreg = ROOT.TH1F("rocreg","rocreg",20,0,1)

    #print len(noreg_roc)
    #print len(reg_roc)


    ROC.converttoROC(0,tree, tree_bkg, "BDT_common5_output","BDT_common5_output", cat, cat, [1000,-1,1])
    ROC.converttoROC(1,tree, tree_bkg, "BDT_reg"+name+"_common5_output","BDT_reg"+name+"_common5_output", cat, cat, [1000,-1,1])

    ROC.changeColorlist([ROOT.kAzure-3,ROOT.kRed])

    ROC.addLabel(0.04,0.03,categorieslegend[icat],0,0.045)
    ROC.WriteHisto(c1 ,None, False, False, pdfout)


    output.addLabel(0.13,0.8, "No Regression: "+noreg_text,0,0.04)
    output.addLabel(0.13,0.75, "Regression: "+reg_text,0,0.04)

    output.changeColorlist([ROOT.kAzure-3,ROOT.kRed,ROOT.kAzure-3,ROOT.kRed])
    output.setLineStyle([0,1],2)

    output.addLabel(0.04,0.03,categorieslegend[icat],0,0.045)
    output.WriteHisto(c1,None, False, True, pdfout,False,None,False,False,0.35)

    del output, ROC, histos

"""

pdfout.closePDF()

del outputfile, pdfout

del c1

