import sys
import os
from glob import glob
from array import array

from ROOT import TChain, TColor, TCanvas

from JetRegression import JetRegression, getHiggsMass,getHiggsMasswcorr
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

#ttHlocation = "/nfs/dust/cms/user/kschweig/JetRegression/trees0527/ttHbb"
ttHlocation = "/nfs/dust/cms/user/kschweig/JetRegression/trees0620_ttHttbar/ttHbb"
ttbarlocation = "/nfs/dust/cms/user/kschweig/JetRegression/trees0527/ttbar_incl"

#weightlocation = "/nfs/dust/cms/user/kschweig/JetRegression/Settingtesting/0601/settings/weights"
#weightlocation = "/nfs/dust/cms/user/kschweig/CMSSW_7_6_3/src/BoostedTTH/BoostedAnalyzer/data/bregweights/"
weightlocation = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/weight_corr/"

sample = "Signal" # Signal or Background

outputname = "compareandtestreg_Gejettargetcomp_MA"

autosel = False
dotargetcomp = True
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#

if autosel:
    weightsel = "*"
    weightlist = glob(weightlocation+"/"+weightsel+".xml")
    #weightsel = "*_0.08_*_30_0.6_*"
    #weightlist = weightlist + glob(weightlocation+"/"+weightsel+".xml")
    targets = len(weightlist)*["Jet_MatchedPartonPt"]
else:
    weights = ["BReg_0627_Parton_1200_BSF05minNS06Shr075_noratio_BDTG.weights.xml",
               "BReg_0627_Parton_1200_BSF05minNS06Shr075_ratio_BDTG.weights.xml",
               "BReg_0627_GenJet_1200_BSF05minNS06Shr075_noratio_BDTG.weights.xml",
               "BReg_0627_GenJet_1200_BSF05minNS06Shr075_ratio_BDTG.weights.xml"]
    weightlist = []
    for w in weights:
        weightlist.append(str(weightlocation + w))
    textforlegend = ["Target: Parton p_{T}","Target: Parton p_{T} / Jet p_{T}","Target: GenJet p_{T}","Target: GenJet p_{T} / Jet p_{T}"]
    targets = ["Jet_MatchedPartonPt","Jet_MatchedPartonPt","Jet_MatchedGenJetwNuPt","Jet_MatchedGenJetwNuPt"]
    targettype = [1,2,1,2]
    specialplot = [1,2,3,4]
    inputconfig = [2,2,2,2]
    higgsmassnames = ["Evt_MCregbbMass", "Evt_MCregbbMass", "Evt_MCregbbMass_genJet_pF", "Evt_MCregbbMass_genJet"]

print weightlist
raw_input("Press ret if weightlist is correct")
#Initialize Plots for all weights
legend = []
for iw, weight in enumerate(weightlist):
    if autosel:
        tmplist = ((weight.split("/")[-1])[0:-len("_BDTG.weights.xml")]).split("_") 
        nTrees = tmplist[-5]
        shrink = tmplist[-4]
        maxDepth = tmplist[-3]
        nCuts = tmplist[-2]
        bsf = tmplist[-1]
        legend.append("1: "+nTrees+" | 2: "+shrink+" | 3: "+maxDepth+" | 4: "+nCuts+" | 5: "+bsf)
if not autosel:
    legend = textforlegend


print legend

