import ROOT

ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Handle, Events, Runs



def getJetCSV(jet, name):
    defaultFailure = -.1
    bTagVal = jet.bDiscriminator(name)
    if(bTagVal > 1.): 
        return 1.
    if(bTagVal < 0.):
        return defaultFailure;

    return bTagVal;

def JetpassesCSV(jet, workingpoint):
    CSVLv2wp = 0.605;
    CSVMv2wp = 0.89;
    CSVTv2wp = 0.97;

    triggername = "pfCombinedInclusiveSecondaryVertexV2BJetTags"

    csvValue = getJetCSV(jet, triggername)
    if workingpoint == "L":
        if csvValue > CSVLv2wp:
            return True
    elif workingpoint == "M":
        if csvValue > CSVMv2wp:
            return True
    elif workingpoint == "T":
        if csvValue > CSVTv2wp:
            return True            
    else:
        print "No workingpint defined"
        exit()
    return False
            

tophad_mean=165
tophad_sigma=17
whad_mean=80
whad_sigma=10

jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"

events = Events('file:/pnfs/desy.de/cms/tier2//store/user/hmildner/TT_TuneCUETP8M1_13TeV-powheg-pythia8/Boostedv3MiniAOD/151121_103807/0000/BoostedTTH_MiniAOD_1.root')

htophadmass = ROOT.TH1F("htophadmass","Reco mass of hadronic Top",50,100,200)



for iev,event in enumerate(events):
    event.getByLabel(jetLabel, jets)
    event.getByLabel(vertexLabel, vertices)

    chi2min = 99999
    tophadval = 99999
    
    if iev%1000 == 0:
        print iev

    for j1 in jets.product():
        for j2 in jets.product():
            for j3 in jets.product():
                if j1 != j2 and j1 != j3 and j2 != j3:
                    if (JetpassesCSV(j3, "M") and not JetpassesCSV(j1, "M") and not JetpassesCSV(j2, "M")):
                        WHadp4 = j1.p4() + j2.p4()
                        HadTopp4 = j3.p4() + WHadp4
                        chi2val = ((HadTopp4.M()  - tophad_mean)*(HadTopp4.M()  - tophad_mean))/(tophad_sigma*tophad_sigma) + ((WHadp4.M()  - whad_mean)*(WHadp4.M()  - whad_mean))/(whad_sigma*whad_sigma)
                        if chi2val < chi2min:
                            chi2min = chi2val
                            tophadval = HadTopp4.M()

    if tophadval != 99999:
        htophadmass.Fill(tophadval)

htophadmass.Draw()
raw_input("Press Ret")
