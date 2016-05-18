import ROOT
import array


from regressionTools import *
from plotscripts.plotting import *
from plotscripts.rootutils import PDFPrinting


ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)


filelist = ["BReg_0330_newVars.root","BReg_0420_wPU.root","BReg_0502_wPU_nocorr.root","BReg_0502_wPU_nocorrandfrac.root","BReg_0509_wPU_noelfrac.root","BReg_0509_wPU_nohadfrac.root","BReg_0509_heppysetting.root","BReg_0511_heppysetting600.root","BReg_0511_heppysetting1200.root"]

outname = "testalltrainings_0518"
#outfile = ROOT.TFile(outname+".root","RECREATE")
pdfout = PDFPrinting(outname)
c1 = ROOT.TCanvas()  



legend = ["Std. Training","Std. Training w/ PU Weight","Std. Training w/o JEC corr.","Std. Training w/o JEC corr and Fracs","Std. Training w/o em Frac","Std. Training w/o had Frac","Heppy Training","Heppy Training w/ 600 Trees","Heppy Training w/ 1200 Trees"] 

allerrors_train = []
allerrors_test = []

ntest = []
ntrain = []


for it, training in enumerate(filelist):
    
    trainingfile = ROOT.TFile(training)

    trees =["TestTree","TrainTree"]
    
    trainval_sq = 0
    testval_sq = 0
    trainval_abs = 0
    testval_abs = 0

    
    test_R2 = PointPlot(2,"R^{2} Statistic",trees)
    test_sqerr = PointPlot(2,"Error with squared loss function",trees)
    test_abserr = PointPlot(2,"Error with abs loss function",trees)

    test_R2.changeColorlist([ROOT.kBlue+2,ROOT.kOrange-3])
    test_sqerr.changeColorlist([ROOT.kBlue+2,ROOT.kOrange-3])
    test_abserr.changeColorlist([ROOT.kBlue+2,ROOT.kOrange-3])

    test_R2.addLabel(0.04,0.03,legend[it],0,0.035)
    test_sqerr.addLabel(0.04,0.03,legend[it],0,0.035)
    test_abserr.addLabel(0.04,0.03,legend[it],0,0.035)
    

    for treename in trees:
        tree = trainingfile.Get(treename)
        
        errors = Errors()

        
        for nev in range(tree.GetEntries()):
            tree.GetEvent(nev)
            errors.addevent(tree.BDTG,tree.Jet_MatchedPartonPt_D_Jet_Pt)

        errors.printerr()
        
        errvals = errors.getvalues()        

        test_R2.addPoint(errvals["R^2"])
        test_sqerr.addPoint(errvals["err_squared_loss"])
        test_abserr.addPoint(errvals["err_abs_loss"])
    
        if treename == "TestTree":
            allerrors_test.append(errvals)
            ntest.append(tree.GetEntries())
            testval_sq = errvals["err_squared_loss"]
            testval_abs = errvals["err_abs_loss"]
        else:
            allerrors_train.append(errvals)
            ntrain.append(tree.GetEntries())
            trainval_sq = errvals["err_squared_loss"]
            trainval_abs = errvals["err_abs_loss"]
            

        del tree, errors, errvals
        
    test_sqerr.addLabel(0.75,0.03,"Difference: "+str((1 - (trainval_sq /  testval_sq))*100)[0:6]+" %",0,0.035)
    test_abserr.addLabel(0.75,0.03,"Difference: "+str((1 - (trainval_abs /  testval_abs))*100)[0:6]+" %",0,0.035)
    
    

    test_R2.WritePointPlot(c1,"ttHbb",pdfout,None,"Max")
    test_sqerr.WritePointPlot(c1,"ttHbb",pdfout)
    test_abserr.WritePointPlot(c1,"ttHbb",pdfout)

    del test_R2,test_sqerr,test_abserr
    del trainingfile


    
test_R2_test = PointPlot(len(legend),"R^{2} Statistic",legend)
test_sqerr_test = PointPlot(len(legend),"Error with squared loss function",legend)
test_abserr_test = PointPlot(len(legend),"Error with abs loss function",legend)

test_R2_test.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
test_sqerr_test.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
test_abserr_test.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])

test_R2_test.addLabel(0.04,0.03,"Test Sampel",0,0.035)
test_sqerr_test.addLabel(0.04,0.03,"Test Sampel",0,0.035)
test_abserr_test.addLabel(0.04,0.03,"Test Sampel",0,0.035)

test_R2_train = PointPlot(len(legend),"R^{2} Statistic",legend)
test_sqerr_train = PointPlot(len(legend),"Error with squared loss function",legend)
test_abserr_train = PointPlot(len(legend),"Error with abs loss function",legend)

test_R2_train.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
test_sqerr_train.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])
test_abserr_train.changeColorlist([ROOT.kBlack,ROOT.kBlue+2,ROOT.kGreen+2,ROOT.kRed+2,ROOT.kViolet-6, ROOT.kOrange-3,ROOT.kBlue-6,ROOT.kRed-4, ROOT.kGreen-7,ROOT.kBlue])

test_R2_train.addLabel(0.04,0.03,"Training Sample",0,0.035)
test_sqerr_train.addLabel(0.04,0.03,"Training Sample",0,0.035)
test_abserr_train.addLabel(0.04,0.03,"Training Sample",0,0.035)


for i in range(len(allerrors_test)):
    
    test_R2_test.addPoint(allerrors_test[i]["R^2"])
    test_sqerr_test.addPoint(allerrors_test[i]["err_squared_loss"])
    test_abserr_test.addPoint(allerrors_test[i]["err_abs_loss"])

    test_R2_train.addPoint(allerrors_train[i]["R^2"])
    test_sqerr_train.addPoint(allerrors_train[i]["err_squared_loss"])
    test_abserr_train.addPoint(allerrors_train[i]["err_abs_loss"])

    
    print ntest[i]
    print ntrain[i]

test_R2_test.WritePointPlot(c1,"ttHbb",pdfout,None,"Max")
test_sqerr_test.WritePointPlot(c1,"ttHbb",pdfout,[0.042,0.06])
test_abserr_test.WritePointPlot(c1,"ttHbb",pdfout)

test_R2_train.WritePointPlot(c1,"ttHbb",pdfout,None,"Max")
test_sqerr_train.WritePointPlot(c1,"ttHbb",pdfout,[0.042,0.06])
test_abserr_train.WritePointPlot(c1,"ttHbb",pdfout)

pdfout.closePDF()
