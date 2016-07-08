import ROOT

from plotting import *
from rootutils import PDFPrinting

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)


filepath = "/nfs/dust/cms/user/kschweig/JetRegression/trees0612/ttHbb.root"

rfile = ROOT.TFile(filepath)

tree = rfile.Get("MVATree")

postfixes = [ "_0612_0" ,"_0612_1" ,"_0612_2" ,"_0612_3" ,"_0612_4" ,"_0612_5" ,"_0612_6" ,"_0612_7" ,"_0612_8" ,"_0612_9" ,"_0612_10" ,"_0612_11",""]
prefix = "Evt_MCregbbMass"

bbMass = normPlots("MC bb Mass (GeV)",True,len(postfixes)+1,["noreg"] + postfixes, [100,50,250])
regout = normPlots("Regression correction Factor",True,len(postfixes),postfixes, [96,0.6,1.6])
regpt = normPlots("p_{T} of regressed Jet",True,len(postfixes)+1,["noreg"]+postfixes, [150,0,300])
bbMass.setmanualegendsize("right",0.6,0.5,0.88,0.88)

bbMass.projecttoHisto(0,tree,"Evt_MCbbMass","Evt_MCbbMass > 0","")
regpt.projecttoHisto(0,tree,"Jet_Pt","Jet_regPt > 0","")

for ip, postfix in enumerate(postfixes):
    bbMass.projecttoHisto(ip+1,tree,prefix+postfix, "Evt_MCbbMass > 0","")
    regout.projecttoHisto(ip,tree,"Jet_regcorr"+postfix, "Jet_regcorr > 0","")
    regpt.projecttoHisto(ip+1,tree,"Jet_regPt"+postfix,"Jet_regPt > 0","")

outname = "plotbbMass_0612_trainings"
outfile = ROOT.TFile(outname+".root","RECREATE")
pdfout = PDFPrinting(outname)
c1 = ROOT.TCanvas()

bbMass.WriteHisto(c1,"ttHbb",False,False,pdfout,False, None, False, False, None, True)
regout.WriteHisto(c1,"ttHbb",False,False,pdfout)
regpt.WriteHisto(c1,"ttHbb",False,False,pdfout)

pdfout.closePDF()


