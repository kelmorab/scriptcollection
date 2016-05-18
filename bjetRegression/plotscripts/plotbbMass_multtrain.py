import ROOT
import glob
import sys
import os
from array import array
#################################
from plotting import *
from rootutils import PDFPrinting
#################################
parentpath = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
sys.path.append(parentpath)
from regressionTools import *



path = "/nfs/dust/cms/user/kschweig/JetRegression/trees0511/ttHbb/"
outputname = "multitrain_plots_0512_2"

f = ROOT.TChain("MVATree")

for infile in glob.glob(path+"*.root"):
    f.Add(infile)


tree = f

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)
#################################################
weights = ["std" , "wPU", "nocorr", "nocorrandfrac","noelfrac","nohadfrac","heppy","heppy1200","heppy600","changedsettings"]
#weights = ["std" , "nohadfrac","heppy"]
histos_regcorr = []
histos_bbMass = []
histos_bbMass0Lep = []
histos_bbMass1Lep = []
histos_bbMass2Lep = []


for w in weights:
    if w is "std":
        w = ""
    else:
        w = "_"+w
    histos_regcorr.append(  ROOT.TH1F("regcorr"+w,"regcorr"+w,50,0.4,1.6)  )
    histos_bbMass.append(  ROOT.TH1F("bbMass"+w,"bbMass"+w,150,50,250)  )
    histos_bbMass0Lep.append(  ROOT.TH1F("bbMass0Lep"+w,"bbMass0Lep"+w,150,50,250)  )
    histos_bbMass1Lep.append(  ROOT.TH1F("bbMass1Lep"+w,"bbMass1Lep"+w,150,50,250)  )
    histos_bbMass2Lep.append(  ROOT.TH1F("bbMass2Lep"+w,"bbMass2Lep"+w,150,50,250)  )

for w in weights:
    if w is "std":
        w = ""
    else:
        w = "_"+w
    tree.Project("regcorr"+w,"Jet_regcorr"+w)
    tree.Project("bbMass"+w,"Evt_MCregbbMass"+w)
    tree.Project("bbMass0Lep"+w,"Evt_MCregbbMass0Lep"+w)
    tree.Project("bbMass1Lep"+w,"Evt_MCregbbMass1Lep"+w)
    tree.Project("bbMass2Lep"+w,"Evt_MCregbbMass2Lep"+w)


regcorr_param = [50,0.4,1.6]
bbMass_param = [150,50,205]

legend = ["Std. Training","Std. Training w/ PU Weight","Std. Training w/o JEC corr.","Std. Training w/o JEC corr and Fracs","Std. Training w/o em Frac","Std. Training w/o had Frac","Heppy Training","Heppy Training w/ 1200 Trees","Heppy Training w/ 600 Trees","Heppy Training w/ 1200 Trees and 30 cuts",] 
#legend = ["Std. Training","Training w/o had Frac","Heppy Training"] 

plots_regcorr = normPlots("Regression correction factor",True,len(legend),legend,regcorr_param)
plots_bbMass = normPlots("MC Higgs Mass",True,len(legend),legend,bbMass_param)
plots_bbMass0Lep =normPlots("MC Higgs Mass w/ 0 matched Leptons",True,len(legend),legend,bbMass_param)
plots_bbMass1Lep = normPlots("MC Higgs Mass w/ 1 matched Lepton",True,len(legend),legend,bbMass_param)
plots_bbMass2Lep =normPlots("MC Higgs Mass w/ 2 matched Leptons",True,len(legend),legend,bbMass_param)

plots_regcorr.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
plots_bbMass.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
plots_bbMass0Lep.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
plots_bbMass1Lep.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
plots_bbMass2Lep.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])


plots_regcorr.setmanualegendsize("left",0.13,0.55,0.51,0.83)
plots_bbMass.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plots_bbMass0Lep.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plots_bbMass1Lep.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plots_bbMass2Lep.setmanualegendsize("right",0.55,0.65,0.88,0.88)


#plots_regcorr.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
#plots_bbMass.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
#plots_bbMass0Lep.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
#plots_bbMass1Lep.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
#plots_bbMass2Lep.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])


plot_quadrdev = PointPlot(len(legend),"Quadratic Deviation Target-Ouput",legend)
plot_quadrdev.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_quadrdev.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
plot_R2 = PointPlot(len(legend),"R^{2} Statistic",legend,)
plot_R2.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_R2.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
plot_errsqu = PointPlot(len(legend),"Error with squared loss function",legend)
plot_errsqu.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_errsqu.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
plot_errabs = PointPlot(len(legend),"Error with abs. loss function",legend)
plot_errabs.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_errabs.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
plot_RSS = PointPlot(len(legend),"Residual sum of squares (RSS)",legend)
plot_RSS.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_RSS.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
plot_TSS = PointPlot(len(legend),"Total sum of squares (TSS)",legend)
plot_TSS.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_TSS.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])
plot_RSE = PointPlot(len(legend),"Residual standard error (RSE)",legend)
plot_RSE.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
#plot_RSE.changeColorlist([ROOT.kBlack, ROOT.kOrange-3,ROOT.kBlue-6])




