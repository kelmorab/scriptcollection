import ROOT
import array

class JetRegression():
    def __init__ (self, weightfile):
        self.name = "BDTG"
        self.weights = weightfile
        reader = ROOT.TMVA.Reader()
        
        self.Jet_pt =array.array('f',[0])
        self.Jet_corr = array.array('f',[0])
        self.rho = array.array('f',[0])
        self.Jet_Eta = array.array('f',[0])
        self.Jet_Mt = array.array('f',[0])
        self.Jet_leadTrackPt = array.array('f',[0])
        self.Jet_leptonPtRel = array.array('f',[0])
        self.Jet_leptonPt =  array.array('f',[0])
        self.Jet_leptonDeltaR = array.array('f',[0])
        self.Jet_nHEFrac = array.array('f',[0])
        self.Jet_nEMEFrac = array.array('f',[0])
        self.Jet_chMult = array.array('f',[0])
        self.Jet_vtxPt = array.array('f',[0])
        self.Jet_vtxMass = array.array('f',[0])
        self.Jet_vtx3DVal = array.array('f',[0])
        self.Jet_vtxNtracks= array.array('f',[0])
        self.Jet_vtx3DSig = array.array('f',[0])
        if(True):
            reader.AddVariable("Jet_pt",self.Jet_pt ); 
            reader.AddVariable("Jet_corr",self.Jet_corr );
            reader.AddVariable("rho",self.rho);
            reader.AddVariable("Jet_eta",self.Jet_Eta );
            reader.AddVariable("Jet_mt",self.Jet_Mt ); 
            reader.AddVariable("Jet_leadTrackPt",self.Jet_leadTrackPt ); 
            reader.AddVariable("Jet_leptonPtRel",self.Jet_leptonPtRel );
            reader.AddVariable("Jet_leptonPt",self.Jet_leptonPt ); 
            reader.AddVariable("Jet_leptonDeltaR",self.Jet_leptonDeltaR );
            reader.AddVariable("Jet_neHEF",self.Jet_nHEFrac ); 
            reader.AddVariable("Jet_neEmEF",self.Jet_nEMEFrac );
            reader.AddVariable("Jet_chMult",self.Jet_chMult );
            reader.AddVariable("Jet_vtxPt",self.Jet_vtxPt );
            reader.AddVariable("Jet_vtxMass",self.Jet_vtxMass );
            reader.AddVariable("Jet_vtx3dL",self.Jet_vtx3DVal );
            reader.AddVariable("Jet_vtxNtrk",self.Jet_vtxNtracks );
            reader.AddVariable("Jet_vtx3deL",self.Jet_vtx3DSig );
        if(False):
            reader.AddVariable("Jet_Pt",self.Jet_pt ); 
            reader.AddVariable("Jet_corr",self.Jet_corr );
            reader.AddVariable("Evt_Rho",self.rho);
            reader.AddVariable("Jet_Eta",self.Jet_Eta );
            reader.AddVariable("Jet_Mt",self.Jet_Mt ); 
            reader.AddVariable("Jet_leadTrackPt",self.Jet_leadTrackPt ); 
            reader.AddVariable("Jet_leptonPtRel",self.Jet_leptonPtRel );
            reader.AddVariable("Jet_leptonPt",self.Jet_leptonPt ); 
            reader.AddVariable("Jet_leptonDeltaR",self.Jet_leptonDeltaR );
            reader.AddVariable("Jet_nHEFrac",self.Jet_nHEFrac ); 
            reader.AddVariable("Jet_nEmEFrac",self.Jet_nEMEFrac );
            reader.AddVariable("Jet_chargedMult",self.Jet_chMult );
            reader.AddVariable("Jet_vtxPt",self.Jet_vtxPt );
            reader.AddVariable("Jet_vtxMass",self.Jet_vtxMass );
            reader.AddVariable("Jet_vtx3DVal",self.Jet_vtx3DVal );
            reader.AddVariable("Jet_vtxNtracks",self.Jet_vtxNtracks );
            reader.AddVariable("Jet_vtx3DSig",self.Jet_vtx3DSig );
        reader.BookMVA(self.name,self.weights)
        self.reader=reader

    def evalReg(self, inputvars):
        print inputvars
        
        self.Jet_pt = inputvars["Jet_Pt"]
        self.Jet_corr = inputvars["Jet_corr"]
        self.rho = inputvars["Evt_Rho"]
        self.Jet_Eta = inputvars["Jet_Eta"]
        self.Jet_Mt = inputvars["Jet_Mt"]
        self.Jet_leadTrackPt = inputvars["Jet_leadTrackPt"]
        self.Jet_leptonPtRel = inputvars["Jet_leptonPtRel"]
        self.Jet_leptonPt =  inputvars["Jet_leptonPt"]
        self.Jet_leptonDeltaR = inputvars["Jet_leptonDeltaR"]
        self.Jet_nHEFrac = inputvars["Jet_nHEFrac"]
        self.Jet_nEMEFrac = inputvars["Jet_nEmEFrac"]
        self.Jet_chMult = inputvars["Jet_chargedMult"]
        self.Jet_vtxPt = inputvars["Jet_vtxPt"]
        self.Jet_vtxMass = inputvars["Jet_vtxMass"]
        self.Jet_vtx3DVal = inputvars["Jet_vtx3DVal"]
        self.Jet_vtxNtracks= inputvars["Jet_vtxNtracks"]
        self.Jet_vtx3DSig = inputvars["Jet_vtx3DSig"]
        
        print self.Jet_pt 
        print self.Jet_corr
        print self.rho
        print self.Jet_Eta
        print self.Jet_Mt
        print self.Jet_leadTrackPt
        print self.Jet_leptonPtRel
        print self.Jet_leptonPt 
        print self.Jet_leptonDeltaR
        print self.Jet_nHEFrac
        print self.Jet_nEMEFrac
        print self.Jet_chMult
        print self.Jet_vtxPt
        print self.Jet_vtxMass
        print self.Jet_vtx3DVal
        print self.Jet_vtxNtracks 
        print self.Jet_vtx3DSig
        print self.reader.EvaluateRegression(self.name)[0]
        return self.reader.EvaluateRegression(self.name)[0]
