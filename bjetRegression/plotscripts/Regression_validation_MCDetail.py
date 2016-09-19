import sys
import os
from glob import glob
from array import array

from ROOT import TChain, TColor, TCanvas

from JetRegression import JetRegression, getHiggsMass
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

signal = "/nfs/dust/cms/user/kschweig/JetRegression/Validation/trees0824/Zjet_m50toInf/"

outputname = "validation_Details_0826"

regressions = ["Jet_regcorr","Jet_regcorr_new","Jet_regcorr_genJet"]
regressionlabels = ["Standard settings","Target: Parton p_{T} ratio","Target: GenJet p_{T} ratio"]
plotbinning = [[70,0.6,1.6],[70,0.6,1.6],[70,0.85,1.45]]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#


pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()

tree_sig = TChain("MVATree")

samplesel = ""
for f in glob(signal+"/*.root"):
    tree_sig.Add(f)

#---------------------------------------------------------
#--------------------- Signal Sample ---------------------
#---------------------------------------------------------
print "Processing Singnal Sample"

# Catplots for regression Bias
corrcatpT = CatPlots("Regression Output",[0,35,50,100,300],"Jet_Pt","Jet p_{T, preReg}",False,False,"ZJets",[40,0.9,1.3],False,[ROOT.kRed+2,ROOT.kOrange-4,ROOT.kGreen+2,ROOT.kBlue+2,])
corrcatpT.addLabel(0.05,0.025,"2 Leptons, 1 #leq jets #leq 2, 1 #leq b-Tag #leq 2",0,0.04)
corrcatpT.projectStacks(tree_sig,"RegJet_regcorr")
corrcatpT.makeStack()
corrcatpT.WriteStack(c1,pdfout)
corrcatpT.WriteNotStacked(c1,pdfout,False)
del corrcatpT


ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 1 #leq jets #leq 2, 1 #leq b-Tag #leq 2",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50)")
ptbal.WriteHisto(c1,"ZJets",False,True,pdfout)

del ptbal


ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 1 #leq jets #leq 2, 1 #leq b-Tag #leq 2",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50)")
ptbal.WriteHisto(c1,"ZJets",False,False,None,False,None, False, False, None, True)
ptbal.fitGauss(0,0.4,1.3)
ptbal.fitGauss(1,0.5,1.4)
ptbal.WriteHisto(c1,"ZJets",False,False,pdfout,False,None, False, False, None, True)

del ptbal

ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 1 Jet, 1 b-Tag",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 1)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 1)")
ptbal.WriteHisto(c1,"ZJets",False,True,pdfout)

del ptbal


ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 1 Jet, 1 b-Tag",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 1)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 1)")
ptbal.WriteHisto(c1,"ZJets",False,False,None,False,None, False, False, None, True)
ptbal.fitGauss(0,0.4,1.3)
ptbal.fitGauss(1,0.5,1.4)
ptbal.WriteHisto(c1,"ZJets",False,False,pdfout,False,None, False, False, None, True)

del ptbal

ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 2 Jets, 1 #leq b-Tag #leq 2",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 2)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 2)")
ptbal.WriteHisto(c1,"ZJets",False,True,pdfout)

del ptbal


ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 2 Jets, 1 #leq b-Tag #leq 2",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 2)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 2)")
ptbal.WriteHisto(c1,"ZJets",False,False,None,False,None, False, False, None, True)
ptbal.fitGauss(0,0.4,1.3)
ptbal.fitGauss(1,0.5,1.4)
ptbal.WriteHisto(c1,"ZJets",False,False,pdfout,False,None, False, False, None, True)

del ptbal

ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 2 Jets, 1 b-Tag",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 2 && N_BTagsM == 1)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 2 && N_BTagsM == 1)")
ptbal.WriteHisto(c1,"ZJets",False,True,pdfout)

del ptbal


ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 2 Jets, 1 b-Tag",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 1 && N_BTagsM == 1)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 1 && N_BTagsM == 1)")
ptbal.WriteHisto(c1,"ZJets",False,False,None,False,None, False, False, None, True)
ptbal.fitGauss(0,0.4,1.3)
ptbal.fitGauss(1,0.5,1.4)
ptbal.WriteHisto(c1,"ZJets",False,False,pdfout,False,None, False, False, None, True)

del ptbal

ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 2 Jets, 2 b-Tags ",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 2 && N_BTagsM == 2)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 2 && N_BTagsM == 2)")
ptbal.WriteHisto(c1,"ZJets",False,True,pdfout)

del ptbal


ptbal = normPlots("p_{T} balance",True,2,["Without Regression","With Regression"],[20,0,2])
ptbal.addLabel(0.02,0.025,"2 Leptons, 2 Jets, 2 b-Tags",0,0.04)
ptbal.changeColorlist([ROOT.kAzure+7, ROOT.kRed-7])
ptbal.projecttoHisto(0,tree_sig,"Evt_PtBal_noreg","(Evt_llpT >= 50 && N_LooseJets == 2&& N_BTagsM == 2)")
ptbal.projecttoHisto(1,tree_sig,"Evt_PtBal_reg","(Evt_llpT >= 50 && N_LooseJets == 2 && N_BTagsM == 2)")
ptbal.WriteHisto(c1,"ZJets",False,False,None,False,None, False, False, None, True)
ptbal.fitGauss(0,0.4,1.3)
ptbal.fitGauss(1,0.5,1.4)
ptbal.WriteHisto(c1,"ZJets",False,False,pdfout,False,None, False, False, None, True)

del ptbal
pdfout.closePDF()
