
#-------------------------------------------------------------------------------------#
# Import standard python modules
import ROOT
import sys
import os
from copy import deepcopy
from glob import glob
from array import array
#
#-------------------------------------------------------------------------------------#
# Import custom modules
from evalBDT import *
from plotscripts.JetRegression import JetRegression, getHiggsMasswcorr, getHiggsMass, gethadtopMasswcorr, gethadtopMass

#-------------------------------------------------------------------------------------#
#
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);
#
#-------------------------------------------------------------------------------------#
# Set Variables
outfilename = sys.argv[1]

inputvariables = [ "RegJet_preregPt",
                   "RegJet_corr",
                   "RegJet_regcorr",
                   "RegJet_Eta",
                   "RegJet_M",
                   "RegJet_preregMt",
                   "RegJet_leadTrackPt",
                   "RegJet_Flav",
                   "RegJet_PartonFlav",
                   "RegJet_leptonPt",
                   "RegJet_leptonPtRel",
                   "RegJet_leptonDeltaR",
                   "RegJet_nHEFrac",
                   "RegJet_cHEFrac",
                   "RegJet_chargedMult",
                   "RegJet_nEmEFrac",
                   "RegJet_totHEFrac",
                   "RegJet_vtxPt",
                   "RegJet_CSV",
                   "RegJet_vtxMass",
                   "RegJet_vtx3DVal",
                   "RegJet_vtxNtracks",
                   "RegJet_vtx3DSig",
                   "RegJet_MatchedPartonFlav",
                   "RegJet_MatchedPartonPt",
                   "RegJet_MatchedPartonDeltaR",
                   "RegJet_MatchedGenJetwNuPt",
                   "RegJet_Phi",
                   "RegJet_E"]

weightlist = ["/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_big_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_noemfrac_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_nohadfrac_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_noFracnovtxMass_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0912_BaseLine_wowortsVars_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/JetRegression/training/trees0905/TMVA/weights/BReg_0906_BaseLine_parton_BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training1__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training2__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training3__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training4__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training5__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training6__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training7__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training80__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training9__BDTG.weights.xml",
              "/nfs/dust/cms/user/kschweig/Code/stuff/weights/training10__BDTG.weights.xml"]

weightnames = ["nominal",
               "Big",
               "noemFrac",
               "nohadFrac",
               "noFracnovtxMass",
               "woworstVars",
               "Parton",
               "Shrinkage01",
               "Shrinkage03",
               "Shrinkage0075",
               "nCuts20",
               "nCuts10",
               "nTrees600",
               "nTrees200",
               "Depth4",
               "Depth5",
               "TMVA"]

inputconfigs = ["A","A","B","C","D",None,"A","A","A","A","A","A","A","A","A","A","A"]
target = ["G","G","G","G","G","G","P","G","G","G","G","G","G","G","G","G","G"]

regressions = {}
targets = {}
for iw, weight in enumerate(weightlist):
    regressions[weightnames[iw]] = JetRegression(weight,[],inputconfigs[iw]) 


outputfile = ROOT.TFile( outfilename, "RECREATE" );


path = "/nfs/dust/cms/user/kschweig/JetRegression/trees0908/BDTTraining/ttHbb/*_1_*nominal*.root"

inputtree = ROOT.TChain("MVATree")

#for f in glob(path):
for f in sys.argv[2:]:    
    inputtree.Add(f)
Regvars_input = {}

for variable in inputvariables:
    Regvars_input.update( { variable : array.array('f',20*[0] ) } )
    inputtree.SetBranchAddress( variable , Regvars_input[variable] )

    
isHiggsJet = array.array('f',20*[0])
isWJet = array.array('f',20*[0])
ishadTopJet = array.array('f',20*[0])

inputtree.SetBranchAddress("RegJet_isHiggsJet", isHiggsJet)
inputtree.SetBranchAddress("RegJet_isWJet", isWJet)
inputtree.SetBranchAddress("RegJet_ishadTopJet", ishadTopJet)


    
outputfile.cd()
    
OutputTree =  ROOT.TTree("MVATree","MVATree");

E_Odd = array.array('f',[0])
E_Weight = array.array('f',[0])
P_Weight = array.array('f',[0])
P69_Weight = array.array('f',[0])
C_Weight = array.array('f',[0])
LSF = array.array('f',[0])

