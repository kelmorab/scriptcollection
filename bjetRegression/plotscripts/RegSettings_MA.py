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
#-------------------------------------------------------------------------------------#
#

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)

#
#-------------------------------------------------------------------------------------#
# Set Variables
bbMass_param = [40,50,205]

outputname = "RegSettings4MA"

#samplenames  = ["Signal"] # Signal or Background
samplenames  = ["Background","Signal"] # Signal or Background
#sampletype = ["ttHbb"]
sampletype = ["ttbar","ttHbb"]

path_regressedTrees = "/nfs/dust/cms/user/kschweig/JetRegression/trees0908/BDTTraining/TreeswRegression0913output"
path_outputtrees = "/nfs/dust/cms/user/kschweig/Code/stuff"


allsettingpostfixes  = ["Shrinkage01",
                        "Shrinkage03",
                        "Shrinkage0075",
                        "nCuts20",
                        "nCuts10",
                        "nTrees600",
                        "nTrees200",
                        "Depth4",
                        "Depth5",
                        "TMVA"]

TMVAOutput = {  "Shrinkage01" : path_outputtrees+"/training1.root" ,
                "Shrinkage03" : path_outputtrees+"/training2.root",
                "Shrinkage0075" : path_outputtrees+"/training3.root",
                "nCuts20" : path_outputtrees+"/training4.root",
                "nCuts10" : path_outputtrees+"/training5.root",
                "nTrees600" : path_outputtrees+"/training6.root",
                "nTrees200" : path_outputtrees+"/training7.root",
                "Depth4" : path_outputtrees+"/training80.root",
                "Depth5"  : path_outputtrees+"/training9.root" ,
                "TMVA"  : path_outputtrees+"/training10.root"  }

TMVASettings = {  "Shrinkage01" : [1200, 0.1, 3, 30],
                  "Shrinkage03" : [1200, 0.3, 3, 30],
                  "Shrinkage0075" : [1200, 0.075, 3, 30],
                  "nCuts20" : [1200, 0.1, 3, 20],
                  "nCuts10" : [1200, 0.1, 3, 10],
                  "nTrees600" : [600, 0.1, 3, 30],
                  "nTrees200" : [200, 0.1, 3, 30],
                  "Depth4" : [1200, 0.075, 4, 30],
                  "Depth5"  : [1200, 0.075, 5, 30],
                  "TMVA"  : [800, 1, 3, 20] }

#
#-------------------------------------------------------------------------------------#


pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()


