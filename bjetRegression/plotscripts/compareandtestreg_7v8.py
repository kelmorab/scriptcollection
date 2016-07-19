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

ttbarlocations = ["/nfs/dust/cms/user/kschweig/JetRegression/trees0701/ttbar_incl",
                  "/nfs/dust/cms/user/kschweig/JetRegression/trees0718/ttbar_incl"]



sample = "Background" # Signal or Background

outputname = "compareandtestreg_7v8_0719"

dotargetcomp = True
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#


weightlist = ["/nfs/dust/cms/user/kschweig/CMSSW_8_0_10/src/BoostedTTH/BoostedAnalyzer/data/bregweights/TMVARegression_0619_GenJet_1200_BSF05minNS06Shr075_patronFlav_BDTG.weights.xml",
           "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/weights/BReg_0719_80XReg_BDTG.weights.xml"]
textforlegend = ["Training for 76X","Traing for 80X"]
targets = ["Jet_MatchedGenJetwNuPt","RegJet_MatchedGenJetwNuPt"]
targettype = [2,2]
inputconfig = [1,2]
higgsmassnames = ["Evt_MCregbbMass", "Evt_MCRegbbMass"]

print weightlist
raw_input("Press ret if weightlist is correct")
#Initialize Plots for all weights
legend = textforlegend


print legend

bbMass_param = [150,50,205]
regcorr = normPlots("Regression Output",True,len(legend),legend,[50,0.6,1.6],True)
regcorr_genjet = normPlots("Regression Output (Target: GenJet)",True,3,["GenJet p_{T} / Jet p_{T}","Output w/ p_{T} as Target","Output w/ p_{T} Ratio as Target"],[50,0.6,1.6],True)
regcorr_targets = normPlots("Regression Targets",True,2,["Parton p_{T} / Jet p_{T} ","GenJet p_{T} / Jet p_{T}"],[50,0.6,1.6],True)
bbmass = normPlots("MC Higgs Mass /GeV",True,len(legend)+1,["No regression"] + legend,bbMass_param,True)
#bbmass0Lep =normPlots("MC Higgs Mass w/ 0 matched Leptons",True,len(legend),legend,bbMass_param)
#bbmass1Lep = normPlots("MC Higgs Mass w/ 1 matched Lepton",True,len(legend),legend,bbMass_param)
#bbmass2Lep =normPlots("MC Higgs Mass w/ 2 matched Leptons",True,len(legend),legend,bbMass_param)
regcorr.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
regcorr_genjet.changeColorlist([ROOT.kBlack, ROOT.kAzure-7, ROOT.kRed-7])
regcorr_targets.changeColorlist([ROOT.kBlack, ROOT.kBlack])
regcorr_targets.setLineStyle(1,2)
bbmass.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7])

regcorr.setmanualegendsize("right",0.55,0.55,0.88,0.88)
regcorr_parton.setmanualegendsize("right",0.55,0.65,0.88,0.88)
regcorr_genjet.setmanualegendsize("right",0.55,0.65,0.88,0.88)
bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)
if autosel:
    regcorr.addLabel(0.92,0.15,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.03)
    regcorr.addLabel(0.945,0.15,"5: BaggedSampleFraction",90,0.03)
    bbmass.addLabel(0.92,0.15,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.03)
    bbmass.addLabel(0.945,0.15,"5: BaggedSampleFraction",90,0.03)


plot_errsqu = PointPlot(len(legend),"Error with squared loss function",legend)
plot_errabs = PointPlot(len(legend),"Error with abs. loss function",legend)

plot_errsqu.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_errabs.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_errsqu.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
plot_errabs.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
if autosel:
    plot_errsqu.addLabel(0.92,0.15,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.03)
    plot_errsqu.addLabel(0.945,0.15,"5: BaggedSampleFraction",90,0.03)
    plot_errabs.addLabel(0.92,0.15,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.03)
    plot_errabs.addLabel(0.945,0.15,"5: BaggedSampleFraction",90,0.03)


pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()

