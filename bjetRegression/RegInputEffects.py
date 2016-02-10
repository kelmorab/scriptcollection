import ROOT
import array


ROOT.gROOT.SetBatch(True)


class JetRegression():
    def __init__ (self, wightfile):
        self.name = "BDTG"

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
        reader.BookMVA(self.name,weightfile)
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


class plots():
    def __init__(self, key):
        self.key = key
        if key == "Jet_Pt":
            self.setTH1(200,0,600)
        elif key == "Jet_corr":
            self.setTH1(60,0.8,1.2)
        elif key == "Evt_Rho":
            self.setTH1(40,0,60)
        elif key == "Jet_Eta":
            self.setTH1(40,-2.4,2.4)
        elif key == "Jet_Mt":
            self.setTH1(200,0,600)
        elif key == "Jet_leadTrackPt":
            self.setTH1(100,0,300)
        elif key == "Jet_leptonPt":
            self.setTH1(60,0,120)
        elif key == "Jet_leptonPtRel":
            self.setTH1(30,0,60)
        elif key == "Jet_leptonDeltaR":
            self.setTH1(20,0,0.5)
        elif key == "Jet_nHEFrac" or key == "Jet_nEmEFrac":
            self.setTH1(20,0,1)
        elif key == "Jet_chargedMult":
            self.setTH1(35,0,70)
        elif key == "Jet_vtxPt":
            self.setTH1(100,0,200)
        elif key == "Jet_vtxMass":
            self.setTH1(14,0,7)
        elif key == "Jet_vtx3DVal":
            self.setTH1(30,0,15)
        elif key == "Jet_vtxNtracks":
            self.setTH1(13,-0.5,12.5)
        elif key == "Jet_vtx3DSig":
            self.setTH1(150,0,300)
        elif key == "Jet_regPt":
            self.setTH1(200,0,600)
        elif key == "Jet_regcorr":
            self.setTH1(60,0.4,1.6)
        else:
            print "Key error!",key,"not supported."
            exit()
            
    def getKey(self):
        return self.key

    def setTH1(self, bins, xmin, xmax):
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax
    
    


