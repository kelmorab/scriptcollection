
# import ROOT in batch mode
import sys
import math
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv




# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.AutoLibraryLoader.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events


#In Heppy defined in PhysicsObject/Heppy/python/analyzers/objects/VertexAnalyzer.py
def testGoodVertex(vertex):
    if vertex.isFake():
        return False
    if vertex.ndof()<=4:
        return False
    if abs(vertex.z())>24:
        return False
    if vertex.position().Rho()>2:
        return False
    return True


#In Heppy defined in PhysicsObject/Heppy/python/physicsobjects/Electron.py and Muon.py

#def getDistancefromVertex(obj, gsf = False):
#    if gsf:
#        return obj.gsfTrack().dz(), obj.gsfTrack().dxy()
#    else:
#        return obj.track().dz(), obj.track().dxy()


def passesmWP(jet):

    btagval = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")
    if btagval > 1 or btagval < 0:
        return -1
    else:
        if btagval > 0.8:
            return btagval
        else:
            return -1




def getDistancefromVertex(obj, vertex, gsf = False):
    if gsf:
        return obj.gsfTrack().dz( vertex.position() ), obj.gsfTrack().dxy( vertex.position() )
    else:
        return obj.track().dz( vertex.position() ), obj.track().dxy( vertex.position() )

#In Heppy defined in PhysicsObject/Heppy/python/analyzers/objects/Leptonnalyzer
def getinclusiveLeptons(electrons, muons, vertex):
    #Def: Cuts
    #el_id = "" #implement later
    el_pt = 5
    el_eta = 2.5
    el_dxy = 0.5
    el_dz = 1.0
    
    #mu_id = "POG_ID_Loose" #implement later
    mu_pt = 3
    mu_eta = 2.4
    mu_dxy = 0.5
    mu_dz = 1.0
    
    #Cut leptons
    inclusiveelectrons = []
    inclusivemuons = []
    for electron in electrons.product():
        dz, dxy = getDistancefromVertex(electron, vertex, True)
        print dz,dxy
        if (electron.gsfTrack().isNonnull() and electron.pt() > el_pt and abs(electron.eta()) < el_eta and abs(dxy) < el_dxy and abs(dz) < el_dz):
            inclusiveelectrons.append(electron)
            print "incl. Ele dz: ",dz
            print "incl. Ele dxy:",dxy
            print "incl. Ele pt: ",electron.pt()
            print "incl. Ele eta:",electron.eta()
    for muon in muons.product():
        if muon.track().isNonnull():
            #print "Myonen:"
            dz, dxy = getDistancefromVertex(muon, vertex)
            print dz,dxy
            if ( muon.pt() > mu_pt and abs(muon.eta()) < mu_eta and abs(dxy) < mu_dxy and abs(dz) < mu_dz):
                inclusivemuons.append(muon)
                print "incl. Mu dz: ",dz
	        print "incl. Mu dxy:",dxy
                print "incl. Mu pt: ",muon.pt()
                print "incl. Mu eta:",muon.eta()
    return inclusiveelectrons + inclusivemuons


def deltaPhi(phi1, phi2):
    res = phi1 - phi2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res


