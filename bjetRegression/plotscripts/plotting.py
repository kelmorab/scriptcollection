
#Neue print PDF funktion in plots classe


import ROOT
from rootutils import PDFPrinting


class plots():
    def __init__(self, key, customparam = None):
        self.language = 0 #0: Englisch, 1: German
        self.key = key
        self.Titlestring = "title"
        self.additionalLabels = []
        self.manualLegendright = False
        self.manualLegendleft = False
        if key == "Jet_Pt":
            self.setTH1(200,0,600)
            self.Titlestring = "Jet p_{T} (GeV)"
        elif key == "Jet_corr":
            self.setTH1(100,0.8,1.2)
            self.Titlestring = "Jet jecFactor('Uncorrected')"
        elif key == "Evt_Rho":
            self.setTH1(40,0,60)
            if self.language == 1:
                self.Titlestring = "#rho (GeV/Einheitsflaeche)"
            else:
                self.Titlestring = "Event #rho (GeV/unit area)"
        elif key == "Jet_Eta":
            self.setTH1(40,-2.4,2.4)
            self.Titlestring = "Jet #eta"
        elif key == "Jet_Mt":
            self.setTH1(200,0,600)
            self.Titlestring = "Jet m_{T} (GeV)"
        elif key == "Jet_leadTrackPt":
            self.setTH1(100,0,300)
            if self.language == 1:
                self.Titlestring = "p_{T} der haertesten Spur im Jet (GeV)"
            else:
                self.Titlestring = "p_{T} of leading Track in Jet (GeV)"
        elif key == "Jet_leptonPt":
            self.setTH1(60,0,120)
            if self.language == 1:
                self.Titlestring = "p_{T} des dem Jet zugeordneten Lepton (Ge^1V)"
            else:
                self.Titlestring = "p_{T} of Lepton matched to Jet (GeV)"
        elif key == "Jet_leptonPtRel":
            self.setTH1(30,0,60)
            if self.language == 1:
                self.Titlestring = "Rel. p_{T} zwischen Jet und zugeordnetem Lepton (GeV)"
            else:
                self.Titlestring = "Rel. p_{T} of Lepton matched and Jet (GeV)"
        elif key == "Jet_leptonDeltaR":
            self.setTH1(20,0,0.5)
            if self.language == 1:
                self.Titlestring = "#Delta R zwischen Jet und zugeordnetem Lepton (GeV)"
            else:
                self.Titlestring = "#Delta R between Jet and matched Lepton"
        elif key == "Jet_leptonPt_all":
            self.setTH1(140,-120,120)
            if self.language == 1:
                self.Titlestring = "p_{T} des dem Jet zugeordneten Lepton (GeV)"
            else:
                self.Titlestring = "p_{T} of Lepton matched to Jet (GeV)"
        elif key == "Jet_nHEFrac" or key == "Jet_nEmEFrac":
            self.setTH1(20,0,1)
            self.Titlestring = key
        elif key == "Jet_chargedMult":
            self.setTH1(35,0,70)
            if self.language == 1:
                self.Titlestring = "Anzahl geladener Teilchen im Jet"
            else:
                self.Titlestring = "Charged Multiplicity of Jet"
        elif key == "Jet_vtxPt":
            self.setTH1(100,0,200)
            self.Titlestring = "Vertex p_{T} (GeV)"
        elif key == "Jet_vtxMass":
            self.setTH1(14,0,7)
            if self.language == 1:
                self.Titlestring = "Vertex Masse (GeV)"
            else:
                self.Titlestring = "Vertex Mass (GeV)"
        elif key == "Jet_vtx3DVal":
            self.setTH1(30,0,15)
            if self.language == 1:
                self.Titlestring = "3D Fluglaenge des Vertex (cm)"
            else:
                self.Titlestring = "3D decay length value of Vertex (cm)"
        elif key == "Jet_vtxNtracks":
            self.setTH1(13,-0.5,12.5)
            if self.language == 1:
                self.Titlestring = "N_{Spuren} des Vertex"
            else:
                self.Titlestring = "N_{tracks} of Vertex"
        elif key == "Jet_vtx3DSig":
            self.setTH1(150,0,300)
            if self.language == 1:
                self.Titlestring = "#sigma der 3D Fluglaenge des Vertex (cm)"
            else:
                self.Titlestring = "#sigma of 3D decay length value of Vertex (cm)"
        elif key == "Jet_regPt":
            self.setTH1(200,0,600)
            if self.language == 1:
                self.Titlestring = "Jet p_{T} nach Regression (GeV)"
            else:
                self.Titlestring = "Regressed Jet p_{T} (GeV)"
        elif key == "Jet_regcorr":
            self.setTH1(96,0.4,1.6)
            self.Titlestring = "p_{T, reg} / p_{T}"
        elif key == "Jet_PtRatioPartonJet":
            self.setTH1(60,0,3)
            self.Titlestring = "p_{T, Parton} / p_{T, Jet} "
        elif key == "Jet_PartonPt" or key == "Jet_MatchedPartonPt":
            self.setTH1(200,0,600)
            self.Titlestring = "Matched Parton p_{T} (GeV)"
        else:
            if customparam is not None:
                if len(customparam) == 3:
                    self.setTH1(customparam[0],customparam[1],customparam[2])
                    self.Titlestring = key
                else:
                    print "Error with custom parameters! Use exactly 3 parameters."
                    exit()
            else:
                print "Key error!",key,"not supported."
                exit()
        
    #call from script, to change language caption
    def changeLanguage(lang):
        if lang == "german":
            self.language = 1
        elif lang == "english":
            self.language = 0
        else:
            print "Not supported language. Set back to default (english)"
            self.language = 0

    #is called in memberfunction
    def setXTitle(self, key, th1f, string = None):
        if string is None:
            th1f.GetXaxis().SetTitle(self.Titlestring)
        else:
            th1f.GetXaxis().SetTitle(string)
        th1f.GetXaxis().SetTitleSize(0.05)
        th1f.GetXaxis().SetTitleOffset(0.75)
        th1f.SetTitle("")

    #is called in memberfunction
    def setYTitle(self, th1f, string = None):
        if string is None:
            if self.language == 1:
                th1f.GetYaxis().SetTitle("Beliebige Einheiten")
            else:
                th1f.GetYaxis().SetTitle("arbitrary units")
        else:
            th1f.GetYaxis().SetTitle(string)
        th1f.GetYaxis().SetTitleSize(0.05)
        th1f.GetYaxis().SetTitleOffset(0.75)

    #is called in memberfunction
    def makeSampletext(self,samplestring):
        if samplestring is "ttHbb":
            label = ROOT.TLatex(0.6275,0.908, 'Sample: t#bar{t}H , H #rightarrow b#bar{b}')
        elif samplestring is "ttbar":
            label = ROOT.TLatex(0.77,0.908, 'Sample: t#bar{t}')
        else:
            print "samplesting no supported"
            label = ROOT.TLatex(0.88,0.908, '')
        label.SetTextFont(42)
        label.SetTextSize(0.045)
        label.SetNDC()
        return label    
        
    #call from script, to add additional labels to plot
    def addLabel(self,xpos,ypos,text,angle,size = 0.045):
        label = ROOT.TLatex(xpos,ypos,text)
        label.SetTextFont(42)
        label.SetTextSize(size)
        label.SetNDC()
        label.SetTextAngle(angle)
        self.additionalLabels.append(label)

    #is called in memberfunction
    def makeCMSstuff(self):
        simul = ROOT.TLatex(0.135, 0.908, 'CMS simulation')
        simul.SetTextFont(42)
        simul.SetTextSize(0.045)
        simul.SetNDC()

        cms = ROOT.TLatex(0.135, 0.86, 'work in progress')
        cms.SetTextFont(42)
        cms.SetTextSize(0.045)
        cms.SetNDC()
        
        return simul, cms
        
    def getKey(self):
        return self.key

    #is called, then initializing histograms
    def setTH1(self, bins, xmin, xmax):
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax

    #is called in memberfunction
    def setSumw2(self, th1f):
        th1f.Sumw2()
        
    #call in script, to change position of legend
    def setmanualegendsize(self,pos,x1,y1,x2,y2):
        if pos is "right":
            self.manualLegendright = True
            self.legenx1r = x1
            self.legeny1r = y1
            self.legenx2r = x2
            self.legeny2r = y2
        if pos is "left":
            self.manualLegendleft = True
            self.legenx1l = x1
            self.legeny1l = y1
            self.legenx2l = x2
            self.legeny2l = y2


