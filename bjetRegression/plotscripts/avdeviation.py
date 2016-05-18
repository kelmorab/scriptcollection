#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
#
#-------------------------------------------------------------------------------------#
# Import custom modules
#from plotting import *
#from rootutils import PDFPrinting
#-------------------------------------------------------------------------------------#
#
#Add path to bjetreg folder to path, that scripts from there can be used
parentpath = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
#bjetregpath = parentpath+"/"+"bjetRegression"

print parentpath
#print bjetregpath
sys.path.append(parentpath)
#print sys.path
from plotscripts.plotting import *
from plotscripts.rootutils import PDFPrinting
from regressionTools import *

#
#-------------------------------------------------------------------------------------#
# Set Variables

path1 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0317_testing/output/"
path2 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0322_testing/output/"
path3 = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/"
path4 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0318_testing/output/"


#filenames= [ path1+"script_200_0.1_3_30.root", path1+"script_1200_0.1_3_30.root" ]
#filenames= [ path1+"script_200_0.1_5_30.root",path1+"script_1200_0.1_5_30.root" ]
#filenames= [ path1+"script_200_0.1_3_30.root",  path1+"script_200_0.1_5_30.root",path1+"script_1200_0.1_3_30.root",path1+"script_1200_0.1_5_30.root" ]
filenames = [ path2+"script_1200_0.3_6_30.root", path2+"script_1200_0.1_6_30.root", path2+"script_1200_0.12_6_30.root", path2+"script_1200_0.08_6_30.root" ] 
#print inputfiles

usetesttree = True #if False use train tree
 
#outputfolder = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/output_5/" #has to be created first
outputname = "avdev_configurations_7"

targetname = "Jet_PartonPt" #name of Regression target

onlydoDeviations = True

yaxis = [[17,20],[11.8,14],[10.1,12],[9.15,10.6],[8.1,9.5]]

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)
#-------------------------------------------------------------------------------------#
#


#print filenames
names = map(lambda x : x.split("/")[-1][:-5], filenames)
print "NAMES",names
legendtext = []
for ifile, name in enumerate(names):
    tmplist = name.split("_") 
    print tmplist
    nTrees = tmplist[-4]
    shrink = tmplist[-3]
    maxDepth = tmplist[-2]
    nCuts = tmplist[-1]
    legendtext.append("1: "+nTrees+" | 2: "+shrink+" | 3: "+maxDepth+" | 4: "+nCuts)

avquaddevplot = PointPlot(len(names),"Av. quadr. deviation (GeV)",legendtext)
avquaddevplot_best90 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 90 %",legendtext)

avquaddevplot.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_best90.setmanualegendsize("right",0.6,0.50,0.88,0.88)

avquaddevplot.addLabel(0.04,0.03,"Test Sample (TMVA plots)",0,0.035)
avquaddevplot_best90.addLabel(0.04,0.03,"Test Sample (TMVA plots)",0,0.035)
avquaddevplot.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_best90.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)

avquaddevplot_train = PointPlot(len(names),"Av. quadr. deviation (GeV)",legendtext)
avquaddevplot_train_best90 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 90 %",legendtext)

avquaddevplot_train.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_train_best90.setmanualegendsize("right",0.6,0.50,0.88,0.88)

avquaddevplot_train.addLabel(0.04,0.03,"Training Sample (TMVA plots)",0,0.035)
avquaddevplot_train_best90.addLabel(0.04,0.03,"Training Sample (TMVA plots)",0,0.035)
avquaddevplot_train.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_train_best90.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)

deviations_test_best90 = normPlots("Quadratic Deviation",True, len(names), legendtext, [200,0,700])
deviations_test = normPlots("Quadratic Deviation",True, len(names), legendtext, [300,0,500])
deviations_train_best90 = normPlots("Quadratic Deviation",True, len(names), legendtext, [200,0,700])

del ifile

c1 = ROOT.TCanvas()
pdfout = PDFPrinting(outputname)
    
c1.cd(1)




quaddev_quatile100_test = normPlots("Quadratic Deviation", True, len(legendtext), legendtext, [300,0,50000])
quaddev_quatile95_test = normPlots("Quadratic Deviation (best 95 %)", True, len(legendtext), legendtext, [300,0,1500])
quaddev_quatile90_test = normPlots("Quadratic Deviation (best 90 %)", True, len(legendtext), legendtext, [300,0,800])
quaddev_quatile85_test = normPlots("Quadratic Deviation (best 85 %)", True, len(legendtext), legendtext, [200,0,600])
quaddev_quatile80_test = normPlots("Quadratic Deviation (best 80 %)", True, len(legendtext), legendtext, [200,0,600])

