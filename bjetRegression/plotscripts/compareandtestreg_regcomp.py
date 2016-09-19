import sys
import os
from glob import glob
from array import array

from ROOT import TChain, TColor, TCanvas

from JetRegression import JetRegression, getHiggsMasswcorr, getHiggsMass, gethadtopMasswcorr, gethadtopMass
from plotting import *
from rootutils import PDFPrinting

parentpath = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
sys.path.append(parentpath)
from regressionTools import *

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)

#
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Settings

samplepath = "/nfs/dust/cms/user/kschweig/JetRegression/trees0908/BDTTraining/TreeswRegression0911output"



samplenames  = ["Background","Signal"] # Signal or Background
sampletype = ["ttbar","ttHbb"]

outputname = "compareandtestreg_0912"

dotargetcomp = False
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
regextentions = ["nominal",
                #"Big",
               #"noemFrac",
               #"nohadFrac",
               "noFracnovtxMass",
               "woworstVars"
                #"Parton",
               ]
legend = ["Nominal","No Frac/VtxM/VtxNTr","No Frac/VtxM/VtxNTr/NPV"]
targetname = ["RegJet_MatchedGenJetwNuPt","RegJet_MatchedGenJetwNuPt","RegJet_MatchedGenJetwNuPt","RegJet_MatchedPartonPt"]
prefix = ["","nofracVtx","nofracVtxNPV"]
Labels = ["Nominal","No Frac/VtxM/VtxNTr","No Frac/VtxM/VtxNTr/NPV"]
inputconfig = ["A","B","C","A"]
"""
weightlist = ["/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_noemfrac_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_parton_BDTG.weights.xml"]
textforlegend = ["nominal","No EMFrac","Training w/ Parton pT"]
targets = ["Jet_MatchedGenJetwNuPt","Jet_MatchedGenJetwNuPt","RegJet_MatchedGenJetwNuPt"]
prefix = ["","noem","parton"]
Labels = ["nominal","No EMFrac","Training w/ Parton pT"]
inputconfig = ["A","B","A"]
"""
bbMass_param = [40,50,205]

pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()

