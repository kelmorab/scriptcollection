import ROOT
import array

class JetRegression():
    def __init__ (self, weightfile,spectatorlist, training):
        self.name = "BDTG"
        self.weights = weightfile
        self.training = training
        reader = ROOT.TMVA.Reader()
        
        self.Jet_pt =array.array('f',[0])
        self.Jet_corr = array.array('f',[0])
        self.nPV = array.array('f',[0])
        self.rho = array.array('f',[0])
        self.Jet_Eta = array.array('f',[0])
        self.Jet_Mt = array.array('f',[0])
        self.Jet_leadTrackPt = array.array('f',[0])
        self.Jet_leptonPtRel = array.array('f',[0])
        self.Jet_leptonPt =  array.array('f',[0])
        self.Jet_leptonDeltaR = array.array('f',[0])
        self.Jet_totHEFrac = array.array('f',[0])
        self.Jet_nEMEFrac = array.array('f',[0])
        #self.Jet_chMult = array.array('f',[0])
        self.Jet_vtxPt = array.array('f',[0])
        self.Jet_vtxMass = array.array('f',[0])
        self.Jet_vtx3DVal = array.array('f',[0])
        self.Jet_vtxNtracks= array.array('f',[0])
        self.Jet_vtx3DSig = array.array('f',[0])
        self.sepc = array.array('f',[0])

        

        reader.AddVariable("Jet_Pt",self.Jet_pt ); 
        reader.AddVariable("Jet_corr",self.Jet_corr );
        if training == "New":
            reader.AddVariable("N_PrimaryVertices",self.nPV);
        elif training == "Old":
            reader.AddVariable("Evt_Rho",self.rho);
        reader.AddVariable("Jet_Eta",self.Jet_Eta );
        reader.AddVariable("Jet_Mt",self.Jet_Mt ); 
        reader.AddVariable("Jet_leadTrackPt",self.Jet_leadTrackPt ); 
        reader.AddVariable("Jet_leptonPtRel",self.Jet_leptonPtRel );
        reader.AddVariable("Jet_leptonPt",self.Jet_leptonPt ); 
        reader.AddVariable("Jet_leptonDeltaR",self.Jet_leptonDeltaR );
        if training == "New":
            reader.AddVariable("Jet_totHEFrac",self.Jet_totHEFrac ); 
            reader.AddVariable("Jet_nEmEFrac",self.Jet_nEMEFrac );
        #reader.AddVariable("Jet_chargedMult",self.Jet_chMult );
        reader.AddVariable("Jet_vtxPt",self.Jet_vtxPt );
        reader.AddVariable("Jet_vtxMass",self.Jet_vtxMass );
        reader.AddVariable("Jet_vtx3DVal",self.Jet_vtx3DVal );
        reader.AddVariable("Jet_vtxNtracks",self.Jet_vtxNtracks );
        reader.AddVariable("Jet_vtx3DSig",self.Jet_vtx3DSig );

        for elem in spectatorlist:
            reader.AddSpectator(str(elem),self.sepc);

        reader.BookMVA(self.name,self.weights)
        self.reader=reader

    def evalReg(self, inputvars, printresult = False):
        self.Jet_pt[0] = inputvars["Jet_Pt"]
        self.Jet_corr[0] = inputvars["Jet_corr"]
        if self.training == "Old":
            self.rho[0] = inputvars["Evt_Rho"]
        elif self.training == "New":
            self.nPV[0] = inputvars["N_PrimaryVertices"]
        self.Jet_Eta[0] = inputvars["Jet_Eta"]
        self.Jet_Mt[0] = inputvars["Jet_Mt"]
        self.Jet_leadTrackPt[0] = inputvars["Jet_leadTrackPt"]
        self.Jet_leptonPtRel[0] = inputvars["Jet_leptonPtRel"]
        self.Jet_leptonPt[0] =  inputvars["Jet_leptonPt"]
        self.Jet_leptonDeltaR[0] = inputvars["Jet_leptonDeltaR"]
        if self.training == "New":
            self.Jet_totHEFrac[0] = min(1.0,inputvars["Jet_nHEFrac"]+inputvars["Jet_cHEFrac"])
            self.Jet_nEMEFrac[0] = min(1.0,inputvars["Jet_nEmEFrac"])
        #self.Jet_chMult[0] = inputvars["Jet_chargedMult"]
        self.Jet_vtxPt[0] = inputvars["Jet_vtxPt"]
        self.Jet_vtxMass[0] = inputvars["Jet_vtxMass"]
        self.Jet_vtx3DVal[0] = inputvars["Jet_vtx3DVal"]
        self.Jet_vtxNtracks[0] = inputvars["Jet_vtxNtracks"]
        self.Jet_vtx3DSig[0] = inputvars["Jet_vtx3DSig"]
        result  = self.reader.EvaluateRegression(self.name)[0]
        if printresult:
            print result
        return result
