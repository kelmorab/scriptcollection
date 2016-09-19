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

ttHlocation = "/nfs/dust/cms/user/kschweig/JetRegression/trees0627/ttHbb"
ttbarlocation = "/nfs/dust/cms/user/kschweig/JetRegression/trees0629/ttbar_incl"

outputname = "regimprov_targetcomp_MA"

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
tree_bkg = TChain("MVATree")

samplesel = ""
for f in glob(ttHlocation+"/*.root"):
    tree_sig.Add(f)

samplesel = "Evt_Odd == 1 &&"
for f in glob(ttbarlocation+"/*.root"):
    tree_bkg.Add(f)


#---------------------------------------------------------
#--------------------- Signal Sample ---------------------
#---------------------------------------------------------
print "Processing Singnal Sample"

# Catplots for regression Bias
for ireg,reg in enumerate(regressions):
    corrcatpT = CatPlots("Regression Output",[0,50,75,100,150,200,300,600],"Jet_Pt","Jet p_{T}",False,False,"ttHbb",plotbinning[ireg])
    corrcatpT.addLabel(0.05,0.025,regressionlabels[ireg],0,0.04)
    corrcatpT.projectStacks(tree_sig,reg)
    corrcatpT.makeStack()
    corrcatpT.WriteStack(c1,pdfout)
    corrcatpT.WriteNotStacked(c1,pdfout,False)
    del corrcatpT

#---------------------------------------------------------
#------------------- Background Sample -------------------
#---------------------------------------------------------
print "Processing Background Sample"
for ireg,reg in enumerate(regressions):
    print reg
    corrcatpT_bkg = CatPlots("Regression Output",[0,50,75,100,150,200,300,600],"Jet_Pt","Jet p_{T}",False,False,"ttbar",plotbinning[ireg])
    corrcatpT_bkg.addLabel(0.05,0.025,regressionlabels[ireg],0,0.04)
    corrcatpT_bkg.projectStacks(tree_bkg,reg)
    corrcatpT_bkg.makeStack()
    corrcatpT_bkg.WriteStack(c1,pdfout)
    corrcatpT_bkg.WriteNotStacked(c1,pdfout,False)
    del corrcatpT_bkg

#---------------------------------------------------------
#--------------------- Signal Sample ---------------------
#---------------------------------------------------------

# Normplots for tagged dijet mass
# Parton Target
dijet = normPlots("Tagged dijet mass closest to 125 GeV / GeV",True,2,["Without Regression","With Regression"],[40,100,160])
dijet.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
dijet.addLabel(0.02,0.025,"Category: 6J4T",0,0.04)
dijet.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
dijet.projecttoHisto(0,tree_sig,"BDT_common5_input_tagged_dijet_mass_closest_to_125","(N_Jets>=6&&N_BTagsM>=4)")
dijet.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_tagged_dijet_mass_closest_to_125","(N_Jets>=6&&N_BTagsM>=4)")
dijet.WriteHisto(c1,"ttHbb",False,False,pdfout)

del dijet

dijet_all = normPlots("Tagged dijet mass closest to 125 GeV / GeV",True,2,["Without Regression","With Regression"],[40,90,150])
dijet_all.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
dijet_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
dijet_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
dijet_all.projecttoHisto(0,tree_sig,"BDT_common5_input_tagged_dijet_mass_closest_to_125")
dijet_all.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_tagged_dijet_mass_closest_to_125")
dijet_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del dijet_all

bestH = normPlots("Best Higgs mass / GeV",True,2,["Without Regression","With Regression"],[40,80,180])
bestH.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
bestH.addLabel(0.02,0.025,"Category: 6J4T",0,0.04)
bestH.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
bestH.projecttoHisto(0,tree_sig,"BDT_common5_input_best_higgs_mass","(N_Jets>=6&&N_BTagsM>=4)")
bestH.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_best_higgs_mass","(N_Jets>=6&&N_BTagsM>=4)")
bestH.WriteHisto(c1,"ttHbb",False,False,pdfout)

del bestH