eSFGFS = array.array('f',[0])
eSFID = array.array('f',[0])
eSFIso = array.array('f',[0])
eSFTrigger = array.array('f',[0])
mSFID = array.array('f',[0])
mSFTrigger = array.array('f',[0])
mSFIso = array.array('f',[0])
mSFHIP = array.array('f',[0])

nleptonicHiggsjets = array.array('I',[0])
nleptonicHadTopjets = array.array('I',[0])


njets = array.array('I',[0])
nbtags = array.array('I',[0])


nPrimaryVertices = array.array('I',[0])
bbmass = array.array('f',[0])
mchiggsmass = array.array('f',[0])
mchadtopmass = array.array('f',[0])


OutputTree.Branch("Evt_Odd",E_Odd,"Evt_Odd/f");
OutputTree.Branch("Weight",E_Weight,"Weight/f");
OutputTree.Branch("Weight_PU",P_Weight,"Weight_PU/f");
OutputTree.Branch("Weight_pu69p2",P69_Weight,"Weight_pu69p2/f");
OutputTree.Branch("Weight_CSV",C_Weight,"Weight_CSV/f");

OutputTree.Branch("Weight_ElectronSFGFS",eSFGFS,"Weight_ElectronSFGFS/f");
OutputTree.Branch("Weight_ElectronSFID",eSFID,"Weight_ElectronSFID/f");
OutputTree.Branch("Weight_ElectronSFIso",eSFIso,"Weight_ElectronSFIso/f");
OutputTree.Branch("Weight_ElectronSFTrigger",eSFTrigger,"Weight_ElectronSFTrigger/f");
OutputTree.Branch("Weight_MuonSFID",mSFID,"Weight_MuonSFID/f");
OutputTree.Branch("Weight_MuonSFTrigger",mSFTrigger,"Weight_MuonSFTrigger/f");
OutputTree.Branch("Weight_MuonSFIso",mSFIso,"Weight_MuonSFIso/f");
OutputTree.Branch("Weight_MuonSFHIP",mSFHIP,"Weight_MuonSFHIP/f");

OutputTree.Branch("Evt_leptonicHiggsJets",nleptonicHiggsjets,"Evt_leptonicHiggsJets/I")
OutputTree.Branch("Evt_leptonicHadTopJets",nleptonicHadTopjets,"Evt_leptonicHadTopJets/I")

OutputTree.Branch("Evt_MCHiggsMass",mchiggsmass,"Evt_MCHiggsMass/F")
OutputTree.Branch("Evt_MCHadTopMass",mchadtopmass,"Evt_MCHadTopMass/F")

OutputTree.Branch("Evt_MCbbMass",bbmass,"Evt_MCbbMass/F")

OutputTree.Branch("N_Jets",njets,"N_Jets/I")
OutputTree.Branch("N_BTagsM",nbtags,"N_BTagsM/I")
OutputTree.Branch("N_PrimaryVertices",nPrimaryVertices,"N_PrimaryVertices/I")

outputs = {}
mchiggs = {}
mchadtop = {}
RegErrors = {}
RegErrorsAbs = {}
RegErrorsQ = {}
Targettype = {}
for ireg, regression in enumerate(weightnames):
    outputs.update( { regression : array.array('f',20*[0]) } )
    mchiggs.update( { regression : array.array('f',[0]) } )
    mchadtop.update( { regression: array.array('f',[0]) } )
    RegErrors.update( { regression : array.array('f',20*[0]) } )
    RegErrorsQ.update( { regression : array.array('f',20*[0]) } )
    RegErrorsAbs.update( { regression : array.array('f',20*[0]) } )
    OutputTree.Branch( "Jet_regoutput_"+regression,outputs[regression],"Jet_regoutput_"+regression+"[N_Jets]/f")
    OutputTree.Branch( "Evt_MCHiggsMass_"+regression,mchiggs[regression],"Evt_MCHiggsMass_"+regression+"/F")
    OutputTree.Branch( "Evt_MCHadTopMass_"+regression,mchadtop[regression],"Evt_MCHadTopMass_"+regression+"/F")
    OutputTree.Branch( "Jet_RegErr_"+regression,RegErrors[regression],"Jet_RegErr_"+regression+"[N_Jets]/f")                 
    OutputTree.Branch( "Jet_RegErrQ_"+regression,RegErrorsQ[regression],"Jet_RegErrQ_"+regression+"[N_Jets]/f")                 
    OutputTree.Branch( "Jet_RegErrAbs_"+regression,RegErrorsAbs[regression],"Jet_RegErrAbs_"+regression+"[N_Jets]/f")                      
    Targettype.update( { regression : target[ireg] } ) 

