

import ROOT
from JetRegression import JetRegression
from plotting import *
from rootutils import PDFPrinting
import bRegVars as bR


ROOT.gROOT.SetBatch(True)

inputfile = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root")
weightfile = "/afs/desy.de/user/h/hmildner/public/regression_weights/weights_ttbar_quark/TMVARegression_BDTG.weights.xml"

outputfileprefix = "ttHbb_0218"

tree = inputfile.Get("MVATree")


#Get Variables from Var Module
readvars = bR.readvars

inputvar = bR.inputvar

inputvars = bR.inputvars
outputvars = bR.outputvars


#jetreg = JetRegression(weightfile) 

inputplots_regcorr = {}
inputplot_regcorr = {}
outputplots_regcorr = {}
outputplots_pt = {}
outputplots_eta = {}
outputplots_mt = {}
outputplots_leppt = {}
outputplots_partonpt = {}

#Categorize by regcorr factor
for key in inputvar:                              
    inputplot_regcorr.update({key : CatPlots(key, [0,0.65,0.75,0.9,1,1.1,1.2,1.3,1.45,2],"regcorr","p_{T, Reg} / p_{T}",False,False)})
    #inputplot_regcorr.update({key : CatPlots(key, [0,0.65,0.75,0.9,0.975,1.025,1.1,1.175,1.25,1.35,1.45,2],"regcorr",False,False)})
    #inputplot_regcorr.update({key : CatPlots(key, [0,0.55,0.65,0.75,0.9,0.975,1.025,1.1,1.25,1.35,1.45,2],"regcorr",False,False)})
for key in inputvars:    
    inputplots_regcorr.update({key : CatPlots(key, [0,0.65,0.75,0.9,1,1.1,1.2,1.3,1.45,2],"regcorr","p_{T, Reg} / p_{T}",False,False)})
    #inputplots_regcorr.update({key : CatPlots(key, [0,0.65,0.75,0.9,0.975,1.025,1.1,1.175,1.25,1.35,1.45,2],"regcorr",False,False)})
    #inputplots_regcorr.update({key : CatPlots(key, [0,0.55,0.65,0.75,0.9,0.975,1.025,1.1,1.25,1.35,1.45,2],"regcorr",False,False)})
for key in outputvars:    
    outputplots_regcorr.update({key : CatPlots(key,[0,0.65,0.75,0.9,1,1.1,1.2,1.3,1.45,2],"regcorr","p_{T, Reg} / p_{T}",False,False)})
    #outputplots_regcorr.update({key : CatPlots(key,[0,0.65,0.75,0.9,0.975,1.025,1.1,1.175,1.25,1.35,1.45,2],"regcorr",False,False)})
    #outputplots_regcorr.update({key : CatPlots(key,[0,0.55,0.65,0.75,0.9,0.975,1.025,1.1,1.25,1.35,1.45,2],"regcorr",False,False)})
#Categorize by Jet_pt
for key in outputvars:
    print "pt"
    outputplots_pt.update({key : CatPlots(key, [0,50,75,100,150,200,300,600],"jetpt","p_{T}",False,False)})
for key in outputvars:    
    outputplots_mt.update({key : CatPlots(key, [0,50,75,100,150,200,400,600],"jetmt","m_{T}",False,False)})
#Categorize by Jet_lepton_pt
for key in outputvars:    
    outputplots_leppt.update({key : CatPlots(key, [0,5,10,30,60,120],"jetleppt","p_{T, Lepton}",False,False)})
#Categorize by PartonPt
for key in outputvars:
    outputplots_partonpt.update({key : CatPlots(key, [0,50,75,100,150,200,300,800],"jetpartonpt","p_{T, Parton}",False,False)})
for key in outputvars:
    outputplots_eta.update({key : CatPlots(key, [-2.4,-1.5,-0.75,-0.25,0.25,0.75,1.5,2.4],"jeteta","#eta",False,False)})



