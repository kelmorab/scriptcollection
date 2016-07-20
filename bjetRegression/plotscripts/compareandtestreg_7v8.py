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

outputname = "compareandtestreg_7v8_0720"

dotargetcomp = True
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#


weightlist = ["/nfs/dust/cms/user/kschweig/CMSSW_8_0_10/src/BoostedTTH/BoostedAnalyzer/data/bregweights/TMVARegression_0619_GenJet_1200_BSF05minNS06Shr075_patronFlav_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/weights/BReg_0720_80XReg_BDTG.weights.xml"]
textforlegend = ["Training for 76X","Traing for 80X"]
targets = ["Jet_MatchedGenJetwNuPt","RegJet_MatchedGenJetwNuPt"]
prefix = ["","Reg"]
Labels = ["CMSSW 76X","CMSSW 80X"]
targettype = [2,2]
inputconfig = [1,2]
higgsmassnames = ["Evt_MCregbbMass", "Evt_MCRegbbMass"]

print weightlist
raw_input("Press ret if weightlist is correct")
#Initialize Plots for all weights
legend = textforlegend


print legend

bbMass_param = [150,50,205]

#inputvars
input_pt = normPlots("Jet_Pt",True,len(legend),legend,[200,0,600])
input_mt = normPlots("Jet_Mt",True,len(legend),legend,[200,0,600])
input_eta = normPlots("Jet_Eta",True,len(legend),legend,[50,-2.5,2.5])
input_leadtrackpt = normPlots("Jet_leadTrackPt",True,len(legend),legend,[50,0,150])
input_corr = normPlots("Jet JEC",True,len(legend),legend,[100,0.8,1.2])
input_lpt = normPlots("Jet_leptonPt",True,len(legend),legend,[60,0,120])
input_lptrel = normPlots("Jet_leptonPtRel",True,len(legend),legend,[20,0,30])
input_ldR = normPlots("Jet_leptonDeltaR",True,len(legend),legend,[20,0,0.5])
input_totHE = normPlots("Jet_totHEFrac",True,len(legend),legend,[20,0,1])
input_nEME = normPlots("Jet_nEmEFrac",True,len(legend),legend,[20,0,1])
input_vpt = normPlots("Jet_vtxPt",True,len(legend),legend,[20,0,100])
input_v3dval = normPlots("Jet_vtx3DVal",True,len(legend),legend,[30,0,15])
input_v3dsig = normPlots("Jet_vtx3DSig",True,len(legend),legend,[50,0,200])
input_vm = normPlots("Jet_vtxMass",True,len(legend),legend,[14,0,7])
input_vnt = normPlots("Jet_vtxNtracks",True,len(legend),legend,[13,-0.5,12.5])
input_pV = normPlots("N_PrimaryVertices",True,len(legend),legend,[26,-.5,25.5])
input_pt.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_mt.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_eta.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_leadtrackpt.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_corr.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_lpt.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_lptrel.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_ldR.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_totHE.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_nEME.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_vpt.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_v3dval.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_v3dsig.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_vm.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_vnt.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
input_pV.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])

regcorr = normPlots("Regression Output",True,len(legend),legend,[50,0.6,1.6])
regcorr_targets = normPlots("Regression Targets",True,2,legend,[50,0.6,1.6])
bbmass = normPlots("MC Higgs Mass /GeV",True,len(legend)+1,["No regression"] + legend,bbMass_param)
#bbmass0Lep =normPlots("MC Higgs Mass w/ 0 matched Leptons",True,len(legend),legend,bbMass_param)
#bbmass1Lep = normPlots("MC Higgs Mass w/ 1 matched Lepton",True,len(legend),legend,bbMass_param)
#bbmass2Lep =normPlots("MC Higgs Mass w/ 2 matched Leptons",True,len(legend),legend,bbMass_param)
regcorr.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
regcorr_targets.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
bbmass.changeColorlist([ROOT.kBlack, ROOT.kAzure-7,  ROOT.kRed-7])

regcorr.setmanualegendsize("right",0.55,0.55,0.88,0.88)
bbmass.setmanualegendsize("right",0.60,0.55,0.88,0.88)


plot_errsqu = PointPlot(len(legend),"Error with squared loss function",legend)
plot_errabs = PointPlot(len(legend),"Error with abs. loss function",legend)

plot_errsqu.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_errabs.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_errsqu.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])
plot_errabs.changeColorlist([ROOT.kAzure-7, ROOT.kRed-7])

pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()