#Class to make stackplots    
class CatPlots(plots):    

    def __init__(self, key, cuts, categorizer, legendtext, symmetricCats = True, symmetricColor = True, sample = None, customparam = None):
        plots.__init__(self, key, customparam)
        self.samplestring = sample
        if len(cuts) < 3: 
            print "More cuts needed"
            exit()
        self.categorizer = categorizer
        self.legendtext = legendtext
        self.setCatHistos(cuts, symmetricCats, categorizer)
        self.setCatColors(symmetricCats, symmetricColor)
        self.makeLegend(legendtext,symmetricCats, symmetricColor)

        

    def setCatHistos(self, cuts, symmetric, categorizer):
        self.histokeys = []
        self.fullpostfix = []
        if symmetric:
            for postfix in ["neg","pos"]:
                for i in range((len(cuts)-1)/2):
                    self.histokeys.append("histo"+str(i)+postfix+"_"+categorizer)
                    self.fullpostfix.append(str(i)+postfix+"_"+categorizer)
        
        else:
            if self.samplestring is not None:
                postfix = self.samplestring
            else:
                postfix = ""
            for i in range(len(cuts)-1):
                self.histokeys.append("histo"+postfix+str(i)+"_"+categorizer)
                self.fullpostfix.append(postfix+str(i)+"_"+categorizer)

        self.Cathistos = {}
        self.Catlookup = {}
        
        cutindex = 0
        
        for i in range(len(self.fullpostfix)):
            self.Cathistos.update({self.histokeys[i] : ROOT.TH1F(self.key+self.fullpostfix[i],self.key+self.fullpostfix[i], self.bins,self.xmin,self.xmax) })
            self.Catlookup.update({self.histokeys[i] : {"left": cuts[cutindex], "right": cuts[cutindex+1]} })
            cutindex = cutindex + 1

        for key in self.histokeys:
            self.setSumw2(self.Cathistos[key])
            #self.setXTitle(key, self.Cathistos[key])

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
                print nhistos
                colorlist = colorlist + colorlist_asym
            for i, key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })
        else:
            print nhistos
            if nhistos == 7:
                colorlist = [ROOT.kBlue+2,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed+2]
                colorlist = colorlist[::-1]
            elif nhistos == 5:
                colorlist = [ROOT.kBlue+2,ROOT.kAzure-4,ROOT.kGreen,ROOT.kOrange-4,ROOT.kRed+2]
                colorlist = colorlist[::-1]
            elif nhistos == 11:
                colorlist = [ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen-3,ROOT.kGreen,ROOT.kGreen+2,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2]
                colorlist[::-1]
            elif nhistos == 9:
                colorlist = [ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2]
                colorlist[::-1]
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
            self.Cathistos[key].SetLineColor(ROOT.kBlack) #set Color
            self.Cathistos[key].SetFillStyle(1001)
            self.Cathistos[key].SetFillColor(self.CatColors[key]) #set Color

    def makeStack(self,order = "<"):
            
        self.makeStyle()
        self.Stackplot = ROOT.THStack("Stack"+self.key,"Stack "+self.key)
        #for i in range(len(self.histokeys)/2):
        #    print self.histokeys[i], self.histokeys[(len(self.histokeys)-1)-i]
         #   self.Stackplot.Add(self.Cathistos[self.histokeys[i]])            
          #  self.Stackplot.Add(self.Cathistos[self.histokeys[(len(self.histokeys)-1)-i]])
        tmplist = []
        for key in self.Cathistos:
            tmplist.append(self.Catlookup[key]["left"])
        tmplist = sorted(tmplist)
        if order == "<":
            tmplist = tmplist #tmplist is orderd from left to right category
        elif order == ">":
            tmplist = tmplist[::-1] #turn tmplist -> ordered from right to left category
        else:
            print "ordering unknown!"
            exit()
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.Stackplot.Add(self.Cathistos[key])            
                    break
        #self.setXTitle(self.key,self.Stackplot)

    def DrawStack(self):
        self.Stackplot.Draw()
        self.leg.Draw("same")
        raw_input("press  Ret")

    def WriteStack(self, canvas, pdfout = None):
        #self.Stackplot.Write()
        self.Stackplot.Draw("histoe")
        self.setXTitle(self.key,self.Stackplot)
        self.leg.Draw("same")
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        if self.samplestring is not None:
            label = self.makeSampletext(self.samplestring)
            label.Draw("same")
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)

    def makeLegend(self, categorizer, symmetricCats, symmetricColor):
        specialpos = ["Jet_regcorr","Jet_corr"]
        if self.getKey() in specialpos:
            self.leg = ROOT.TLegend(0.13,0.55,0.43,0.83)
        else:
            self.leg = ROOT.TLegend(0.6,0.55,0.88,0.88)
        self.leg.SetBorderSize(0)
        self.leg.SetTextFont(42)
        self.leg.SetFillStyle(0)
        tmplist = []
        for key in self.Cathistos:
            tmplist.append(self.Catlookup[key]["left"])
        tmplist = sorted(tmplist)
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.leg.AddEntry(self.Cathistos[key],str(self.Catlookup[key]["left"])+" <= "+categorizer+" < "+str(self.Catlookup[key]["right"]))
                    break
                    
    def getHistos(self, getstack = True):
        hlist = []
        if getstack:
            hlist = [self.Stackplot]
        else:
            for key in self.Cathistos:
                hlist.append(self.Cathistos[key])
        return hlist

