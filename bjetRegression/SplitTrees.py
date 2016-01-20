#Usage: python SplitTrees.py treename inputfile outpath prefix
import ROOT
import sys
import os


#Get system arguments
treename = sys.argv[1]
inputfilename = sys.argv[2]
outpath = sys.argv[3]
outfile_prefix = sys.argv[4]


EventsPerFile = 100000


inputfile = ROOT.TFile(inputfilename)
inputTree = inputfile.Get(treename)

outputTree_num = (inputTree.GetEntries() / EventsPerFile) + 1

outputFiles = []
for i in range(outputTree_num):
    outputFiles.append(str(outfile_prefix)+"_"+str(i)+".root")
print outputFiles
eventnum = 1
currentoutfileindex = 0
print "Inputfile has",inputTree.GetEntries(),"Entries --> There will be",outputTree_num,"Trees"
tmpOutFile = ROOT.TFile(str(outpath)+"/"+str(outputFiles[currentoutfileindex]),"RECREATE")
for i in range(inputTree.GetEntries()+1):
    if(eventnum == EventsPerFile+1 or i == inputTree.GetEntries()):
        print "saving in i=",i
        eventnum = 1
        #Save tmpTree to file before deleting it
        print "Saving Tree ",currentoutfileindex,"(",tmpTree,")","with",tmpTree.GetEntries(),"Events in File",tmpOutFile
        tmpOutFile.cd()
        tmpTree.Write()
        del tmpTree
        del tmpOutFile
        if  i == inputTree.GetEntries():
            exit()
        else:
            currentoutfileindex = currentoutfileindex +1 
            tmpOutFile = ROOT.TFile(str(outpath)+"/"+str(outputFiles[currentoutfileindex]),"RECREATE")
    if(eventnum == 1):
        print "Creating tmptree in i=",i,"with index=",currentoutfileindex
        #Clone Tree without any entries, to get empty tree with same branches
        tmpTree = inputTree.CloneTree(0)
    inputTree.GetEvent(i)
    tmpTree.Fill()
    eventnum = eventnum + 1
    


