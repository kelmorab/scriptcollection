import ROOT
from glob import glob
import sys
import os


from plotscripts.plotting import *
from plotscripts.rootutils import PDFPrinting

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)


path = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/"
wildcard = "BReg_0612*.root"

filelist = glob(path+wildcard)

legend = []
for f in filelist:
    legend.append(os.path.basename(f.split(".")[0]))
print filelist
print legend


BDTOutput = normPlots("BDT Output (GeV)", True, len(legend), legend, [50,0.4,1.6])

for ifile,outfile in enumerate(filelist):

    print outfile
    rootfile = ROOT.TFile(outfile)
    tree = rootfile.Get("TestTree")
    print tree
    BDTOutput.projecttoHisto(ifile,tree,"BDTG")
    
    del rootfile,tree


outname = "plotTMVAOutput_0612"
outfile = ROOT.TFile(outname+".root","RECREATE")
pdfout = PDFPrinting(outname)
c1 = ROOT.TCanvas()

BDTOutput.WriteHisto(c1,"ttbar",False,False,pdfout)

pdfout.closePDF()
