#Usage: python simple_reg_performance.py RegOutput.root outputname
#
#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from array import array
#-------------------------------------------------------------------------------------#
#
#
#-------------------------------------------------------------------------------------#
#Add path to bjetreg folder to path, that scripts from there can be used
parentpath = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
bjetregpath = parentpath+"/"+"bjetRegression"

print parentpath
print bjetregpath
sys.path.append(bjetregpath)
#-------------------------------------------------------------------------------------#
#
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from plotscripts.plotting import *
from plotscripts.rootutils import PDFPrinting
from regressionTools import *
#-------------------------------------------------------------------------------------#

ROOT.gStyle.SetOptStat(0);
#ROOT.gROOT.SetBatch(True)

#read Regressiion output file:
inputfile = ROOT.TFile(sys.argv[1])


for key in inputfile.GetListOfKeys():
    if key.GetName() == "InputVariables_Id":
        idir = key
    if key.GetName() == "TestTree":
        testtreekey = key
    if key.GetName() == "TrainTree":
        traintreekey = key
    #print key

inputvardir = inputfile.Get(idir.GetName())

usetesttree = True
useboth = False
keylist = []
arraydict = {}
binvars = {}
for key in inputvardir.GetListOfKeys():
    if key.GetClassName() == 'TH1F':
        keylist.append(inputvardir.Get(key.GetName()).GetName().split("__")[0]) #Get key for plotting module from inputvar histo
        arraydict.update({ inputvardir.Get(key.GetName()).GetName().split("__")[0] : array('f',[0])})
        if inputvardir.Get(key.GetName()).GetName().split("__")[0] != "var1" and inputvardir.Get(key.GetName()).GetName().split("__")[0] != "target":
            binvars.update({inputvardir.Get(key.GetName()).GetName().split("__")[0] : [50,-1,1]})
        else:
            binvars.update({inputvardir.Get(key.GetName()).GetName().split("__")[0] : [100,-1,4]})
keylist.append("BDTG")
arraydict.update({"BDTG" : array('f',[0])})
binvars.update({"BDTG" : [100,-1,4]})

print keylist
print arraydict
print binvars



print ""
print ""

TwoDdic = {}

#make 2d histos for target with every inputvariable
for i in range(len(keylist)-1):
    tmp = TwoDplot(keylist[i],keylist[len(keylist)-1], binvars[keylist[i]], binvars[keylist[len(keylist)-1]] )
    TwoDdic.update({tmp.GetCombinedKey() : tmp})


normHdic = {}

for i in range(len(keylist)):
    tmp = normPlots(keylist[i], False, 2, [], binvars[keylist[i]])
    normHdic.update({keylist[i] : tmp}) 



targetvsBDTGH = normPlots("BDTG", True, 2, ["target","BDGT"], [100,-1,4])
targetvsvar1H = normPlots("target", True, 2, ["target","var1"], [100,-1,4])


performanceHdic = { "div_evt" : normPlots("div_event", False, 2, [], [60,0,0.3])}




print TwoDdic
print normHdic
print performanceHdic

raw_input("press ret")

if useboth:
    trees =  [inputfile.Get(testtreekey.GetName()),inputfile.Get(traintreekey.GetName())]
else:
    if usetesttree:
        trees = [inputfile.Get(testtreekey.GetName())]
    else:
        trees = [inputfile.Get(traintreekey.GetName())]



nEntries = 0

for tree in trees:
    errors = Errors()
    
    print "Starting with tree",tree
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

        tree.GetEvent(ie)        
        
        errors.addevent(arraydict["BDTG"][0],arraydict["target"][0])
        

        for key in keylist:
            #print key, arraydict[key][0]
            normHdic[key].FillnormHisto(arraydict[key][0])
            
        performanceHdic["div_evt"].FillnormHisto((arraydict["BDTG"][0] - arraydict["target"][0])*(arraydict["BDTG"][0] - arraydict["target"][0]))

        targetvsBDTGH.FillnormHisto(arraydict["target"][0],0)
        targetvsBDTGH.FillnormHisto(arraydict["BDTG"][0],1)

        targetvsvar1H.FillnormHisto(arraydict["target"][0],0)
        targetvsvar1H.FillnormHisto(arraydict["var1"][0],1)
        
        entryValues = {}

        for key in TwoDdic:
            name0 = key.split("__")[0]
            name1 = key.split("__")[1]
            TwoDdic[key].FillTwoDplot(arraydict[name0][0],arraydict[name1][0])
        #find max/min
        xmin = min(xmin, min(arraydict["target"][0],arraydict["BDTG"][0]))
        xmax = max(xmax, max(arraydict["target"][0],arraydict["BDTG"][0]))
        
        tV.append(arraydict["target"][0])
        rV.append(arraydict["BDTG"][0])
        wV.append(1)

        



hist  = ROOT.TH2F( "hist for mutinf",  "hist for mutinf",  150, xmin, xmax, 100, xmin, xmax );
#histT = ROOT.TH2F( "histT", "histT", 150, xmin, xmax, 100, xmin, xmax );

for iev in range(nEntries):
    #d = rV[iev]-tV[iev]
    hist.Fill(rV[iev],tV[iev],wV[iev])





#exit()


c1 = ROOT.TCanvas()
"""
for key in TwoDdic:
    TwoDdic[key].GetTH2F().Draw("colz")
    c1.Update()
    raw_input("press ret")
"""
outputfile = ROOT.TFile(sys.argv[2]+".root","RECREATE")
pdfout = PDFPrinting(sys.argv[2])
#c1 = ROOT.TCanvas()



hist.Draw("colz")
c1.Update()
c1.Write()

print xmin, xmax

pdfout.addCanvastoPDF(c1)

for key in keylist:
    normHdic[key].WriteHisto(c1,None,False,False, pdfout)

for key in performanceHdic:
    performanceHdic[key].WriteHisto(c1,None,False,False, pdfout)

targetvsBDTGH.WriteHisto(c1,None,False,False, pdfout)
targetvsvar1H.WriteHisto(c1,None,False,False, pdfout)

"""
for key in TwoDdic:
    TwoDdic[key].WriteTwoDPlot(c1,pdfout)
"""
pdfout.closePDF()


print "Mutual Information on",tree,"->",computeMutualInfo(hist)
getDiviationtests(normHdic["target"].getHistos()[0],normHdic["BDTG"].getHistos()[0])

errors.computeerr()
errors.printerr()

"""
milist = []
for key in TwoDdic:
    milist.append([key ,computeMutualInfo(TwoDdic[key].GetTH2F())])

milist_sorted = sorted(milist, key = lambda x : float(x[1]))

for elem in milist_sorted[::-1]:
    print elem[0], elem[1]


res = 0
for i in range(len(milist)):
    res = res + milist[i][1]

print res/(len(milist)-1)

"""
