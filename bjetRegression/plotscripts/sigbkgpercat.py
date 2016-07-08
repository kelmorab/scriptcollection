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

ttHlocation= "/nfs/dust/cms/user/kschweig/JetRegression/trees0627/ttHbb"
ttbarlocation = "/nfs/dust/cms/user/kschweig/JetRegression/trees0627/ttbar_incl"


tth = ['t#bar{t}H',ROOT.kBlue+1 , '*20']
ttl = ['t#bar{t}+l',ROOT.kRed-7,'*(GenEvt_I_TTPlusCC==0&&GenEvt_I_TTPlusBB==0)']
ttc = ['t#bar{t}+c#bar{c}',ROOT.kRed,'*(GenEvt_I_TTPlusCC==1)']
ttb = ['t#bar{t}+b',ROOT.kRed+2,'*(GenEvt_I_TTPlusBB==1)']
tt2b = ['t#bar{t}+2b',ROOT.kRed+3,'*(GenEvt_I_TTPlusBB==2)']
ttbb = ['t#bar{t}+b#bar{b}',ROOT.kRed+4,'*(GenEvt_I_TTPlusBB==3)']








outputname = "sigbkgpercat_0701"

regressions = ["Jet_regcorr","Jet_regcorr_new","Jet_regcorr_genJet"]
regressionlabels = ["Standard settings","Corrected fractions","Target: GenJet p_{T} ratio"]
plotbinning = [[70,0.6,1.6],[70,0.6,1.6],[70,0.85,1.45]]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#

ttHtree = TChain("MVATree")
ttbartree = TChain("MVATree")
for f in glob(ttHlocation+"/*.root"):   
    print f
    ttHtree.Add(f)
for f in glob(ttbarlocation+"/*.root"):    
    print f
    ttbartree.Add(f)

boosted = "0"
Evt = "2*(Evt_Odd == 0)"
weight = "Weight"
selection= [Evt+"*"+weight+ttl[2],
            Evt+"*"+weight+ttc[2],
            Evt+"*"+weight+ttb[2],
            Evt+"*"+weight+tt2b[2],
            Evt+"*"+weight+ttbb[2],
            Evt+"*"+weight+tth[2]]

catsel=["*((N_Jets>=6&&N_BTagsM>=4)&&!"+boosted+")",
        "*((N_Jets>=6&&N_BTagsM==2)&&!"+boosted+")",
        "*((N_Jets==4&&N_BTagsM==3)&&!"+boosted+")",
        "*((N_Jets==5&&N_BTagsM==3)&&!"+boosted+")",
        "*((N_Jets>=6&&N_BTagsM==3)&&!"+boosted+")",
        "*((N_Jets==4&&N_BTagsM>=4)&&!"+boosted+")",
        "*((N_Jets==5&&N_BTagsM>=4)&&!"+boosted+")",             
    ]

cats = ["6J4T",
        "6J2T",
        "4J3T",
        "5J3T",
        "6J3T",
        "4J4T",
        "5J4T" ]

pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()

usetree = [1,1,1,1,1,0]

for isel, sel in enumerate(catsel):
    print "Processing:",cats[isel]
    ltext = [ttl[0],ttc[0],ttb[0],tt2b[0],ttbb[0],"20 x "+tth[0]]
    clist = [ttl[1],ttc[1],ttb[1],tt2b[1],ttbb[1],tth[1]]
    Stack = StackPlots("BDT Output",6,ltext,5*["Box"]+["Line"],[20,-1,1],True)
    Stack.addLabel(0.02,0.025,"Category: "+cats[isel],0,0.04)
    Stack.setmanualegendsize("right",0.7,0.58,0.88,0.88)
    Stack.changeColorlist(clist)
    for i in range(len(usetree)):
        if usetree[i] == 1:
            tree = ttbartree
        else:
            tree = ttHtree
        Stack.projecttoHisto(i,tree,"BDT_common5_output",selection[i] + sel + "*1")
    Stack.WriteHisto(c1,None,False,pdfout, None, False,False,0.1)
    del Stack

pdfout.closePDF()



