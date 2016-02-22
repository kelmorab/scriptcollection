import ROOT
from plotting2 import *
from rootutils import PDFPrinting
import bRegVars as bR
from JetRegression import JetRegression 
import glob

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);


outputvars = bR.outputvars 
inputjetvars = bR.inputvars 
inputevtvars = bR.inputvar


inputfile = {"ttHbb" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root")}
#             "ttbar" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttbar.root")}

weightpath = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0211_testing/weights"

weightfiles = glob.glob(weightpath+"/*.xml")
print weightfiles

trainings = []

nTrees_list = [" 200"," 600","1000","1400"]
Shrinkage_list = [0.1,0.5]
nCuts_list = [20]
MaxDepth_list = [2,3]

for nTrees in nTrees_list:
    for shrink in Shrinkage_list:
        for maxdepth in MaxDepth_list:
            for nCuts in nCuts_list:
                trainings.append("1: "+str(nTrees)+" | 2: "+str(shrink)+ " | 3: "+str(maxdepth)+" | 4: "+str(nCuts))
print trainings
print len(trainings)
outputhistos = {}
for key in outputvars:
    outputhistos.update({key : normPlots(key, True, len(trainings), trainings)})
    outputhistos[key].addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
    outputhistos[key].setmanualegendsize("right",0.6,0.3,0.88,0.88)
    outputhistos[key].setmanualegendsize("left",0.13,0.3,0.43,0.83)


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
            if iev == 150000:
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

                    regpt = regression.evalReg(inputvars)

                    outputhistos["Jet_regPt"].FillnormHisto(regpt,iweight)
                    outputhistos["Jet_regcorr"].FillnormHisto(regpt/inputjetvars["Jet_Pt"],iweight)
                    
        del regression
        #if iweight == 0:
        #    break
    #####
    c1 = ROOT.TCanvas()
    c1.cd()

    postfix = ""
    
    outputfile = ROOT.TFile(key+"inputvars"+postfix+".root","RECREATE")
    outputfile.cd()

    pdfout = PDFPrinting(sample+"trainingcomp"+postfix)
    
    print sample
    
    for histokey  in outputhistos:
        outputhistos[histokey].WriteHisto(c1, sample, False, False, pdfout)

    pdfout.closePDF()
    
    del c1


