
#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
from glob import glob
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from plotting import *
from rootutils import PDFPrinting

sys.path.append("/nfs/dust/cms/user/kschweig/pyroot-plotscripts")
from plotutils import getSepaTests3, getROClist
#-------------------------------------------------------------------------------------#
#
#ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);
#
#-------------------------------------------------------------------------------------#
# Set Variables

path = "/nfs/dust/cms/user/kschweig/JetRegression/trees0701/"

inputtree_sig = ROOT.TChain("MVATree")
inputtree_bkg = ROOT.TChain("MVATree")

for f in glob(path+"ttHbb/*.root"):
    inputtree_sig.Add(f)
for f in glob(path+"ttbar_incl/*.root"):
    inputtree_bkg.Add(f)

#outputname = "ttHbb_commonbdt5_comp"
outputname = "commonbdt5_0701_ouput_comp"

Evt = "Evt_Odd == 0"
weight = "(Weight * Weight_PU * Weight_LeptonSF)"
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



categorieslegend=["6j4t",
                  "6j2t",
                  "4j3t",
                  "5j3t",
                  "6j3t",
                  "4j4t",
                  "5j4t",             
                  ]
                  #"boosted"]

binning = { 'Evt_CSV_Average':[17,0.3,1],
            'Evt_Deta_JetsAverage':[20,0,4],
            'HT':[20,0,1000],
            'M3':[30,0,600],
            'MET':[50,0,200],
            'MHT':[15,0,250],
            'Mlb':[15,0,250],
            'all_sum_pt_with_met':[10,0,1000],
            'aplanarity':[20,0,0.4],
            'avg_btag_disc_btags':[30,0.8,1.05],
            'avg_dr_tagged_jets':[ 10,1.6,3.6],
            'best_higgs_mass': [30,0,600 ],
            'closest_tagged_dijet_mass':[ 50,0,250],
            'dEta_fn':[ 20,0,5],
            'dev_from_avg_disc_btags':[ 25,0,0.008],
            'dr_between_lep_and_closest_jet':[25,0,4],
            'fifth_highest_CSV':[20,-2,2],
            'first_jet_pt':[ 15,0,400],
            'fourth_highest_btag':[ 22,-.1,1],
            'fourth_jet_pt':[32,0,160],
            'h0':[ 15,0.2,0.4],
            'h1':[27,-.2,.34],
            'h2':[15,-0.2,0.4],
            'h3':[15,-0.2,1.0],
            'invariant_mass_of_everything':[15,0,1500],
            'lowest_btag':[ 10,0,1],
            'maxeta_jet_jet':[ 50 , -2.4, 2.4],
            'maxeta_jet_tag':[ 25,0.2,1.6],
            'maxeta_tag_tag':[ 25,0,1.5],
            'min_dr_tagged_jets':[12,0,2.4],
            'pt_all_jets_over_E_all_jets':[10,0.2,1.2],
            'second_highest_btag':[11,0.8,1],
            'second_jet_pt':[ 40,0,300],
            'sphericity':[20,0,1],
            'tagged_dijet_mass_closest_to_125':[ 30,80,180],
            'third_highest_btag':[ 10,0,1],
            'third_jet_pt': [40,0,400]}



#
#
#-------------------------------------------------------------------------------------#

tree = inputtree_sig

common5_input = []
reg_common5_input = []

for branch in tree.GetListOfBranches():
    if branch.GetName().startswith("BDT_common5_input_"):
        common5_input.append(branch.GetName())
    if branch.GetName().startswith("BDT_reg_common5_input_"):
        reg_common5_input.append(branch.GetName())

#print common5_input
#print reg_common5_input

noreg_plots = {}
reg_plots = {}

