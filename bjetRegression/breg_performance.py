#Usage: python simple_reg_performance.py RegOutput.root outputname
#
#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from array import array
from glob import glob
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from plotscripts.plotting import *
from plotscripts.rootutils import PDFPrinting
from regressionTools import *
#-------------------------------------------------------------------------------------#
#

#
#-------------------------------------------------------------------------------------#
# Set Variables
singlemode = False
useglob = False

if not singlemode:
    if useglob:
        filenames = glob(str(sys.argv[3])+"/*.root")
    else:
        filenames = sys.argv[3:] 
    #inputfiles = map(lambda x : ROOT.TFile(x), filenames)
    names = map(lambda x : x.split("/")[-1][:-5], filenames)
    
else:
    filenames = [sys.argv[3]]
    #inputfiles = [ROOT.TFile(sys.argv[3])]
    names = map(lambda x : x.split("/")[-1][:-5], filenames)
    

#print inputfiles

usetesttree = True #if False use train tree
 
outputfolder = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/output_5/" #has to be created first

tableprefix = "firstrun_"+sys.argv[2]+"_"

targetname = "Jet_PartonPt" #name of Regression target

maxevts = 100000000

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)
#-------------------------------------------------------------------------------------#
#

errordic = {}
testdic = {}

for ifile, filename in enumerate(filenames):
    inputfile = ROOT.TFile(filename)
    for key in inputfile.GetListOfKeys():
        if key.GetName() == "InputVariables_Id":
            idir = key
        if key.GetName() == "TestTree":
            testtreekey = key
        if key.GetName() == "TrainTree":
            traintreekey = key
        #print key

    inputvardir = inputfile.Get(idir.GetName())


    keylist = []
    arraydict = {}
    for key in inputvardir.GetListOfKeys():
        if key.GetClassName() == 'TH1F':
            keylist.append(inputvardir.Get(key.GetName()).GetName().split("__")[0]) #Get key for plotting module from inputvar histo
            arraydict.update({ inputvardir.Get(key.GetName()).GetName().split("__")[0] : array('f',[0])})
    #        if inputvardir.Get(key.GetName()).GetName().split("__")[0] != "var1" and inputvardir.Get(key.GetName()).GetName().split("__")[0] != targetname:
    #            binvars.update({inputvardir.Get(key.GetName()).GetName().split("__")[0] : [50,-1,1]})
    #        else:
    #            binvars.update({inputvardir.Get(key.GetName()).GetName().split("__")[0] : [100,-1,4]})
    keylist.append("BDTG")
    arraydict.update({"BDTG" : array('f',[0])})
    #binvars.update({"BDTG" : [100,-1,4]})

    #print keylist
    #print arraydict
    #print binvars



    #print ""
    #print ""

    #TwoDdic = {}

    #make 2d histos for target with every inputvariable
    #for i in range(len(keylist)-1):
    #    tmp = TwoDplot(keylist[i],keylist[len(keylist)-1], binvars[keylist[i]], binvars[keylist[len(keylist)-1]] )
    #    TwoDdic.update({tmp.GetCombinedKey() : tmp})


    normHdic = {}

    for i in range(len(keylist)):
        if keylist[i] == "BDTG":
            tmp = normPlots(keylist[i], False, 2, [], [200,0,600] )
        else:
            tmp = normPlots(keylist[i], False, 2)
        normHdic.update({keylist[i] : tmp}) 



    targetvsBDTGH = normPlots("BDTG", True, 2, [targetname,"BDTG"],[200,0,600])
    targetvsvar1H = normPlots(targetname, True, 2, [targetname,"Jet_Pt"])


    performanceHdic = { "div_evt" : normPlots("div_event", False, 2, [], [100,0,2])}




    #print TwoDdic
    #print normHdic
    #print performanceHdic

    #raw_input("press ret")

    if usetesttree:
        tree = inputfile.Get(testtreekey.GetName())
    else:
        tree = inputfile.Get(traintreekey.GetName())

    nEntries = 0

    #Set Classes for test and errors
    errors = Errors()
    tests = Tests()

    nEntries = tree.GetEntries()
    for key in keylist:
        tree.SetBranchAddress(key, arraydict[key])


    xmin = 1000000000
    xmax = -1000000000

    rV = []
    tV = []
    wV = []


    for ie in range(nEntries):

        if ie%10000 == 0:
            print ie
        if ie == maxevts:
            break

        tree.GetEvent(ie)        

        errors.addevent(arraydict["BDTG"][0],arraydict[targetname][0])


        for key in keylist:
            #print key, arraydict[key][0]
            normHdic[key].FillnormHisto(arraydict[key][0])

        performanceHdic["div_evt"].FillnormHisto((arraydict["BDTG"][0] - arraydict[targetname][0])*(arraydict["BDTG"][0] - arraydict[targetname][0]))

        targetvsBDTGH.FillnormHisto(arraydict[targetname][0],0)
        targetvsBDTGH.FillnormHisto(arraydict["BDTG"][0],1)

        targetvsvar1H.FillnormHisto(arraydict[targetname][0],0)
        targetvsvar1H.FillnormHisto(arraydict["Jet_Pt"][0],1)

        entryValues = {}

        #for key in TwoDdic:
        #    name0 = key.split("__")[0]
        #    name1 = key.split("__")[1]
        #    TwoDdic[key].FillTwoDplot(arraydict[name0][0],arraydict[name1][0])
        #find max/min
        xmin = min(xmin, min(arraydict[targetname][0],arraydict["BDTG"][0]))
        xmax = max(xmax, max(arraydict[targetname][0],arraydict["BDTG"][0]))

        tV.append(arraydict[targetname][0])
        rV.append(arraydict["BDTG"][0])
        wV.append(1)




    mutinfoH = TwoDplot("BDTG Output","Jet_PartonPt",[150, xmin, xmax], [100, xmin, xmax])
    #hist  = ROOT.TH2F( "hist for mutinf",  "hist for mutinf",  150, xmin, xmax, 100, xmin, xmax )
    #histT = ROOT.TH2F( "histT", "histT", 150, xmin, xmax, 100, xmin, xmax );

    for iev in range(nEntries):
        if iev == maxevts:
            break
        #d = rV[iev]-tV[iev]
        #hist.Fill(rV[iev],tV[iev],wV[iev])
        mutinfoH.FillTwoDplot(rV[iev],tV[iev])



    pdfout = PDFPrinting(outputfolder+sys.argv[1]+names[ifile])
    outputfile = ROOT.TFile(outputfolder+sys.argv[1]+names[ifile]+".root","RECREATE")
    outputfile.cd()
    c1 = ROOT.TCanvas()

    #hist.Draw("colz")
    #c1.Update()
    #c1.Write()

    #print xmin, xmax

    #pdfout.addCanvastoPDF(c1)

    #-----------------------------------------------------------------------------------------------------------------------------------#
    # Remove for other files
    tmplist = names[ifile].split("_") 
    nTree = tmplist[-4]
    shrink = tmplist[-3]
    maxDepth = tmplist[-2]
    nCuts = tmplist[-1]
    
    targetvsBDTGH.addLabel(0.925,0.115,"nTrees: "+nTree+", Shrinkage: "+shrink+", MaxDepth: "+maxDepth+", nCuts: "+nCuts,90,0.032)
    targetvsvar1H.addLabel(0.925,0.115,"nTrees: "+nTree+", Shrinkage: "+shrink+", MaxDepth: "+maxDepth+", nCuts: "+nCuts,90,0.032)
    for key in keylist:
        normHdic[key].addLabel(0.925,0.115,"nTrees: "+nTree+", Shrinkage: "+shrink+", MaxDepth: "+maxDepth+", nCuts: "+nCuts,90,0.032)
    for key in performanceHdic:
        performanceHdic[key].addLabel(0.925,0.115,"nTrees: "+nTree+", Shrinkage: "+shrink+", MaxDepth: "+maxDepth+", nCuts: "+nCuts,90,0.032)
    mutinfoH.addLabel(0.89,0.115,"nTrees: "+nTree+", Shrinkage: "+shrink+", MaxDepth: "+maxDepth+", nCuts: "+nCuts,90,0.032)
    #-----------------------------------------------------------------------------------------------------------------------------------#
    

    mutinfoH.WriteTwoDPlot(c1,"ttbar",pdfout)

    for key in keylist:
        normHdic[key].WriteHisto(c1,"ttbar",False,False, pdfout)
        for i in range(normHdic[key].getNumOfHistos()):
            normHdic[key].getHistos()[i].Write()
        
    for key in performanceHdic:
        performanceHdic[key].WriteHisto(c1,"ttbar",False,False, pdfout)
        for i in range(performanceHdic[key].getNumOfHistos()):
            performanceHdic[key].getHistos()[i].Write()

    targetvsBDTGH.WriteHisto(c1,"ttbar",False,False, pdfout)
    targetvsvar1H.WriteHisto(c1,"ttbar",False,False, pdfout)


    pdfout.closePDF()
    
    tests.computeMutualInfo(mutinfoH.GetTH2F())
    tests.runDiviationtests(normHdic[targetname].getHistos()[0],normHdic["BDTG"].getHistos()[0])

    errors.computeerr()
    
    
    tests.printtests()
    errors.printerr()

    errordic.update({ names[ifile] : errors })
    testdic.update({ names[ifile] : tests })
    
    
    #Delete variables that could lead to memory problems
    del c1, pdfout, normHdic, performanceHdic, targetvsBDTGH, targetvsvar1H, outputfile, mutinfoH, tests, errors, tree, inputfile