for iev in range(tree.GetEntries()):
    if iev%10000 == 0:
        print iev
    if iev == 200000:
        break
    tree.GetEvent(iev)
    

    
    readvars["N_Jets"] = tree.N_Jets 
    readvars["Evt_Rho"] = tree.Evt_Rho
    
    readvars["Jet_Pt"] = tree.Jet_Pt                 
    readvars["Jet_corr"] = tree.Jet_corr   
    readvars["Jet_Eta"] = tree.Jet_Eta       
    readvars["Jet_Mt"] = tree.Jet_Mt           
    readvars["Jet_leadTrackPt"] = tree.Jet_leadTrackPt
    readvars["Jet_Flav"] = tree.Jet_Flav      
    
    readvars["Jet_leptonPt"] = tree.Jet_leptonPt
    readvars["Jet_leptonPtRel"] = tree.Jet_leptonPtRel
    readvars["Jet_leptonDeltaR"] = tree.Jet_leptonDeltaR
        
    readvars["Jet_nHEFrac"] = tree.Jet_nHEFrac     
    readvars["Jet_nEmEFrac"] = tree.Jet_nEmEFrac
    readvars["Jet_chargedMult"] = tree.Jet_chargedMult
        
    readvars["Jet_vtxPt"] = tree.Jet_vtxPt    
    readvars["Jet_vtxMass"] = tree.Jet_vtxMass 
    readvars["Jet_vtx3DVal"] = tree.Jet_vtx3DVal    
    readvars["Jet_vtxNtracks"] = tree.Jet_vtxNtracks 
    readvars["Jet_vtx3DSig"] = tree.Jet_vtx3DSig
        
    readvars["Jet_PartonFlav"] = tree.Jet_PartonFlav
    readvars["Jet_PartonPt"] = tree.Jet_PartonPt


    inputvar["Evt_Rho"] = readvars["Evt_Rho"]
    isbjet = False
    for ijet in range(readvars["N_Jets"]):
        if abs(readvars["Jet_Flav"][ijet]) == 5 and abs(readvars["Jet_PartonFlav"][ijet]) == 5:
            isbjet = True
            inputvars["Jet_Pt"] = readvars["Jet_Pt"][ijet]
            inputvars["Jet_corr"] = readvars["Jet_corr"][ijet]
            inputvars["Jet_Eta"] = readvars["Jet_Eta"][ijet]
            inputvars["Jet_Mt"] = readvars["Jet_Mt"][ijet]
            inputvars["Jet_leadTrackPt"] = readvars["Jet_leadTrackPt"][ijet]
            inputvars["Jet_leptonPt"] = readvars["Jet_leptonPt"][ijet]
            inputvars["Jet_leptonPt_all"] = readvars["Jet_leptonPt"][ijet]
            inputvars["Jet_leptonPtRel"] = readvars["Jet_leptonPtRel"][ijet]
            inputvars["Jet_leptonDeltaR"] = readvars["Jet_leptonDeltaR"][ijet]
            inputvars["Jet_nHEFrac"] = readvars["Jet_nHEFrac"][ijet]
            inputvars["Jet_nEmEFrac"] = readvars["Jet_nEmEFrac"][ijet]
            inputvars["Jet_chargedMult"] = readvars["Jet_chargedMult"][ijet]
            inputvars["Jet_vtxPt"] = readvars["Jet_vtxPt"][ijet]
            inputvars["Jet_vtxMass"] = readvars["Jet_vtxMass"][ijet]
            inputvars["Jet_vtx3DVal"] = readvars["Jet_vtx3DVal"][ijet]
            inputvars["Jet_vtxNtracks"] = readvars["Jet_vtxNtracks"][ijet]
            inputvars["Jet_vtx3DSig"] = readvars["Jet_vtx3DSig"][ijet]
            tmpdict = inputvars
            tmpdict.update(inputvar)

            #outputvars["Jet_regPt"] = jetreg.evalReg(tmpdict)
            outputvars["Jet_regPt"] = tree.Jet_regPt[ijet]
            outputvars["Jet_regcorr"] = outputvars["Jet_regPt"]/inputvars["Jet_Pt"]
            for key in inputplots_regcorr:
                inputplots_regcorr[key].FillCatHistos(inputvars[key],outputvars["Jet_regcorr"])
            for key in outputplots_regcorr:
                outputplots_regcorr[key].FillCatHistos(outputvars[key],outputvars["Jet_regcorr"])
            for key in outputplots_pt:
                outputplots_pt[key].FillCatHistos(outputvars[key],inputvars["Jet_Pt"])
            for key in outputplots_eta:
                outputplots_eta[key].FillCatHistos(outputvars[key],inputvars["Jet_Eta"])
            for key in outputplots_mt:
                outputplots_mt[key].FillCatHistos(outputvars[key],inputvars["Jet_Mt"])
            for key in outputplots_leppt:
                outputplots_leppt[key].FillCatHistos(outputvars[key], inputvars["Jet_leptonPt"])
            for key in outputplots_partonpt:
                outputplots_partonpt[key].FillCatHistos(outputvars[key], readvars["Jet_PartonPt"][ijet])
    if isbjet:
        for key in inputplot_regcorr:
            inputplot_regcorr[key].FillCatHistos(inputvar[key],outputvars["Jet_regcorr"])


outputfile = ROOT.TFile(outputfileprefix+"_regcorr"+".root","RECREATE")    
ROOT.gROOT.SetBatch(True)
outputfile.cd()


c1 = ROOT.TCanvas()
c1.cd()

for key in inputplot_regcorr:
    inputplot_regcorr[key].makeStack(">")
    inputplot_regcorr[key].WriteStack(c1)
for key in inputplots_regcorr:
    inputplots_regcorr[key].makeStack(">")
    inputplots_regcorr[key].WriteStack(c1)
for key in outputplots_regcorr:
    outputplots_regcorr[key].makeStack(">")
    outputplots_regcorr[key].WriteStack(c1)


PDFPrinting(outputfileprefix+'_regcorr',True,outputfile)

del outputfile


outputfile = ROOT.TFile(outputfileprefix+"_pt"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_pt:
    outputplots_pt[key].makeStack()
    outputplots_pt[key].WriteStack(c1)

PDFPrinting(outputfileprefix+'_pt',True,outputfile)

del outputfile


outputfile = ROOT.TFile(outputfileprefix+"_eta"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_eta:
    outputplots_eta[key].makeStack()
    outputplots_eta[key].WriteStack(c1)

PDFPrinting(outputfileprefix+'_eta',True,outputfile)

del outputfile

outputfile = ROOT.TFile(outputfileprefix+"_mt"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_mt:
    outputplots_mt[key].makeStack()
    outputplots_mt[key].WriteStack(c1)

PDFPrinting(outputfileprefix+'_mt',True,outputfile)

del outputfile

outputfile = ROOT.TFile(outputfileprefix+"_leppt"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_leppt:
    outputplots_leppt[key].makeStack()
    outputplots_leppt[key].WriteStack(c1)
    
PDFPrinting(outputfileprefix+'_leppt',True,outputfile)

del outputfile

outputfile = ROOT.TFile(outputfileprefix+"_partonpt"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_partonpt:
    outputplots_partonpt[key].makeStack()
    outputplots_partonpt[key].WriteStack(c1)
    
PDFPrinting(outputfileprefix+'_partonpt',True,outputfile)

del outputfile