if False:
    for var in common5_input:
        var = var[len("BDT_common5_input_"):]
        noreg_plots.update(  {  var : normPlots(  var , True , len(categorieslegend) , categorieslegend , binning[var]  )  }  )
        reg_plots.update(  {  var : normPlots(  var , True , len(categorieslegend) , categorieslegend , binning[var]  )  }  )
    noreg_output = normPlots(  "BDT Output" , True , len(categorieslegend) , categorieslegend , [10,-1,1]  )
    reg_output = normPlots(  "BDT Output" , True , len(categorieslegend) , categorieslegend , [10,-1,1]  )

    noreg_ROC = normPlots(  "ROC Curve" , True , len(categorieslegend) , categorieslegend , [20,0,1]  )
    reg_ROC = normPlots(  "ROC Curve" , True , len(categorieslegend) , categorieslegend , [20,0,1]  )

    

    for icat, cat in enumerate(categoriesSELECTION):
        for variable in common5_input:
            var = variable[len("BDT_common5_input_"):]
            noreg_plots[var].projecttoHisto(icat, tree, variable, cat)
        for variable in reg_common5_input:
            var = variable[len("BDT_reg_common5_input_"):]
            reg_plots[var].projecttoHisto(icat, tree, variable, cat)
        noreg_output.projecttoHisto(icat, tree, "BDT_common5_output", cat)
        reg_output.projecttoHisto(icat, tree, "BDT_reg_common5_output", cat)



    c1 = ROOT.TCanvas()
    outputfile = ROOT.TFile(outputname+"_cat.root","RECREATE")
    outputfile.cd()

    pdfout = PDFPrinting(outputname+"_cat")

    for key in noreg_plots:
        print key
        noreg_plots[key].addLabel(0.04,0.03,"no Regression",0,0.035)
        reg_plots[key].addLabel(0.04,0.03,"Regression",0,0.035)
        noreg_plots[key].WriteHisto(c1, "ttHbb", False, False, pdfout)
        reg_plots[key].WriteHisto(c1, "ttHbb", False, False, pdfout)

    noreg_output.addLabel(0.04,0.03,"no Regression",0,0.035)
    reg_output.addLabel(0.04,0.03,"Regression",0,0.035)
    noreg_output.WriteHisto(c1, "ttHbb", False, False, pdfout)
    reg_output.WriteHisto(c1, "ttHbb", False, False, pdfout)

    pdfout.closePDF()


    del c1, outputfile, pdfout

if False:
    c1 = ROOT.TCanvas()
    outputfile = ROOT.TFile(outputname+"_noregVreg.root","RECREATE")
    outputfile.cd()

    pdfout = PDFPrinting(outputname+"_noregVreg")

    for icat, cat in enumerate(categoriesSELECTION):
        plots = {}

        for var in common5_input:
            var = var[len("BDT_common5_input_"):]
            plots.update(  {  var : normPlots(  var , True , 2,  ["No Regression", "Regression"] , binning[var]  )  }  )
        output = normPlots(  "BDT Output" , True , 2 , ["No Regression", "Regression"] , [10,-1,1]  )

        for variable in common5_input:
            var = variable[len("BDT_common5_input_"):]
            var_reg = "BDT_reg_common5_input_"+variable[len("BDT_common5_input_"):]

            plots[var].projecttoHisto(0, tree, variable, cat)
            plots[var].projecttoHisto(1, tree, var_reg, cat)

            print variable
            plots[var].addLabel(0.04,0.03,categorieslegend[icat],0,0.035)
            plots[var].WriteHisto(c1, "ttHbb", False, False, pdfout)


        output.projecttoHisto(0, tree,"BDT_common5_output" , cat)
        output.projecttoHisto(1, tree,"BDT_reg_common5_output" , cat)

        output.addLabel(0.04,0.03,categorieslegend[icat],0,0.035)
        output.WriteHisto(c1, "ttHbb", False, False, pdfout)

    pdfout.closePDF()

    del c1, outputfile, pdfout


if True:
    c1 = ROOT.TCanvas()



    tree_bkg = inputtree_bkg

    names = ["_genJet"]


    for name in names:


        outputfile = ROOT.TFile(outputname+"_noregVreg"+name+".root","RECREATE")
        outputfile.cd()
        
        pdfout = PDFPrinting(outputname+"_noregVreg"+name)

        
        for icat, cat in enumerate(categoriesSELECTION):
            plots = {}

            legend_all = ["No Regression t#bar{t}", "No Regression t#bar{t}H,  H #rightarrow b#bar{b}","Regression t#bar{t}", "Regression t#bar{t}H,  H #rightarrow b#bar{b}"]

            for var in common5_input:
                var = var[len("BDT_common5_input_"):]
                plots.update(  {  var : normPlots(  var , True , 4,  legend_all , binning[var]  )  }  )

            output = normPlots(  "BDT Output" , True , 4 , legend_all , [10,-1,1]  )

            ROC = normPlots( "ROC Curve" , True , 2, ["No Regression","Regression"], [10,0,1] )

            for variable in common5_input:

                var = variable[len("BDT_common5_input_"):]
                var_reg = "BDT_reg"+name+"_common5_input_"+variable[len("BDT_common5_input_"):]

                #liste =  ["all_sum_pt_with_met","sphericity","invariant_mass_of_everything", "closest_tagged_dijet_mass","best_higgs_mass","M3","first_jet_pt","second_jet_pt","third_jet_pt"]
                liste =  ["closest_tagged_dijet_mass","best_higgs_mass",'tagged_dijet_mass_closest_to_125']
                #liste =  []


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

        pdfout.closePDF()
        
        del outputfile, pdfout

    del c1