writevaluetopy(errordic,outputfolder+tableprefix+"error_values")
writevaluetopy(testdic,outputfolder+tableprefix+"test_values")
         
#Save error and test results in latex tables
writevaluetable(errordic,outputfolder+tableprefix+"table_error_all","script",["all"])
writevaluetable(errordic,outputfolder+tableprefix+"table_error_errors","script",["RSE", "R^2", "err_squared_loss", "err_abs_loss"])
writevaluetable(errordic,outputfolder+tableprefix+"table_error_R2","script",["R^2","RSS","TSS"])

writevaluetable(testdic,outputfolder+tableprefix+"table_test_all","script",["all"])
writevaluetable(testdic,outputfolder+tableprefix+"table_test_run","script",["runtest-r","runtest-r_exp","runtest-r_div_sig"])
writevaluetable(testdic,outputfolder+tableprefix+"table_test_div","script",["max_div_abs_up", "max_div_abs_down", "max_div_percent_up", "max_div_percent_down"])
writevaluetable(testdic,outputfolder+tableprefix+"table_test_rest","script",[ "chi2", "KS", "Binned_div", "mutualinfo"])

"""

pylines = [writevaliedotpy(errordic,outputfolder+tableprefix+"error_values")
             writevaliedotpy(testdic,outputfolder+tableprefix+"test_values")]
         
         #Save error and test results in latex tables
filelines = [writevaluetable(errordic,outputfolder+tableprefix+"table_error_all","script",["all"]),
             writevaluetable(errordic,outputfolder+tableprefix+"table_error_errors","script",["RSE", "R^2", "err_squared_loss", "err_abs_loss"]),
             writevaluetable(errordic,outputfolder+tableprefix+"table_error_R2","script",["R^2","RSS","TSS"]),
             
             writevaluetable(testdic,outputfolder+tableprefix+"table_test_all","script",["all"]),
             writevaluetable(testdic,outputfolder+tableprefix+"table_test_run","script",["runtest-r","runtest-r_exp","runtest-r_div_sig"]),
             writevaluetable(testdic,outputfolder+tableprefix+"table_test_div","script",["max_div_abs_up", "max_div_abs_down", "max_div_percent_up", "max_div_percent_down"]),
             writevaluetable(testdic,outputfolder+tableprefix+"table_test_rest","script",[ "chi2", "KS", "Binned_div", "mutualinfo"])]

for fl in filelines:
    with open(fl[0]+'.txt', 'w') as f:
        for line in fl[1:]:
            f.write(line)
    f.close
    del f

for fl in pylines:
    with open(fl[0]+'.py', 'w') as f:
        for line in fl[1:]:
            f.write(line)
    f.close
    del f
"""
print "saving tables to",outputfolder+tableprefix+"table*"