bbMass_param = [63,80,220]
regcorr = normPlots("Regression Output",True,len(legend),legend,[50,0.6,1.6])
regcorr_parton = normPlots("Regression Output (Target: Parton)",True,3,["Parton p_{T} / Jet p_{T}","Output w/ p_{T} as Target","Output w/ p_{T} Ratio as Target"],[50,0.6,1.6])
regcorr_genjet = normPlots("Regression Output (Target: GenJet)",True,3,["GenJet p_{T} / Jet p_{T}","Output w/ p_{T} as Target","Output w/ p_{T} Ratio as Target"],[50,0.6,1.6])
regcorr_targets = normPlots("Regression Targets",True,2,["Parton p_{T} / Jet p_{T} ","GenJet p_{T} / Jet p_{T}"],[50,0.6,1.6])
bbmass = normPlots("MC Higgs Mass [GeV]",True,len(legend)+1,["No regression"] + legend,bbMass_param)
#bbmass0Lep =normPlots("MC Higgs Mass w/ 0 matched Leptons",True,len(legend),legend,bbMass_param)
#bbmass1Lep = normPlots("MC Higgs Mass w/ 1 matched Lepton",True,len(legend),legend,bbMass_param)
#bbmass2Lep =normPlots("MC Higgs Mass w/ 2 matched Leptons",True,len(legend),legend,bbMass_param)
regcorr.changeColorlist([ROOT.kAzure+8, ROOT.kAzure-7, ROOT.kPink+4, ROOT.kRed-7])
regcorr_parton.changeColorlist([ROOT.kBlack,ROOT.kAzure+8, ROOT.kAzure-7])
regcorr_genjet.changeColorlist([ROOT.kBlack, ROOT.kPink+4, ROOT.kRed-7])
regcorr_targets.changeColorlist([ROOT.kBlack, ROOT.kBlack])
regcorr_targets.setLineStyle(1,2)
bbmass.changeColorlist([ROOT.kBlack, ROOT.kAzure+8, ROOT.kAzure-7, ROOT.kPink+4, ROOT.kRed-7])

regcorr.setmanualegendsize("right",0.55,0.55,0.88,0.88)
regcorr_parton.setmanualegendsize("right",0.55,0.65,0.88,0.88)
regcorr_genjet.setmanualegendsize("right",0.55,0.65,0.88,0.88)
bbmass.setmanualegendsize("right",0.525,0.55,0.88,0.88)
if autosel:
    regcorr.addLabel(0.92,0.15,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.03)
    regcorr.addLabel(0.945,0.15,"5: BaggedSampleFraction",90,0.03)
    bbmass.addLabel(0.92,0.15,"1: nTrees | 2: Shrinkage | 3: MaxDepth | 4: nCuts",90,0.03)
    bbmass.addLabel(0.945,0.15,"5: BaggedSampleFraction",90,0.03)


plot_errsqu = PointPlot(len(legend),"Error with squared loss function",legend)
plot_errabs = PointPlot(len(legend),"Error with abs. loss function",legend)