bestH_all = normPlots("Best Higgs mass / GeV",True,2,["Without Regression","With Regression"],[40,80,180])
bestH_all.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
bestH_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
bestH_all.projecttoHisto(0,tree_sig,"BDT_common5_input_best_higgs_mass")
bestH_all.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_best_higgs_mass")
bestH_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del bestH_all

closesdijet = normPlots("Closest tagged dijet mass / GeV",True,2,["Without Regression","With Regression"],[50,30,170])
closesdijet.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
closesdijet.addLabel(0.02,0.025,"Category: 6J4T",0,0.04)
closesdijet.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
closesdijet.projecttoHisto(0,tree_sig,"BDT_common5_input_closest_tagged_dijet_mass","(N_Jets>=6&&N_BTagsM>=4)")
closesdijet.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_closest_tagged_dijet_mass","(N_Jets>=6&&N_BTagsM>=4)")
closesdijet.WriteHisto(c1,"ttHbb",False,False,pdfout)

del closesdijet

closesdijet_all = normPlots("Closest tagged dijet mass  / GeV",True,2,["Without Regression","With Regression"],[50,30,170])
closesdijet_all.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
closesdijet_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
closesdijet_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
closesdijet_all.projecttoHisto(0,tree_sig,"BDT_common5_input_closest_tagged_dijet_mass")
closesdijet_all.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_closest_tagged_dijet_mass")
closesdijet_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del closesdijet_all

mcbbmass = normPlots("MC Higgs mass /GeV",True,2,["Without Regression","With Regression"],[40,80,180])
mcbbmass.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
mcbbmass.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
mcbbmass.projecttoHisto(0,tree_sig,"Evt_MCbbMass","Evt_MCbbMass > 0")
mcbbmass.projecttoHisto(1,tree_sig,"Evt_MCregbbMass_new","Evt_MCbbMass > 0")
mcbbmass.WriteHisto(c1,"ttHbb",False,False,pdfout)
mcbbmass.fitGauss(0,95,138)
mcbbmass.fitGauss(1,105,145)
mcbbmass.WriteHisto(c1,"ttHbb",False,False,pdfout, False, None, False,False,None)

del mcbbmass

mcbbmass0lep = normPlots("MC Higgs mass w/ 0 matched Leptons /GeV",True,2,["Without Regression","With Regression"],[40,80,180])
mcbbmass0lep.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
mcbbmass0lep.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
mcbbmass0lep.projecttoHisto(0,tree_sig,"Evt_MCbbMass0Lep","Evt_MCbbMass0Lep > 0")
mcbbmass0lep.projecttoHisto(1,tree_sig,"Evt_MCregbbMass0Lep_new","Evt_MCbbMass0Lep > 0")
mcbbmass0lep.WriteHisto(c1,"ttHbb",False,False,pdfout)

del mcbbmass0lep

mcbbmass2lep = normPlots("MC Higgs mass w/ 2 matched Leptons /GeV",True,2,["Without Regression","With Regression"],[40,80,180])
mcbbmass2lep.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
mcbbmass2lep.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
mcbbmass2lep.projecttoHisto(0,tree_sig,"Evt_MCbbMass2Lep","Evt_MCbbMass2Lep > 0")
mcbbmass2lep.projecttoHisto(1,tree_sig,"Evt_MCregbbMass2Lep_new","Evt_MCbbMass2Lep > 0")
mcbbmass2lep.WriteHisto(c1,"ttHbb",False,False,pdfout)

del mcbbmass2lep

#GenJet Target
dijet_genJet = normPlots("Tagged dijet mass closest to 125 GeV / GeV",True,2,["Without Regression","With Regression"],[40,100,160])
dijet_genJet.addLabel(0.02,0.025,"Category: 6J4T",0,0.04)
dijet_genJet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
dijet_genJet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
dijet_genJet.projecttoHisto(0,tree_sig,"BDT_common5_input_tagged_dijet_mass_closest_to_125","(N_Jets>=6&&N_BTagsM>=4)")
dijet_genJet.projecttoHisto(1,tree_sig,"BDT_reg_genJet_common5_input_tagged_dijet_mass_closest_to_125","(N_Jets>=6&&N_BTagsM>=4)")
dijet_genJet.WriteHisto(c1,"ttHbb",False,False,pdfout)