class CatPlots(plots):    

    def __init__(self, key, cuts, categorizer, symmetricCats = True, symmetricColor = True):
        plots.__init__(self, key)
        if len(cuts) < 3: 
            print "More cuts needed"
            exit()
        self.setCatHistos(cuts, symmetricCats, categorizer)
        self.setCatColors(symmetricCats, symmetricColor)
        self.makeLegend(categorizer,symmetricCats, symmetricColor)
        
    def setCatHistos(self, cuts, symmetric, categorizer):
        self.histokeys = []
        fullpostfix = []
        if symmetric:
            for postfix in ["neg","pos"]:
                for i in range((len(cuts)-1)/2):
                    self.histokeys.append("histo"+str(i)+postfix+"_"+categorizer)
                    fullpostfix.append(str(i)+postfix+"_"+categorizer)
        
        else:
            for i in range(len(cuts)-2):
                self.histokeys.append("histo"+str(i)+"_"+categorizer)
                fullpostfix.append(str(i)+"_"+categorizer)

        self.Cathistos = {}
        self.Catlookup = {}
        
        cutindex = 0
        
        for i in range(len(fullpostfix)):
            self.Cathistos.update({self.histokeys[i] : ROOT.TH1F(self.key+fullpostfix[i],self.key+fullpostfix[i], self.bins,self.xmin,self.xmax) })
            self.Catlookup.update({self.histokeys[i] : {"left": cuts[cutindex], "right": cuts[cutindex+1]} })
            cutindex = cutindex + 1
            
    def setCatColors(self, symmetricCats, symmetricColors):
        #Works only for 6 symmetric Categories
        colorlist = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen]
        colorlist_asym = [ROOT.kGreen+2, ROOT.kBlue+2, ROOT.kRed+2]
        colorlist_add = [ROOT.kViolet, ROOT.kYellow,ROOT.kOrange]
        self.CatColors = {}
        if symmetricCats:
            if symmetricColors:
                colorlist = colorlist + colorlist[::-1]
            else:
                colorlist = colorlist + colorlist_asym
            for i, key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })
        else:
            colorlist = colorlist + colorlist_add
            for i,key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })

    def FillCatHistos(self, fillval, catval):
        for key in self.histokeys:
            if catval >= self.Catlookup[key]["left"] and catval < self.Catlookup[key]["right"]:
                self.Cathistos[key].Fill(fillval)
                break
    
    def makeStyle(self):
        for key in self.histokeys:
            self.Cathistos[key].SetLineColor(self.CatColors[key]) #set Color
            self.Cathistos[key].SetFillStyle(1001)
            self.Cathistos[key].SetFillColor(self.CatColors[key]) #set Color

    def makeStack(self):
        self.makeStyle()
        self.Stackplot = ROOT.THStack("Stack"+self.key,"Stack "+self.key)
        
        for i in range(len(self.histokeys)/2):
            self.Stackplot.Add(self.Cathistos[self.histokeys[i]])            
            self.Stackplot.Add(self.Cathistos[self.histokeys[(len(self.histokeys)-1)-i]])
            
    def DrawStack(self):
        self.Stackplot.Draw()
        self.leg.Draw("same")
        raw_input("press  Ret")

    def WriteStack(self, canvas):
        #self.Stackplot.Write()
        self.Stackplot.Draw()
        self.leg.Draw("same")
        canvas.Update()
        canvas.Write()

    def makeLegend(self, categorizer, symmetricCats, symmetricColor):
        specialpos = ["Jet_regcorr","Jet_corr"]
        if self.getKey() in specialpos:
            self.leg = ROOT.TLegend(0.1,0.7,0.3,0.9)
        else:
            self.leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
        #tmplist = []
        #for key in self.Cathistos:
        #    tmplist.append(self.Catlookup[key]["left"])
        for key in self.Cathistos:
            self.leg.AddEntry(self.Cathistos[key],str(self.Catlookup[key]["left"])+" <= "+categorizer+" < "+str(self.Catlookup[key]["right"]))


inputfile = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbar_nominal.root")
weightfile = "/afs/desy.de/user/h/hmildner/public/regression_weights/weights_ttbar_quark/TMVARegression_BDTG.weights.xml"

outputfileprefix = "testout1"

tree = inputfile.Get("MVATree")

readvars = {"N_Jets" : 0,
            "Evt_Rho": 0,
            "Jet_Pt" : [],
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

inputvar = {"Evt_Rho": 0}

inputvars = {"Jet_Pt" : [],
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

jetreg = JetRegression(weightfile) 

inputplots_regcorr = {}
inputplot_regcorr = {}
outputplots_regcorr = {}
outputplots_pt = {}
outputplots_leppt = {}


#Categorize by regcorr factor
for key in inputvar:    
    inputplot_regcorr.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],"regcorr",True,False)})
for key in inputvars:    
    inputplots_regcorr.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],"regcorr",True,False)})
for key in outputvars:    
    outputplots_regcorr.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],"regcorr",True,False)})
#Categorize by Jet_pt
#for key in inputvar:    
#    inputplot_pt.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],False,False)})
#for key in inputvars:    
#    inputplots_pt.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],False,False)})
for key in outputvars:    
    outputplots_pt.update({key : CatPlots(key, [0,50,100,150,300,600],"jetpt",False,False)})
#Categorize by Jet_lepton_pt
#for key in inputvar:    
#    inputplot_leppt.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],False,False)})
#for key in inputvars:    
#    inputplots_leppt.update({key : CatPlots(key, [0,0.8,0.9,1,1.1,1.2,2],False,False)})
for key in outputvars:    
    outputplots_leppt.update({key : CatPlots(key, [0,30,50,80,100,120],"jetleppt",False,False)})