plot_errsqu.setmanualegendsize("right",0.475,0.65,0.88,0.88)
plot_errabs.setmanualegendsize("right",0.475,0.65,0.88,0.88)
plot_errsqu.changeColorlist([ROOT.kAzure+8, ROOT.kAzure-7, ROOT.kPink+4, ROOT.kRed-7])
plot_errabs.changeColorlist([ROOT.kAzure+8, ROOT.kAzure-7, ROOT.kPink+4, ROOT.kRed-7])
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
        for f in glob(ttbarlocation+"/*.root"):
            tree.Add(f)

    if iw == 0 and dotargetcomp:
        partonvgenjet_ratio = TwoDplot("Parton","GenJet", [50,0.8,1.2],[50,0.8,1.2],True)
        partonvgenjet_ratio.setAxisTitle("Parton p_{T} ratio","GenJet p_{T} ratio")
        partonvgenjet_ratio.projecttoTwoDplot(tree,"(Jet_MatchedPartonPt/Jet_Pt):(Jet_MatchedGenJetwNuPt/Jet_Pt)","abs(Jet_MatchedPartonFlav) == 5")
        partonvgenjet_ratio.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[0.8,0.8,1.2,1.2])
        partonvgenjet_pt = TwoDplot("Parton","GenJet", [100,30,200],[100,30,200],True)
        partonvgenjet_pt.setAxisTitle("Parton p_{T} ","GenJet ")

        partonvgenjet_pt.projecttoTwoDplot(tree,"(Jet_MatchedPartonPt):(Jet_MatchedGenJetwNuPt)","abs(Jet_MatchedPartonFlav) == 5")
        partonvgenjet_pt.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[30,30,200,200])
        

    regression = JetRegression(weight,[],"A")

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

    tree.SetBranchAddress(targets[iw],Target)
    tree.SetBranchAddress("Jet_Pt",JetPt)
    tree.SetBranchAddress("Jet_regcorr",Jetregcorr)
    tree.SetBranchAddress("Jet_Mt",JetMt)
    tree.SetBranchAddress("Jet_Eta",Jeteta)
    tree.SetBranchAddress("Jet_Phi",Jetphi)
    tree.SetBranchAddress("Jet_E",JetE)
    tree.SetBranchAddress("Jet_corr",Jetcorr)
    tree.SetBranchAddress("Jet_corrJES",Jetcorrhelper)
    tree.SetBranchAddress("Jet_leptonPt",Jetleptonpt)
    tree.SetBranchAddress("Jet_leptonPtRel",Jetleptonptrel)
    tree.SetBranchAddress("Jet_leptonDeltaR",JetleptonDR)
    tree.SetBranchAddress("Jet_leadTrackPt",Jetleadtrackpt)
    tree.SetBranchAddress("Jet_totHEFrac",JettothadFrac)
    tree.SetBranchAddress("Jet_nEmEFrac",JetnEmFrac)
    tree.SetBranchAddress("Jet_idtotHEFrac",JetidtothadFrac)
    tree.SetBranchAddress("Jet_idnEmEFrac",JetidnEmFrac)
    tree.SetBranchAddress("Jet_vtxPt",JetvtxPt)
    tree.SetBranchAddress("Jet_vtxMass",JetvtxMass)
    tree.SetBranchAddress("Jet_vtx3DVal",Jetvtx3dVal)
    tree.SetBranchAddress("Jet_vtx3DSig",Jetvtx3dSig)
    tree.SetBranchAddress("Jet_vtxNtracks",JetvtxNTracks)
    tree.SetBranchAddress("N_PrimaryVertices",NPrimaryVertices)
    tree.SetBranchAddress("N_Jets",NJets)
    tree.SetBranchAddress(higgsmassnames[iw],bbmass_fromTree)
    tree.SetBranchAddress("Evt_MCbbMass",bbmass_noreg)
    tree.SetBranchAddress("Jet_isHiggsJet", isHiggsJet)

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
                if inputconfig[iw] == 1:
                    inputvars["Jet_totHEFrac"] = JettothadFrac[nj]
                    inputvars["Jet_nEmEFrac"] = JetnEmFrac[nj]
                    inputvars["Jet_corr"] = Jetcorr[nj]
                elif inputconfig[iw] == 2:
                    inputvars["Jet_totHEFrac"] = JetidtothadFrac[nj]
                    inputvars["Jet_nEmEFrac"] = JetidnEmFrac[nj]
                    inputvars["Jet_corr"] = Jetcorrhelper[nj]
                else:
                    print "Error with inputconifg settinig"
                    exit()

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
                if specialplot[iw] is 1:
                    regcorr_parton.FillnormHisto(regoutval,1)
                    regcorr_parton.FillnormHisto(Target[nj]/JetPt[nj],0)
                    regcorr_targets.FillnormHisto(Target[nj]/JetPt[nj],0)
                if specialplot[iw] is 2:
                    regcorr_parton.FillnormHisto(regoutval,2)
                if specialplot[iw] is 3:
                    regcorr_genjet.FillnormHisto(Target[nj]/JetPt[nj],0)
                    regcorr_targets.FillnormHisto(Target[nj]/JetPt[nj],1)
                    regcorr_genjet.FillnormHisto(regoutval,1)
                if specialplot[iw] is 4:
                    regcorr_genjet.FillnormHisto(regoutval,2)

                errors.addevent(regoutval,Target[nj]/JetPt[nj])
                
                targetvoutput.FillTwoDplot(Target[nj]/JetPt[nj],regoutval)

                #Hier muss noch was gefuellt werden
        if len(higgsjets) == 2:
            
            bbmass.FillnormHisto(getHiggsMasswcorr(higgsjets[0][0],higgsjets[0][1],higgsjets[0][2],higgsjets[0][3],higgsjets[0][4],
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
    
    targetvoutput.WriteTwoDplot(c1,"ttHbb",True,None,pdfout,False,False,[0.6,0.7,1.6,1.5])
    
    del tree, regression, errors, targetvoutput



regcorr.WriteHisto(c1,"ttHbb",False,False,pdfout)
regcorr_parton.WriteHisto(c1,"ttHbb",False,False,pdfout)
regcorr_genjet.WriteHisto(c1,"ttHbb",False,False,pdfout)
regcorr_targets.WriteHisto(c1,"ttHbb",False,False,pdfout)
bbmass.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
plot_errabs.WritePointPlot(c1,"ttHbb",pdfout)
plot_errsqu.WritePointPlot(c1,"ttHbb",pdfout)
pdfout.closePDF()