for isample,sample in enumerate(sampletype):
    tree = ROOT.TChain("MVATree")
    if samplenames[isample] is "Signal":
        samplesel = ""
        for f in glob(path_regressedTrees+"/ttHbb*.root"):
            print f
            tree.Add(f)
    else:
        print "hallo"
        samplesel = "Evt_Odd == 0 &&"
        for f in glob(path_regressedTrees+"/ttbar*.root"):
            print f
            tree.Add(f)
            
    weightexpression = samplesel+"1"

    ########################################################################################
    ########################################################################################
    # All
    ########################################################################################
    ########################################################################################

    namelist = allsettingpostfixes
    legendtext = []
    for ikey, key in enumerate(namelist):
        legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))




    regoutput = normPlots("Regression output",True,len(legendtext),legendtext,[50,0.6,1.6])
    regpt = normPlots("Jet p_{T, postReg}",True,len(legendtext),legendtext,[80,0,400])

    




    for ikey, key in enumerate(namelist):
        regoutput.projecttoHisto(ikey,tree,"Jet_regoutput_"+key,weightexpression)
        regpt.projecttoHisto(ikey,tree,"Jet_regoutput_"+key+"*Jet_preregPt",weightexpression)

        outputfile.cd()           
        regoutcat = CatPlots("Regression output",[0,50,75,100,150,200,300,600],"Jet_preregPt","Jet p_{T, preReg}",False,False,sample,[50,0.6,1.6])
        regoutcat.addLabel(0.05,0.025,legendtext[ikey],0,0.04)
        regoutcat.projectStacks(tree,"Jet_regoutput_"+key)
        regoutcat.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
        regoutcat.makeStack()
        regoutcat.WriteStack(c1,pdfout)
        regoutcat.WriteNotStacked(c1,pdfout,False)
        #raw_input("")
        del regoutcat

    regoutput.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regpt.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regoutput.WriteHisto(c1,sample,False,True,pdfout)
    regpt.WriteHisto(c1,sample,False,True,pdfout)

    del regpt,regoutput


    ########################################################################################
    ########################################################################################
    # nTrees
    ########################################################################################
    ########################################################################################


    namelist = ["nTrees200","nTrees600","Shrinkage01"]
    legendtext = []
    for ikey, key in enumerate(namelist):
        legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))


    regoutput = normPlots("Regression output",True,len(legendtext),legendtext,[50,0.6,1.6])
    regpt = normPlots("Jet p_{T, postReg}",True,len(legendtext),legendtext,[80,0,400])

    regoutput.changeColorlist([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    regpt.changeColorlist([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])

    bbmass = normPlots("MC Higgs mass /GeV",True,len(legendtext)+1,["No regression"] + legendtext,bbMass_param)
    bbmass.changeColorlist([ROOT.kBlack, ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression)

    for ikey, key in enumerate(namelist):
        regoutput.projecttoHisto(ikey,tree,"Jet_regoutput_"+key,weightexpression)
        regpt.projecttoHisto(ikey,tree,"Jet_regoutput_"+key+"*Jet_preregPt",weightexpression)
        bbmass.projecttoHisto(ikey+1,tree,"Evt_MCHiggsMass_"+key,weightexpression)

    outputfile.cd()           

    regoutput.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regpt.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regoutput.WriteHisto(c1,sample,False,True,pdfout)
    regpt.WriteHisto(c1,sample,False,True,pdfout)
    bbmass.WriteHisto(c1,sample,False,True,pdfout)
    del regpt,regoutput



    ########################################################################################
    ########################################################################################
    # MaxDepth
    ########################################################################################
    ########################################################################################
    namelist = ["Depth5","Depth4","Shrinkage0075"]
    legendtext = []
    for ikey, key in enumerate(namelist):
        legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))


    regoutput = normPlots("Regression output",True,len(legendtext),legendtext,[50,0.6,1.6])
    regpt = normPlots("Jet p_{T, postReg}",True,len(legendtext),legendtext,[80,0,400])

    regoutput.changeColorlist([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    regpt.changeColorlist([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])


    bbmass = normPlots("MC Higgs mass /GeV",True,len(legendtext)+1,["No regression"] + legendtext,bbMass_param)
    bbmass.changeColorlist([ROOT.kBlack, ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression)


    for ikey, key in enumerate(namelist):
        regoutput.projecttoHisto(ikey,tree,"Jet_regoutput_"+key,weightexpression)
        regpt.projecttoHisto(ikey,tree,"Jet_regoutput_"+key+"*Jet_preregPt",weightexpression)
        bbmass.projecttoHisto(ikey+1,tree,"Evt_MCHiggsMass_"+key,weightexpression)

    regoutput.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regpt.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regoutput.WriteHisto(c1,sample,False,True,pdfout)
    regpt.WriteHisto(c1,sample,False,True,pdfout)
    bbmass.WriteHisto(c1,sample,False,True,pdfout)
    del regpt,regoutput


    ########################################################################################
    ########################################################################################
    # nCuts
    ########################################################################################
    ########################################################################################
    namelist = ["nCuts10","nCuts20","Shrinkage01"]
    legendtext = []
    for ikey, key in enumerate(namelist):
        legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))


    regoutput = normPlots("Regression output",True,len(legendtext),legendtext,[50,0.6,1.6])
    regpt = normPlots("Jet p_{T, postReg}",True,len(legendtext),legendtext,[80,0,400])

    regoutput.changeColorlist([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    regpt.changeColorlist([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])


    bbmass = normPlots("MC Higgs mass /GeV",True,len(legendtext)+1,["No regression"] + legendtext,bbMass_param)
    bbmass.changeColorlist([ROOT.kBlack, ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression)


    for ikey, key in enumerate(namelist):
        regoutput.projecttoHisto(ikey,tree,"Jet_regoutput_"+key,weightexpression)
        regpt.projecttoHisto(ikey,tree,"Jet_regoutput_"+key+"*Jet_preregPt",weightexpression)
        bbmass.projecttoHisto(ikey+1,tree,"Evt_MCHiggsMass_"+key,weightexpression)

    outputfile.cd()           
    regoutput.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regpt.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regoutput.WriteHisto(c1,sample,False,True,pdfout)
    regpt.WriteHisto(c1,sample,False,True,pdfout)
    bbmass.WriteHisto(c1,sample,False,True,pdfout)
    del regpt,regoutput


    ########################################################################################
    ########################################################################################
    # TMVA
    ########################################################################################
    ########################################################################################
    namelist = ["TMVA","Shrinkage0075"]
    legendtext = []
    for ikey, key in enumerate(namelist):
        legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))


    regoutput = normPlots("Regression output",True,len(legendtext),legendtext,[50,0.6,1.6])
    regpt = normPlots("Jet p_{T, postReg}",True,len(legendtext),legendtext,[80,0,400])

    regoutput.changeColorlist([ROOT.kGreen-2, ROOT.kRed])
    regpt.changeColorlist([ROOT.kGreen-2, ROOT.kRed])


    bbmass = normPlots("MC Higgs mass /GeV",True,len(legendtext)+1,["No regression"] + legendtext,bbMass_param)
    bbmass.changeColorlist([ROOT.kBlack, ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed])
    bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression)


    for ikey, key in enumerate(namelist):
        regoutput.projecttoHisto(ikey,tree,"Jet_regoutput_"+key,weightexpression)
        regpt.projecttoHisto(ikey,tree,"Jet_regoutput_"+key+"*Jet_preregPt",weightexpression)
        bbmass.projecttoHisto(ikey+1,tree,"Evt_MCHiggsMass_"+key,weightexpression)

    outputfile.cd()           
    regoutput.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regpt.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regoutput.WriteHisto(c1,sample,False,True,pdfout)
    regpt.WriteHisto(c1,sample,False,True,pdfout)
    bbmass.WriteHisto(c1,sample,False,True,pdfout)
    del regpt,regoutput


    ########################################################################################
    ########################################################################################
    # Some plots
    ########################################################################################
    ########################################################################################
    namelist = ["Shrinkage01","Depth5","nCuts20","TMVA"]
    legendtext = []
    for ikey, key in enumerate(namelist):
        legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))


    regoutput = normPlots("Regression output",True,len(legendtext),legendtext,[50,0.6,1.6])
    regpt = normPlots("Jet p_{T, postReg}",True,len(legendtext),legendtext,[80,0,400])

    regoutput.changeColorlist([ROOT.kGreen-2,ROOT.kCyan+1, ROOT.kPink+8, ROOT.kOrange-7])
    regpt.changeColorlist([ROOT.kGreen-2,ROOT.kCyan+1, ROOT.kPink+8, ROOT.kOrange-7])


    bbmass = normPlots("MC Higgs mass /GeV",True,len(legendtext)+1,["No regression"] + legendtext,bbMass_param)
    bbmass.changeColorlist([ROOT.kBlack, ROOT.kGreen-2,ROOT.kCyan+1, ROOT.kPink+8, ROOT.kOrange-7])
    bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression)


    for ikey, key in enumerate(namelist):
        regoutput.projecttoHisto(ikey,tree,"Jet_regoutput_"+key,weightexpression)
        regpt.projecttoHisto(ikey,tree,"Jet_regoutput_"+key+"*Jet_preregPt",weightexpression)
        bbmass.projecttoHisto(ikey+1,tree,"Evt_MCHiggsMass_"+key,weightexpression)

    outputfile.cd()           
    regoutput.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regpt.addLabel(0.93,0.2,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.037)
    regoutput.WriteHisto(c1,sample,False,True,pdfout)
    regpt.WriteHisto(c1,sample,False,True,pdfout)
    bbmass.WriteHisto(c1,sample,False,True,pdfout)
    del regpt,regoutput



    del tree


