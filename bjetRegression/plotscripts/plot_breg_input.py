import ROOT
from plotting import *
from rootutils import PDFPrinting
import bRegVars as bR

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);


inputjetvars = bR.inputvars 
inputevtvars = bR.inputvar

inputfile = {"ttHbb" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root"),
             "ttbar" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttbar.root")}

sample = "ttHbb"


inputjethistos = {}
inputevthistos = {}
for key in inputjetvars:
    inputjethistos.update({key : normPlots(key, True, 2, ["t#bar{t}H, H #rightarrow b#bar{b}","t#bar{t}"])})
for key in inputevtvars:
    inputevthistos.update({key : normPlots(key, True, 2, ["t#bar{t}H, H #rightarrow b#bar{b}","t#bar{t}"])})

corr_eta_list = [{"Jet_corr": CatPlots("Jet_corr", [-2.4,-1.5,-0.75,-0.25,0.25,0.75,1.5,2.4],"jeteta","#eta",False,False, "ttHbb")},
                 {"Jet_corr": CatPlots("Jet_corr", [-2.4,-1.5,-0.75,-0.25,0.25,0.75,1.5,2.4],"jeteta","#eta",False,False, "ttbar")}]


for ikey,key in enumerate(inputfile):
    tree = inputfile[key].Get("MVATree")
    print "Procession Sample:",key
    for iev in range(tree.GetEntries()):
        if iev <= 100000:
            if iev%10000 == 0:
                print iev
        else:
            if iev%50000 == 0:
                print iev
        if iev == 2000000:
            break
        tree.GetEvent(iev)


        inputevtvars["Evt_Rho"] = tree.Evt_Rho
        isbjet = False
        for ijet in range(tree.N_Jets):
            if abs(tree.Jet_PartonFlav[ijet]) == 5 and abs(tree.Jet_Flav[ijet]) == 5:
                isbjet = True
                inputjetvars["Jet_Pt"] = tree.Jet_Pt[ijet]
                inputjetvars["Jet_corr"] = tree.Jet_corr[ijet]
                inputjetvars["Jet_Eta"] = tree.Jet_Eta[ijet]
                inputjetvars["Jet_Mt"] = tree.Jet_Mt[ijet]
                inputjetvars["Jet_leadTrackPt"] = tree.Jet_leadTrackPt[ijet]
                inputjetvars["Jet_leptonPt"] = tree.Jet_leptonPt[ijet]
                inputjetvars["Jet_leptonPt_all"] = tree.Jet_leptonPt[ijet]
                inputjetvars["Jet_leptonPtRel"] = tree.Jet_leptonPtRel[ijet]
                inputjetvars["Jet_leptonDeltaR"] = tree.Jet_leptonDeltaR[ijet]
                inputjetvars["Jet_nHEFrac"] = tree.Jet_nHEFrac[ijet]
                inputjetvars["Jet_nEmEFrac"] = tree.Jet_nEmEFrac[ijet]
                inputjetvars["Jet_chargedMult"] = tree.Jet_chargedMult[ijet]
                inputjetvars["Jet_vtxPt"] = tree.Jet_vtxPt[ijet]
                inputjetvars["Jet_vtxMass"] = tree.Jet_vtxMass[ijet]
                inputjetvars["Jet_vtx3DVal"] = tree.Jet_vtx3DVal[ijet]
                inputjetvars["Jet_vtxNtracks"] = tree.Jet_vtxNtracks[ijet]
                inputjetvars["Jet_vtx3DSig"] = tree.Jet_vtx3DSig[ijet]
                for key in inputjethistos:
                    inputjethistos[key].FillnormHisto(inputjetvars[key],ikey)
                corr_eta_list[ikey]["Jet_corr"].FillCatHistos(inputjetvars["Jet_corr"],inputjetvars["Jet_Eta"])
        if isbjet:
                for key in inputevthistos:
                    inputevthistos[key].FillnormHisto(inputevtvars[key],ikey)

inputhistos = inputjethistos
inputhistos.update(inputevthistos)

c1 = ROOT.TCanvas()
c1.cd()

postfix = "_test"

outputfile = ROOT.TFile(sample+"inputvars"+postfix+".root","RECREATE")
outputfile.cd()

pdfout = PDFPrinting(sample+"inputvars"+postfix)

fillhisto = False

for key in inputhistos:
    inputhistos[key].WriteHisto(c1, None, fillhisto, True, pdfout)

keylist = []
for key in inputfile:
    keylist.append(key)

for ih, Cathist in enumerate(corr_eta_list):
    Cathist["Jet_corr"].makeStack()
    Cathist["Jet_corr"].WriteStack(c1, pdfout)

pdfout.closePDF()


#PDFPrinting(sample+"inputvars"+postfix,True,outputfile)
