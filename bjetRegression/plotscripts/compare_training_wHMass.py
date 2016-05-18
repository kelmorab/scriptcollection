from __future__ import division

import ROOT
from plotting import *
from rootutils import PDFPrinting
import bRegVars as bR
from JetRegression import JetRegression 
from math import sqrt
import sys
import os

#-------------------------------------------------------------------------------------#
#
#Add path to bjetreg folder to path, that scripts from there can be used
parentpath = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
#bjetregpath = parentpath+"/"+"bjetRegression"

print parentpath
#print bjetregpath
sys.path.append(parentpath)
from regressionTools import *

#
#-------------------------------------------------------------------------------------#



ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);


outputvars = bR.outputvars 
inputjetvars = bR.inputvars 
inputevtvars = bR.inputvar

outputname = "regression_comparison_test_1_0405"

inputfile = {"ttHbb" : ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0330/ttHbb.root")}

weightpath = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/weights/"


newSpectators_ratio = ["Jet_MatchedPartonPt",
                       "Jet_MatchedPartonFlav" ,
                       "Jet_PartonFlav" ,
                       "Jet_Flav" ,
                       "Evt_Odd" ,
                       "Evt_Rho"]

oldSpectators_ratio = ["Jet_MatchedPartonPt",
                       "Jet_MatchedPartonFlav" ,
                       "Jet_Flav" ,
                       "Evt_Odd" ,
                       "N_PrimaryVertices",
                       "Jet_totHEFrac", 
                       "Jet_nEmEFrac"]


newSpectators = ["Jet_MatchedPartonFlav" ,
                 "Jet_PartonFlav" ,
                 "Jet_Flav" ,
                 "Evt_Odd" ,
                 "Evt_Rho"]

oldSpectators = ["Jet_MatchedPartonFlav" ,
                 "Jet_Flav" ,
                 "Evt_Odd" ,
                 "N_PrimaryVertices",
                 "Jet_totHEFrac", 
                 "Jet_nEmEFrac"]



weights = {"Normal" : ["TMVARegression_0329_newVars_BDTG.weights.xml","TMVARegression_0329_oldVars_BDTG.weights.xml"],
           "Ratio" : ["TMVARegression_0330_newVars_BDTG.weights.xml","TMVARegression_0330_oldVars_BDTG.weights.xml"]}

weights_add = {"Normal" : [[newSpectators,"New"],
                           [oldSpectators,"Old"]],
               "Ratio" : [[newSpectators_ratio,"New"],
                          [oldSpectators_ratio,"Old"]]}



binning_outputdev_target = {"Normal" : [250,0,700], "Ratio" : [150,0,4.5]}
binning_outputdev_dev = {"Normal" : [400,-400,300], "Ratio" : [200,-4,0.7]}

binning_outputdev_zoom_target = {"Normal" : [100,20,150], "Ratio" : [100,0.6,1.5]}
binning_outputdev_zoom_dev = {"Normal" : [100,-50,50], "Ratio" : [100,-0.4,0.4]}




outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()

pdfout = PDFPrinting(outputname)
c1 = ROOT.TCanvas()



for isample,sample in enumerate(inputfile):
    print "Procession Sample:",sample
    
    

    setflag = False

    legend_all = ["New input variables (Target: p_{T} Ratio)", "Old input variables (Target: p_{T} Ratio)","New input variables (Target: p_{T})", "Old input variables (Target: p_{T})"]

    ptregplot_all = normPlots("Jet_regPt",True,4,legend_all,[150,0,500])
    ptcorrplot_all = normPlots("Jet_regcorr",True,4,legend_all)
    mHplot_all = normPlots("inv. Mass of Higgs (GeV)",True,5,["no Regression"]+legend_all,[125,50,250])
    
    ptregplot_all.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])
    ptcorrplot_all.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])
    mHplot_all.changeColorlist([ROOT.kBlack,ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])

    ptregplot_all.setmanualegendsize("right",0.55,0.55,0.88,0.88)
    ptcorrplot_all.setmanualegendsize("left",0.13,0.5,0.41,0.83)
    mHplot_all.setmanualegendsize("right",0.55,0.55,0.88,0.88)


    avquaddevplot_all_normal = PointPlot(4,"Av. quadr. deviation (GeV)",legend_all)
    avquaddevplot_all_normal.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])

    avquaddevplot_all_ratio = PointPlot(4,"Av. quadr. deviation",legend_all)
    avquaddevplot_all_ratio.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])

    avquaddevplot_all_normal_fromhisto = PointPlot(4,"Av. quadr. deviation (GeV)",legend_all)
    avquaddevplot_all_normal_fromhisto.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])

    avquaddevplot_all_ratio_fromhisto = PointPlot(4,"Av. quadr. deviation",legend_all)
    avquaddevplot_all_ratio_fromhisto.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])


    nhisto_all = 0
    
    for version in weights:
        #1D Histograms 
        ptregplot = normPlots("Jet_regPt",True,2,["New input variables", "Old input variables"],[150,0,500])
        ptcorrplot = normPlots("Jet_regcorr",True,2,["New input variables", "Old input variables"])
        mHplot = normPlots("inv. Mass of Higgs (GeV)",True,2,["New input variables", "Old input variables"],[125,50,250])
        
        if version == "Normal":
            labeltext = "Target: p_{T} of matched Parton"
        else:
            labeltext = "Target: p_{T} Ratio between Parton and Jet"
        
        ptregplot.addLabel(0.04,0.03,labeltext,0,0.035)
        ptcorrplot.addLabel(0.04,0.03,labeltext,0,0.035)
        mHplot.addLabel(0.04,0.03,labeltext,0,0.035)

        ptregplot.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])
        ptcorrplot.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])
        mHplot.changeColorlist([ROOT.kViolet+9, ROOT.kPink-1,ROOT.kOrange-3,ROOT.kSpring-5])

        #Set Graph plots
        avquaddevplot = PointPlot(2,"Av. quadr. deviation",["New variables","Old variables"])

        avquaddevplot.addLabel(0.04,0.03,labeltext,0,0.035)


        avquaddevplot_fromhisto = PointPlot(2,"Av. quadr. deviation",["New variables","Old variables"])

        avquaddevplot_fromhisto.addLabel(0.04,0.03,labeltext+" from histo",0,0.035)


        #Set 2D Plots
        resprereg_old = TwoDplot("resprereg","",[100,0,300],[100,-1,1])
        respostreg_old = TwoDplot("respostreg","",[100,0,300],[100,-1,1])
        outputdif_full_old_ratio = TwoDplot("outputdif_full","",[binning_outputdev_target["Ratio"][0],binning_outputdev_target["Ratio"][1],binning_outputdev_target["Ratio"][2]],[binning_outputdev_dev["Ratio"][0],binning_outputdev_dev["Ratio"][1],binning_outputdev_dev["Ratio"][2]])
        outputdif_zoom_old_ratio = TwoDplot("outputdif_zoom","",[binning_outputdev_zoom_target["Ratio"][0],binning_outputdev_zoom_target["Ratio"][1],binning_outputdev_zoom_target["Ratio"][2]],[binning_outputdev_zoom_dev["Ratio"][0],binning_outputdev_zoom_dev["Ratio"][1],binning_outputdev_zoom_dev["Ratio"][2]])

        outputdif_full_old_normal = TwoDplot("outputdif_full","",[binning_outputdev_target["Normal"][0],binning_outputdev_target["Normal"][1],binning_outputdev_target["Normal"][2]],[binning_outputdev_dev["Normal"][0],binning_outputdev_dev["Normal"][1],binning_outputdev_dev["Normal"][2]])
        outputdif_zoom_old_normal = TwoDplot("outputdif_zoom","",[binning_outputdev_zoom_target["Normal"][0],binning_outputdev_zoom_target["Normal"][1],binning_outputdev_zoom_target["Normal"][2]],[binning_outputdev_zoom_dev["Normal"][0],binning_outputdev_zoom_dev["Normal"][1],binning_outputdev_zoom_dev["Normal"][2]])


        resprereg_new = TwoDplot("resprereg","",[100,0,300],[100,-1,1])
        respostreg_new = TwoDplot("respostreg","",[100,0,300],[100,-1,1])
        outputdif_full_new_ratio = TwoDplot("outputdif_full","",[binning_outputdev_target["Ratio"][0],binning_outputdev_target["Ratio"][1],binning_outputdev_target["Ratio"][2]],[binning_outputdev_dev["Ratio"][0],binning_outputdev_dev["Ratio"][1],binning_outputdev_dev["Ratio"][2]])
        outputdif_zoom_new_ratio = TwoDplot("outputdif_zoom","",[binning_outputdev_zoom_target["Ratio"][0],binning_outputdev_zoom_target["Ratio"][1],binning_outputdev_zoom_target["Ratio"][2]],[binning_outputdev_zoom_dev["Ratio"][0],binning_outputdev_zoom_dev["Ratio"][1],binning_outputdev_zoom_dev["Ratio"][2]])

        outputdif_full_new_normal = TwoDplot("outputdif_full","",[binning_outputdev_target["Normal"][0],binning_outputdev_target["Normal"][1],binning_outputdev_target["Normal"][2]],[binning_outputdev_dev["Normal"][0],binning_outputdev_dev["Normal"][1],binning_outputdev_dev["Normal"][2]])
        outputdif_zoom_new_normal = TwoDplot("outputdif_zoom","",[binning_outputdev_zoom_target["Normal"][0],binning_outputdev_zoom_target["Normal"][1],binning_outputdev_zoom_target["Normal"][2]],[binning_outputdev_zoom_dev["Normal"][0],binning_outputdev_zoom_dev["Normal"][1],binning_outputdev_zoom_dev["Normal"][2]])
        
        

        resprereg_old.setAxisTitle("p_{T, Parton} - p_{T, Jet} / p_{T, Jet}","p_{T, Jet}")
        respostreg_old.setAxisTitle("p_{T, Parton} - p_{T, Reg} / p_{T, Reg}","p_{T, Reg}") 

        outputdif_full_old_ratio.setAxisTitle("Output-Target Deviation","p_{T} Ratio")
        outputdif_zoom_old_ratio.setAxisTitle("Output-Target Deviation","p_{T} Ratio")

        outputdif_full_old_normal.setAxisTitle("Output-Target Deviation","p_{T, Parton}")
        outputdif_zoom_old_normal.setAxisTitle("Output-Target Deviation","p_{T, Parton}")


        resprereg_old.addLabel(0.04,0.03,labeltext+" (Old input variables)",0,0.035)
        respostreg_old.addLabel(0.04,0.03,labeltext+" (Old input variables)",0,0.035)
        outputdif_full_old_ratio.addLabel(0.04,0.03,labeltext+" (Old input variables)",0,0.035)
        outputdif_zoom_old_ratio.addLabel(0.04,0.03,labeltext+" (Old input variables)",0,0.035)

        outputdif_full_old_normal.addLabel(0.04,0.03,labeltext+" (Old input variables)",0,0.035)
        outputdif_zoom_old_normal.addLabel(0.04,0.03,labeltext+" (Old input variables)",0,0.035)

        resprereg_new.setAxisTitle("p_{T, Parton} - p_{T, Jet} / p_{T, Jet}","p_{T, Jet}")
        respostreg_new.setAxisTitle("p_{T, Parton} - p_{T, Reg} / p_{T, Reg}","p_{T, Reg}") 
        outputdif_full_new_ratio.setAxisTitle("Output-Target Deviation","p_{T} Ratio")
        outputdif_zoom_new_ratio.setAxisTitle("Output-Target Deviation","p_{T} Ratio")
        outputdif_full_new_normal.setAxisTitle("Output-Target Deviation","p_{T, Parton}")
        outputdif_zoom_new_normal.setAxisTitle("Output-Target Deviation","p_{T, Parton}")



        resprereg_new.addLabel(0.04,0.03,labeltext+" (New input variables)",0,0.035)
        respostreg_new.addLabel(0.04,0.03,labeltext+" (New input variables)",0,0.035)
     
        outputdif_full_new_ratio.addLabel(0.04,0.03,labeltext+" (New input variables)",0,0.035)
        outputdif_zoom_new_ratio.addLabel(0.04,0.03,labeltext+" (New input variables)",0,0.035)

        outputdif_full_new_normal.addLabel(0.04,0.03,labeltext+" (New input variables)",0,0.035)
        outputdif_zoom_new_normal.addLabel(0.04,0.03,labeltext+" (New input variables)",0,0.035)


        plots2D = [[resprereg_new, respostreg_new, outputdif_full_new_ratio, outputdif_zoom_new_ratio, outputdif_full_new_normal, outputdif_zoom_new_normal],[resprereg_old, respostreg_old, outputdif_full_old_ratio, outputdif_zoom_old_ratio,outputdif_full_old_normal, outputdif_zoom_old_normal]]

        for iweight, weightfile in enumerate(weights[version]):
            print "Procession Regression "+str(iweight)
            regression = JetRegression(weightpath+weightfile,weights_add[version][iweight][0],weights_add[version][iweight][1])

            resprereg = plots2D[iweight][0]
            respostreg = plots2D[iweight][1]
            outputdif_full_ratio = plots2D[iweight][2]
            outputdif_zoom_ratio = plots2D[iweight][3]
            outputdif_full_normal = plots2D[iweight][4]
            outputdif_zoom_normal = plots2D[iweight][5]
            

            tree = inputfile[sample].Get("MVATree")


            avdev_target = [float(0),0]
            avdev_target_all_normal = [float(0),0]
            avdev_target_all_ratio = [float(0),0]
            
            deviations = []
            deviations_all_normal = []
            deviations_all_ratio = []

            for iev in range(tree.GetEntries()):
                if iev%10000 == 0:
                    pass
                    print iev
                if iev == 100001:
                    break

                #print avdev_target

                tree.GetEvent(iev)
                
                inputevtvars["Evt_Rho"] = tree.Evt_Rho
                inputevtvars["N_PrimaryVertices"] = tree.N_PrimaryVertices
                regcorrlist = []
                for ijet in range(tree.N_Jets):
                    if abs(tree.Jet_MatchedPartonFlav[ijet]) == 5 and abs(tree.Jet_Flav[ijet]) == 5:
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
                        inputjetvars["Jet_cHEFrac"] = tree.Jet_cHEFrac[ijet]
                        inputjetvars["Jet_nEmEFrac"] = tree.Jet_nEmEFrac[ijet]
                        #inputjetvars["Jet_chargedMult"] = tree.Jet_chargedMult[ijet]
                        inputjetvars["Jet_vtxPt"] = tree.Jet_vtxPt[ijet]
                        inputjetvars["Jet_vtxMass"] = tree.Jet_vtxMass[ijet]
                        inputjetvars["Jet_vtx3DVal"] = tree.Jet_vtx3DVal[ijet]
                        inputjetvars["Jet_vtxNtracks"] = tree.Jet_vtxNtracks[ijet]
                        inputjetvars["Jet_vtx3DSig"] = tree.Jet_vtx3DSig[ijet]

                        inputvars = inputjetvars
                        inputvars.update(inputevtvars)

                        regout = regression.evalReg(inputvars)
                    
                        if version == "Normal":
                            ptregplot.FillnormHisto(regout,iweight)
                            ptcorrplot.FillnormHisto(regout/inputjetvars["Jet_Pt"],iweight)
                            ptregplot_all.FillnormHisto(regout,nhisto_all)
                            ptcorrplot_all.FillnormHisto(regout/inputjetvars["Jet_Pt"],nhisto_all)
                            regcorrlist.append(regout)
                            tmp = ( regout - tree.Jet_MatchedPartonPt[ijet] )*( regout - tree.Jet_MatchedPartonPt[ijet] )
                            avdev_target[0] =  avdev_target[0] +( tmp )
                            deviations.append(tmp)
                            avdev_target[1] = avdev_target[1] + 1
                            avdev_target_all_normal[0] = avdev_target[0]
                            avdev_target_all_normal[1] = avdev_target[1]
                            deviations_all_normal.append(tmp)
                            tmp = (((regout/inputjetvars["Jet_Pt"]) - (tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"]))*((regout/inputjetvars["Jet_Pt"]) - (tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"])))
                            avdev_target_all_ratio[0] = avdev_target_all_ratio[0] + tmp
                            avdev_target_all_ratio[1] = avdev_target_all_ratio[1] + 1
                            deviations_all_ratio.append(tmp)

                            resprereg.FillTwoDplot(inputjetvars["Jet_Pt"],(tree.Jet_MatchedPartonPt[ijet]-inputjetvars["Jet_Pt"])/inputjetvars["Jet_Pt"])
                            respostreg.FillTwoDplot(regout,(tree.Jet_MatchedPartonPt[ijet]-regout)/regout)
                            outputdif_full_normal.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet],regout - tree.Jet_MatchedPartonPt[ijet])
                            outputdif_zoom_normal.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet],regout - tree.Jet_MatchedPartonPt[ijet])
                            outputdif_full_ratio.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"],regout/inputjetvars["Jet_Pt"] - tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"])
                            outputdif_zoom_ratio.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"],regout/inputjetvars["Jet_Pt"] - tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"])



                        elif version == "Ratio":
                            ptregplot.FillnormHisto(regout*inputjetvars["Jet_Pt"],iweight)
                            ptcorrplot.FillnormHisto(regout,iweight)
                            ptregplot_all.FillnormHisto(regout*inputjetvars["Jet_Pt"],nhisto_all)
                            ptcorrplot_all.FillnormHisto(regout,nhisto_all)
                            regcorrlist.append(regout*inputjetvars["Jet_Pt"])

                            tmp = ( regout - (tree.Jet_MatchedPartonPt[ijet] / inputjetvars["Jet_Pt"])) * ( regout - (tree.Jet_MatchedPartonPt[ijet] / inputjetvars["Jet_Pt"]))
                            avdev_target[0] =  avdev_target[0] + ( tmp  )
                            avdev_target[1] = avdev_target[1] + 1
                            deviations.append(tmp)
                            avdev_target_all_ratio[0] = avdev_target[0]
                            avdev_target_all_ratio[1] = avdev_target[1]
                            deviations_all_ratio.append(tmp)
                            tmp = ((regout*inputjetvars["Jet_Pt"]) - tree.Jet_MatchedPartonPt[ijet]) * ((regout*inputjetvars["Jet_Pt"]) - tree.Jet_MatchedPartonPt[ijet])
                            avdev_target_all_normal[0] = avdev_target_all_normal[0] + ( tmp )
                            avdev_target_all_normal[1] = avdev_target_all_normal[1] + 1
                            deviations_all_normal.append(tmp)
                           


                            resprereg.FillTwoDplot(inputjetvars["Jet_Pt"],(tree.Jet_MatchedPartonPt[ijet]-inputjetvars["Jet_Pt"])/inputjetvars["Jet_Pt"])
                            respostreg.FillTwoDplot(regout*inputjetvars["Jet_Pt"],(tree.Jet_MatchedPartonPt[ijet]-(regout*inputjetvars["Jet_Pt"]))/(regout*inputjetvars["Jet_Pt"]))
                            outputdif_full_ratio.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"],regout - (tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"]))
                            outputdif_zoom_ratio.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"],regout - (tree.Jet_MatchedPartonPt[ijet]/inputjetvars["Jet_Pt"]))
                            outputdif_full_normal.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet],regout*inputjetvars["Jet_Pt"] - (tree.Jet_MatchedPartonPt[ijet]))
                            outputdif_zoom_normal.FillTwoDplot(tree.Jet_MatchedPartonPt[ijet],regout*inputjetvars["Jet_Pt"] - (tree.Jet_MatchedPartonPt[ijet]))

                        #print "b",avdev_target

                    else:
                        regcorrlist.append(-99)
                        
                if tree.N_MatchedHiggsJets == 2:
                    veclist = []
                    veclist_noreg = []
                    for ijet in range(tree.N_Jets):
                        if tree.Jet_isHiggsJet[ijet] == 1 and regcorrlist[ijet] != -99:
                            tmp = ROOT.TLorentzVector()
                            tmp.SetPtEtaPhiM(regcorrlist[ijet],tree.Jet_Eta[ijet],tree.Jet_Phi[ijet],tree.Jet_M[ijet])
                            veclist.append(tmp)
                            tmp1 = ROOT.TLorentzVector()
                            tmp1.SetPtEtaPhiM(tree.Jet_Pt[ijet],tree.Jet_Eta[ijet],tree.Jet_Phi[ijet],tree.Jet_M[ijet])
                            veclist_noreg.append(tmp1)
                
                            del tmp, tmp1
                    if len(veclist) == 2:
                        mHplot.FillnormHisto((veclist[0]+veclist[1]).M(),iweight)
                        mHplot_all.FillnormHisto((veclist[0]+veclist[1]).M(),nhisto_all+1)
                        if not setflag:
                            mHplot_all.FillnormHisto((veclist_noreg[0]+veclist_noreg[1]).M(),0)
                            
            htmp_dev = ROOT.TH1F("htmp_dev","htmp_dev",300,0,max(deviations))
            htmp_dev_normal = ROOT.TH1F("htmp_dev_normal","htmp_dev_normal",300,0,max(deviations_all_normal))
            htmp_dev_ratio = ROOT.TH1F("htmp_dev_ratio","htmp_dev_ratio",300,0,max(deviations_all_ratio))

            sum_ = 0
            mean_ = avdev_target[0]/avdev_target[1]
            for i in range( avdev_target[1] ):
               sum_ = sum_ + ( ( deviations[i] - mean_) * ( deviations[i] - mean_) )
               htmp_dev.Fill(deviations[i])
            print sum_, avdev_target[1]
            rms_ = sqrt(sum_ / avdev_target[1])
            averagedev_error = rms_ / (sqrt(mean_ * 2.0 * avdev_target[1])) 

            sum_ = 0
            mean_ = avdev_target_all_normal[0]/avdev_target_all_normal[1]
            for i in range( avdev_target_all_normal[1] ):
               sum_ = sum_ + ( ( deviations_all_normal[i] - mean_) * ( deviations_all_normal[i] - mean_) )  
               htmp_dev_normal.Fill(deviations_all_normal[i])
            rms_ = sqrt(sum_ / avdev_target_all_normal[1])
            averagedev_all_normal_error = rms_ / (sqrt(mean_ * 2.0 * avdev_target_all_normal[1])) 

            sum_ = 0
            mean_ = avdev_target_all_ratio[0]/avdev_target_all_ratio[1]
            for i in range( avdev_target_all_ratio[1] ):
               sum_ = sum_ + ( ( deviations_all_ratio[i] - mean_) * ( deviations_all_ratio[i] - mean_) )
               htmp_dev_ratio.Fill(deviations_all_ratio[i])
            rms_ = sqrt(sum_ / avdev_target_all_ratio[1])
            averagedev_all_ratio_error = rms_ / (sqrt(mean_ * 2.0 * avdev_target_all_ratio[1])) 

            
            avquaddevplot.addPoint(sqrt(avdev_target[0]/avdev_target[1]),averagedev_error)       
            avquaddevplot_all_normal.addPoint(sqrt(avdev_target_all_normal[0]/avdev_target_all_normal[1]),averagedev_all_normal_error)
            avquaddevplot_all_ratio.addPoint(sqrt(avdev_target_all_ratio[0]/avdev_target_all_ratio[1]),averagedev_all_ratio_error)
            avquaddevplot_fromhisto.addPoint(*getAvQuadDevfromHisto(htmp_dev))       
            avquaddevplot_all_normal_fromhisto.addPoint(*getAvQuadDevfromHisto(htmp_dev_normal))
            avquaddevplot_all_ratio_fromhisto.addPoint(*getAvQuadDevfromHisto(htmp_dev_ratio))

            del regression
            setflag = True
            nhisto_all = nhisto_all + 1
            del resprereg, respostreg, outputdif_full_ratio, outputdif_zoom_ratio, outputdif_full_normal, outputdif_zoom_normal
            del htmp_dev, htmp_dev_normal, htmp_dev_ratio

        mHplot.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
        ptregplot.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
        ptcorrplot.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
        avquaddevplot.WritePointPlot(c1,"ttHbb",pdfout)
        avquaddevplot_fromhisto.WritePointPlot(c1,"ttHbb",pdfout)

        for plots in plots2D:
            for plot in plots:
                plot.WriteTwoDplot(c1,"ttHbb",True,None,pdfout)
            

        del mHplot, ptregplot, ptcorrplot, avquaddevplot, plots2D

    mHplot_all.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
    ptregplot_all.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
    ptcorrplot_all.WriteHisto(c1,"ttHbb",False,False,pdfout,True)
    avquaddevplot_all_normal.WritePointPlot(c1,"ttHbb",pdfout)
    avquaddevplot_all_normal_fromhisto.WritePointPlot(c1,"ttHbb",pdfout)
    avquaddevplot_all_ratio.WritePointPlot(c1,"ttHbb",pdfout)
    avquaddevplot_all_ratio_fromhisto.WritePointPlot(c1,"ttHbb",pdfout)

pdfout.closePDF()