#Make Shrinkage comparison on test and training sample:
namelist = ["Shrinkage03","Shrinkage01","Shrinkage0075","TMVA"]
shirnkagecomp_testtrain = PointPlot(2*len(namelist),"Error with squared loss function",2*namelist)
legendtext = []
for key in namelist:
    legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))
    inputfile =  ROOT.TFile(TMVAOutput[key])
    testtree = inputfile.Get("TestTree")
    traintree = inputfile.Get("TrainTree")
    shirnkagecomp_testtrain.projectPointfromHMean(traintree,"(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)*(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")
    shirnkagecomp_testtrain.projectPointfromHMean(testtree,"(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)*(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")

outputfile.cd()
shirnkagecomp_testtrain.addLabel(0.42,0.11,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",0,0.037)
shirnkagecomp_testtrain.Legendtext = legendtext #set legend after initializing plot object
shirnkagecomp_testtrain.setGroupOptions([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed, ROOT.kOrange-7],["TrainingSample","TestSample"])
shirnkagecomp_testtrain.WritePointPlot(c1, "ttbar",pdfout,None,"Min",True)

del inputfile, testtree, traintree



#Make aomparison for all test and training sample:
namelist = allsettingpostfixes
shirnkagecomp_testtrain = PointPlot(2*len(namelist),"Error with squared loss function",2*namelist)
legendtext = []
for key in namelist:
    legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))
    inputfile =  ROOT.TFile(TMVAOutput[key])
    testtree = inputfile.Get("TestTree")
    traintree = inputfile.Get("TrainTree")
    shirnkagecomp_testtrain.projectPointfromHMean(traintree,"(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)*(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")
    shirnkagecomp_testtrain.projectPointfromHMean(testtree,"(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)*(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")