#Class to make "normal" histogramms
class normPlots(plots):
    def __init__(self, key, comparison = False, nComparisons = 2, legendtext = [], customparam = None):
        plots.__init__(self, key, customparam)
        if comparison:
            self.nHistos = nComparisons
        else:
            self.nHistos = 1
        self.legendtext = legendtext
        if comparison:
            self.histos = []
            for i in range(nComparisons):
                self.histos.append(ROOT.TH1F(self.key+"_"+str(i),self.key+"_"+str(i), self.bins,self.xmin,self.xmax))
        else:
            self.histos = [ROOT.TH1F(self.key,self.key, self.bins,self.xmin,self.xmax)]
        for histo in self.histos:
            self.setSumw2(histo)


    
    def makeStyle(self, maxyval, dofilling = False):
        colorlist = [ROOT.kViolet+9,ROOT.kViolet+1,ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen-3,ROOT.kGreen,ROOT.kGreen+2,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2,ROOT.kMagenta+2,ROOT.kPink+2,ROOT.kRed-4, ROOT.kBlue-5, ROOT.kYellow-6]
        self.setXTitle(self.key,self.histos[0])
        self.setYTitle(self.histos[0])
        self.histos[0].GetYaxis().SetRangeUser(0,maxyval*1.1)
        for iHisto, histo in enumerate(self.histos):
            histo.SetLineWidth(2)
            histo.SetLineColor(colorlist[iHisto])
            if dofilling:
                histo.SetFillStyle(1001)
                histo.SetFillColor(ROOT.kCyan-10)

    def makeLegend(self, legendtext):
        if len(legendtext) != self.nHistos:
            if self.nHistos != 1:
                print "Generating generic Legendtext"
            legendtext = []
            for i in range(self.nHistos):
                legendtext.append(self.key+" "+str(i))
        specialpos = ["Jet_regcorr","Jet_corr"]
        if self.getKey() in specialpos:
            if self.manualLegendleft:
                leg = ROOT.TLegend(self.legenx1l,self.legeny1l,self.legenx2l,self.legeny2l)
            else:    
                leg = ROOT.TLegend(0.13,0.70,0.43,0.83)
        else:
            if self.manualLegendright:
                leg = ROOT.TLegend(self.legenx1r, self.legeny1r,self.legenx2r,self.legeny2r)
            else:    
                leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.SetFillStyle(0)
        for ihisto, histo in enumerate(self.histos):
            print "adding", legendtext[ihisto]
            leg.AddEntry(histo, legendtext[ihisto])
        return leg

    def FillnormHisto(self,fillval,nHisto = 0):
        self.histos[nHisto].Fill(fillval)
        
    def WriteHisto(self, canvas, samplestring = None, dofilling = False, Drawnormalized = False, pdfout = None):
        if Drawnormalized:
            for histo in self.histos:
                ScaletoInt(histo)
        maxy = 0
        for histo in self.histos:
            tmpval = histo.GetBinContent(histo.GetMaximumBin())
            if tmpval > maxy:
                maxy = tmpval
        self.makeStyle(maxy, dofilling)
        legend = self.makeLegend(self.legendtext)
        stuff = "histoe"
        for histo in self.histos:
            histo.Draw(stuff)
            if not stuff.endswith("same"):
                stuff = stuff + " same"
        canvas.Update()
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        if self.nHistos > 1:
            print "drawing legend"
            legend.Draw("same")
        if samplestring is not None:
            samplelabel = self.makeSampletext(samplestring)
            samplelabel.Draw("same")
        if len(self.additionalLabels) > 0:
            for label in self.additionalLabels:
                label.Draw("same")
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)
        
    def getHistos(self):
        hlist = []
        for histo in self.histos:
            hlist.append(histo)
        return hlist


