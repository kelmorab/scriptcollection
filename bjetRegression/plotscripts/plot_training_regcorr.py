import ROOT
from plotting import *
from rootutils import PDFPrinting
import bRegVars as bR
from JetRegression import JetRegression 
import glob
from exporthistos import *


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);


outputvars = bR.outputvars 
inputjetvars = bR.inputvars 
inputevtvars = bR.inputvar


inputfile = {"ttHbb" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root")}
#             "ttbar" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttbar.root")}

weightpath = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/weights"


weightfiles = glob.glob(weightpath+"/*.xml")
print weightfiles

trainings = ["Target: p_{T, Parton}, nCuts: 20", "Target: p_{T,Jet} / p_{T,Parton}, nCuts: 20","Target: p_{T, Parton}, nCuts: 40"]
flag = [False, True, False]

outputhistos = {}
for key in outputvars:
    outputhistos.update({key : normPlots(key, True, len(trainings), trainings )})
    outputhistos[key].addLabel(0.92,0.325,"nTrees: 200, Shrinkage: 0.1, MaxDepth: 3",90,0.03)
    #outputhistos[key].setmanualegendsize("right",0.6,0.3,0.88,0.88)
    #outputhistos[key].setmanualegendsize("left",0.13,0.3,0.43,0.83)


raw_input("Press Ret")
for isample,sample in enumerate(inputfile):
    print "Procession Sample:",sample
    for iweight, weightfile in enumerate(weightfiles):
        print "Procession Regression "+str(iweight)+" of "+str(len(trainings)-1)
        regression = JetRegression(weightfile)

        tree = inputfile[sample].Get("MVATree")
        
        for iev in range(tree.GetEntries()):
            if iev%10000 == 0:
                print iev
            if iev == 10000:
                break
            tree.GetEvent(iev)

            inputevtvars["Evt_Rho"] = tree.Evt_Rho
            for ijet in range(tree.N_Jets):
                if abs(tree.Jet_PartonFlav[ijet]) == 5 and abs(tree.Jet_Flav[ijet]) == 5:
                    inputjetvars["Jet_Pt"] = tree.Jet_Pt[ijet]
                    inputjetvars["Jet_corr"] = tree.Jet_corr[ijet]
                    inputjetvars["Jet_Eta"] = tree.Jet_Eta[ijet]
                    inputjetvars["Jet_Mt"] = tree.Jet_Mt[ijet]
                    inputjetvars["Jet_leadTrackPt"] = tree.Jet_leadTrackPt[ijet]
                    inputjetvars["Jet_leptonPt"] = tree.Jet_leptonPt[ijet]
                    inputjetvars["Jet_leptonPt_all"] = tree.Jet_leptonPt[ijet]
                    inputjetvars["Jet_leptonPtRel"] = tree.Jet_leptonPtRel[ijet]
                    inputjetvars["Jet_leptonDeltaR"] = tree.Jet_leptonDeltaR[ijet]
                    #inputjetvars["Jet_nHEFrac"] = tree.Jet_nHEFrac[ijet]
                    #inputjetvars["Jet_nEmEFrac"] = tree.Jet_nEmEFrac[ijet]
                    inputjetvars["Jet_chargedMult"] = tree.Jet_chargedMult[ijet]
                    inputjetvars["Jet_vtxPt"] = tree.Jet_vtxPt[ijet]
                    inputjetvars["Jet_vtxMass"] = tree.Jet_vtxMass[ijet]
                    inputjetvars["Jet_vtx3DVal"] = tree.Jet_vtx3DVal[ijet]
                    inputjetvars["Jet_vtxNtracks"] = tree.Jet_vtxNtracks[ijet]
                    inputjetvars["Jet_vtx3DSig"] = tree.Jet_vtx3DSig[ijet]

                    inputvars = inputjetvars
                    inputvars.update(inputevtvars)

                    regout = regression.evalReg(inputvars)
                    if flag[iweight]:
                        outputhistos["Jet_regPt"].FillnormHisto((1/regout)*inputjetvars["Jet_Pt"],iweight)
                        outputhistos["Jet_regcorr"].FillnormHisto(1/regout,iweight)
                    else:
                        outputhistos["Jet_regPt"].FillnormHisto(regout,iweight)
                        outputhistos["Jet_regcorr"].FillnormHisto(regout/inputjetvars["Jet_Pt"],iweight)
                    
        del regression
        #if iweight == 0:
        #    break
    #####
    c1 = ROOT.TCanvas()
    c1.cd()

    postfix = "4"
    
    outputfile = ROOT.TFile(key+"regcorrtraining"+postfix+".root","RECREATE")
    outputfile.cd()
    

    
    pdfout = PDFPrinting(sample+"regcorrtraining"+postfix)
    
    print sample
    
    histosforexport = []

    for histokey  in outputhistos:
        outputhistos[histokey].WriteHisto(c1, sample, False, False, pdfout)
        histosforexport.append(outputhistos[histokey])

    pdfout.closePDF()

    exporthistos("exported", histosforexport)
    
    del c1