dijet_genJet_all = normPlots("Tagged dijet mass closest to 125 GeV / GeV",True,2,["Without Regression","With Regression"],[40,90,150])
dijet_genJet_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
dijet_genJet_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
dijet_genJet_all.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
dijet_genJet_all.projecttoHisto(0,tree_sig,"BDT_common5_input_tagged_dijet_mass_closest_to_125")
dijet_genJet_all.projecttoHisto(1,tree_sig,"BDT_reg_genJet_common5_input_tagged_dijet_mass_closest_to_125")
dijet_genJet_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del dijet_genJet,dijet_genJet_all 

bestH_genjet = normPlots("Best Higgs mass / GeV",True,2,["Without Regression","With Regression"],[40,80,180])
bestH_genjet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
bestH_genjet.addLabel(0.02,0.025,"Category: 6J4T",0,0.04)
bestH_genjet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
bestH_genjet.projecttoHisto(0,tree_sig,"BDT_common5_input_best_higgs_mass","(N_Jets>=6&&N_BTagsM>=4)")
bestH_genjet.projecttoHisto(1,tree_sig,"BDT_reg_genJet_common5_input_best_higgs_mass","(N_Jets>=6&&N_BTagsM>=4)")
bestH_genjet.WriteHisto(c1,"ttHbb",False,False,pdfout)

del bestH_genjet

bestH_genjet_all = normPlots("Best Higgs mass / GeV",True,2,["Without Regression","With Regression"],[40,80,180])
bestH_genjet_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
bestH_genjet_all.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
bestH_genjet_all.projecttoHisto(0,tree_sig,"BDT_common5_input_best_higgs_mass")
bestH_genjet_all.projecttoHisto(1,tree_sig,"BDT_reg_genJet_common5_input_best_higgs_mass")
bestH_genjet_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del bestH_genjet_all

closesdijet_genjet = normPlots("Closest tagged dijet mass / GeV",True,2,["Without Regression","With Regression"],[50,30,170])
closesdijet_genjet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
closesdijet_genjet.addLabel(0.02,0.025,"Category: 6J4T",0,0.04)
closesdijet_genjet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
closesdijet_genjet.projecttoHisto(0,tree_sig,"BDT_common5_input_closest_tagged_dijet_mass","(N_Jets>=6&&N_BTagsM>=4)")
closesdijet_genjet.projecttoHisto(1,tree_sig,"BDT_reg_genJet_common5_input_closest_tagged_dijet_mass","(N_Jets>=6&&N_BTagsM>=4)")
closesdijet_genjet.WriteHisto(c1,"ttHbb",False,False,pdfout)

del closesdijet_genjet

closesdijet_genjet_all = normPlots("Closest tagged dijet mass  / GeV",True,2,["Without Regression","With Regression"],[50,30,170])
closesdijet_genjet_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
closesdijet_genjet_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
closesdijet_genjet_all.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
closesdijet_genjet_all.projecttoHisto(0,tree_sig,"BDT_common5_input_closest_tagged_dijet_mass")
closesdijet_genjet_all.projecttoHisto(1,tree_sig,"BDT_reg_genJet_common5_input_closest_tagged_dijet_mass")
closesdijet_genjet_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del closesdijet_genjet_all

mcbbmass_genJet = normPlots("MC Higgs mass /GeV",True,2,["Without Regression","With Regression"],[40,80,180])
mcbbmass_genJet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
mcbbmass_genJet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
mcbbmass_genJet.projecttoHisto(0,tree_sig,"Evt_MCbbMass","Evt_MCbbMass > 0")
mcbbmass_genJet.projecttoHisto(1,tree_sig,"Evt_MCregbbMass_genJet","Evt_MCbbMass > 0")
mcbbmass_genJet.WriteHisto(c1,"ttHbb",False,False,pdfout)
mcbbmass_genJet.fitGauss(0,95,138)
mcbbmass_genJet.fitGauss(1,105,145)
mcbbmass_genJet.WriteHisto(c1,"ttHbb",False,False,pdfout, False, None, False,False,None)