quaddev_quatile100_train = normPlots("Quadratic Deviation", True, len(legendtext), legendtext, [300,0,50000])
quaddev_quatile95_train = normPlots("Quadratic Deviation (best 95 %)", True, len(legendtext), legendtext, [300,0,1500])
quaddev_quatile90_train = normPlots("Quadratic Deviation (best 90 %)", True, len(legendtext), legendtext, [300,0,800])
quaddev_quatile85_train = normPlots("Quadratic Deviation (best 85 %)", True, len(legendtext), legendtext, [200,0,600])
quaddev_quatile80_train = normPlots("Quadratic Deviation (best 80 %)", True, len(legendtext), legendtext, [200,0,600])

quaddevs_train = [quaddev_quatile100_train,quaddev_quatile95_train,quaddev_quatile90_train,quaddev_quatile85_train,quaddev_quatile80_train]
quaddevs_test = [quaddev_quatile100_test,quaddev_quatile95_test,quaddev_quatile90_test,quaddev_quatile85_test,quaddev_quatile80_test]
    
for i in range(len(quaddevs_train)):
    quaddevs_train[i].addLabel(0.04,0.03,"Training Sample",0,0.035)
    quaddevs_test[i].addLabel(0.04,0.03,"Test Sample",0,0.035)

quaddevs_list = [quaddevs_test,quaddevs_train]

dev_quatile100_test = normPlots("Deviation", True, len(legendtext), legendtext, [250,-500,500])
dev_quatile100_train = normPlots("Deviation", True, len(legendtext), legendtext, [250,-500,500])

dev_quatile100_test.addLabel(0.04,0.03,"Training Sample",0,0.035)
dev_quatile100_train.addLabel(0.04,0.03,"Test Sample",0,0.035)

devs_list = [ dev_quatile100_test,dev_quatile100_train]

errorlist_train = []
errorlist_test = []

errorlist = [errorlist_test,errorlist_train]