for iw, weight in enumerate(weightlist):


    targetvoutput = TwoDplot("Target","Output",[50,0.6,1.6],[40,0.7,1.5],True)
    targetvoutput.setAxisTitle("Target","Output")

    print "Processing weight",iw,"of",len(weightlist)-1
    print "Weight name:",weight.split("/")[-1]

    tree = TChain("MVATree")


    if sample is "Signal":
        samplesel = ""
        for f in glob(ttHlocation+"/*.root"):
            tree.Add(f)

    else:
        samplesel = "Evt_Odd == 1 &&"
        for f in glob(ttbarlocations[iw]+"/*.root"):
            tree.Add(f)

    if iw == 0 and dotargetcomp:
        partonvgenjet_ratio = TwoDplot("Parton","GenJet", [50,0.8,1.2],[50,0.8,1.2],True)
        partonvgenjet_ratio.setAxisTitle("Parton p_{T} ratio","GenJet p_{T} ratio")
        partonvgenjet_ratio.projecttoTwoDplot(tree,"(Jet_MatchedPartonPt/Jet_Pt):(Jet_MatchedGenJetwNuPt/Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5")
        partonvgenjet_ratio.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.8,0.8,1.2,1.2])
        partonvgenjet_pt = TwoDplot("Parton","GenJet", [100,30,200],[100,30,200],True)
        partonvgenjet_pt.setAxisTitle("Parton p_{T} ","GenJet ")

        partonvgenjet_pt.projecttoTwoDplot(tree,"(Jet_MatchedPartonPt):(Jet_MatchedGenJetwNuPt)","abs(Jet_MatchedPartonFlav) == 5")
        partonvgenjet_pt.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[30,30,200,200])


    regression = JetRegression(weight,[],"New")

    nEvents = tree.GetEntries()

    errors = Errors()

    inputvars = {}

    Target = array('f',20*[0])
    JetPt = array('f',20*[0])
    Jetregcorr =array('f',20*[0])
    JetMt = array('f',20*[0])
    Jetcorr = array('f',20*[0])
    Jetcorrhelper = array('f',20*[0])
    Jeteta  = array('f',20*[0])
    Jetphi  = array('f',20*[0])
    JetE  = array('f',20*[0])
    Jetleadtrackpt = array('f',20*[0])
    Jetleptonpt = array('f',20*[0])
    JetleptonDR = array('f',20*[0])
    Jetleptonptrel = array('f',20*[0])
    JetnEmFrac = array('f',20*[0])
    JettothadFrac = array('f',20*[0])
    JetidnEmFrac = array('f',20*[0])
    JetidtothadFrac = array('f',20*[0])
    JetvtxPt = array('f',20*[0])
    JetvtxMass = array('f',20*[0])
    Jetvtx3dVal = array('f',20*[0])
    Jetvtx3dSig = array('f',20*[0])
    JetvtxNTracks = array('f',20*[0])
    NPrimaryVertices = array('i',[0])
    NJets = array('i',[0])
    bbmass_fromTree = array('f',[0])
    bbmass_noreg = array('f',[0])
    isHiggsJet = array('f',20*[0])

    if inputconfig[iw] == 1:
        tree.SetBranchAddress("Jet_MatchedGenJetwNuPt",Target)
        tree.SetBranchAddress("Jet_Pt",JetPt)
        tree.SetBranchAddress("Jet_regcorr",Jetregcorr)
        tree.SetBranchAddress("Jet_Mt",JetMt)
        tree.SetBranchAddress("Jet_Eta",Jeteta)
        tree.SetBranchAddress("Jet_Phi",Jetphi)
        tree.SetBranchAddress("Jet_E",JetE)
        tree.SetBranchAddress("Jet_corr",Jetcorrhelper)
        tree.SetBranchAddress("Jet_leptonPt",Jetleptonpt)
        tree.SetBranchAddress("Jet_leptonPtRel",Jetleptonptrel)
        tree.SetBranchAddress("Jet_leptonDeltaR",JetleptonDR)
        tree.SetBranchAddress("Jet_leadTrackPt",Jetleadtrackpt)
        tree.SetBranchAddress("Jet_idtotHEFrac",JettothadFrac)
        tree.SetBranchAddress("Jet_idnEmEFrac",JetnEmFrac)
        tree.SetBranchAddress("Jet_vtxPt",JetvtxPt)
        tree.SetBranchAddress("Jet_vtxMass",JetvtxMass)
        tree.SetBranchAddress("Jet_vtx3DVal",Jetvtx3dVal)
        tree.SetBranchAddress("Jet_vtx3DSig",Jetvtx3dSig)
        tree.SetBranchAddress("Jet_vtxNtracks",JetvtxNTracks)
        tree.SetBranchAddress("N_PrimaryVertices",NPrimaryVertices)
        tree.SetBranchAddress("N_Jets",NJets)
        #tree.SetBranchAddress(higgsmassnames[iw],bbmass_fromTree)
        #tree.SetBranchAddress("Evt_MCbbMass",bbmass_noreg)
        #tree.SetBranchAddress("Jet_isHiggsJet", isHiggsJet)
    if inputconfig[iw] == 2:
        tree.SetBranchAddress("RegJet_MatchedGenJetwNuPt",Target)
        tree.SetBranchAddress("RegJet_Pt",JetPt)
        tree.SetBranchAddress("RegJet_regcorr",Jetregcorr)
        tree.SetBranchAddress("RegJet_Mt",JetMt)
        tree.SetBranchAddress("RegJet_Eta",Jeteta)
        tree.SetBranchAddress("RegJet_Phi",Jetphi)
        tree.SetBranchAddress("RegJet_E",JetE)
        tree.SetBranchAddress("RegJet_corr",Jetcorr)
        tree.SetBranchAddress("RegJet_leptonPt",Jetleptonpt)
        tree.SetBranchAddress("RegJet_leptonPtRel",Jetleptonptrel)
        tree.SetBranchAddress("RegJet_leptonDeltaR",JetleptonDR)
        tree.SetBranchAddress("RegJet_leadTrackPt",Jetleadtrackpt)
        tree.SetBranchAddress("RegJet_totHEFrac",JettothadFrac)
        tree.SetBranchAddress("RegJet_nEmEFrac",JetnEmFrac)
        tree.SetBranchAddress("RegJet_vtxPt",JetvtxPt)
        tree.SetBranchAddress("RegJet_vtxMass",JetvtxMass)
        tree.SetBranchAddress("RegJet_vtx3DVal",Jetvtx3dVal)
        tree.SetBranchAddress("RegJet_vtx3DSig",Jetvtx3dSig)
        tree.SetBranchAddress("RegJet_vtxNtracks",JetvtxNTracks)
        tree.SetBranchAddress("N_PrimaryVertices",NPrimaryVertices)
        tree.SetBranchAddress("N_RegJets",NJets)
        #tree.SetBranchAddress(higgsmassnames[iw],bbmass_fromTree)
        #tree.SetBranchAddress("Evt_MCbbMass",bbmass_noreg)
        #tree.SetBranchAddress("RegJet_isHiggsJet", isHiggsJet)


    for ev in range(nEvents):
        if ev == 100:
            pass
            #break
        tree.GetEvent(ev)
        inputvars["N_PrimaryVertices"] = NPrimaryVertices[0]
        higgsjets = [] #append [pt,eta,phi,E,corr]
        inputstrings = []
        for nj in range(NJets[0]):
            if Jetregcorr[nj] > 0 and Target[nj] > 0:
                inputvars["Jet_Pt"] = JetPt[nj]
                inputvars["Jet_Eta"] = Jeteta[nj]
                inputvars["Jet_Mt"] = JetMt[nj]
                inputvars["Jet_leadTrackPt"] = Jetleadtrackpt[nj]
                inputvars["Jet_leptonPt"] = Jetleptonpt[nj]
                inputvars["Jet_leptonPtRel"] = Jetleptonptrel[nj]
                inputvars["Jet_leptonDeltaR"] = JetleptonDR[nj]
                inputvars["Jet_vtxPt"] = JetvtxPt[nj]
                inputvars["Jet_vtxMass"] = JetvtxMass[nj]
                inputvars["Jet_vtx3DVal"] = Jetvtx3dVal[nj]
                inputvars["Jet_vtx3DSig"] = Jetvtx3dSig[nj]
                inputvars["Jet_vtxNtracks"] = JetvtxNTracks[nj]
                inputvars["Jet_totHEFrac"] = JettothadFrac[nj]
                inputvars["Jet_nEmEFrac"] = JetnEmFrac[nj]
                inputvars["Jet_corr"] = Jetcorr[nj]

                regoutval = regression.evalReg(inputvars)

                if targettype[iw] is 1:
                    regoutval = regoutval / JetPt[nj]

                if isHiggsJet[nj] == 1:
                    higgsjets.append([JetPt[nj],Jeteta[nj],Jetphi[nj],JetE[nj],regoutval])
                    inputstrings.append(inputvars)
                    #print "is higgs jet"
                    #for key in inputvars:
                    #    print key, inputvars[key]


                regcorr.FillnormHisto(regoutval,iw)

                errors.addevent(regoutval,Target[nj]/JetPt[nj])

                targetvoutput.FillTwoDplot(Target[nj]/JetPt[nj],regoutval)

                #Hier muss noch was gefuellt werden
        if len(higgsjets) == 2:

            bbmass.FillnormHisto(getHiggsMass(higgsjets[0][0],higgsjets[0][1],higgsjets[0][2],higgsjets[0][3],higgsjets[0][4],
                                              higgsjets[1][0],higgsjets[1][1],higgsjets[1][2],higgsjets[1][3],higgsjets[1][4]),
                                 iw+1)
            if iw == 0:
                bbmass.FillnormHisto(bbmass_noreg[0], 0)

        #else:
        #    if bbmass_fromTree[00] > 0:
        #        print 0,"|", bbmass_fromTree[0]



    errors.printerr()
    errvals = errors.getvalues()
    plot_errabs.addPoint(errvals["err_abs_loss"])
    plot_errsqu.addPoint(errvals["err_squared_loss"])

    targetvoutput.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.6,0.7,1.6,1.5])

    del tree, regression, errors, targetvoutput



regcorr.WriteHisto(c1,"ttbar",False,False,pdfout)
regcorr_parton.WriteHisto(c1,"ttbar",False,False,pdfout)
regcorr_genjet.WriteHisto(c1,"ttbar",False,False,pdfout)
regcorr_targets.WriteHisto(c1,"ttbar",False,False,pdfout)
bbmass.WriteHisto(c1,"ttbar",False,False,pdfout,True)
plot_errabs.WritePointPlot(c1,"ttbar",pdfout)
plot_errsqu.WritePointPlot(c1,"ttbar",pdfout)
pdfout.closePDF()