del mcbbmass_genJet

mcbbmass0lep_genJet = normPlots("MC Higgs mass w/ 0 matched Leptons /GeV",True,2,["Without Regression","With Regression"],[40,80,180])
mcbbmass0lep_genJet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
mcbbmass0lep_genJet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
mcbbmass0lep_genJet.projecttoHisto(0,tree_sig,"Evt_MCbbMass0Lep","Evt_MCbbMass0Lep > 0")
mcbbmass0lep_genJet.projecttoHisto(1,tree_sig,"Evt_MCregbbMass0Lep_genJet","Evt_MCbbMass0Lep > 0")
mcbbmass0lep_genJet.WriteHisto(c1,"ttHbb",False,False,pdfout)

del mcbbmass0lep_genJet

mcbbmass2lep_genJet = normPlots("MC Higgs mass w/ 2 matched Leptons /GeV",True,2,["Without Regression","With Regression"],[40,80,180])
mcbbmass2lep_genJet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
mcbbmass2lep_genJet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
mcbbmass2lep_genJet.projecttoHisto(0,tree_sig,"Evt_MCbbMass2Lep","Evt_MCbbMass2Lep > 0")
mcbbmass2lep_genJet.projecttoHisto(1,tree_sig,"Evt_MCregbbMass2Lep_genJet","Evt_MCbbMass2Lep > 0")
mcbbmass2lep_genJet.WriteHisto(c1,"ttHbb",False,False,pdfout)

del mcbbmass2lep_genJet


#Targets:
target =  normPlots("Regression Targets",True,2,["Parton p_{T} / Jet p_{T} ","GenJet p_{T} / Jet p_{T}"],[50,0.6,1.6])
target.changeColorlist([ROOT.kBlack,ROOT.kBlack])
target.projecttoHisto(0,tree_sig,"Jet_MatchedPartonPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.projecttoHisto(1,tree_sig,"Jet_MatchedGenJetwNuPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.setLineStyle(1,2)
target.WriteHisto(c1,"ttHbb",False,False,pdfout)

#2Dplots
partonvgenjet_ratio = TwoDplot("Parton","GenJet", [50,0.8,1.2],[50,0.8,1.2])
partonvgenjet_ratio.setAxisTitle("Parton p_{T} ratio","GenJet p_{T} ratio")
partonvgenjet_ratio.projecttoTwoDplot(tree_sig,"(Jet_MatchedPartonPt/Jet_Pt):(Jet_MatchedGenJetwNuPt/Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5")
partonvgenjet_ratio.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[0.8,0.8,1.2,1.2])

partonvgenjet_pt = TwoDplot("Parton","GenJet", [100,30,200],[100,30,200])
partonvgenjet_pt.setAxisTitle("Parton p_{T} ","GenJet ")
partonvgenjet_pt.projecttoTwoDplot(tree_sig,"(Jet_MatchedPartonPt):(Jet_MatchedGenJetwNuPt)","abs(Jet_MatchedPartonFlav) == 5")
partonvgenjet_pt.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[30,30,200,200])

del target, partonvgenjet_ratio, partonvgenjet_pt

#---------------------------------------------------------
#------------------- Background Sample -------------------
#---------------------------------------------------------

hadtopmass = normPlots("MC Had. Top mass /GeV",True,2,["Without Regression","With Regression"],[80,80,240])
hadtopmass.addLabel(0.95,0.64,"Target: #frac{Parton p_{T}}{Jet p_{T}}",90,0.035)
hadtopmass.changeColorlist([ROOT.kBlack,ROOT.kAzure+7])
hadtopmass.projecttoHisto(0,tree_bkg,"Evt_MChadtopMass","Evt_MChadtopMass > 0")
hadtopmass.projecttoHisto(1,tree_bkg,"Evt_MCreghadtopMass_new","Evt_MChadtopMass > 0")
hadtopmass.WriteHisto(c1,"ttbar",False,False,pdfout)
hadtopmass.fitGauss(0,140,195)
hadtopmass.fitGauss(1,145,200)
hadtopmass.WriteHisto(c1,"ttbar",False,False,pdfout, False, None, False,False,None)