for ifile, filename in enumerate(filenames):
    print "Processing:",names[ifile] 
    inputfile = ROOT.TFile(filename)
    for key in inputfile.GetListOfKeys():
        if key.GetName() == "Method_BDT":
            bdtdir = key
        if key.GetName() == "TestTree":
            testtreekey = key
        if key.GetName() == "TrainTree":
            traintreekey = key

    treekeys = [testtreekey, traintreekey]
        
    Method_dir = inputfile.Get(bdtdir.GetName())
    BDTG_dir = Method_dir.Get("BDTG")
    


    for key in BDTG_dir.GetListOfKeys():
        if key.GetName() == 'MVA_BDTGtest_Quadr_Deviation_target_0_':
            hdev = key.ReadObj()
        if key.GetName() == 'MVA_BDTGtest_Quadr_Dev_best90perc_target_0_':
            hdev_best90 = key.ReadObj()
        if key.GetName() == 'MVA_BDTGtrain_Quadr_Deviation_target_0_':
            hdev_train = key.ReadObj()
        if key.GetName() == 'MVA_BDTGtrain_Quadr_Dev_best90perc_target_0_':
            hdev_train_best90 = key.ReadObj()
            
            
    print hdev.GetEntries(), hdev_train.GetEntries()
            
    deviations_test_best90.AddTH1F(hdev_best90, ifile)
    deviations_test.AddTH1F(hdev, ifile)
    deviations_train_best90.AddTH1F(hdev_train_best90, ifile)
            
    avquaddevplot.addPoint(*getAvQuadDevfromHisto(hdev))
    avquaddevplot_best90.addPoint(*getAvQuadDevfromHisto(hdev_best90))
    avquaddevplot_train.addPoint(*getAvQuadDevfromHisto(hdev_train))
    avquaddevplot_train_best90.addPoint(*getAvQuadDevfromHisto(hdev_train_best90))

    


    labels = ["Test Sampel","Training Sampel"]

    for ikey, key in enumerate(treekeys):
        print "Processing:",key.GetName()
        
        err = Errors()

        quaddevvOutput = TwoDplot("BDTG","QuadDev",[150,0,400],[300,0,50000])
        quaddevvOutput_zoom = TwoDplot("BDTG","QuadDev",[150,0,400],[100,0,10000])
        quaddevvTarget = TwoDplot("Target","QuadDev",[150,0,450],[300,0,50000])
        quaddevvTarget_zoom = TwoDplot("Target","QuadDev",[150,0,450],[300,0,10000])
        quaddevvJetPt = TwoDplot("JetPt","QuadDev",[150,0,450],[300,0,50000])
        quaddevvJetPt_zoom = TwoDplot("JetPt","QuadDev",[150,0,450],[300,0,10000])


        devvOuput = TwoDplot("BDTG","Deviation",[150,0,400],[250,-500,500])
        devvTarget = TwoDplot("Target","Deviation",[150,0,450],[250,-500,500])
        devvJetPt = TwoDplot("JetPt","Deviation",[150,0,450],[250,-500,500])
        
        quaddevvOutput.setAxisTitle("Quadratic Deviation","BDT Output")
        quaddevvOutput_zoom.setAxisTitle("Quadratic Deviation","BDT Output")
        quaddevvTarget.setAxisTitle("Quadratic Deviation","BDT Target")
        quaddevvTarget_zoom.setAxisTitle("Quadratic Deviation","BDT Target")
        quaddevvJetPt.setAxisTitle("Quadratic Deviation","Jet p_{T}")
        quaddevvJetPt_zoom.setAxisTitle("Quadratic Deviation","Jet p_{T}")



        devvOuput.setAxisTitle("Deviation","BDT Output")
        devvTarget.setAxisTitle("Deviation","BDT Target")
        devvJetPt.setAxisTitle("Deviation","Jet p_{T}")

        quaddevvOutput.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        quaddevvOutput_zoom.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        quaddevvTarget.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        quaddevvTarget_zoom.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        quaddevvJetPt.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        quaddevvJetPt_zoom.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)


        devvOuput.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        devvTarget.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)
        devvJetPt.addLabel(0.04,0.03,labels[ikey]+"("+legendtext[ifile]+")",0,0.035)


        tree = inputfile.Get(key.GetName())
        
        entries = tree.GetEntries()
        
        quaddevs = []
        devs = []

        for i in range(entries):
            if i%100000 == 0:
                pass
                print i
            if i == 100:
                pass
                #break

            tree.GetEvent(i)

            #print tree.BDTG,tree.Jet_PartonPt
            dev = (tree.BDTG - tree.Jet_PartonPt)
            quaddev =  dev * dev
            output  = tree.BDTG
            target = tree.Jet_PartonPt
            jetpt = tree.Jet_Pt

            err.addevent(output, target)
            
            quaddevs.append(quaddev)
            devs.append(dev)

            quaddevvOutput.FillTwoDplot(output, quaddev)
            quaddevvOutput_zoom.FillTwoDplot(output, quaddev)
            quaddevvTarget.FillTwoDplot(target, quaddev)
            quaddevvTarget_zoom.FillTwoDplot(target, quaddev)
            quaddevvJetPt.FillTwoDplot(jetpt, quaddev)
            quaddevvJetPt_zoom.FillTwoDplot(jetpt, quaddev)

            devvOuput.FillTwoDplot(output, dev)
            devvTarget.FillTwoDplot(target, dev)
            devvJetPt.FillTwoDplot(jetpt, dev)
            
        devs = sorted(devs)
        quaddevs = sorted(quaddevs)
        
        #print quaddevs

        err.printerr()

        quaddev_quatile100 = quaddevs_list[ikey][0]
        quaddev_quatile95 = quaddevs_list[ikey][1]
        quaddev_quatile90 = quaddevs_list[ikey][2]
        quaddev_quatile85  = quaddevs_list[ikey][3]
        quaddev_quatile80 = quaddevs_list[ikey][4]
        dev_quatile100 = devs_list[ikey]
        
        for i in range(len(quaddevs)):
            quaddev_quatile100.FillnormHisto(quaddevs[i], ifile)
            dev_quatile100.FillnormHisto(devs[i], ifile)
            if i <= int(len(quaddevs)*0.95):
                quaddev_quatile95.FillnormHisto(quaddevs[i], ifile)
            if i <= int(len(quaddevs)*0.90):
                quaddev_quatile90.FillnormHisto(quaddevs[i], ifile)
            if i <= int(len(quaddevs)*0.85):
                quaddev_quatile85.FillnormHisto(quaddevs[i], ifile)
            if i <= int(len(quaddevs)*0.80):
                quaddev_quatile80.FillnormHisto(quaddevs[i], ifile)
        
        if not onlydoDeviations:
            quaddevvOutput.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            quaddevvOutput_zoom.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            quaddevvTarget.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            quaddevvTarget_zoom.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            quaddevvJetPt.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            quaddevvJetPt_zoom.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
        
            devvOuput.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            devvTarget.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
            devvJetPt.WriteTwoDplot(c1,"ttbar",True,None, pdfout)
        
        errorlist[ikey].append(deepcopy(err))

        del tree, err
        del quaddevvOutput, quaddevvOutput_zoom, quaddevvTarget, quaddevvTarget_zoom, devvOuput, devvTarget
        

