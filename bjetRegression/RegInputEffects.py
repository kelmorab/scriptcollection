import ROOT
import array

class JetRegression():
    def __init__ (self, wightfile):
        self.name = "BDTG"

        reader = ROOT.TMVA.Reader()
        
        self.Jet_pt =array.array('f',[0])
        self.Jet_corr = array.array('f',[0])
        self.rho = array.array('f',[0])
        self.Jet_eta = array.array('f',[0])
        self.Jet_mt = array.array('f',[0])
        self.Jet_leadTrackPt = array.array('f',[0])
        self.Jet_leptonPtRel = array.array('f',[0])
        self.Jet_leptonPt =  array.array('f',[0])
        self.Jet_leptonDeltaR = array.array('f',[0])
        self.Jet_neHEF = array.array('f',[0])
        self.Jet_neEmEF = array.array('f',[0])
        self.Jet_chMult = array.array('f',[0])
        self.Jet_vtxPt = array.array('f',[0])
        self.Jet_vtxMass = array.array('f',[0])
        self.Jet_vtx3DVal = array.array('f',[0])
        self.Jet_vtxNtracks= array.array('f',[0])
        self.Jet_vtx3DSig = array.array('f',[0])
        reader.AddVariable("Jet_Pt",self.Jet_pt ); 
        reader.AddVariable("Jet_corr",self.Jet_corr );
        reader.AddVariable("Evt_Rho",self.rho);
        reader.AddVariable("Jet_Eta",self.Jet_Eta );
        reader.AddVariable("Jet_Mt",self.Jet_M ); 
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
        reader.BookMVA(self.name,weightfile)
        self.reader=reader

    def evalReg(self, inputvars):
        if len(inputvars) == 17: continue
        self.Jet_pt =inputvars["Jet_Pt"]
        self.Jet_corr = inputvars["Jet_corr"]
        self.rho = inputvars["Evt_Rho"]
        self.Jet_eta = inputvars["Jet_Eta"]
        self.Jet_mt = inputvars["Jet_Mt"]
        self.Jet_leadTrackPt = inputvars["Jet_leadTrackPt"]
        self.Jet_leptonPtRel = inputvars["Jet_leptonPtRel"]
        self.Jet_leptonPt =  inputvars["Jet_leptonPt"]
        self.Jet_leptonDeltaR = inputvars["Jet_leptonDeltaR"]
        self.Jet_neHEF = inputvars["Jet_nHEFrac"]
        self.Jet_neEmEF = inputvars["Jet_nEmEFrac"]
        self.Jet_chMult = inputvars["Jet_chargedMult"]
        self.Jet_vtxPt = inputvars["Jet_vtxPt"]
        self.Jet_vtxMass = inputvars["Jet_vtxMass"]
        self.Jet_vtx3DVal = inputvars["Jet_vtx3DVal"]
        self.Jet_vtxNtracks= inputvars["Jet_vtxNtracks"]
        self.Jet_vtx3DSig = inputvars["Jet_vtx3DSig"]
        
        return self.reader.EvaluateRegression(self.name)[0]


class plots():
    def __init__(self, key):
        self.key = key
        if key == "Jet_pt":
            setTH1(200,0,600)
        elif key == "Jet_corr":
            setTH1(40,0.4,1.6)
        elif key == "Evt_rho":
            setTH1(30,0,60)
        elif key == "Jet_Eta":
            setTH1(40,-2.4,2.4)
        elif key == "Jet_Mt":
            setTH1(50,0,100)
        elif key == "Jet_leadTrackPt":
            setTH1(100,0,300)
        elif key == "Jet_leptonPt":
            setTH1(60,0,120)
        elif key == "Jet_leptonPtRel":
            setTH1(30,0,60)
        elif key == "Jet_leptonDeltaR":
            setTH1(20,0,0.5)
        elif key == "Jet_nHEFrac" or key == "Jet_nEmEFrac":
            setTH1(20,0,1)
        elif key == "Jet_chargedMult":
            setTH1(35,0,70)
        elif key == "Jet_vtxPt":
            setTH1(100,0,200)
        elif key == "Jet_vtxMass":
            setTH1(14,0,7)
        elif key == "Jet_vtx3DVal":
            setTH1(30,0,15)
        elif key == "Jet_vtxNtracks":
            setTH1(13,-0.5,12.5)
        elif key == "Jet_vtx3DSig":
            setTH1(150,0,300)
        else:
            print "Key error!"
            exit()

    def getKey(self):
        return self.key

    def setTH1(self, bins, xmin, xmax):
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax

class CatPlots(plots):    

    def __init__(self, key, cuts, categorizer, symmetric = True):
        plots.__init__(self, key)
        histos = setCatHistis(
    
    def setCatHistos(self, cut0, cut1, cut2, cut3, categorizer):
        self.Cathistos = { "histo0neg" : ROOT.TH1F(self.key+"0neg", self.key+"0neg", self.bins, self.xmin, self.xmax),
                           "histo1neg" : ROOT.TH1F(self.key+"1neg", self.key+"1neg", self.bins, self.xmin, self.xmax),
                           "histo2neg" : ROOT.TH1F(self.key+"2neg", self.key+"2neg", self.bins, self.xmin, self.xmax),
                           "histo2pos" : ROOT.TH1F(self.key+"0pos", self.key+"0pos", self.bins, self.xmin, self.xmax),
                           "histo1pos" : ROOT.TH1F(self.key+"1pos", self.key+"1pos", self.bins, self.xmin, self.xmax),
                           "histo0pos" : ROOT.TH1F(self.key+"2pos", self.key+"2pos", self.bins, self.xmin, self.xmax)}
        
    def FillCatHistos(self, 

        
inputfile = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_nominal.root")
weightfile = ""


tree = inputfile1.Get("MVATree")

readvars = {"NJets" : 0,
            "Evt_rho": 0,
            "Jet_pt" : [],
            "Jet_corr" : [],
            "Jet_Eta" : [],
            "Jet_Mt" : [],
            "Jet_leadTrackPt" : [],
            "Jet_Flav" : [],
            "Jet_leptonPt" : [],
            "Jet_leptonPtRel" : [],
            "Jet_leptonDeltaR" : [],
            "Jet_nHEFrac" : [],
            "Jet_nEmEFrac" : [],
            "Jet_chargedMult" : [],
            "Jet_vtxPt" : [],
            "Jet_vtxMass" : [],
            "Jet_vtx3DVal" : [],
            "Jet_vtxNtracks" : [],
            "Jet_vtx3DSig" : [],
            "Jet_PartonFlav" : [],
            "Jet_PartonPt" : []}

inputvars = {"Evt_rho": 0,
            "Jet_pt" : [],
            "Jet_corr" : [],
            "Jet_Eta" : [],
            "Jet_Mt" : [],
            "Jet_leadTrackPt" : [],
            "Jet_leptonPt" : [],
            "Jet_leptonPtRel" : [],
            "Jet_leptonDeltaR" : [],
            "Jet_nHEFrac" : [],
            "Jet_nEmEFrac" : [],
            "Jet_chargedMult" : [],
            "Jet_vtxPt" : [],
            "Jet_vtxMass" : [],
            "Jet_vtx3DVal" : [],
            "Jet_vtxNtracks" : [],
            "Jet_vtx3DSig" : []}

outputvars = {"Jet_regPt": [],
              "Jet_regcorr" : []}


tree.SetBranchAddress("NJets",readvars["NJets"]);
tree.SetBranchAddress("Evt_Rho",readvars["Evt_Rho"]);

tree.SetBranchAddress("Jet_Pt",readvars["Jet_pt"]);                     
tree.SetBranchAddress("Jet_corr",readvars["Jet_corr"]);                 
tree.SetBranchAddress("Jet_Eta", readvars["Jet_Eta"]);                   
tree.SetBranchAddress("Jet_M", readvars["Jet_M"]);                       
tree.SetBranchAddress("Jet_leadTrackPt", readvars["Jet_leadTrackPt"]);   
tree.SetBranchAddress("Jet_Flav", readvars["Jet_Flav"]);                 

tree.SetBranchAddress("Jet_leptonPt", readvars["Jet_leptonPt");         
tree.SetBranchAddress("Jet_leptonPtRel", readvars["Jet_leptonPtRel"]);   
tree.SetBranchAddress("Jet_leptonDeltaR", readvars["Jet_leptonDeltaR"]); 

tree.SetBranchAddress("Jet_nHEFrac", readvars["Jet_nHEFrac"]);           
tree.SetBranchAddress("Jet_nEmEFrac", readvars["Jet_nEMEFrac"]);         
tree.SetBranchAddress("Jet_chargedMult", readvars["Jet_chMult"]);        

tree.SetBranchAddress("Jet_vtxPt", readvars["Jet_vtxPt"]);               
tree.SetBranchAddress("Jet_vtxMass", readvars["Jet_vtxMass"]);           
tree.SetBranchAddress("Jet_vtx3DVal", readvars["Jet_vtx3DVal"]);         
tree.SetBranchAddress("Jet_vtxNtracks", readvars["Jet_vtxNtracks"]);     
tree.SetBranchAddress("Jet_vtx3DSig", readvars["Jet_vtx3DSig"]);         

tree.SetBranchAddress("Jet_PartonFlav", readvars["Jet_PartonFlav"]);     
tree.SetBranchAddress("Jet_PartonPt", readvars["Jet_PartonPt"]);         

jetreg = JetRegression(weightfile) 









for iev in range(tree.GetEntries()):
    tree.GetEvent(iev)
    inputvars["Evt_rho"] = readvars["Evt_rho"]   
    for ijet in readvars["NJets"]:
            inputvars["Jet_pt"] = readvars["Jet_pt"][ijet]
            inputvars["Jet_corr"] = readvars["Jet_corr"][ijet]
            inputvars["Jet_Eta"] = readvars["Jet_Eta"][ijet]
            inputvars["Jet_Mt"] = readvars["Jet_Mt"][ijet]
            inputvars["Jet_leadTrackPt"] = readvars["Jet_leadTrackPt"][ijet]
            inputvars["Jet_leptonPt"] = readvars["Jet_leptonPt"][ijet]
            inputvars["Jet_leptonPtRel"] = readvars["Jet_leptonPtRel"][ijet]
            inputvars["Jet_leptonDeltaR"] = readvars["Jet_leptonDeltaR"][ijet]
            inputvars["Jet_nHEFrac"] = readvars["Jet_nHEFrac"][ijet]
            inputvars["Jet_nEmEFrac"] = readvars["Jet_nEmEFrac"][ijet]
            inputvars["Jet_chargedMult"] = readvars["Jet_chargedMult"][ijet]
            inputvars["Jet_vtxPt"] = readvars["Jet_vtxPt"][ijet]
            inputvars["Jet_vtxMass"] = readvars["Jet_vtxMass"][ijet]
            inputvars["Jet_vtx3DVal"] = readvars["Jet_vtx3DVal"][ijet]
            inputvars["Jet_vtxNtracks"] = readvars["Jet_vtxNtracks"][ijet]
            inputvars["Jet_vtx3DSig"] = readvars["Jet_vtx3DSig"][ijet]
                    
            outputvars["Jet_regPt"] = jetreg.evaluate(inputvars)
            outputvars["Jet_regcorr"] = outputvars["Jet_regPt"]/inputvars["Jet_Pt"]