hadtopmass_genJet = normPlots("MC Had. Top mass /GeV",True,2,["Without Regression","With Regression"],[80,80,240])
hadtopmass_genJet.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
hadtopmass_genJet.changeColorlist([ROOT.kBlack,ROOT.kRed-7])
hadtopmass_genJet.projecttoHisto(0,tree_bkg,"Evt_MChadtopMass","Evt_MChadtopMass > 0")
hadtopmass_genJet.projecttoHisto(1,tree_bkg,"Evt_MCreghadtopMass_genJet","Evt_MChadtopMass > 0")
hadtopmass_genJet.WriteHisto(c1,"ttbar",False,False,pdfout)
hadtopmass_genJet.fitGauss(0,140,195)
hadtopmass_genJet.fitGauss(1,145,200)
hadtopmass_genJet.WriteHisto(c1,"ttbar",False,False,pdfout, False, None, False,False,None)


#Targets:
target =  normPlots("Regression Targets",True,2,["Parton p_{T} / Jet p_{T} ","GenJet p_{T} / Jet p_{T}"],[50,0.6,1.6])
target.changeColorlist([ROOT.kBlack,ROOT.kBlack])
target.projecttoHisto(0,tree_bkg,"Jet_MatchedPartonPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.projecttoHisto(1,tree_bkg,"Jet_MatchedGenJetwNuPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.setLineStyle(1,2)
target.WriteHisto(c1,"ttbar",False,False,pdfout)
     
#2Dplots
partonvgenjet_ratio = TwoDplot("Parton","GenJet", [50,0.8,1.2],[50,0.8,1.2])
partonvgenjet_ratio.setAxisTitle("Parton p_{T} ratio","GenJet p_{T} ratio")
partonvgenjet_ratio.projecttoTwoDplot(tree_bkg,"(Jet_MatchedPartonPt/Jet_Pt):(Jet_MatchedGenJetwNuPt/Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5")
partonvgenjet_ratio.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.8,0.8,1.2,1.2])

partonvgenjet_pt = TwoDplot("Parton","GenJet", [100,30,200],[100,30,200])
partonvgenjet_pt.setAxisTitle("Parton p_{T} ","GenJet ")
partonvgenjet_pt.projecttoTwoDplot(tree_bkg,"(Jet_MatchedPartonPt):(Jet_MatchedGenJetwNuPt)","abs(Jet_MatchedPartonFlav) == 5")
partonvgenjet_pt.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[30,30,200,200])


del target, partonvgenjet_ratio, partonvgenjet_pt


#---------------------------------------------------------
#------------------------- Mixed -------------------------
#---------------------------------------------------------

target =  normPlots("Parton p_{T} / Jet p_{T} ",True,2,["t#bar{t}H , H #rightarrow b#bar{b}","t#bar{t}"],[50,0.6,1.6])
target.changeColorlist([ROOT.kViolet+7,ROOT.kSpring-5])
target.projecttoHisto(0,tree_sig,"Jet_MatchedPartonPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.projecttoHisto(1,tree_bkg,"Jet_MatchedPartonPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.WriteHisto(c1,None,False,True,pdfout)

del target

target =  normPlots("GenJet p_{T} / Jet p_{T} ",True,2,["t#bar{t}H , H #rightarrow b#bar{b}","t#bar{t}"],[50,0.6,1.6])
target.changeColorlist([ROOT.kViolet+7,ROOT.kSpring-5])
target.projecttoHisto(0,tree_sig,"Jet_MatchedGenJetwNuPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.projecttoHisto(1,tree_bkg,"Jet_MatchedGenJetwNuPt / Jet_Pt","abs(Jet_MatchedPartonFlav) == 5 && Jet_MatchedGenJetwNuPt > 0 && Jet_MatchedGenJetwNuPt < 600")
target.WriteHisto(c1,None,False,True,pdfout)

del target

dijet_both_all = normPlots("Tagged dijet mass closest to 125 GeV / GeV",True,3,["Without Regression","With Parton Regression","With GenJet Regression"],[40,90,150])
dijet_both_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
dijet_both_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
dijet_both_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7,ROOT.kRed-7])
dijet_both_all.projecttoHisto(0,tree_sig,"BDT_common5_input_tagged_dijet_mass_closest_to_125")
dijet_both_all.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_tagged_dijet_mass_closest_to_125")
dijet_both_all.projecttoHisto(2,tree_sig,"BDT_reg_genJet_common5_input_tagged_dijet_mass_closest_to_125")
dijet_both_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del dijet_both_all   


