#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
from array import array
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from plotting import *
from rootutils import PDFPrinting
#-------------------------------------------------------------------------------------#
#

#
#-------------------------------------------------------------------------------------#
# Set Variables

path1 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0317_testing/output/"
path3 = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/"
path4 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0318_testing/output/"


compdic = { "Target Comparison" : [path1+"script_1200_0.1_5_30.root", path3+"BReg_0323_ratiotest_Jet_D_Parton_1200_0.1_5_30.root",path4+"script_1200_0.1_4_20.root"] }
targetdic = { path1+"script_1200_0.1_5_30.root" : ["BDTG" , "BDTG / Jet_Pt", "BDTG / Jet_PartonPt", "Jet_Pt / BDTG"],
              path3+"BReg_0323_ratiotest_Jet_D_Parton_1200_0.1_5_30.root" : ["(1/BDTG) * Jet_Pt", "1/BDTG"  , "((1/BDTG) * Jet_Pt) / ((1/Jet_Pt_D_Jet_PartonPt) * Jet_Pt) ", "BDTG"],
              path4+"script_1200_0.1_4_20.root" : ["BDTG*Jet_Pt", "BDTG","((BDTG) * Jet_Pt) / ((Jet_PartonPt_D_Jet_Pt) * Jet_Pt) ", "1/BDTG" ] } 

#print inputfiles

usetesttree = True #if False use train tree
 
outputfolder = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/output_5/" #has to be created first
outputname = "outname_targetcomp_norm"

targetname = "Jet_PartonPt" #name of Regression target
th1param1 = [200,0,600]
th1param2 = [96,0.4,1.6]
th1param3 = [60,0,2.5]


ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)
#-------------------------------------------------------------------------------------#
#

compplots = []

for comp in compdic:
    print "Processing", comp

    filenames = compdic[comp]
    names = map(lambda x : x.split("/")[-1][:-5], filenames)



    #Initialize Plotting
    legend = ["Unregressed","Target: p_{T} of matched Parton","Target: p_{T} of matched Parton / Jet p_{T}","Target: Jet p_{T} / p_{T} of matched Parton"]
    targetvsBDTGH = normPlots("Jet_regPt", True, len(legend), legend)
    targetvsBDTGregcorrH = normPlots("Matched Parton p_{T} / Jet p_{T}", True, len(legend), legend,th1param2)
    targetvsBDTGPTJetPartonH = normPlots("Jet_Pt_D_Jet_PartonPt",True,len(legend), legend)    
    targetvsBDTGPTJetPartonH_ = normPlots("Jet_Pt_D_Jet_PartonPt",True,len(legend), legend)    

    targetvsBDTGH.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])
    targetvsBDTGregcorrH.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])
    targetvsBDTGPTJetPartonH.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])
    targetvsBDTGPTJetPartonH_.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])

    targetvsBDTGH.setmanualegendsize("right",0.6,0.65,0.88,0.83)
    targetvsBDTGregcorrH.setmanualegendsize("right",0.6,0.65,0.68,0.83)
    targetvsBDTGPTJetPartonH.setmanualegendsize("right",0.6,0.65,0.88,0.83)
    targetvsBDTGPTJetPartonH_.setmanualegendsize("right",0.6,0.65,0.88,0.83)
    #targetvsBDTGH.setmanualegendsize("left",0.13,0.65,0.41,0.83)
    #targetvsBDTGregcorrH.setmanualegendsize("left",0.13,0.65,0.41,0.83)
    #targetvsBDTGPTJetPartonH.setmanualegendsize("left",0.13,0.65,0.41,0.83)
    
    targetvsBDTGH.addLabel(0.04,0.03,comp,0,0.035)
    targetvsBDTGregcorrH.addLabel(0.04,0.03,comp,0,0.035)
    targetvsBDTGPTJetPartonH.addLabel(0.04,0.03,comp,0,0.035)
    targetvsBDTGPTJetPartonH_.addLabel(0.04,0.03,comp,0,0.035)



    targetadded = False
    nhisto = 1

    targetvsBDTGHnames = []
    targetvsBDTGregcorrHnames = [] 
    targetvsBDTGPTJetPartonHnames = []
    for histo in targetvsBDTGH.getHistos():
        targetvsBDTGHnames.append(histo.GetName())
    for histo in targetvsBDTGregcorrH.getHistos():
        targetvsBDTGregcorrHnames.append(histo.GetName())
    for histo in targetvsBDTGPTJetPartonH.getHistos():
        targetvsBDTGPTJetPartonHnames.append(histo.GetName())



    for ifile, filename in enumerate(filenames):
        inputfile = ROOT.TFile(filename)
        for key in inputfile.GetListOfKeys():
            if key.GetName() == "TestTree":
                testtreekey = key
            if key.GetName() == "TrainTree":
                traintreekey = key

        if usetesttree:
            tree = inputfile.Get(testtreekey.GetName())
        else:
            tree = inputfile.Get(traintreekey.GetName())
            


            
        if not targetadded:
            targetvsBDTGH.projecttoHisto(0, tree,targetname, "", "")
            targetvsBDTGregcorrH.projecttoHisto(0, tree,targetname+"/ Jet_Pt","","")
            targetvsBDTGPTJetPartonH.projecttoHisto(0, tree," Jet_Pt / "+targetname,"","")
            targetvsBDTGPTJetPartonH_.projecttoHisto(0, tree," Jet_Pt / "+targetname,"","")
            targetadded = True
            
        targetvsBDTGH.projecttoHisto(nhisto, tree ,targetdic[filename][0],"","")
        targetvsBDTGregcorrH.projecttoHisto(nhisto, tree ,targetdic[filename][1],"","")
        targetvsBDTGPTJetPartonH.projecttoHisto(nhisto, tree ,targetdic[filename][2],"","")
        targetvsBDTGPTJetPartonH_.projecttoHisto(nhisto, tree ,targetdic[filename][3],"","")
        

        nhisto += 1

    compplots.append([deepcopy(targetvsBDTGH),deepcopy(targetvsBDTGregcorrH),deepcopy(targetvsBDTGPTJetPartonH),deepcopy(targetvsBDTGPTJetPartonH_)])
    

    
    del targetvsBDTGH
    del targetvsBDTGregcorrH
    del targetvsBDTGPTJetPartonH
    del inputfile, tree
    del targetvsBDTGHnames
    del targetvsBDTGregcorrHnames, targetvsBDTGPTJetPartonHnames,filenames,names
    
    #raw_input("Press ret")



"""
pdfout = PDFPrinting("outname_configcomp")
outputfile = ROOT.TFile("outname_configcomp"+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()    

for plots in compplots:
    for plot in plots:
        plot.WriteHisto(c1,"ttbar",False,False,pdfout)

pdfout.closePDF()
"""

pdfout_norm = PDFPrinting(outputname)
outputfile_norm = ROOT.TFile(outputname+".root","RECREATE")
outputfile_norm.cd()
c1_norm = ROOT.TCanvas()    

for plots in compplots:
    for plot in plots:
        plot.WriteHisto(c1_norm,"ttbar",False,True,pdfout_norm)
    
pdfout_norm.closePDF()