for iw, weight in enumerate(weightlist):


    targetvoutput = TwoDplot("Target","Output",[50,0.6,1.6],[40,0.7,1.5])
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

    if dotargetcomp:
        partonvgenjet_ratio = TwoDplot("Parton","GenJet", [50,0.8,1.2],[50,0.8,1.2])
        partonvgenjet_ratio.setAxisTitle("Parton p_{T} ratio","GenJet p_{T} ratio")
        partonvgenjet_ratio.projecttoTwoDplot(tree,"("+prefix[iw]+"Jet_MatchedPartonPt/"+prefix[iw]+"Jet_Pt):("+prefix[iw]+"Jet_MatchedGenJetwNuPt/"+prefix[iw]+"Jet_Pt)","abs("+prefix[iw]+"Jet_MatchedPartonFlav) == 5")
        partonvgenjet_ratio.addLabel(0.45,0.908,"Correlation: "+str(partonvgenjet_ratio.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
        partonvgenjet_ratio.addLabel(0.02,0.025,Labels[iw],0,0.04)
        partonvgenjet_ratio.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.8,0.8,1.2,1.2])
        partonvgenjet_pt = TwoDplot("Parton","GenJet", [100,30,200],[100,30,200])
        partonvgenjet_pt.setAxisTitle("Parton p_{T} ","GenJet ")
        partonvgenjet_pt.projecttoTwoDplot(tree,"("+prefix[iw]+"Jet_MatchedPartonPt):("+prefix[iw]+"Jet_MatchedGenJetwNuPt)","abs("+prefix[iw]+"Jet_MatchedPartonFlav) == 5")
        partonvgenjet_pt.addLabel(0.45,0.908,"Correlation: "+str(partonvgenjet_pt.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
        partonvgenjet_pt.addLabel(0.02,0.025,Labels[iw],0,0.04)
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
        tree.SetBranchAddress("Jet_corrJES",Jetcorr)
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
        if ev == 1000000:
            pass
            break
        if ev%100000 == 0:
            print ev
        tree.GetEvent(ev)

        input_pV.FillnormHisto(NPrimaryVertices[0],iw)

        inputvars["N_PrimaryVertices"] = NPrimaryVertices[0]
        higgsjets = [] #append [pt,eta,phi,E,corr]
        inputstrings = []
        for nj in range(NJets[0]):
            if Jetregcorr[nj] > 0 and Target[nj] > 0:
                if inputconfig[iw] == 2:
                    inputvars["Jet_Pt"] = JetPt[nj]/Jetregcorr[nj]
                    inputvars["Jet_Mt"] = JetMt[nj]/Jetregcorr[nj]
                    input_pt.FillnormHisto(JetPt[nj]/Jetregcorr[nj],iw)
                    input_mt.FillnormHisto(JetMt[nj]/Jetregcorr[nj],iw)
                else:
                    inputvars["Jet_Pt"] = JetPt[nj]
                    inputvars["Jet_Mt"] = JetMt[nj]
                    input_pt.FillnormHisto(JetPt[nj],iw)
                    input_mt.FillnormHisto(JetMt[nj],iw)

                inputvars["Jet_Eta"] = Jeteta[nj]
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



                input_eta.FillnormHisto(Jeteta[nj],iw)
                input_leadtrackpt.FillnormHisto(Jetleadtrackpt[nj],iw)
                input_corr.FillnormHisto(Jetcorr[nj],iw)
                input_lpt.FillnormHisto(Jetleptonpt[nj],iw)
                input_lptrel.FillnormHisto(Jetleptonptrel[nj],iw)
                input_ldR.FillnormHisto(JetleptonDR[nj],iw)
                input_totHE.FillnormHisto(JettothadFrac[nj],iw)
                input_nEME.FillnormHisto(JetnEmFrac[nj],iw)
                input_vpt.FillnormHisto(JetvtxPt[nj],iw)
                input_v3dval.FillnormHisto(Jetvtx3dVal[nj],iw)
                input_v3dsig.FillnormHisto(Jetvtx3dSig[nj],iw)
                input_vm.FillnormHisto(JetvtxMass[nj],iw)
                input_vnt.FillnormHisto(JetvtxNTracks[nj],iw)
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
                if inputconfig[iw] == 2:
                    errors.addevent(regoutval,Target[nj]/(JetPt[nj]/Jetregcorr[nj]))
                    targetvoutput.FillTwoDplot(Target[nj]/(JetPt[nj]/Jetregcorr[nj]),regoutval)
                else:
                    errors.addevent(regoutval,Target[nj]/JetPt[nj])
                    targetvoutput.FillTwoDplot(Target[nj]/JetPt[nj],regoutval)


                regcorr_targets.FillnormHisto(Target[nj]/JetPt[nj],iw)

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

    targetvoutput.addLabel(0.45,0.908,"Correlation: "+str(targetvoutput.GetTH2F().GetCorrelationFactor())[0:6],0,0.04)
    targetvoutput.addLabel(0.02,0.025,Labels[iw],0,0.04)
    targetvoutput.WriteTwoDplot(c1,"ttbar",True,None,pdfout,False,False,[0.6,0.7,1.6,1.5])

    del tree, regression, errors, targetvoutput



regcorr.WriteHisto(c1,"ttbar",False,True,pdfout)
regcorr_targets.WriteHisto(c1,"ttbar",False,True,pdfout)
bbmass.WriteHisto(c1,"ttbar",False,False,pdfout,True)
plot_errabs.WritePointPlot(c1,"ttbar",pdfout)
plot_errsqu.WritePointPlot(c1,"ttbar",pdfout)
input_pt.WriteHisto(c1,"ttbar",False,True,pdfout)
input_mt.WriteHisto(c1,"ttbar",False,True,pdfout)
input_eta.WriteHisto(c1,"ttbar",False,True,pdfout)
input_leadtrackpt.WriteHisto(c1,"ttbar",False,True,pdfout)
input_corr.WriteHisto(c1,"ttbar",False,True,pdfout)
input_lpt.WriteHisto(c1,"ttbar",False,True,pdfout)
input_lptrel.WriteHisto(c1,"ttbar",False,True,pdfout)
input_ldR.WriteHisto(c1,"ttbar",False,True,pdfout)
input_totHE.WriteHisto(c1,"ttbar",False,True,pdfout)
input_nEME.WriteHisto(c1,"ttbar",False,True,pdfout)
input_vpt.WriteHisto(c1,"ttbar",False,True,pdfout)
input_v3dval.WriteHisto(c1,"ttbar",False,True,pdfout)
input_v3dsig.WriteHisto(c1,"ttbar",False,True,pdfout)
input_vm.WriteHisto(c1,"ttbar",False,True,pdfout)
input_vnt.WriteHisto(c1,"ttbar",False,True,pdfout)
input_pV.WriteHisto(c1,"ttbar",False,True,pdfout)


pdfout.closePDF()
