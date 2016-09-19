import sys
import os
from glob import glob
from array import array

from ROOT import TChain, TColor, TCanvas

from plotting import *
from rootutils import PDFPrinting

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)


samples = ["/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/ttbar_incl",
          # "/nfs/dust/cms/user/kschweig/JetRegression/trees0822/ttHbb"
          ]
samplenames  = ["Background","Signal"] # Signal or Background
sampletype = ["ttbar","ttHbb"]

outputname = "bvl_inputvars_0907"

legend = ["b jets","Light and c jets"]

pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()


for isample,sample in enumerate(samples):
    print "Processing sample",isample+1,"of",len(samples)
    tree = TChain("MVATree")
    
    
    if samplenames[isample] is "Signal":
        samplesel = ""
    else:
        samplesel = "Evt_Odd == 1 &&"
    for f in glob(sample+"/*_??_nominal*.root"):
        print f
        tree.Add(f)
    
    plotlist = []
    #Inputvariables
    input_pt = normPlots("Jet_Pt",True,len(legend),legend,[60,0,300])
    input_mt = normPlots("Jet_Mt",True,len(legend),legend,[60,0,300])
    input_eta = normPlots("Jet_Eta",True,len(legend),legend,[50,-2.5,2.5])
    input_leadtrackpt = normPlots("Jet_leadTrackPt",True,len(legend),legend,[50,0,150])
    input_corr = normPlots("Jet JEC",True,len(legend),legend,[40,0.95,1.2])
    input_lpt = normPlots("Jet_leptonPt",True,len(legend),legend,[40,0,80])
    input_lptrel = normPlots("Jet_leptonPtRel",True,len(legend),legend,[20,0,10])
    input_ldR = normPlots("Jet_leptonDeltaR",True,len(legend),legend,[20,0,0.5])
    input_totHE = normPlots("Jet_totHEFrac",True,len(legend),legend,[20,0,1])
    input_chHE = normPlots("Jet_chHEFrac",True,len(legend),legend,[20,0,1])
    input_nHE = normPlots("Jet_nHEFrac",True,len(legend),legend,[20,0,1])
    input_nEME = normPlots("Jet_nEmEFrac",True,len(legend),legend,[20,0,1]) 
    input_chEME = normPlots("Jet_chEmEFrac",True,len(legend),legend,[20,0,1]) 
    input_totEME = normPlots("Jet_totEmEFrac",True,len(legend),legend,[20,0,1]) 
    input_vpt = normPlots("Jet_vtxPt",True,len(legend),legend,[20,0,100]) 
    input_v3dval = normPlots("Jet_vtx3DVal",True,len(legend),legend,[30,0,15]) 
    input_v3dsig = normPlots("Jet_vtx3DSig",True,len(legend),legend,[50,0,200]) 
    input_vm = normPlots("Jet_vtxMass",True,len(legend),legend,[14,0,7]) 
    input_vnt = normPlots("Jet_vtxNtracks",True,len(legend),legend,[13,-0.5,12.5]) 
    input_pV = normPlots("N_PrimaryVertices",True,len(legend),legend,[31,-.5,30.5]) 
    #Ratios
    ratio_JetvParton = normPlots("p_{T, Jet} / p_{T, Parton}",True,len(legend),legend,[50,0.2,2.2]) 
    ratio_JetvParton_b_regVnoreg = normPlots("p_{T, Jet} / p_{T, Parton}",True,2,["Without regression","With regression"],[50,0.2,2.2]) 
    ratio_JetvGenJet = normPlots("p_{T, Jet} / p_{T, GenJet}",True,len(legend),legend,[50,0,2]) 
    ratio_JetvPartonpostreg = normPlots("p_{T, Jet} / p_{T, Parton}",True,len(legend),legend,[50,0.2,2.2]) 
    ratio_JetvGenJetpostreg = normPlots("p_{T, Jet} / p_{T, GenJet}",True,len(legend),legend,[50,0,2]) 
    ratio_totEnergyFractions = normPlots("E_{tot hadr} / E_{tot em} ",True,len(legend),legend,[20,0,1]) 
    ratio_chEnergyFractions = normPlots("E_{ch hadr} / E_{ch em} ",True,len(legend),legend,[20,0,1]) 
    ratio_nEnergyFractions = normPlots("E_{n hadr} / E_{n em} ",True,len(legend),legend,[20,0,1]) 

    plotlist.append(input_pt)
    plotlist.append(input_mt)
    plotlist.append(input_eta)
    plotlist.append(input_leadtrackpt)
    plotlist.append(input_corr)
    plotlist.append(input_lpt)
    plotlist.append(input_lptrel )
    plotlist.append(input_ldR )
    plotlist.append(input_totHE )
    plotlist.append(input_chHE )
    plotlist.append(input_nHE )
    plotlist.append(input_nEME )
    plotlist.append(input_chEME)
    plotlist.append(input_totEME )
    plotlist.append(input_vpt )
    plotlist.append(input_v3dval )
    plotlist.append(input_v3dsig )
    plotlist.append(input_vm )
    plotlist.append(input_vnt )
    plotlist.append(input_pV)
    #Ratios
    plotlist.append(ratio_JetvParton)
    plotlist.append(ratio_JetvGenJet)
    plotlist.append(ratio_JetvPartonpostreg)
    plotlist.append(ratio_JetvGenJetpostreg)
    plotlist.append(ratio_totEnergyFractions)
    plotlist.append(ratio_chEnergyFractions )
    plotlist.append(ratio_nEnergyFractions )

    #Style
    for plot in plotlist:
        plot.changeColorlist([ROOT.kGreen-2,ROOT.kBlue-4])

    ratio_JetvParton_b_regVnoreg.changeColorlist([ROOT.kBlack, ROOT.kRed-7])

    ratio_JetvParton.addLabel(0.02,0.025,"no regression applied",0,0.04)
    ratio_JetvGenJet.addLabel(0.02,0.025,"no regression applied",0,0.04)
    ratio_JetvPartonpostreg.addLabel(0.02,0.025,"regression applied",0,0.04)
    ratio_JetvGenJetpostreg.addLabel(0.02,0.025,"regression applied",0,0.04)
    ratio_JetvParton_b_regVnoreg.addLabel(0.02,0.025,"Only b jets",0,0.04)

    ratio_chEnergyFractions.setmanualegendsize("right",0.6,0.12,0.88,0.30)
    ratio_totEnergyFractions.setmanualegendsize("right",0.6,0.12,0.88,0.30)
    input_chEME.setmanualegendsize("right",0.6,0.12,0.88,0.30)
    input_chHE.setmanualegendsize("right",0.13,0.65,0.41,0.83)
    input_totHE.setmanualegendsize("right",0.13,0.65,0.41,0.83)



    selections = [samplesel+"abs(Jet_Flav) == 5",samplesel+"abs(Jet_Flav) != 5"]

    
    for isel, selection in enumerate(selections):
        print "using selection",isel+1,"of",len(selections)
        print "Projection inputvariables"
        input_pt.projecttoHisto(isel, tree, "RegJet_preregPt",selection)
        print "next"
        input_mt.projecttoHisto(isel, tree, "RegJet_preregMt",selection)
        input_eta.projecttoHisto(isel, tree, "RegJet_Eta",selection)
        input_leadtrackpt.projecttoHisto(isel, tree, "RegJet_leadTrackPt",selection)
        input_corr.projecttoHisto(isel, tree, "RegJet_corr",selection)
        input_lpt.projecttoHisto(isel, tree, "RegJet_leptonPt",selection)
        input_lptrel.projecttoHisto(isel, tree, "RegJet_leptonPtRel",selection)
        input_ldR.projecttoHisto(isel, tree, "RegJet_leptonDeltaR",selection)
        input_totHE.projecttoHisto(isel, tree, "RegJet_totHEFrac",selection)
        input_chHE.projecttoHisto(isel, tree, "RegJet_cHEFrac",selection)
        input_nHE.projecttoHisto(isel, tree, "RegJet_nHEFrac",selection)
        input_nEME.projecttoHisto(isel, tree, "RegJet_nEmEFrac",selection)
        input_chEME.projecttoHisto(isel, tree, " 1 - RegJet_totHEFrac + RegJet_nEmEFrac",selection)
        input_totEME.projecttoHisto(isel, tree, "1 - RegJet_totHEFrac",selection)
        input_vpt.projecttoHisto(isel, tree, "RegJet_vtxPt",selection)
        input_v3dval.projecttoHisto(isel, tree, "RegJet_vtx3DVal",selection)
        input_v3dsig.projecttoHisto(isel, tree, "RegJet_vtx3DSig",selection)
        input_vm.projecttoHisto(isel, tree, "RegJet_vtxMass",selection)
        input_vnt.projecttoHisto(isel, tree, "RegJet_vtxNtracks",selection)
        input_pV.projecttoHisto(isel, tree, "N_PrimaryVertices",selection)
        print "Projection ratio variables"
        ratio_JetvParton.projecttoHisto(isel, tree, "RegJet_preregPt / RegJet_MatchedPartonPt",selection)
        ratio_JetvGenJet.projecttoHisto(isel, tree, "RegJet_preregPt / RegJet_MatchedGenJetwNuPt",selection)
        ratio_JetvPartonpostreg.projecttoHisto(isel, tree, "RegJet_Pt / RegJet_MatchedPartonPt",selection)
        ratio_JetvGenJetpostreg.projecttoHisto(isel, tree, "RegJet_Pt / RegJet_MatchedGenJetwNuPt",selection)
        ratio_totEnergyFractions.projecttoHisto(isel, tree, "RegJet_totHEFrac / (1 - RegJet_totHEFrac)",selection)
        ratio_chEnergyFractions.projecttoHisto(isel, tree, "RegJet_cHEFrac / (1 - RegJet_totHEFrac + RegJet_nEmEFrac)",selection)
        ratio_nEnergyFractions.projecttoHisto(isel, tree, "RegJet_nHEFrac / RegJet_nEmEFrac",selection)
        
    ratio_JetvParton_b_regVnoreg.projecttoHisto(1,tree,"RegJet_Pt / RegJet_MatchedPartonPt",samplesel+"abs(Jet_Flav) == 5")
    ratio_JetvParton_b_regVnoreg.projecttoHisto(0,tree,"RegJet_preregPt / RegJet_MatchedPartonPt",samplesel+"abs(Jet_Flav) == 5")


    for plot in plotlist:
        plot.WriteHisto(c1,sampletype[isample],False,True,pdfout)


    ratio_JetvParton.fitGauss(0,0.7,1.2)
    ratio_JetvParton.fitGauss(1,0.7,1.25)
    ratio_JetvParton.setmanualegendsize("right",0.5,0.58,0.90,0.88)
    ratio_JetvParton.WriteHisto(c1,sampletype[isample],False,True,pdfout, False, None, False,False,None,True,[1,2,ROOT.kBlack,2])

    ratio_JetvPartonpostreg.fitGauss(0,0.7,1.25)
    ratio_JetvPartonpostreg.fitGauss(1,0.7,1.25)
    ratio_JetvPartonpostreg.setmanualegendsize("right",0.5,0.58,0.90,0.88)
    ratio_JetvPartonpostreg.WriteHisto(c1,sampletype[isample],False,True,pdfout, False, None, False,False,None,True,[1,2,ROOT.kBlack,2])

    ratio_JetvParton_b_regVnoreg.WriteHisto(c1,sampletype[isample],False,True,pdfout, False, None, False,False,None,False,[1,2,ROOT.kBlack,2])

    ratio_JetvParton_b_regVnoreg.fitGauss(0,0.7,1.2)
    ratio_JetvParton_b_regVnoreg.fitGauss(1,0.7,1.25)
    ratio_JetvParton_b_regVnoreg.setmanualegendsize("right",0.5,0.58,0.90,0.88)
    ratio_JetvParton_b_regVnoreg.WriteHisto(c1,sampletype[isample],False,True,pdfout, False, None, False,False,None,True,[1,2,ROOT.kBlack,2])



pdfout.closePDF()