for isample,sample in enumerate(sampletype):
    #inputvars
    regcorr = normPlots("Regression output",True,len(legend),legend,[50,0.6,1.6])
    bbmass = normPlots("MC Higgs mass /GeV",True,len(legend)+1,["No regression"] + legend,bbMass_param)
    hadtopmass = normPlots("MC had top mass /GeV",True,len(legend)+1,["No regression"] + legend,[80,100,280])
    hadtopmass1Lep = normPlots("MC had top mass w/ 1 matched lepton /GeV",True,len(legend)+1,["No regression"] + legend,[80,100,280])
    hadtopmass0Lep = normPlots("MC had top mass w/ 1 matched lepton /GeV",True,len(legend)+1,["No regression"] + legend,[80,100,280])
    bbmass0Lep =normPlots("MC Higgs mass w/ 0 matched leptons",True,len(legend)+1,legend,bbMass_param)
    bbmass1Lep = normPlots("MC Higgs mass w/ 1 matched lepton",True,len(legend)+1,legend,bbMass_param)
    bbmass2Lep =normPlots("MC Higgs mass w/ 2 matched leptons",True,len(legend)+1,legend,bbMass_param)
    regcorr.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7, ROOT.kGreen-2])
    bbmass.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])
    bbmass0Lep.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])
    bbmass1Lep.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])
    bbmass2Lep.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])
    hadtopmass.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])
    hadtopmass1Lep.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])
    hadtopmass0Lep.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7, ROOT.kGreen-2])

    regcorr.setmanualegendsize("right",0.55,0.55,0.88,0.88)
    bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass0Lep.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass1Lep.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    bbmass2Lep.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    hadtopmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    hadtopmass1Lep.setmanualegendsize("right",0.60,0.55,0.88,0.88)
    hadtopmass0Lep.setmanualegendsize("right",0.60,0.55,0.88,0.88)

    plot_errsqu = PointPlot(len(legend),"Error with squared loss function",legend)
    plot_errabs = PointPlot(len(legend),"Error with abs. loss function",legend)

    plot_errsqu.setmanualegendsize("right",0.55,0.65,0.88,0.88)
    plot_errabs.setmanualegendsize("right",0.55,0.65,0.88,0.88)
    plot_errsqu.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7, ROOT.kGreen-2])
    plot_errabs.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7, ROOT.kGreen-2])

    tree = TChain("MVATree")
    print samplenames, isample
    if samplenames[isample] is "Signal":
        samplesel = ""
        for f in glob(samplepath+"/ttHbb*.root"):
            print f
            tree.Add(f)
    else:
        print "hallo"
        samplesel = "Evt_Odd == 1 &&"
        for f in glob(samplepath+"/ttbar*.root"):
            print f
            tree.Add(f)
        
    nEvents = tree.GetEntries()

    #weightexpression = "Weight_ElectronSFID*Weight_MuonSFID*Weight_MuonSFIso*Weight_ElectronSFGFS*Weight_MuonSFHIP* Weight_ElectronSFTrigger * Weight_MuonSFTrigger"
    weightexpression = "1"
    
    bbmass.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression)
    bbmass0Lep.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression+"*Evt_leptonicHiggsJets==0")
    bbmass1Lep.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression+"*Evt_leptonicHiggsJets==1")
    bbmass2Lep.projecttoHisto(0,tree,"Evt_MCHiggsMass",weightexpression+"*Evt_leptonicHiggsJets==2")
    hadtopmass.projecttoHisto(0,tree,"Evt_MCHadTopMass",weightexpression)
    hadtopmass0Lep.projecttoHisto(0,tree,"Evt_MCHadTopMass",weightexpression+"*Evt_leptonicHadTopJets==0")
    hadtopmass1Lep.projecttoHisto(0,tree,"Evt_MCHadTopMass",weightexpression+"*Evt_leptonicHadTopJets==1")
    
    for ireg, regression in enumerate(regextentions):
        #print ireg
        regcorr.projecttoHisto(ireg,tree,"Jet_regoutput_"+regression,weightexpression)
        bbmass.projecttoHisto(ireg+1,tree,"Evt_MCHiggsMass_"+regression,weightexpression)
        bbmass0Lep.projecttoHisto(ireg+1,tree,"Evt_MCHiggsMass_"+regression,weightexpression+"*Evt_leptonicHiggsJets==0")
        bbmass1Lep.projecttoHisto(ireg+1,tree,"Evt_MCHiggsMass_"+regression,weightexpression+"*Evt_leptonicHiggsJets==1")
        bbmass2Lep.projecttoHisto(ireg+1,tree,"Evt_MCHiggsMass_"+regression,weightexpression+"*Evt_leptonicHiggsJets==2")
        hadtopmass.projecttoHisto(ireg+1,tree,"Evt_MCHadTopMass_"+regression,weightexpression)
        hadtopmass0Lep.projecttoHisto(ireg+1,tree,"Evt_MCHadTopMass_"+regression,weightexpression+"*Evt_leptonicHadTopJets==0")
        hadtopmass1Lep.projecttoHisto(ireg+1,tree,"Evt_MCHadTopMass_"+regression,weightexpression+"*Evt_leptonicHadTopJets==1")
        
        regoutcat = CatPlots("Regression output",[0,50,75,100,150,200,300,600],"Jet_preregPt","Jet p_{T, preReg}",False,False,sample,[50,0.6,1.6])
        regoutcat.addLabel(0.05,0.025,Labels[ireg],0,0.04)
        regoutcat.projectStacks(tree,"Jet_regoutput_"+regression)

        regoutcat.makeStack()
        regoutcat.WriteStack(c1,pdfout)
        regoutcat.WriteNotStacked(c1,pdfout,False)


        plot_errsqu.projectPointfromHMean(tree, "Jet_RegErrQ_"+regression,"Jet_RegErrQ_"+regression+" > 0")
        plot_errabs.projectPointfromHMean(tree, "Jet_RegErrAbs_"+regression,"Jet_RegErrAbs_"+regression+" > 0")

        del regoutcat



    regcorr.WriteHisto(c1,sample,False,True,pdfout)
    bbmass.WriteHisto(c1,sample,False,False,pdfout,True)
    bbmass0Lep.WriteHisto(c1,sample,False,False,pdfout,True)
    bbmass1Lep.WriteHisto(c1,sample,False,False,pdfout,True)
    bbmass2Lep.WriteHisto(c1,sample,False,False,pdfout,True)
    hadtopmass.WriteHisto(c1,sample,False,False,pdfout,True)
    hadtopmass0Lep.WriteHisto(c1,sample,False,False,pdfout,True)
    hadtopmass1Lep.WriteHisto(c1,sample,False,False,pdfout,True)
    plot_errabs.WritePointPlot(c1,sample,pdfout)
    plot_errsqu.WritePointPlot(c1,sample,pdfout)

    del tree,regcorr, bbmass, bbmass0Lep, bbmass1Lep, bbmass2Lep, hadtopmass, hadtopmass0Lep, hadtopmass1Lep, plot_errabs, plot_errsqu

pdfout.closePDF()
