
import ROOT

class plots():
    def __init__(self, key):
        self.key = key
        if key == "Jet_Pt":
            self.setTH1(200,0,600)
        elif key == "Jet_corr":
            self.setTH1(100,0.8,1.2)
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
        self.fullpostfix = []
        if symmetric:
            for postfix in ["neg","pos"]:
                for i in range((len(cuts)-1)/2):
                    self.histokeys.append("histo"+str(i)+postfix+"_"+categorizer)
                    self.fullpostfix.append(str(i)+postfix+"_"+categorizer)
        
        else:
            for i in range(len(cuts)-2):
                self.histokeys.append("histo"+str(i)+"_"+categorizer)
                self.fullpostfix.append(str(i)+"_"+categorizer)

        self.Cathistos = {}
        self.Catlookup = {}
        
        cutindex = 0
        
        for i in range(len(self.fullpostfix)):
            self.Cathistos.update({self.histokeys[i] : ROOT.TH1F(self.key+self.fullpostfix[i],self.key+self.fullpostfix[i], self.bins,self.xmin,self.xmax) })
            self.Catlookup.update({self.histokeys[i] : {"left": cuts[cutindex], "right": cuts[cutindex+1]} })
            cutindex = cutindex + 1
            
    def setCatColors(self, symmetricCats, symmetricColors):
        nhistos = len(self.fullpostfix)
        colorlist = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen]
        colorlist_asym = [ROOT.kGreen+2, ROOT.kBlue+2, ROOT.kRed+2]
        colorlist_add = [ROOT.kViolet, ROOT.kYellow,ROOT.kOrange, ROOT.kAzure, ROOT.kPink+10]
        self.CatColors = {}
        if symmetricCats:
            if symmetricColors:
                if nhistos == 12:
                    colorlist = [ROOT.kBlue+2,ROOT.kBlue+1,ROOT.kBlue,ROOT.kGreen-2,ROOT.kGreen-1,ROOT.kGreen,ROOT.kGreen,ROOT.kGreen+1,ROOT.kGreen+2,ROOT.kRed,ROOT.kRed+1,ROOT.kRed+2]
                if nhistos == 10:
                    colorlist = [ROOT.kBlue+2,ROOT.kBlue+1,ROOT.kBlue,ROOT.kGreen-2,ROOT.kGreen,ROOT.kGreen,ROOT.kGreen+2,ROOT.kRed,ROOT.kRed+1,ROOT.kRed+2]
                if nhistos == 8:
                    colorlist = [ROOT.kBlue+2,ROOT.kBlue,ROOT.kGreen-2,ROOT.kGreen,ROOT.kGreen,ROOT.kGreen+2,ROOT.kRed,ROOT.kRed+2]
            else:
                colorlist = colorlist + colorlist_asym
            for i, key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })
        else:
            colorlist = [ROOT.kViolet+7,ROOT.kViolet+6,ROOT.kViolet+1,ROOT.kViolet,ROOT.kViolet-4,ROOT.kViolet-8,ROOT.kMagenta+1,ROOT.kMagenta-10]
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
        canvas.SetTitle(self.key)
        canvas.Update()
        canvas.Write()

    def makeLegend(self, categorizer, symmetricCats, symmetricColor):
        specialpos = ["Jet_regcorr","Jet_corr"]
        if self.getKey() in specialpos:
            self.leg = ROOT.TLegend(0.1,0.6,0.4,0.9)
        else:
            self.leg = ROOT.TLegend(0.6,0.6,0.9,0.9)
        tmplist = []
        for key in self.Cathistos:
            tmplist.append(self.Catlookup[key]["left"])
        tmplist = sorted(tmplist)
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.leg.AddEntry(self.Cathistos[key],str(self.Catlookup[key]["left"])+" <= "+categorizer+" < "+str(self.Catlookup[key]["right"]))
                    break