outputfile.cd()
shirnkagecomp_testtrain.addLabel(0.42,0.11,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",0,0.037)
shirnkagecomp_testtrain.Legendtext = legendtext #set legend after initializing plot object
shirnkagecomp_testtrain.setGroupOptions([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed, ROOT.kOrange-7,ROOT.kCyan+1, ROOT.kMagenta-4, ROOT.kYellow-3, ROOT.kSpring+8,ROOT.kBlue-2,ROOT.kPink-5],["TrainingSample","TestSample"])
shirnkagecomp_testtrain.WritePointPlot(c1, "ttbar",pdfout,None,"Min",True)

del inputfile, testtree, traintree,shirnkagecomp_testtrain


#Make aomparison for all test and training sample:
namelist = ["Shrinkage03","Shrinkage01","Shrinkage0075","Depth5","nCuts20","TMVA"]
shirnkagecomp_testtrain = PointPlot(2*len(namelist),"Error with squared loss function",2*namelist)
legendtext = []
for key in namelist:
    legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))
    inputfile =  ROOT.TFile(TMVAOutput[key])
    testtree = inputfile.Get("TestTree")
    traintree = inputfile.Get("TrainTree")
    shirnkagecomp_testtrain.projectPointfromHMean(traintree,"(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)*(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")
    shirnkagecomp_testtrain.projectPointfromHMean(testtree,"(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)*(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")

outputfile.cd()
shirnkagecomp_testtrain.addLabel(0.42,0.11,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",0,0.037)
shirnkagecomp_testtrain.Legendtext = legendtext #set legend after initializing plot object
shirnkagecomp_testtrain.setmanualegendsize("right",0.5,0.5,0.88,0.82)
shirnkagecomp_testtrain.setGroupOptions([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed,ROOT.kCyan+1, ROOT.kPink+8, ROOT.kOrange-7],["TrainingSample","TestSample"])
shirnkagecomp_testtrain.WritePointPlot(c1, "ttbar",pdfout,None,"Min",True)

del inputfile, testtree, traintree,shirnkagecomp_testtrain

#Make aomparison for all test and training sample:
namelist = ["Shrinkage03","Shrinkage01","Shrinkage0075","Depth5","nCuts20","TMVA"]
shirnkagecomp_testtrain = PointPlot(2*len(namelist),"Error with absolute loss function",2*namelist)
legendtext = []
for key in namelist:
    legendtext.append("1: "+str(TMVASettings[key][0])+" | 2: "+str(TMVASettings[key][1])+" | 3: "+str(TMVASettings[key][2])+" | 4: "+str(TMVASettings[key][3]))
    inputfile =  ROOT.TFile(TMVAOutput[key])
    testtree = inputfile.Get("TestTree")
    traintree = inputfile.Get("TrainTree")
    shirnkagecomp_testtrain.projectPointfromHMean(traintree,"abs(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")
    shirnkagecomp_testtrain.projectPointfromHMean(testtree,"abs(BDTG - Jet_MatchedGenJetwNuPt_D_Jet_Pt)")

outputfile.cd()
shirnkagecomp_testtrain.addLabel(0.42,0.11,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",0,0.037)
shirnkagecomp_testtrain.Legendtext = legendtext #set legend after initializing plot object
shirnkagecomp_testtrain.setmanualegendsize("right",0.5,0.5,0.88,0.82)
shirnkagecomp_testtrain.setGroupOptions([ROOT.kBlue, ROOT.kGreen-2, ROOT.kRed,ROOT.kCyan+1, ROOT.kPink+8, ROOT.kOrange-7],["TrainingSample","TestSample"])
shirnkagecomp_testtrain.WritePointPlot(c1, "ttbar",pdfout,None,"Min",True)

del inputfile, testtree, traintree,shirnkagecomp_testtrain

pdfout.closePDF()