def deltaR2(eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = deltaPhi(phi1, phi2)
    return deta*deta + dphi*dphi


def bestMatch(lepton, Jets):
    deltaR2Min = float('+inf')
    bm = None
    for jet in Jets:
        dR2 = deltaR2( lepton.eta(), lepton.phi(), jet.eta(), jet.phi())
        if dR2 < deltaR2Min:
            deltaR2Min = dR2
            bm = jet
    return bm, deltaR2Min

def deltaR( *args ):
    return math.sqrt( deltaR2(*args) )

def matchLeptonswithJets(leptons, Jets, deltaR2Max, ptcut,  filter = lambda x,y: True):
    pairs = {}
    if len(leptons)==0:
        return pairs
    if len(Jets)==0:
        return dict(zip(leptons, [None]*len(leptons)))
    Jets1 = []
    for jet in Jets:
        if jet.pt() > ptcut:
           Jets1.append(jet) 
    for lepton in leptons:
        bm, dr2 = bestMatch(lepton, [jet for jet in Jets1 if filter(lepton, jet)])
        if dr2 < deltaR2Max:
            pairs[lepton] = bm
#        else:
#            pairs[lepton] = None
    return pairs


muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
photons, photonLabel = Handle("std::vector<pat::Photon>"), "slimmedPhotons"
taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
fatjets, fatjetLabel = Handle("std::vector<pat::Jet>"), "slimmedJetsAK8"
mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
verticesScore = Handle("edm::ValueMap<float>")

varlist = ["jetlepptRel","jetleppt","jetlepdeltaR"]

histos = [ ROOT.TH1F(varlist[0],varlist[0],160,0,1600),
           ROOT.TH1F(varlist[1],varlist[1],20,0,2),
           ROOT.TH1F(varlist[2],varlist[2],10,0,1)
         ]








# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
#events = Events('file:/pnfs/desy.de/cms/tier2//store/user/hmildner/TT_TuneCUETP8M1_13TeV-powheg-pythia8/Boostedv3MiniAOD/151121_103807/0000/BoostedTTH_MiniAOD_1.root')
events = Events('file:/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/F0B51548-BE6F-E511-9C6C-001E0BED1522.root')


#outputname = "leptonvars.root"

nJetswleptons = 0
nJets = 0
nbJetswleptons = 0
nbJets = 0



for iev,event in enumerate(events):
    #raw_input("next Event")
    if iev >= 1000: break 
    event.getByLabel(jetLabel, jets)
    #event.getByLabel(electronLabel, electrons) 
    #event.getByLabel(muonLabel, muons)
    #event.getByLabel(vertexLabel,vertices)
    #print "run/event",event.eventAuxiliary().run(),"/",event.eventAuxiliary().event();
    #    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    """
    print vertices.product()
    goodVertices = []
    for vertex in vertices.product():
        if testGoodVertex(vertex):
            goodVertices.append(vertex)
    usevertex = goodVertices[0] if len(goodVertices)>0 else vertices.product[0]
    """
    if iev%1000 == 0:
        pass
    if iev == 10:
        exit()
    print "Event:",iev
    """
    jetLepDR = 0.4
    print "********************************"
    print electrons.product(), muons.product()
    print "********************************"
    inclusiveLeptons = getinclusiveLeptons(electrons, muons, usevertex)
    print "********************************"
    print inclusiveLeptons
    print "********************************"
    print jets.product()
    print "********************************"
    jlpairs = matchLeptonswithJets(inclusiveLeptons, jets.product(), jetLepDR**2, 10)
    print "---------->",jlpairs,"<----------"
    #raw_input("")
    if len(jlpairs) > 0:
        flag = True
        for l in jlpairs:
            pair = jlpairs[l]
            #print "lepons:",type(l), "Jet:",type(pair),"E/eT/pT/eta/phi/charge/hadronFlavour",pair.energy(),"/",pair.et(),"/",pair.pt(),"/",pair.eta(),"/",pair.phi(),"/",pair.charge(),"/",pair.hadronFlavour()
    
    else:
        flag = False

    """
    exit()
    for j in jets.product():
        if j.pt() < 30: continue
        """
        jetleptons = [l for l in jlpairs if jlpairs[l] == j]
        #print "<<<<<<<<<<<",jlpairs,">>>>>>>>>>>>"
        if len(jetleptons) > 0:
            for lepton in jetleptons:
                print ">>>>>>>>>>>>>>>",jetleptons,"<<<<<<<<<<<<<<<<<<<<<"
                #raw_input(" ")
                nJetswleptons = nJetswleptons + 1
                #print j.partonFlavour()
                if j.partonFlavour() == 5 or j.partonFlavour() == -5:
                    nbJetswleptons = nbJetswleptons + 1
        #    jetlepptRel = ptRel(ROOT.reco.Candidate.p4(jetleptons[0]),j.p4())
        #    jetleppt = jetleptons[0].pt()
        #    jetlepdeltaR = deltaR(ROOT.reco.Candidate.p4(jetleptons[0]).eta(),ROOT.reco.Candidate.p4(jetleptons[0]).phi(),j.p4().eta(),j.p4().phi())
        #else:
        #    jetlepptRel = -99
        #    jetleppt =  -99
        #    jetlepdeltaR = -99
        """
        nJets = nJets + 1
        mwpval = passesmWP(j)

        exit()
    
        if mwpval > 0:
            print j.pt(),"|",j.partonFlavour(),"|",mwpval,"|",j.userFloat('vtxPx'),"|",j.userFloat("vtx3DVal")
        
        
        #if j.partonFlavour() == 5 or j.partonFlavour() == -5:
        #    nbJets = nbJets + 1
        #raw_input("")
        #histos[0].Fill(jetlepptRel)
        #histos[1].Fill(jetleppt)
        #histos[2].Fill(jetlepdeltaR)


#print "Number of Jets with matched leptons:  ", nJetswleptons
#print "Number of Jets:                       ", nJets
#print "Fraction of Jets with matched leptons:", nJetswleptons/float(nJets)
#print "Number of b-Jets with matched leptons:  ", nbJetswleptons
#print "Number of b-Jets:                       ", nbJets
#print "Fraction of b-Jets with matched leptons:", nbJetswleptons/float(nbJets)

#outputfile = ROOT.TFile(outputname,"RECREATE")

#for histo in histos:
#    outputfile.WriteTObject(histo)