"""
avquaddevplot.WritePointPlot(c1,"ttbar",pdfout, [17,20.5])
avquaddevplot_best90.WritePointPlot(c1,"ttbar",pdfout, [10.3,12.2])
avquaddevplot_train.WritePointPlot(c1,"ttbar",pdfout , [17,20.5])
avquaddevplot_train_best90.WritePointPlot(c1,"ttbar",pdfout , [10.3,12.2])        
"""
avquaddevplot.WritePointPlot(c1,"ttbar",pdfout,yaxis[0])
avquaddevplot_best90.WritePointPlot(c1,"ttbar",pdfout,yaxis[2])
avquaddevplot_train.WritePointPlot(c1,"ttbar",pdfout,yaxis[0])
avquaddevplot_train_best90.WritePointPlot(c1,"ttbar",pdfout,yaxis[2])        


avquaddevplot_2 = PointPlot(len(names),"Av. quadr. deviation (GeV)",legendtext)
avquaddevplot_2_best95= PointPlot(len(names),"Av. quadr. deviation (GeV) of best 95 %",legendtext)
avquaddevplot_2_best90 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 90 %",legendtext)
avquaddevplot_2_best85 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 85 %",legendtext)
avquaddevplot_2_best80 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 80 %",legendtext)

avquaddevplots_2 = [avquaddevplot_2,avquaddevplot_2_best95,avquaddevplot_2_best90,avquaddevplot_2_best85,avquaddevplot_2_best80]

avquaddevplot_2.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_2_best95.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_2_best90.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_2_best85.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_2_best80.setmanualegendsize("right",0.6,0.50,0.88,0.88)


avquaddevplot_2.addLabel(0.04,0.03,"Test Sample",0,0.035)
avquaddevplot_2_best95.addLabel(0.04,0.03,"Test Sample",0,0.035)
avquaddevplot_2_best90.addLabel(0.04,0.03,"Test Sample",0,0.035)
avquaddevplot_2_best85.addLabel(0.04,0.03,"Test Sample",0,0.035)
avquaddevplot_2_best80.addLabel(0.04,0.03,"Test Sample",0,0.035)

avquaddevplot_2.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_2_best95.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_2_best90.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_2_best85.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_2_best80.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)

for k in range(len(quaddevs_list[0])):
    for n in range(len(names)):
        avquaddevplots_2[k].addPoint(*getAvQuadDevfromHisto(quaddevs_list[0][k].getHistos()[n]))



#avquaddevplots_2[0].WritePointPlot(c1,"ttbar",pdfout,[17,20.5]) 
avquaddevplots_2[0].WritePointPlot(c1,"ttbar",pdfout,yaxis[0]) 
avquaddevplots_2[1].WritePointPlot(c1,"ttbar",pdfout,yaxis[1]) 
#avquaddevplots_2[2].WritePointPlot(c1,"ttbar",pdfout,[10.3,12.2]) 
avquaddevplots_2[2].WritePointPlot(c1,"ttbar",pdfout,yaxis[2]) 
avquaddevplots_2[3].WritePointPlot(c1,"ttbar",pdfout,yaxis[3]) 
avquaddevplots_2[4].WritePointPlot(c1,"ttbar",pdfout,yaxis[4]) 


if not onlydoDeviations:
    for i in range(len(quaddevs_list)):
        for j in range(len(quaddevs_list[0])):
            quaddevs_list[i][j].WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)

    """    
    quaddev_quatile100.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    quaddev_quatile95.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    quaddev_quatile90.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    quaddev_quatile85.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    quaddev_quatile80.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    dev_quatile100.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    """

avquaddevplot_train_2 = PointPlot(len(names),"Av. quadr. deviation (GeV)",legendtext)
avquaddevplot_train_2_best95= PointPlot(len(names),"Av. quadr. deviation (GeV) of best 95 %",legendtext)
avquaddevplot_train_2_best90 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 90 %",legendtext)
avquaddevplot_train_2_best85 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 85 %",legendtext)
avquaddevplot_train_2_best80 = PointPlot(len(names),"Av. quadr. deviation (GeV) of best 80 %",legendtext)

avquaddevplots_train_2 = [avquaddevplot_train_2,avquaddevplot_train_2_best95,avquaddevplot_train_2_best90,avquaddevplot_train_2_best85,avquaddevplot_train_2_best80]

