#Usage: python compute_reg_performace_eval.py RegOutput.root
import ROOT
import sys
from plotscripts.plotting import *
from plotscripts.rootutils import PDFPrinting
from regressionTools import computeMutualInfo
from array import array

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)

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
for key in inputvardir.GetListOfKeys():
    if key.GetClassName() == 'TH1F':
        keylist.append(inputvardir.Get(key.GetName()).GetName().split("__")[0]) #Get key for plotting module from inputvar histo
        arraydict.update({ inputvardir.Get(key.GetName()).GetName().split("__")[0] : array('f',[0])})
keylist.append("Jet_regPt")
arraydict.update({"Jet_regPt" : array('f',[0])})

print keylist

    


print ""
print ""

TwoDdic = {}

#make 2d histos for target with every inputvariable
for i in range(len(keylist)-1):
    tmp = TwoDplot(keylist[i],keylist[len(keylist)-1])
    TwoDdic.update({tmp.GetCombinedKey() : tmp})

print TwoDdic



if useboth:
    trees =  [inputfile.Get(testtreekey.GetName()),inputfile.Get(traintreekey.GetName())]
else:
    if usetesttree:
        trees = [inputfile.Get(testtreekey.GetName())]
    else:
        trees = [inputfile.Get(traintreekey.GetName())]



nEntries = 0

for tree in trees:
    print "Starting with tree",tree
    nEntries = tree.GetEntries()
    for key in keylist:
        if key == "Jet_regPt":
            tree.SetBranchAddress("BDTG", arraydict[key])
        else:
            tree.SetBranchAddress(key, arraydict[key])
    
    xmin = 1000000000
    xmax = -1000000000
    
    rV = []
    tV = []
    wV = []

    for ie in range(nEntries):
    
        if ie%10000 == 0:
            print ie
            
        entryValues = {}
        tree.GetEvent(ie)
        for key in TwoDdic:
            name0 = key.split("__")[0]
            name1 = key.split("__")[1]
            TwoDdic[key].FillTwoDplot(arraydict[name0][0],arraydict[name1][0])
        #find max/min
        xmin = min(xmin, min(arraydict["Jet_PartonPt"][0],arraydict["Jet_regPt"][0]))
        xmax = max(xmax, max(arraydict["Jet_PartonPt"][0],arraydict["Jet_regPt"][0]))
        
        tV.append(arraydict["Jet_PartonPt"][0])
        rV.append(arraydict["Jet_regPt"][0])
        wV.append(1)


hist  = ROOT.TH2F( "hist",  "hist",  150, xmin, xmax, 100, xmin, xmax );
#histT = ROOT.TH2F( "histT", "histT", 150, xmin, xmax, 100, xmin, xmax );

for iev in range(nEntries):
    #d = rV[iev]-tV[iev]
    hist.Fill(rV[iev],tV[iev],wV[iev])
    

print computeMutualInfo(hist)


exit()

"""
c1 = ROOT.TCanvas()
for key in TwoDdic:
    TwoDdic[key].GetTH2F().Draw("colz")
    c1.Update()
    raw_input("press ret")
raw_input("press ret")
"""

outputfile = ROOT.TFile(sys.argv[2]+".root","RECREATE")
pdfout = PDFPrinting(sys.argv[2])
c1 = ROOT.TCanvas()

for key in TwoDdic:
    TwoDdic[key].WriteTwoDPlot(c1,pdfout)

pdfout.closePDF()


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