plot_quadrdev.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_R2.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_errsqu.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_errabs.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_RSS.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_TSS.setmanualegendsize("right",0.55,0.65,0.88,0.88)
plot_RSE.setmanualegendsize("right",0.55,0.65,0.88,0.88)






nEntries = tree.GetEntries()

outputarrays = []
outputvalues = []
targetvalues = []
deviations = []
errors = []

for iw in range(len(weights)):
    outputvalues.append([])
    outputarrays.append(array('f',20*[0]))
    deviations.append(0)
    errors.append(Errors())

    
MatchedPartonPt = array('f',20*[0])
JetPt = array('f',20*[0])
nJets = array('i',[0])

tree.SetBranchAddress("Jet_MatchedPartonPt",MatchedPartonPt)
tree.SetBranchAddress("Jet_Pt",JetPt)
tree.SetBranchAddress("N_Jets",nJets)

for iw,w in enumerate(weights):
    if w == "std":
        w = ""
    else:
        w = "_"+w
    tree.SetBranchAddress("Jet_regcorr"+w, outputarrays[iw])


print "Processing Entries for quadr. Deviation"
for n in range(nEntries):
    if n % 50000 == 0:
        print n
    if n == 10:
        pass
        #break
    tree.GetEvent(n)
    for i in range(nJets[0]):        
        #print nJets[0]
        #print outputarrays[0]
        #print JetPt
        #print MatchedPartonPt
        if outputarrays[0][i] > 0 and MatchedPartonPt[i] > 0:
            for iw, w in enumerate(weights):
                outputvalues[iw].append(outputarrays[iw][i])
                errors[iw].addevent(outputarrays[iw][i],(MatchedPartonPt[i]/JetPt[i]))
            targetvalues.append(MatchedPartonPt[i]/JetPt[i])
        

for iw, w in enumerate(weights):
    print "Computing deviation for",w
    for iv,value in enumerate(outputvalues[iw]):
        deviations[iw] = deviations[iw] + (  ( value - targetvalues[iv] ) * ( value - targetvalues[iv] )  )
    deviations[iw] = deviations[iw] / len(outputvalues[iw])
    print "Deviation for",w," = ",deviations[iw]
for dev in deviations:
    plot_quadrdev.addPoint(dev)



for i in range(len(weights)):
    errors[i].printerr()
    errvals = errors[i].getvalues()
    plots_regcorr.AddTH1F(histos_regcorr[i],i)
    plots_bbMass.AddTH1F(histos_bbMass[i],i)
    plots_bbMass0Lep.AddTH1F(histos_bbMass0Lep[i],i)
    plots_bbMass1Lep.AddTH1F(histos_bbMass1Lep[i],i)
    plots_bbMass2Lep.AddTH1F(histos_bbMass2Lep[i],i)
    plot_R2.addPoint(errvals["R^2"])
    plot_errabs.addPoint(errvals["err_abs_loss"])
    plot_errsqu.addPoint(errvals["err_squared_loss"])
    plot_RSS.addPoint(errvals["RSS"])
    plot_TSS.addPoint(errvals["TSS"])
    plot_RSE.addPoint(errvals["RSE"])
    

pdfout= PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()    

#for i in range(len(weights)):
plots_regcorr.WriteHisto(c1,"ttHbb",False,False,pdfout)
plots_bbMass.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
plots_bbMass0Lep.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
plots_bbMass1Lep.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
plots_bbMass2Lep.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
#plot_quadrdev.WritePointPlot(c1,"ttHbb",pdfout, [52.1,52.15])
plot_quadrdev.WritePointPlot(c1,"ttHbb",pdfout)
plot_R2.WritePointPlot(c1,"ttHbb",pdfout,[0.135,0.3],"Max")
plot_errabs.WritePointPlot(c1,"ttHbb",pdfout)
plot_errsqu.WritePointPlot(c1,"ttHbb",pdfout)
plot_RSS.WritePointPlot(c1,"ttHbb",pdfout)
plot_TSS.WritePointPlot(c1,"ttHbb",pdfout)
plot_RSE.WritePointPlot(c1,"ttHbb",pdfout)
pdfout.closePDF()