avquaddevplot_train_2.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_train_2_best95.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_train_2_best90.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_train_2_best85.setmanualegendsize("right",0.6,0.50,0.88,0.88)
avquaddevplot_train_2_best80.setmanualegendsize("right",0.6,0.50,0.88,0.88)


avquaddevplot_train_2.addLabel(0.04,0.03,"Training Sample",0,0.035)
avquaddevplot_train_2_best95.addLabel(0.04,0.03,"Training Sample",0,0.035)
avquaddevplot_train_2_best90.addLabel(0.04,0.03,"Training Sample",0,0.035)
avquaddevplot_train_2_best85.addLabel(0.04,0.03,"Training Sample",0,0.035)
avquaddevplot_train_2_best80.addLabel(0.04,0.03,"Training Sample",0,0.035)

avquaddevplot_train_2.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_train_2_best95.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_train_2_best90.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_train_2_best85.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
avquaddevplot_train_2_best80.addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)


for k in range(len(quaddevs_list[1])):
    for n in range(len(names)):
        avquaddevplots_train_2[k].addPoint(*getAvQuadDevfromHisto(quaddevs_list[1][k].getHistos()[n]))


"""
#avquaddevplots_train_2[0].WritePointPlot(c1,"ttbar",pdfout,[17,20.5]) 
avquaddevplots_train_2[0].WritePointPlot(c1,"ttbar",pdfout,yaxis[0]) 
avquaddevplots_train_2[1].WritePointPlot(c1,"ttbar",pdfout,yaxis[1]) 
#avquaddevplots_train_2[2].WritePointPlot(c1,"ttbar",pdfout,[10.3,12.2]) 
avquaddevplots_train_2[2].WritePointPlot(c1,"ttbar",pdfout,yaxis[2]) 
avquaddevplots_train_2[3].WritePointPlot(c1,"ttbar",pdfout,yaxis[3]) 
avquaddevplots_train_2[4].WritePointPlot(c1,"ttbar",pdfout,yaxis[4]) 
"""

avquaddevplots_train_2[0].WritePointPlot(c1,"ttbar",pdfout) 
avquaddevplots_train_2[1].WritePointPlot(c1,"ttbar",pdfout) 
avquaddevplots_train_2[2].WritePointPlot(c1,"ttbar",pdfout) 
avquaddevplots_train_2[3].WritePointPlot(c1,"ttbar",pdfout) 
avquaddevplots_train_2[4].WritePointPlot(c1,"ttbar",pdfout) 


if not onlydoDeviations:
    deviations_test.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    deviations_test_best90.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)
    deviations_train_best90.WriteHisto(c1,"ttbar",False, False, pdfout, False, False, True)



errorplot_test_R2 = PointPlot(len(names),"R^{2} Statistic",legendtext)
errorplot_test_err_squared = PointPlot(len(names),"Error with squared loss function (GeV)",legendtext)
errorplot_test_err_abs = PointPlot(len(names),"Error with abs loss function (GeV)",legendtext)
errorplot_train_R2 = PointPlot(len(names),"R^{2} Statistic",legendtext)
errorplot_train_err_squared = PointPlot(len(names),"Error with squared loss function (GeV)",legendtext)
errorplot_train_err_abs = PointPlot(len(names),"Error with abs loss function (GeV)",legendtext)

errorplots = [[errorplot_test_R2,errorplot_test_err_squared,errorplot_test_err_abs],[errorplot_train_R2,errorplot_train_err_squared,errorplot_train_err_abs]]


for i in range(len(errorlist)):
    #for j in range(len(errorplots[i])):
    for j in range(len(errorplots[i])):
        errorplots[i][j].addLabel(0.04,0.03,labels[i],0,0.035)
        errorplots[i][j].addLabel(0.92,0.325,"1: nTrees, 2: Shrinkage, 3: MaxDepth, 4:nCuts",90,0.03)
    for k in range(len(errorlist[i])):
        errorplots[i][0].addPoint(errorlist[i][k].getvalues()["R^2"])
        errorplots[i][1].addPoint(errorlist[i][k].getvalues()["err_squared_loss"])
        errorplots[i][2].addPoint(errorlist[i][k].getvalues()["err_abs_loss"])

for i in range(len(errorplots)):
    for j in range(len(errorplots[i])):
        if j == 0:
            errorplots[i][j].WritePointPlot(c1,"ttbar",pdfout,None, "Max") 
        else:
            errorplots[i][j].WritePointPlot(c1,"ttbar",pdfout) 

pdfout.closePDF()