bestH_both_all = normPlots("Best Higgs mass / GeV",True,3,["Without Regression","With Parton Regression","With GenJet Regression"],[40,80,180])
bestH_both_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
bestH_both_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7,ROOT.kRed-7])
bestH_both_all.projecttoHisto(0,tree_sig,"BDT_common5_input_best_higgs_mass")
bestH_both_all.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_best_higgs_mass")
bestH_both_all.projecttoHisto(2,tree_sig,"BDT_reg_genJet_common5_input_best_higgs_mass")
bestH_both_all.WriteHisto(c1,"ttHbb",False,False,pdfout)

del bestH_both_all


closesdijet_both_all = normPlots("Closest tagged dijet mass  / GeV",True,3,["Without Regression","With Parton Regression","With GenJet Regression"],[50,30,170])
closesdijet_both_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
closesdijet_both_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
closesdijet_both_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7,ROOT.kRed-7])
closesdijet_both_all.projecttoHisto(0,tree_sig,"BDT_common5_input_closest_tagged_dijet_mass")
closesdijet_both_all.projecttoHisto(1,tree_sig,"BDT_reg_new_common5_input_closest_tagged_dijet_mass")
closesdijet_both_all.projecttoHisto(2,tree_sig,"BDT_reg_genJet_common5_input_closest_tagged_dijet_mass")
closesdijet_both_all.WriteHisto(c1,"ttHbb",False,False,pdfout,False,None,False,False,0.05)


del closesdijet_both_all


dijet_both_all = normPlots("Tagged dijet mass closest to 125 GeV / GeV",True,3,["Without Regression","With Parton Regression","With GenJet Regression"],[40,90,150])
dijet_both_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
dijet_both_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
dijet_both_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7,ROOT.kRed-7])
dijet_both_all.projecttoHisto(0,tree_bkg,"BDT_common5_input_tagged_dijet_mass_closest_to_125")
dijet_both_all.projecttoHisto(1,tree_bkg,"BDT_reg_new_common5_input_tagged_dijet_mass_closest_to_125")
dijet_both_all.projecttoHisto(2,tree_bkg,"BDT_reg_genJet_common5_input_tagged_dijet_mass_closest_to_125")
dijet_both_all.WriteHisto(c1,"ttbar",False,False,pdfout,False,None,False,False,0.05)

del dijet_both_all   


bestH_both_all = normPlots("Best Higgs mass / GeV",True,3,["Without Regression","With Parton Regression","With GenJet Regression"],[40,80,180])
bestH_both_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
bestH_both_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7,ROOT.kRed-7])
bestH_both_all.projecttoHisto(0,tree_bkg,"BDT_common5_input_best_higgs_mass")
bestH_both_all.projecttoHisto(1,tree_bkg,"BDT_reg_new_common5_input_best_higgs_mass")
bestH_both_all.projecttoHisto(2,tree_bkg,"BDT_reg_genJet_common5_input_best_higgs_mass")
bestH_both_all.WriteHisto(c1,"ttbar",False,False,pdfout)

del bestH_both_all


