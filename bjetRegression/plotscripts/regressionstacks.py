#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
from array import array
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from plotting import *
from rootutils import PDFPrinting
#-------------------------------------------------------------------------------------#
#

#
#-------------------------------------------------------------------------------------#
# Set Variables

path1 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0317_testing/output/"
path3 = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/"
path4 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0318_testing/output/"


compdic = { "Target Comparison" : [path1+"script_1200_0.1_5_30.root"] }
#compdic = { "Target Comparison" : [path1+"script_1200_0.1_5_30.root", path3+"BReg_0323_ratiotest_Jet_D_Parton_1200_0.1_5_30.root",path4+"script_1200_0.1_4_20.root"] }
branchdic = { path1+"script_1200_0.1_5_30.root" : ["Jet_PartonPt"],
              path3+"BReg_0323_ratiotest_Jet_D_Parton_1200_0.1_5_30.root" : ["Jet_Pt_D_Jet_PartonPt"],
              path4+"script_1200_0.1_4_20.root" : ["Jet_PartonPt_D_Jet_Pt" ] } 

#print inputfiles

usetesttree = True #if False use train tree
 
outputfolder = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/output_5/" #has to be created first
outputname = "outname_stacks_norm"

targetname = "Jet_PartonPt" #name of Regression target
th1param1 = [200,30,400]
th1param2 = [96,0.6,1.6]
th1param3 = [60,0,2.5]


ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)
#-------------------------------------------------------------------------------------#
#

compplots = []

for comp in compdic:
    print "Processing", comp

    filenames = compdic[comp]
    names = map(lambda x : x.split("/")[-1][:-5], filenames)



    #Initialize Plotting

    
    for ifile, filename in enumerate(filenames):

        stackplot1 = CatPlots("Regressed Jet p{T}",[0,0.9,1,1.1,1.2,1.4,1.7,3],"Jet_PartonPt_D_Jet_Pt_1","Jet_PartonPt / Jet_Pt",False,False,"ttbar",th1param1)
        stackplot2 = CatPlots("Regressed correction factor",[0,0.9,1,1.1,1.2,1.4,1.7,3],"Jet_PartonPt_D_Jet_Pt_2","Jet_PartonPt / Jet_Pt",False,False,"ttbar",th1param2)
        targetplot = ROOT.TH1F("targeptplot","targetplot",th1param2[0],th1param2[1],th1param2[2])
        

        inputfile = ROOT.TFile(filename)
        for key in inputfile.GetListOfKeys():
            if key.GetName() == "TestTree":
                testtreekey = key
            if key.GetName() == "TrainTree":
                traintreekey = key

        if usetesttree:
            tree = inputfile.Get(testtreekey.GetName())
        else:
            tree = inputfile.Get(traintreekey.GetName())
            
        jetpt_tree = array('f',[0])
        target_tree = array('f',[0])
        bdtg_tree = array('f',[0])
            
        tree.SetBranchAddress("Jet_Pt", jetpt_tree) #Get Jet Pt
        tree.SetBranchAddress(branchdic[filename][0],target_tree)#Get Target
        tree.SetBranchAddress("BDTG", bdtg_tree)#Get BDT Output

        
        for iev in range(tree.GetEntries()):
            if iev%10000 == 0:
                pass
                print iev
            if iev == 10000000:
                break
            
            tree.GetEvent(iev)
            
            jetpt = jetpt_tree[0]
            if filename == compdic[comp][0]:
                partonpt = target_tree[0]
            elif filename == compdic[comp][1]:
                partonpt = (1/target_tree[0]) * jetpt_tree[0]
            elif filename == compdic[comp][2]:
                partonpt = target_tree[0] * jetpt_tree[0]
            else:
                exit()
            if filename == compdic[comp][0]:
                regpt = bdtg_tree[0]
            elif filename == compdic[comp][1]:
                regpt = (1/bdtg_tree[0]) * jetpt_tree[0]
            elif filename == compdic[comp][2]:
                regpt = bdtg_tree[0] * jetpt_tree[0]
            else:
                exit()
                
            stackplot1.FillCatHistos(regpt,(partonpt/jetpt))
            stackplot2.FillCatHistos(regpt/jetpt,(partonpt/jetpt))
            targetplot.Fill(partonpt/jetpt)
        
        compplots.append([deepcopy(stackplot1),deepcopy(stackplot2)])
        del stackplot1, stackplot2

    
    del inputfile, tree
    del filenames,names
    
    #raw_input("Press ret")



"""
pdfout = PDFPrinting("outname_configcomp")
outputfile = ROOT.TFile("outname_configcomp"+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()    

for plots in compplots:
    for plot in plots:
        plot.WriteHisto(c1,"ttbar",False,False,pdfout)

pdfout.closePDF()
"""

pdfout_norm = PDFPrinting(outputname)
outputfile_norm = ROOT.TFile(outputname+".root","RECREATE")
outputfile_norm.cd()
c1_norm = ROOT.TCanvas()    

for plots in compplots:
    bla = 0
    for plot in plots:
        plot.makeStack()
        if bla == 1:
            plot.AddTH1FtoStack(targetplot)
        plot.WriteNotStacked(c1_norm,pdfout_norm)
        plot.WriteStack(c1_norm,pdfout_norm)
        bla += 1
pdfout_norm.closePDF()
