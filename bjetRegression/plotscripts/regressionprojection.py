#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
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
path2 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0322_testing/output/"
path3 = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/"
path4 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0318_testing/output/"


compdic = { "nTrees Comparison (Depth: 3)" : [path1+"script_1200_0.1_3_30.root",path1+"script_1600_0.1_3_30.root",path1+"script_600_0.1_3_30.root",path1+"script_200_0.1_3_30.root"],
            "nTrees Comparison (Depth: 5)" : [path1+"script_1200_0.1_5_30.root",path1+"script_1600_0.1_5_30.root",path1+"script_600_0.1_5_30.root",path1+"script_200_0.1_5_30.root"],
            "nCuts Comparison" : [path1+"script_1200_0.1_5_30.root",path1+"script_1200_0.1_5_40.root",path1+"script_1200_0.1_5_50.root"],
            "MaxDepth Comparison with 1200 Trees" : [path1+"script_1200_0.1_2_30.root",path1+"script_1200_0.1_3_30.root",path1+"script_1200_0.1_4_30.root",path1+"script_1200_0.1_5_30.root",path2+"script_1200_0.1_6_30.root",path2+"script_1200_0.1_8_30.root",path2+"script_1200_0.1_10_30.root"],
            "Shrinkage Comparison" : [path2+"script_1200_0.3_6_30.root",path2+"script_1200_0.1_6_30.root",path2+"script_1200_0.12_6_30.root",path2+"script_1200_0.08_6_30.root"],
            "MaxDepth Comparison with 1200 Trees (small)" : [path1+"script_1200_0.1_3_30.root",path1+"script_1200_0.1_5_30.root",path2+"script_1200_0.1_8_30.root",path2+"script_1200_0.1_10_30.root"],
            "MaxDepth Comparison with 200 Trees" : [path1+"script_200_0.1_2_30.root",path1+"script_200_0.1_3_30.root",path1+"script_200_0.1_4_30.root",path1+"script_200_0.1_5_30.root"] }


#print inputfiles

usetesttree = True #if False use train tree
 
outputfolder = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/output_5/" #has to be created first
outputname = "outname_configcomp_norm"

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
    legendtext = []
    for ifile, filename in enumerate(filenames):
        tmplist = names[ifile].split("_") 
        nTrees = tmplist[-4]
        shrink = tmplist[-3]
        maxDepth = tmplist[-2]
        nCuts = tmplist[-1]
        legendtext.append("1: "+nTrees+" | 2: "+shrink+" | 3: "+maxDepth+" | 4: "+nCuts)


    legend = ["p_{T} of matched Parton (Target)"]+legendtext
    targetvsBDTGH = normPlots("BDT Output (GeV)", True, len(legend), legend, th1param1)
    legend = ["p_{T, Parton} (Target) / p_{T}"]+legendtext
    targetvsBDTGregcorrH = normPlots("BDTG Target(Output) / Jet p_{T}", True, len(legend), legend, th1param2)
    legend = ["p_{T} / p_{T, Parton} (Target)"]+legendtext
    targetvsBDTGPTJetPartonH = normPlots("Jet_Pt_D_Jet_PartonPt",True,len(legend), legend)    

    targetvsBDTGH.addLabel(0.925,0.115,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.032)
    targetvsBDTGregcorrH.addLabel(0.925,0.115,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.032)
    targetvsBDTGPTJetPartonH.addLabel(0.925,0.115,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.032)
    
    targetvsBDTGH.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])
    targetvsBDTGregcorrH.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])
    targetvsBDTGPTJetPartonH.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet+6, ROOT.kOrange-3,ROOT.kPink-8,ROOT.kTeal-5])

    targetvsBDTGH.setmanualegendsize("right",0.6,0.65,0.88,0.83)
    targetvsBDTGregcorrH.setmanualegendsize("right",0.6,0.65,0.68,0.83)
    targetvsBDTGPTJetPartonH.setmanualegendsize("right",0.6,0.65,0.88,0.83)
    #targetvsBDTGH.setmanualegendsize("left",0.13,0.65,0.41,0.83)
    #targetvsBDTGregcorrH.setmanualegendsize("left",0.13,0.65,0.41,0.83)
    #targetvsBDTGPTJetPartonH.setmanualegendsize("left",0.13,0.65,0.41,0.83)
    
    targetvsBDTGH.addLabel(0.04,0.03,comp,0,0.035)
    targetvsBDTGregcorrH.addLabel(0.04,0.03,comp,0,0.035)
    targetvsBDTGPTJetPartonH.addLabel(0.04,0.03,comp,0,0.035)



    del ifile, filename
    
    #raw_input("Press ret")
    
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
            targetadded = True
            
        targetvsBDTGH.projecttoHisto(nhisto, tree ,"BDTG","","")
        targetvsBDTGregcorrH.projecttoHisto(nhisto, tree ,"BDTG / Jet_Pt","","")
        targetvsBDTGPTJetPartonH.projecttoHisto(nhisto, tree ,"BDTG /"+targetname,"","")
        
        nhisto += 1

    compplots.append([deepcopy(targetvsBDTGH),deepcopy(targetvsBDTGregcorrH),deepcopy(targetvsBDTGPTJetPartonH)])

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