Regvars = {}
for variable in inputvariables:
    Regvars.update( { variable : array.array('f',20*[0] ) } )
    OutputTree.Branch(variable[len("Reg"):],Regvars[variable],variable[len("Reg"):]+"[N_Jets]/f")




nEvents = inputtree.GetEntries()


for iev in range(nEvents):

    if iev%1000 == 0:
        print iev
    
    inputtree.GetEvent(iev)

    E_Odd[0] = inputtree.Evt_Odd
    E_Weight[0] = inputtree.Weight
    P_Weight[0] = inputtree.Weight_PU
    P69_Weight[0] = inputtree.Weight_pu69p2
    C_Weight[0] = inputtree.Weight_CSV
    
    eSFGFS[0] = inputtree.Weight_ElectronSFGFS
    eSFID[0] = inputtree.Weight_ElectronSFID
    eSFIso[0] = inputtree.Weight_ElectronSFIso
    eSFTrigger[0] = inputtree.Weight_ElectronSFTrigger
    mSFID[0] = inputtree.Weight_MuonSFID
    mSFTrigger[0] = inputtree.Weight_MuonSFTrigger
    mSFIso[0] = inputtree.Weight_MuonSFIso
    mSFHIP[0] = inputtree.Weight_MuonSFHIP
    njets[0] = inputtree.N_Jets
    nbtags[0] = inputtree.N_BTagsM
    nPrimaryVertices[0] = inputtree.N_PrimaryVertices
    bbmass[0] = inputtree.Evt_MCbbMass
    nlHj = 0
    nlTj = 0
    higgsjets = [] #append [pt,eta,phi,E,corr]
    hadtopjet = [] #append [pt,eta,phi,E,corr]
    Wjets = [] #append [pt,eta,phi,E,corr]

    for i in range(inputtree.N_Jets):
        for variable in inputvariables:
            Regvars[variable][i] = Regvars_input[variable][i]
        correction = {}  
        inputvars = {}        
        inputvars["N_PrimaryVertices"] =  inputtree.N_PrimaryVertices 
        if  Regvars_input["RegJet_CSV"][i] >= 0.8:
            inputvars["Jet_Pt"] =  Regvars_input["RegJet_preregPt"][i]
            inputvars["Jet_corr"] =  Regvars_input["RegJet_corr"][i]
            inputvars["Jet_Eta"] =  Regvars_input["RegJet_Eta"][i]
            inputvars["Jet_Mt"] =  Regvars_input["RegJet_preregMt"][i]
            inputvars["Jet_leadTrackPt"] =  Regvars_input["RegJet_leadTrackPt"][i]
            inputvars["Jet_leptonPtRel"] = Regvars_input["RegJet_leptonPtRel"][i]
            inputvars["Jet_leptonPt"] = Regvars_input["RegJet_leptonPt"][i]
            inputvars["Jet_leptonDeltaR"] = Regvars_input["RegJet_leptonDeltaR"][i]
            inputvars["Jet_totHEFrac"] = Regvars_input["RegJet_totHEFrac"][i]
            inputvars["Jet_nEmEFrac"] = Regvars_input["RegJet_nEmEFrac"][i]
            inputvars["Jet_vtxMass"] = Regvars_input["RegJet_vtxMass"][i]
            inputvars["Jet_vtxPt"] = Regvars_input["RegJet_vtxPt"][i]
            inputvars["Jet_vtx3DVal"] = Regvars_input["RegJet_vtx3DVal"][i]
            inputvars["Jet_vtxNtracks"] = Regvars_input["RegJet_vtxNtracks"][i]
            inputvars["Jet_vtx3DSig"] = Regvars_input["RegJet_vtx3DSig"][i]

            for regression in weightnames:
                outputs[regression][i] = regressions[regression].evalReg(inputvars)
                correction[regression] = regressions[regression].evalReg(inputvars)
                if Targettype[regression] == "G":
                    targetval = Regvars_input["RegJet_MatchedGenJetwNuPt"][i]/Regvars_input["RegJet_preregPt"][i]
                elif Targettype[regression] == "P":
                    targetval = Regvars_input["RegJet_MatchedPartonPt"][i]/Regvars_input["RegJet_preregPt"][i]
                else:
                    targetval = -100.0
                RegErrors[regression][i] = ( correction[regression] - targetval )
                RegErrorsQ[regression][i] = ( correction[regression] - targetval ) * ( correction[regression] - targetval )
                RegErrorsAbs[regression][i] = abs( correction[regression] - targetval )
                
        else:
            for regression in weightnames:
                outputs[regression][i] = -1.0
                correction[regression] = 1.0
                RegErrors[regression][i] = -100.0
                RegErrorsQ[regression][i] = -100.0
                RegErrorsAbs[regression][i] = -100.0
        
        # set regcorr to 1 for jets that were not regressed in ntuple for computing the prereg energy
        treeregcorr = Regvars_input["RegJet_regcorr"][i]
        if treeregcorr < 0:
            treeregcorr = 1
        if isHiggsJet[i] == 1:
            higgsjets.append([Regvars_input["RegJet_preregPt"][i],Regvars_input["RegJet_Eta"][i],Regvars_input["RegJet_Phi"][i],Regvars_input["RegJet_E"][i]/treeregcorr,correction])
            if Regvars_input["RegJet_leptonPt"][i] > 0:
                nlHj = nlHj + 1 #Sum up number of jets with leptons used for higgs mass
        if isWJet[i] == 1:
            Wjets.append([Regvars_input["RegJet_preregPt"][i],Regvars_input["RegJet_Eta"][i],Regvars_input["RegJet_Phi"][i],Regvars_input["RegJet_E"][i]/treeregcorr,correction])
            if Regvars_input["RegJet_leptonPt"][i] > 0:
                nlTj = nlTj + 1 #Sum up number of jets with leptons used for hadronic top mass
        if ishadTopJet[i] == 1:
            hadtopjet.append([Regvars_input["RegJet_preregPt"][i],Regvars_input["RegJet_Eta"][i],Regvars_input["RegJet_Phi"][i],Regvars_input["RegJet_E"][i]/treeregcorr,correction])
            if Regvars_input["RegJet_leptonPt"][i] > 0:
                nlTj = nlTj + 1 #Sum up number of jets with leptons used for hadronic top mass

            
    nleptonicHiggsjets[0] = nlHj 
    nleptonicHadTopjets[0] = nlTj
    if len(higgsjets) == 2:
        for regression in weightnames:
            mchiggs[regression][0] = getHiggsMasswcorr(higgsjets[0][0],higgsjets[0][1],higgsjets[0][2],higgsjets[0][3],higgsjets[0][4][regression],
                                                       higgsjets[1][0],higgsjets[1][1],higgsjets[1][2],higgsjets[1][3],higgsjets[1][4][regression])
        mchiggsmass[0] = getHiggsMass(higgsjets[0][0],higgsjets[0][1],higgsjets[0][2],higgsjets[0][3],
                                      higgsjets[1][0],higgsjets[1][1],higgsjets[1][2],higgsjets[1][3])
    else:
        for regression in weightnames:
            mchiggs[regression][0] = -1.0
        mchiggsmass[0] = -1.0
        
    if len(Wjets) == 2 and len(hadtopjet) == 1:
        for regression in weightnames:
            mchadtop[regression][0] = gethadtopMasswcorr(Wjets[0][0],Wjets[0][1],Wjets[0][2],Wjets[0][3],Wjets[0][4][regression],
                                                         Wjets[1][0],Wjets[1][1],Wjets[1][2],Wjets[1][3],Wjets[1][4][regression],
                                                         hadtopjet[0][0],hadtopjet[0][1],hadtopjet[0][2],hadtopjet[0][3],hadtopjet[0][4][regression])
        mchadtopmass[0] = gethadtopMass(Wjets[0][0],Wjets[0][1],Wjets[0][2],Wjets[0][3],
                                        Wjets[1][0],Wjets[1][1],Wjets[1][2],Wjets[1][3],
                                        hadtopjet[0][0],hadtopjet[0][1],hadtopjet[0][2],hadtopjet[0][3])
    else:
        for regression in weightnames:
            mchadtop[regression][0] = -1.0
        mchadtopmass[0] = -1.0
            
            
    pass
    OutputTree.Fill()

OutputTree.Write();
