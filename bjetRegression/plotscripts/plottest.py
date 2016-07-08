from plotting import *
from rootutils import PDFPrinting

import ROOT


ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)


outputname = "plottest"

tfile = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0620_ttHttbar/ttHbb.root")

tree = tfile.Get("MVATree")


plots = normPlots("Higgs Mass",True,2,["Parton Pt","GenJetwNu Pt"],[60,100,160])
plots.projecttoHisto(0,tree,"Evt_MCregbbMass","Evt_MCregbbMass > 0")
plots.projecttoHisto(1,tree,"Evt_MCregbbMass_genJet_pF","Evt_MCregbbMass > 0")

pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()

plots.WriteHisto(c1,"ttHbb",False,False,pdfout)
pdfout.closePDF()