for iev in range(tree.GetEntries()):
    if iev%10000 == 0:
        print iev
    if iev == 100000:
        break
    tree.GetEvent(iev)
    

    
    readvars["N_Jets"] = tree.N_Jets 
    readvars["Evt_Rho"] = tree.Evt_Rho
    
    readvars["Jet_Pt"] = tree.Jet_Pt                 
    readvars["Jet_corr"] = tree.Jet_corr   
    readvars["Jet_Eta"] = tree.Jet_Eta       
    readvars["Jet_Mt"] = tree.Jet_Mt           
    readvars["Jet_leadTrackPt"] = tree.Jet_leadTrackPt
    readvars["Jet_Flav"] = tree.Jet_Flav      
    
    readvars["Jet_leptonPt"] = tree.Jet_leptonPt
    readvars["Jet_leptonPtRel"] = tree.Jet_leptonPtRel
    readvars["Jet_leptonDeltaR"] = tree.Jet_leptonDeltaR
        
    readvars["Jet_nHEFrac"] = tree.Jet_nHEFrac     
    readvars["Jet_nEmEFrac"] = tree.Jet_nEmEFrac
    readvars["Jet_chargedMult"] = tree.Jet_chargedMult
        
    readvars["Jet_vtxPt"] = tree.Jet_vtxPt    
    readvars["Jet_vtxMass"] = tree.Jet_vtxMass 
    readvars["Jet_vtx3DVal"] = tree.Jet_vtx3DVal    
    readvars["Jet_vtxNtracks"] = tree.Jet_vtxNtracks 
    readvars["Jet_vtx3DSig"] = tree.Jet_vtx3DSig
        
    readvars["Jet_PartonFlav"] = tree.Jet_PartonFlav
    readvars["Jet_PartonPt"] = tree.Jet_PartonPt


    inputvar["Evt_Rho"] = readvars["Evt_Rho"]
    isbjet = False
    for ijet in range(readvars["N_Jets"]):
        if abs(readvars["Jet_Flav"][ijet]) == 5 and abs(readvars["Jet_PartonFlav"][ijet]) == 5:
            isbjet = True
            inputvars["Jet_Pt"] = readvars["Jet_Pt"][ijet]
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
            tmpdict = inputvars
            tmpdict.update(inputvar)

            #outputvars["Jet_regPt"] = jetreg.evalReg(tmpdict)
            outputvars["Jet_regPt"] = tree.Jet_regPt[ijet]
            outputvars["Jet_regcorr"] = outputvars["Jet_regPt"]/inputvars["Jet_Pt"]
            for key in inputplots_regcorr:
                inputplots_regcorr[key].FillCatHistos(inputvars[key],outputvars["Jet_regcorr"])
            for key in outputplots_regcorr:
                outputplots_regcorr[key].FillCatHistos(outputvars[key],outputvars["Jet_regcorr"])
            for key in outputplots_pt:
                outputplots_pt[key].FillCatHistos(outputvars[key],inputvars["Jet_Pt"])
            for key in outputplots_leppt:
                outputplots_leppt[key].FillCatHistos(outputvars[key], inputvars["Jet_leptonPt"])
    if isbjet:
        for key in inputplot_regcorr:
            inputplot_regcorr[key].FillCatHistos(inputvar[key],outputvars["Jet_regcorr"])


outputfile = ROOT.TFile(outputfileprefix+"_regcorr"+".root","RECREATE")    
ROOT.gROOT.SetBatch(True)
outputfile.cd()


c1 = ROOT.TCanvas()
c1.cd()

for key in inputplot_regcorr:
    inputplot_regcorr[key].makeStack()
    inputplot_regcorr[key].WriteStack(c1)
for key in inputplots_regcorr:
    inputplots_regcorr[key].makeStack()
    inputplots_regcorr[key].WriteStack(c1)
for key in outputplots_regcorr:
    outputplots_regcorr[key].makeStack()
    outputplots_regcorr[key].WriteStack(c1)

del outputfile

outputfile = ROOT.TFile(outputfileprefix+"_pt"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_pt:
    outputplots_pt[key].makeStack()
    outputplots_pt[key].WriteStack(c1)

del outputfile

outputfile = ROOT.TFile(outputfileprefix+"_leppt"+".root","RECREATE")    
outputfile.cd()

for key in outputplots_leppt:
    outputplots_leppt[key].makeStack()
    outputplots_leppt[key].WriteStack(c1)
    
del outputfile

    













