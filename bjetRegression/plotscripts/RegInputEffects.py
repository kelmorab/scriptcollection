

import ROOT
from JetRegression import JetRegression
from plotting import *
from rootutils import PDFPrinting

ROOT.gROOT.SetBatch(True)

inputfile = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root")
weightfile = "/afs/desy.de/user/h/hmildner/public/regression_weights/weights_ttbar_quark/TMVARegression_BDTG.weights.xml"

outputfileprefix = "ttHbb_0214"

tree = inputfile.Get("MVATree")

readvars = {"N_Jets" : 0,
            "Evt_Rho": 0,
            "Jet_Pt" : [],
            "Jet_corr" : [],
            "Jet_Eta" : [],
            "Jet_Mt" : [],
            "Jet_leadTrackPt" : [],
            "Jet_Flav" : [],
            "Jet_leptonPt" : [],
            "Jet_leptonPtRel" : [],
            "Jet_leptonDeltaR" : [],
            "Jet_nHEFrac" : [],
            "Jet_nEmEFrac" : [],
            "Jet_chargedMult" : [],
            "Jet_vtxPt" : [],
            "Jet_vtxMass" : [],
            "Jet_vtx3DVal" : [],
            "Jet_vtxNtracks" : [],
            "Jet_vtx3DSig" : [],
            "Jet_PartonFlav" : [],
            "Jet_PartonPt" : []}

inputvar = {"Evt_Rho": 0}

inputvars = {"Jet_Pt" : [],
             "Jet_corr" : [],
             "Jet_Eta" : [],
             "Jet_Mt" : [],
             "Jet_leadTrackPt" : [],
             "Jet_leptonPt" : [],
             "Jet_leptonPtRel" : [],
             "Jet_leptonDeltaR" : [],
             "Jet_nHEFrac" : [],
             "Jet_nEmEFrac" : [],
             "Jet_chargedMult" : [],
             "Jet_vtxPt" : [],
             "Jet_vtxMass" : [],
             "Jet_vtx3DVal" : [],
             "Jet_vtxNtracks" : [],
             "Jet_vtx3DSig" : []}

outputvars = {"Jet_regPt": [],
              "Jet_regcorr" : []}

#jetreg = JetRegression(weightfile) 

inputplots_regcorr = {}
inputplot_regcorr = {}
outputplots_regcorr = {}
outputplots_pt = {}
outputplots_mt = {}
outputplots_leppt = {}
outputplots_partonpt = {}

#Categorize by regcorr factor
for key in inputvar:                           
    inputplot_regcorr.update({key : CatPlots(key, [0,0.55,0.65,0.75,0.85,0.95,1,1.05,1.15,1.25,1.35,1.45,2],"regcorr",True,True)})
for key in inputvars:    
    inputplots_regcorr.update({key : CatPlots(key, [0,0.55,0.65,0.75,0.85,0.95,1,1.05,1.15,1.25,1.35,1.45,2],"regcorr",True,True)})
for key in outputvars:    
    outputplots_regcorr.update({key : CatPlots(key,[0,0.55,0.65,0.75,0.85,0.95,1,1.05,1.15,1.25,1.35,1.45,2],"regcorr",True,True)})
#Categorize by Jet_pt
for key in outputvars:    
    outputplots_pt.update({key : CatPlots(key, [0,50,75,100,150,200,300,600],"jetpt",False,False)})
for key in outputvars:    
    outputplots_mt.update({key : CatPlots(key, [0,50,75,100,150,200,400,600],"jetmt",False,False)})
#Categorize by Jet_lepton_pt
for key in outputvars:    
    outputplots_leppt.update({key : CatPlots(key, [0,30,50,80,100,120],"jetleppt",False,False)})
#Categorize by PartonPt
for key in outputvars:
    outputplots_partonpt.update({key : CatPlots(key, [0,50,75,100,150,200,300,800],"jetpartonpt",False,False)})




for iev in range(tree.GetEntries()):
    if iev%10000 == 0:
        print iev
    if iev == 100000:
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