class TwoDplot(plots):
    def __init__(self, key1, key2, customparam1 = None,  customparam2 = None):
        plots.__init__(self, key1,customparam1)
        self.key1bins = self.bins
        self.key1min = self.xmin
        self.key1max = self.xmax
        self.key1title = self.Titlestring
        plots.__init__(self, key2,customparam2)
        self.key2bins = self.bins
        self.key2min = self.xmin
        self.key2max = self.xmax
        self.key2title = self.Titlestring
        
        self.combinedkey = key1+"__"+key2
        
        self.histo = ROOT.TH2F(self.combinedkey,self.combinedkey,self.key1bins,self.key1min,self.key1max,self.key2bins,self.key2min,self.key2max)

        self.makeStyle()

    def makeStyle(self):
        self.setXTitle(None,self.histo,self.key1title )
        self.setYTitle(self.histo, self.key2title)
        
    def FillTwoDplot(self, key1val, key2val):
        self.histo.Fill(key1val, key2val)

    def WriteTwoDPlot(self, canvas, pdfout = None):
        self.histo.Draw("colz")
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        canvas.SetTitle(self.combinedkey)
        canvas.SetName(self.combinedkey)
        canvas.Update()
        canvas.Write()
        

    def GetTH2F(self):
        return self.histo
        
    def GetCombinedKey(self):
        return self.combinedkey

    

def ScaletoInt(th1f):
    th1f.Scale(1/float(th1f.Integral()))