closesdijet_both_all = normPlots("Closest tagged dijet mass  / GeV",True,3,["Without Regression","With Parton Regression","With GenJet Regression"],[50,30,170])
closesdijet_both_all.addLabel(0.95,0.64,"Target: #frac{GenJet p_{T}}{Jet p_{T}}",90,0.035)
closesdijet_both_all.setmanualegendsize("right",0.12,0.65,0.4,0.83)
closesdijet_both_all.changeColorlist([ROOT.kBlack,ROOT.kAzure+7,ROOT.kRed-7])
closesdijet_both_all.projecttoHisto(0,tree_bkg,"BDT_common5_input_closest_tagged_dijet_mass")
closesdijet_both_all.projecttoHisto(1,tree_bkg,"BDT_reg_new_common5_input_closest_tagged_dijet_mass")
closesdijet_both_all.projecttoHisto(2,tree_bkg,"BDT_reg_genJet_common5_input_closest_tagged_dijet_mass")
closesdijet_both_all.WriteHisto(c1,"ttbar",False,False,pdfout,False,None,False,False,0.1)

del closesdijet_both_all


outputvtarget = TwoDplot("Target","Output",[70,0.7,1.3],[60,0.85,1.3])
outputvtarget.addLabel(0.02,0.025,"Target: Parton p_{T} / Jet p_{T}",0,0.04)
outputvtarget.setAxisTitle("Regression Output","Target ",)
outputvtarget.projecttoTwoDplot(tree_bkg,"(Jet_regcorr_new):(Jet_MatchedPartonPt / Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5 && Jet_regcorr > 0")
outputvtarget.addLabel(0.45,0.908,"Correlation: "+str(outputvtarget.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
outputvtarget.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.85,0.85,1.3,1.3])

del outputvtarget

outputvtarget = TwoDplot("Target","Output",[70,0.7,1.3],[60,0.85,1.3])
outputvtarget.addLabel(0.02,0.025,"Target: GenJet p_{T} / Jet p_{T}",0,0.04)
outputvtarget.setAxisTitle("Regression Output","Target ")
outputvtarget.projecttoTwoDplot(tree_bkg,"(Jet_regcorr_genJet):(Jet_MatchedGenJetwNuPt / Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5 && Jet_regcorr > 0")
outputvtarget.addLabel(0.45,0.908,"Correlation: "+str(outputvtarget.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
outputvtarget.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.85,0.85,1.3,1.3])

del outputvtarget

outputvtarget = TwoDplot("Target","Output",[40,0.7,1.3],[35,0.85,1.3])
outputvtarget.addLabel(0.02,0.025,"Target: Parton p_{T} / Jet p_{T}",0,0.04)
outputvtarget.setAxisTitle("Regression Output","Target ",)
outputvtarget.projecttoTwoDplot(tree_sig,"(Jet_regcorr_new):(Jet_MatchedPartonPt / Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5 && Jet_regcorr > 0")
outputvtarget.addLabel(0.38,0.908,"Correlation: "+str(outputvtarget.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
outputvtarget.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[0.85,0.85,1.3,1.3])

del outputvtarget

outputvtarget = TwoDplot("Target","Output",[40,0.7,1.3],[35,0.85,1.3])
outputvtarget.addLabel(0.02,0.025,"Target: GenJet p_{T} / Jet p_{T}",0,0.04)
outputvtarget.setAxisTitle("Regression Output","Target ")
outputvtarget.projecttoTwoDplot(tree_sig,"(Jet_regcorr_genJet):(Jet_MatchedGenJetwNuPt / Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5 && Jet_regcorr > 0")
outputvtarget.addLabel(0.38,0.908,"Correlation: "+str(outputvtarget.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
outputvtarget.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[0.85,0.85,1.3,1.3])

del outputvtarget

outputvtarget = TwoDplot("jetpt","Output",[40,0.7,1.3],[35,0.85,1.3])
outputvtarget.addLabel(0.02,0.025,"Target: GenJet p_{T} / Jet p_{T}",0,0.04)
outputvtarget.setAxisTitle("Regression Output","Target ")
outputvtarget.projecttoTwoDplot(tree_sig,"(Jet_regcorr_genJet):(Jet_MatchedGenJetwNuPt / Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5 && Jet_regcorr > 0")
outputvtarget.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[0.85,0.85,1.3,1.3])

del outputvtarget


pdfout.closePDF()





