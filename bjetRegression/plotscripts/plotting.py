
#Neue print PDF funktion in plots classe
import copy
from array import array

import ROOT
from rootutils import PDFPrinting


myrnd = ROOT.TRandom3()

class plots():
    def __init__(self, key, customparam = None):
        self.language = 0 #0: Englisch, 1: German
        self.key = key
        self.Titlestring = "title"
        self.additionalLabels = []
        self.manualLegendright = False
        self.manualLegendleft = False
        self.manualcolors = False
        self.uselogscale = False
        self.noCMS = False
        if key == "Jet_Pt":
            if customparam is None:
                self.setTH1(200,0,600)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "Jet p_{T} (GeV)"
        elif key == "Jet_corr":
            if customparam is None:
                self.setTH1(100,0.8,1.2)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "Jet jecFactor('Uncorrected')"
        elif key == "Evt_Rho":
            if customparam is None:
                self.setTH1(40,0,60)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "#rho (GeV/Einheitsflaeche)"
            else:
                self.Titlestring = "Event #rho (GeV/unit area)"
        elif key == "N_PrimaryVertices":
            if customparam is None:
                self.setTH1(26,-.5,25.5)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "Anzahl Primaervertices"
            else:
                self.Titlestring = "Number of Primary vertices"
        elif key == "Jet_Eta":
            if customparam is None:
                self.setTH1(40,-2.4,2.4)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "Jet #eta"
        elif key == "Jet_Mt":
            if customparam is None:
                self.setTH1(200,0,600)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "Jet m_{T} (GeV)"
        elif key == "Jet_leadTrackPt":
            if customparam is None:
                self.setTH1(100,0,300)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "p_{T} der haertesten Spur im Jet (GeV)"
            else:
                self.Titlestring = "p_{T} of leading Track in Jet (GeV)"
        elif key == "Jet_leptonPt":
            if customparam is None:
                self.setTH1(60,0,120)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "p_{T} des dem Jet zugeordneten Lepton (Ge^1V)"
            else:
                self.Titlestring = "p_{T} of Lepton matched to Jet (GeV)"
        elif key == "Jet_leptonPtRel":
            if customparam is None:
                self.setTH1(30,0,60)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "Rel. p_{T} zwischen Jet und zugeordnetem Lepton (GeV)"
            else:
                self.Titlestring = "Rel. p_{T} of Lepton matched and Jet (GeV)"
        elif key == "Jet_leptonDeltaR":
            if customparam is None:
                self.setTH1(20,0,0.5)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "#Delta R zwischen Jet und zugeordnetem Lepton (GeV)"
            else:
                self.Titlestring = "#Delta R between Jet and matched Lepton"
        elif key == "Jet_leptonPt_all":
            if customparam is None:
                self.setTH1(140,-120,120)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "p_{T} des dem Jet zugeordneten Lepton (GeV)"
            else:
                self.Titlestring = "p_{T} of Lepton matched to Jet (GeV)"
        elif key == "Jet_nHEFrac" or key == "Jet_nEmEFrac":
            if customparam is None:
                self.setTH1(20,0,1)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = key
        elif key == "Jet_chargedMult":
            if customparam is None:
                self.setTH1(35,0,70)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "Anzahl geladener Teilchen im Jet"
            else:
                self.Titlestring = "Charged Multiplicity of Jet"
        elif key == "Jet_vtxPt":
            if customparam is None:
                self.setTH1(100,0,200)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "Vertex p_{T} (GeV)"
        elif key == "Jet_vtxMass":
            if customparam is None:
                self.setTH1(14,0,7)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "Vertex Masse (GeV)"
            else:
                self.Titlestring = "Vertex Mass (GeV)"
        elif key == "Jet_vtx3DVal":
            if customparam is None:
                self.setTH1(30,0,15)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "3D Fluglaenge des Vertex (cm)"
            else:
                self.Titlestring = "3D decay length value of Vertex (cm)"
        elif key == "Jet_vtxNtracks":
            if customparam is None:
                self.setTH1(13,-0.5,12.5)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "N_{Spuren} des Vertex"
            else:
                self.Titlestring = "N_{tracks} of Vertex"
        elif key == "Jet_vtx3DSig":
            if customparam is None:
                self.setTH1(150,0,300)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "#sigma der 3D Fluglaenge des Vertex (cm)"
            else:
                self.Titlestring = "#sigma of 3D decay length value of Vertex (cm)"
        elif key == "Jet_regPt":
            if customparam is None:
                self.setTH1(200,0,600)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            if self.language == 1:
                self.Titlestring = "Jet p_{T} nach Regression (GeV)"
            else:
                self.Titlestring = "Regressed Jet p_{T} (GeV)"
        elif key == "Jet_regcorr":
            if customparam is None:
                self.setTH1(96,0.4,1.6)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "p_{T, reg} / p_{T}"
        elif key == "Jet_PtRatioPartonJet":
            if customparam is None:
                self.setTH1(60,0,3)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "p_{T, Parton} / p_{T, Jet} "
        elif key == "Jet_PartonPt" or key == "Jet_MatchedPartonPt":
            if customparam is None:
                self.setTH1(200,0,600)
            else:
                self.setTH1(customparam[0],customparam[1],customparam[2])
            self.Titlestring = "Matched Parton p_{T} (GeV)"
        elif key == "Jet_PartonPt_D_Jet_Pt":
            self.setTH1(60,0,3)
            self.Titlestring = "Matched Parton P_{T} / Jet P_{T}"
        elif key == "Jet_Pt_D_Jet_PartonPt":
            self.setTH1(60,0,2.5)
            self.Titlestring = "Jet P_{T} / Matched Parton P_{T}"
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
    def changeLanguage(self,lang):
        if lang == "german":
            self.language = 1
        elif lang == "english":
            self.language = 0
        else:
            print "Not supported language. Set back to default (english)"
            self.language = 0

    def changeColorlist(self, colorlist = []):
        if len(colorlist) != 0:
            self.manualcolors = True
            self.manualcolorlist = colorlist

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
        th1f.GetYaxis().SetTitleOffset(0.8)

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
        simul = ROOT.TLatex(0.135, 0.908, '#scale[1.2]{#bf{CMS}} #it{simulation}')
        simul.SetTextFont(42)
        simul.SetTextSize(0.045)
        simul.SetNDC()

        cms = ROOT.TLatex(0.135, 0.86, 'work in progress')
        cms.SetTextFont(42)
        cms.SetTextSize(0.045)
        cms.SetNDC()

        return simul, cms

    #call from script
    def donotmakeCMSstuff(self):
        self.noCMS = True

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

    def getLine(self, x1, y1, x2 ,y2, horizontal = False, vertical = False, canvas = None):
        if canvas is not None and vertical:
            line = ROOT.TLine(x1,y1,x2,canvas.GetUymax())
        elif canvas is not None and horizontal:
            line = ROOT.TLine(x1,y1,canvas.GetUxmax(), y2)
        else:
            line = ROOT.TLine(x1,y1,x2, y2)
        line.SetLineWidth(1)
        line.SetLineStyle(2)
        line.SetLineColor(ROOT.kBlack)
        return line



#Class to make stackplots
class CatPlots(plots):

    def __init__(self, key, cuts, categorizer, legendtext, symmetricCats = True, symmetricColor = True, sample = None, customparam = None, hideyLabels = False):
        plots.__init__(self, key, customparam)
        self.samplestring = sample
        if len(cuts) < 3:
            print "More cuts needed"
            exit()
        self.categorizer = categorizer
        self.legendtext = legendtext
        self.extrath1f = []
        self.drawextrath1f = False
        self.symmetricCats = symmetricCats
        self.symmetricColor = symmetricColor
        self.setCatHistos(cuts, symmetricCats, categorizer)
        self.setCatColors(symmetricCats, symmetricColor)
        self.hideyLabels = hideyLabels
        #self.makeLegend(self.legendtext,symmetricCats, symmetricColor)



    def setCatHistos(self, cuts, symmetric, categorizer):
        self.histokeys = []
        self.fullpostfix = []
        if symmetric:
            for postfix in ["neg","pos"]:
                for i in range((len(cuts)-1)/2):
                    rand = str(ROOT.gRandom.Integer(10000))
                    self.histokeys.append("histo"+rand+str(i)+postfix+"_"+categorizer)
                    self.fullpostfix.append(rand+str(i)+postfix+"_"+categorizer)

        else:
            if self.samplestring is not None:
                postfix = self.samplestring
            else:
                postfix = ""
            for i in range(len(cuts)-1):
                rand = str(ROOT.gRandom.Integer(10000))
                self.histokeys.append("histo"+rand+postfix+str(i)+"_"+categorizer)
                self.fullpostfix.append(rand+postfix+str(i)+"_"+categorizer)

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
                #print nhistos
                colorlist = colorlist + colorlist_asym
            for i, key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })
        else:
            if nhistos == 7:
                #colorlist = [ROOT.kBlue+2,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed+2]
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
            self.colorlist = colorlist
            for i,key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })

    def FillCatHistos(self, fillval, catval):
        for key in self.histokeys:
            if catval >= self.Catlookup[key]["left"] and catval < self.Catlookup[key]["right"]:
                self.Cathistos[key].Fill(fillval)
                break

    def getColorlist(self):
        return self.colorlist


    def makeStyle(self):
        for key in self.histokeys:
            self.Cathistos[key].SetLineColor(ROOT.kBlack) #set Color
            self.Cathistos[key].SetFillStyle(1001)
            self.Cathistos[key].SetFillColor(self.CatColors[key]) #set Color

    def makeStack(self,order = "<"):
        rand = str(ROOT.gRandom.Integer(10000))
        self.makeStyle()
        self.Stackplot = ROOT.THStack("Stack"+self.key+rand,"Stack "+self.key+rand)
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
        self.sortedHistos = []
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.Stackplot.Add(self.Cathistos[key])
                    self.sortedHistos.append(self.Cathistos[key])
                    break
        #self.setXTitle(self.key,self.Stackplot)
    def AddTH1FtoStack(self, th1f):
        th1f.SetLineWidth(3)
        th1f.SetLineColor(ROOT.kRed)
        self.extrath1f.append(th1f)
        self.drawextrath1f = True

    def DrawStack(self):
        self.Stackplot.Draw()
        self.leg.Draw("same")
        raw_input("press  Ret")

    def projectStacks(self, tree, varexp, addselection = "1"):
        for key in self.Cathistos:
            selection = addselection+" && " + self.categorizer+" >= "+str(self.Catlookup[key]["left"])+ "&& " + self.categorizer +" < " +str(self.Catlookup[key]["right"])
            tree.Project(self.Cathistos[key].GetName(),varexp,selection)

    def WriteStack(self, canvas, pdfout = None):
        #self.Stackplot.Write()
        self.makeLegend(self.legendtext,self.symmetricCats, self.symmetricColor,"box")
        self.Stackplot.Draw("histoe")
        if self.hideyLabels:
            self.Stackplot.GetYaxis().SetLabelSize(0)
        self.setXTitle(self.key,self.Stackplot)
        self.setYTitle(self.Stackplot)
        self.leg.Draw("same")
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        if self.drawextrath1f:
            for th1f in self.extrath1f:
                th1f.Draw("same")
        if self.samplestring is not None:
            sstring = self.makeSampletext(self.samplestring)
            sstring.Draw("same")
        if len(self.additionalLabels) > 0:
            for label in self.additionalLabels:
                label.Draw("same")
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)

    def WriteNotStacked(self, canvas, pdfout = None, DrawNormalized = True):
        histos = copy.deepcopy(self.sortedHistos)
        if DrawNormalized:
            print "NORMALIZED"
            for histo in histos:
                ScaletoInt(histo)
        stuff = "histoe"
        if self.hideyLabels:
            histos[0].GetYaxis().SetLabelSize(0)
        histos[0].SetTitle("")
        self.setXTitle(self.key,histos[0])
        self.setYTitle(histos[0])
        maxval = 0
        for histo in histos:
            if histo.GetMaximum() > maxval:
                maxval = histo.GetMaximum()
        for ih,histo in enumerate(histos):
            histo.GetYaxis().SetRangeUser(0,maxval*1.1)
            histo.SetLineColor(self.colorlist[ih])
            histo.SetLineWidth(2)
            histo.SetFillStyle(0)
            histo.Draw(stuff)
            if not stuff.endswith("same"):
                stuff = stuff + " same"
        self.makeLegend(self.legendtext,self.symmetricCats, self.symmetricColor,"box")
        self.leg.Draw("same")
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        if self.drawextrath1f:
            for th1f in self.extrath1f:
                th = copy.deepcopy(th1f)
                if DrawNormalized:
                    ScaletoInt(th)
                th.Draw("same")
        if self.samplestring is not None:
            sstring = self.makeSampletext(self.samplestring)
            sstring.Draw("same")
        if len(self.additionalLabels) > 0:
            for label in self.additionalLabels:
                label.Draw("same")
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)


    def makeLegend(self, categorizer, symmetricCats, symmetricColor,style= "box"):
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
        if style is "box":
            option = "F"
        elif style is "line":
            option = "L"
        else:
            option = "F"
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.leg.AddEntry(self.Cathistos[key],str(self.Catlookup[key]["left"])+" <= "+categorizer+" < "+str(self.Catlookup[key]["right"]),option)
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
    def __init__(self, key, comparison = False, nComparisons = 2, legendtext = [], customparam = None, hideyLabels = False):
        plots.__init__(self, key, customparam)
        self.graph = False
        self.ROCCurve = False
        self.hideyLabels = hideyLabels
        if comparison:
            self.nHistos = nComparisons
        else:
            self.nHistos = 1
        self.legendtext = legendtext
        self.Fits = self.nHistos*[None]
        if comparison:
            self.histos = []
            for i in range(nComparisons):
                tmpstr = (self.key+"_"+str(i)+"_"+str(ROOT.gRandom.Integer(10000))).replace(" ","_")
                self.histos.append(ROOT.TH1F(tmpstr,tmpstr, self.bins,self.xmin,self.xmax))
        else:
            self.histos = [ROOT.TH1F(self.key,self.key, self.bins,self.xmin,self.xmax)]
        for histo in self.histos:
            self.setSumw2(histo)



    def makeStyle(self, maxyval, dofilling = False , ytitle = None, yoffsetTop = None):
        colorlist = [ROOT.kViolet+9,ROOT.kViolet+1,ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen-3,ROOT.kGreen,ROOT.kGreen+2,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2,ROOT.kMagenta+2,ROOT.kPink+2,ROOT.kRed-4, ROOT.kBlue-5, ROOT.kYellow-6]
        if self.manualcolors:
            if len(self.manualcolorlist) >= len(self.histos):
                colorlist = self.manualcolorlist
        if self.ROCCurve:
            self.setXTitle(self.key,self.histos[0],"Signal Eff.")
            self.setYTitle(self.histos[0], self.ROCYTitle)
        else:
            self.setXTitle(self.key,self.histos[0])
            if ytitle != None:
                self.setYTitle(self.histos[0], ytitle)
            else:
                self.setYTitle(self.histos[0])
        if yoffsetTop is None:
            self.histos[0].GetYaxis().SetRangeUser(0,maxyval*1.1)
        else:
            self.histos[0].GetYaxis().SetRangeUser(0,maxyval*(1.0 + yoffsetTop))
        for iHisto, histo in enumerate(self.histos):
            histo.SetLineWidth(2)
            histo.SetLineColor(colorlist[iHisto])
            if self.graph:
                histo.SetMarkerColor(colorlist[iHisto])
                histo.SetFillColor(0)
            if dofilling:
                histo.SetFillStyle(1001)
                histo.SetFillColor(ROOT.kCyan-10)

    def makeLegend(self, legendtext, addstats):
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
                leg = ROOT.TLegend(0.13,0.65,0.41,0.83)
        else:
            if self.manualLegendright:
                leg = ROOT.TLegend(self.legenx1r, self.legeny1r,self.legenx2r,self.legeny2r)
            else:
                leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.SetFillStyle(0)
        for ihisto, histo in enumerate(self.histos):
            #print "adding", legendtext[ihisto]
            leg.AddEntry(histo, legendtext[ihisto])
            if addstats:
                leg.AddEntry(histo,"Mean: "+str(histo.GetMean(1))[:6]+" RMS: "+str(histo.GetRMS(1))[:6],"")


        return leg


    def setLineStyle(self, nHisto, style = 1):
        if type(nHisto) is list:
            for h in nHisto:
                if style >= 1 and style <= 10:
                    self.histos[h].SetLineStyle(style)
        else:
            self.histos[nHisto].SetLineStyle(style)


    def FillnormHisto(self,fillval,nHisto = 0):
        self.histos[nHisto].Fill(fillval)

    def AddTH1F(self, th1f, nHisto, dosumw2 = True):
        if dosumw2:
            self.setSumw2(th1f)
        self.histos[nHisto] = copy.deepcopy(th1f)

    def projecttoHisto(self, nHisto, tree, varexp, select = "", option = ""):
        tmpstr = "tmp_"+str(ROOT.gRandom.Integer(1000))
        tmph = ROOT.TH1F(tmpstr,tmpstr, self.bins,self.xmin,self.xmax)
        self.setSumw2(tmph)
        tree.Project(tmpstr, varexp, select)
        self.histos[nHisto] = copy.deepcopy(tmph)
        del tmph


    def WriteHisto(self, canvas, samplestring = None, dofilling = False, Drawnormalized = False, pdfout = None, savehisto = False, ytitle = None, plotlogx = False, plotlogy = False, yoffsetTop = None, addstats = False):
        c1 = ROOT.TCanvas()
        c1.cd(1)
        c1.SetLogy(0)
        c1.SetLogx(0)
        if plotlogy:
            c1.SetLogy(1)
        if plotlogx:
            c1.SetLogx(1)

        if Drawnormalized:
            for histo in self.histos:
                ScaletoInt(histo)
        maxy = 0
        if not self.graph:
            for histo in self.histos:
                tmpval = histo.GetBinContent(histo.GetMaximumBin())
                if tmpval > maxy:
                    maxy = tmpval
        self.makeStyle(maxy, dofilling, ytitle, yoffsetTop)
        legend = self.makeLegend(self.legendtext, addstats)
        if self.hideyLabels:
            self.histos[0].GetYaxis().SetLabelSize(0)
        if not self.graph:
            stuff = "histoe"
        else:
            stuff = "AL"
        for histo in self.histos:
            #print "adding", histo
            if savehisto:
                histo.Write()
            histo.Draw(stuff)
            if not stuff.endswith("same"):
                stuff = stuff + " same"
                if self.graph:
                    stuff = "L"
        #canvas.Update()
        simul, cms = self.makeCMSstuff()
        for fit in self.Fits:
            if fit is not None:
                fit.Draw("same")
        if not self.noCMS:
            simul.Draw("same")
            cms.Draw("same")
        if self.nHistos > 1:
            #print "drawing legend"
            legend.Draw("same")
        if samplestring is not None:
            samplelabel = self.makeSampletext(samplestring)
            samplelabel.Draw("same")
        if len(self.additionalLabels) > 0:
            for label in self.additionalLabels:
                label.Draw("same")
        c1.Update()
        canvas = c1
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)


        #Xcanvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)

    def getHistos(self):
        hlist = []
        for histo in self.histos:
            hlist.append(histo)
        return hlist

    def getNumOfHistos(self):
        return len(self.histos)

    def fitGauss(self, nHisto, leftbound, rightbound):
        fit = ROOT.TF1("Fit_histo_"+str(nHisto),"gaus", leftbound, rightbound)
        fit.SetParameter(0,1)
        fit.SetParameter(1,1)
        fit.SetParameter(2,1.5)
        fit.SetLineWidth(2)
        fit.SetLineColor(self.histos[nHisto].GetLineColor())
        self.histos[nHisto].Fit("Fit_histo_"+str(nHisto),"","",leftbound, rightbound)
        self.Fits[nHisto] = copy.deepcopy(fit)
        del fit

    def converttoROC(self, nHisto, tree_sig,tree_bkg, varexp_sig, varexp_bkg, select_sig = "", select_bkg = "", varbinning = [10,-1,1], rej= True):
        tmpstr = "tmp_"+str(ROOT.gRandom.Integer(1000))
        tmpstr_sig = "tmp_"+str(ROOT.gRandom.Integer(1000))
        tmpstr_bkg = "tmp_"+str(ROOT.gRandom.Integer(1000))
        tmph_sig = ROOT.TH1F(tmpstr_sig,tmpstr_sig, varbinning[0],varbinning[1],varbinning[2])
        tmph_bkg = ROOT.TH1F(tmpstr_bkg,tmpstr_bkg, varbinning[0],varbinning[1],varbinning[2])
        self.setSumw2(tmph_sig)
        self.setSumw2(tmph_bkg)
        tree_sig.Project(tmpstr_sig, varexp_sig, select_sig)
        tree_bkg.Project(tmpstr_bkg, varexp_bkg, select_bkg)

        #Compute Values for ROC Curve
        nBins=tmph_sig.GetNbinsX()
        nBins2=tmph_bkg.GetNbinsX()
        integral1=tmph_sig.Integral(0,nBins+1)
        integral2=tmph_bkg.Integral(0,nBins2+1)



        nonZeroBins=[]
        for i in range(nBins,-1,-1):
            if tmph_sig.GetBinContent(i)>0. or tmph_bkg.GetBinContent(i)>0.:
                nonZeroBins.append(i)
        roc = ROOT.TGraphAsymmErrors(len(nonZeroBins)+1)

        if rej:
            roc.SetPoint(0,0,1)
        else:
            roc.SetPoint(0,0,0)
        point=1
        for i in nonZeroBins:
            eff1=0
            eff2=0
            if integral1 > 0:
                eff1=tmph_sig.Integral(i,nBins+1)/integral1
            if integral2 > 0:
                eff2=tmph_bkg.Integral(i,nBins+1)/integral2
            if rej:
                roc.SetPoint(point,eff1,1-eff2)
            else:
                roc.SetPoint(point,eff1,eff2)
            point+=1

        tmph = roc
        self.graph = True

        self.ROCCurve = True
        if rej:
            self.ROCYTitle = "Background Rej."
        else:
            self.ROCYTitle = "Background Eff."

        self.histos[nHisto] = copy.deepcopy(tmph)
        del tmph





class TwoDplot(plots):
    def __init__(self, key1, key2, customparam1 = None,  customparam2 = None, hidezLabel = False):
        self.hidezLabel = hidezLabel
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

        if customparam1 or customparam2:
            self.customparamused = True
        else:
            self.customparamused = False

        self.combinedkey = key1+"__"+key2

        ranstr = "_"+str(ROOT.gRandom.Integer(10000))

        self.histo = ROOT.TH2F(self.combinedkey+ranstr,self.combinedkey+ranstr,self.key1bins,self.key1min,self.key1max,self.key2bins,self.key2min,self.key2max)

        self.customAxisTitle = False

        #self.makeStyle()

    def makeStyle(self):
        self.setXTitle(None,self.histo,self.key1title )
        self.setYTitle(self.histo, self.key2title)

    def FillTwoDplot(self, key1val, key2val):
        self.histo.Fill(key1val, key2val)

    def WriteTwoDplot(self, canvas, samplestring = None, printStatBox = False, StatBoxNames = None,  pdfout = None, plotlogx = False, plotlogy = False, drawLine = []):
        c1 = ROOT.TCanvas()
        c1.cd(1)
        c1.SetLogy(0)
        c1.SetLogx(0)
        if plotlogy:
            c1.SetLogy(1)
        if plotlogx:
            c1.SetLogx(1)
        if self.hidezLabel:
            self.histo.GetZaxis().SetLabelSize(0)
        self.histo.SetTitle("")
        self.histo.Draw("colz")
        simul, cms = self.makeCMSstuff()
        if samplestring is not None:
            samplelabel = self.makeSampletext(samplestring)
            samplelabel.Draw("same")
        if not self.noCMS:
            simul.Draw("same")
            cms.Draw("same")
        if len(drawLine) is 4:
            line = self.getLine(drawLine[0],drawLine[1],drawLine[2],drawLine[3])
            line.Draw("same")

        if printStatBox:
            if StatBoxNames is not None:
                legend = self.printStats(StatBoxNames[0],StatBoxNames[1])
            else:
                if self.customparamused:
                    legend = self.printStats()
                else:
                    legend = self.printStats(self.key1title,self.key2title)
            legend.Draw("same")
        if self.customAxisTitle:
            self.setXTitle("", self.histo, self.Xcustom)
            self.setYTitle(self.histo, self.Ycustom)
        if len(self.additionalLabels) > 0:
            for label in self.additionalLabels:
                label.Draw("same")


        canvas = c1
        canvas.SetTitle(self.combinedkey)
        canvas.SetName(self.combinedkey)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)

    def GetTH2F(self):
        return self.histo

    def GetCombinedKey(self):
        return self.combinedkey

    def projecttoTwoDplot(self, tree, varexp, select = "", option = ""):
        tmpstr = "tmp_"+str(ROOT.gRandom.Integer(1000))
        tmph = ROOT.TH2F(tmpstr,tmpstr,self.key1bins,self.key1min,self.key1max,self.key2bins,self.key2min,self.key2max)
        self.setSumw2(tmph)
        tree.Project(tmpstr, varexp, select)
        self.histo = copy.deepcopy(tmph)
        del tmph


    def setAxisTitle(self, yAxis, xAxis):
        self.customAxisTitle = True
        self.Xcustom = xAxis
        self.Ycustom = yAxis


    def printStats(self, xaxis = "x", yaxis = "y"):
        leg = ROOT.TLegend(0.7,0.70,0.88,0.88)
        leg.AddEntry(0,"Mean "+str(xaxis)+": "+str(self.histo.GetMean(1))[:6],"")
        leg.AddEntry(0,"Mean "+str(yaxis)+": "+str(self.histo.GetMean(2))[:6],"")
        leg.AddEntry(0,"RMS "+str(xaxis)+": "+str(self.histo.GetRMS(1))[:6],"")
        leg.AddEntry(0,"RMS "+str(yaxis)+": "+str(self.histo.GetRMS(2))[:6],"")
        leg.SetMargin(leg.GetMargin()*0.4)
        #leg.SetBorderSize(0)
        leg.SetTextFont(42)
        #leg.SetFillStyle(0)
        return leg

class PointPlot(plots):
    def __init__(self, nPoints, YLabel, legendtext = []):
        tmpstr = "_"+str(ROOT.gRandom.Integer(1000))
        self.histo = ROOT.TH1F("pointplot"+tmpstr,"pointplot"+tmpstr,100,0,nPoints+0.7)
        self.pointsadded = 0;
        self.grapherrorlist = []
        self.maxPoints = nPoints
        self.Pointvalues = []
        self.manualcolors = False
        self.YLabel = YLabel
        self.Legendtext = legendtext
        self.additionalLabels = []
        self.manualLegendright = False
        self.manualLegendleft = False


    def addPoint(self, m, em = 0):
        #tmpgraph = ROOT.TGraphErrors(1,array('f',[self.pointsadded+0.5]),array('f',[m]),array('f',[0]),array('f',[em]))
        #tmpgraph.SetPoint(1,self.pointsadded+0.5,m)
        #tmpgraph.SetPointError(1,0,em)
        #tmpgraph.Draw()
        self.grapherrorlist.append(ROOT.TGraphErrors(1,array('f',[self.pointsadded+0.5]),array('f',[m]),array('f',[0]),array('f',[em])))
        self.Pointvalues.append(m)
        self.pointsadded += 1
        #del tmpgraph

    def makeStyle(self, fixedy):
        if self.manualcolors:
            colorlist = self.manualcolorlist
        else:
            colorlist =  [ROOT.kViolet+9,ROOT.kViolet+1,ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen-3,ROOT.kGreen,ROOT.kGreen+2,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2,ROOT.kMagenta+2,ROOT.kPink+2,ROOT.kRed-4, ROOT.kBlue-5, ROOT.kYellow-6]
        maxP = -99999999999
        minP = 99999999999
        for n in range(self.maxPoints):
            if self.Pointvalues[n] < minP:
                minP = self.Pointvalues[n]
            if self.Pointvalues[n] > maxP:
                maxP = self.Pointvalues[n]
            self.grapherrorlist[n].SetMarkerColor(colorlist[n])
            self.grapherrorlist[n].SetMarkerSize(1.)
            self.grapherrorlist[n].SetMarkerStyle(21)
        a = minP-(minP*0.05)
        b = maxP+(maxP*0.125)
        self.minimum = minP
        self.maximum = maxP
        if fixedy is not None:
            self.histo.GetYaxis().SetRangeUser(fixedy[0],fixedy[1])
        else:
            self.histo.GetYaxis().SetRangeUser(a,b)
        self.histo.GetXaxis().SetNdivisions(000)
        self.histo.GetXaxis().SetLabelSize(0)
        self.setYTitle(self.histo, self.YLabel)
        self.setXTitle("",self.histo, "")
        self.histo.SetTitle("")

    def makeLegend(self):
        if self.manualLegendleft:
            leg = ROOT.TLegend(self.legenx1l,self.legeny1l,self.legenx2l,self.legeny2l)
        elif self.manualLegendright:
            leg = ROOT.TLegend(self.legenx1r,self.legeny1r,self.legenx2r,self.legeny2r)
        else:
            leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
        for n in range(self.maxPoints):
            leg.AddEntry(self.grapherrorlist[n],self.Legendtext[n],"p")
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.SetFillStyle(0)
        return leg


    def WritePointPlot(self, canvas, samplestring = None, pdfout = None, fixedy = None, showwline = "Min"):
        if self.pointsadded == self.maxPoints:
            c1 = ROOT.TCanvas()
            c1.cd(1)
            c1.SetLogy(0)
            c1.SetLogx(0)
            self.makeStyle(fixedy)
            self.histo.Draw("")
            for nP in range(self.maxPoints):
                #print "Drawing point",nP
                self.grapherrorlist[nP].Draw("P")
            legend = self.makeLegend()
            legend.Draw("same")
            if samplestring is not None:
                samplelabel = self.makeSampletext(samplestring)
                samplelabel.Draw("same")
            simul, cms = self.makeCMSstuff()
            if len(self.additionalLabels) > 0:
                for label in self.additionalLabels:
                    label.Draw("same")
            if showwline is not None:
                    if showwline == "Min":
                        line = self.getLine(0,self.minimum,self.maxPoints+0.7,self.minimum,True,False)
                        drawline = True
                    elif showwline == "Max":
                        line = self.getLine(0,self.maximum,self.maxPoints+0.7,self.maximum,True,False)
                        drawline = True
                    else:
                        drawline = False
            else:
                drawline = False
            if drawline:
                line.Draw("same")
            simul.Draw("same")
            cms.Draw("same")
            canvas = c1
            canvas.SetTitle("blubb")
            canvas.SetName("blubb")
            canvas.Update()
            canvas.Write()
            if pdfout is not None:
                pdfout.addCanvastoPDF(canvas)
        else:
            print "Added Points and set Point at initialisation are different"

class StackPlots(plots):

    def __init__(self, key, nHistos, legendtext = [], styles = None, customparam = None,hideyLabels = False):
        plots.__init__(self, key, customparam)
        self.nHistos = nHistos
        self.histos = []
        self.legendtext = legendtext
        self.hideyLabels = hideyLabels
        self.styles = nHistos*["Box"]
        if styles is not None:
            if len(styles) == nHistos:
                self.styles = styles
            else:
                print "Len of style not equal to number of histos"
        for i in range(nHistos):
            tmpstr = (self.key+"_"+str(i)+"_"+str(ROOT.gRandom.Integer(10000))).replace(" ","_")
            self.histos.append(ROOT.TH1F(tmpstr,tmpstr, self.bins,self.xmin,self.xmax))
        for histo in self.histos:
            self.setSumw2(histo)

    def makeStyle(self, maxyval, ytitle = None, yoffsetTop = None):
        colorlist = [ROOT.kViolet+9,ROOT.kViolet+1,ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen-3,ROOT.kGreen,ROOT.kGreen+2,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2,ROOT.kMagenta+2,ROOT.kPink+2,ROOT.kRed-4, ROOT.kBlue-5, ROOT.kYellow-6]
        if self.manualcolors:
            if len(self.manualcolorlist) >= len(self.histos):
                colorlist = self.manualcolorlist
        self.setXTitle(self.key,self.histos[0])
        if ytitle != None:
            self.setYTitle(self.histos[0], ytitle)
        else:
            self.setYTitle(self.histos[0])
        #if yoffsetTop is None:
        #    self.histos[0].GetYaxis().SetRangeUser(0,maxyval*1.1)
        #else:
        #    self.histos[0].GetYaxis().SetRangeUser(0,maxyval*(1.0 + yoffsetTop))
        for iHisto, histo in enumerate(self.histos):
            histo.SetLineWidth(2)
            if self.styles[iHisto] == "Box":
                histo.SetLineColor(ROOT.kBlack)
                histo.SetFillStyle(1001)
                histo.SetFillColor(colorlist[iHisto])
            elif self.styles[iHisto] == "Line":
                histo.SetLineColor(colorlist[iHisto])
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
                leg = ROOT.TLegend(0.13,0.65,0.41,0.83)
        else:
            if self.manualLegendright:
                leg = ROOT.TLegend(self.legenx1r, self.legeny1r,self.legenx2r,self.legeny2r)
            else:
                leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.SetFillStyle(0)
        for ihisto, histo in enumerate(self.histos):
            if self.styles[ihisto] == "Box":
                leg.AddEntry(histo, legendtext[ihisto], "F")
            elif self.styles[ihisto] == "Line":
                leg.AddEntry(histo, legendtext[ihisto], "L")
        return leg

    def projecttoHisto(self, nHisto, tree, varexp, select = "", option = ""):
        tmpstr = "tmp_"+str(ROOT.gRandom.Integer(1000))
        tmph = ROOT.TH1F(tmpstr,tmpstr, self.bins,self.xmin,self.xmax)
        self.setSumw2(tmph)
        tree.Project(tmpstr, varexp, select)
        self.histos[nHisto] = copy.deepcopy(tmph)
        del tmph


    def makeStack(self):
        rand = str(ROOT.gRandom.Integer(10000))
        #self.makeStyle()
        self.Stackplot = ROOT.THStack("Stack"+self.key+rand,"Stack "+self.key+rand)
        self.histos.reverse()
        self.styles.reverse()
        for ihisto,histo in enumerate(self.histos):
            if self.styles[ihisto] == "Box":
                self.Stackplot.Add(histo)
        self.histos.reverse()
        self.styles.reverse()

    def WriteHisto(self, canvas, samplestring = None, Drawnormalized = False, pdfout = None,  ytitle = None, plotlogx = False, plotlogy = False, yoffsetTop = 0.1):
        c1 = ROOT.TCanvas()
        c1.cd(1)
        c1.SetLogy(0)
        c1.SetLogx(0)
        if plotlogy:
            c1.SetLogy(1)
        if plotlogx:
            c1.SetLogx(1)
        maxy = 1
        if Drawnormalized:
            for histo in self.histos:
                ScaletoInt(histo)

        self.makeStyle(maxy, ytitle, yoffsetTop)
        if self.hideyLabels:
            for i in range(self.nHistos):
                self.histos[i].GetYaxis().SetLabelSize(0)
        self.makeStack()
        """
        maxy =  self.Stackplot.GetBinContent(histo.GetMaximumBin())
        for histo in self.histos:
            if self.styles[ihisto] == "Line":
                tmpval = histo.GetBinContent(histo.GetMaximumBin())
                if tmpval > maxy:
                    maxy = tmpval
"""
        legend = self.makeLegend(self.legendtext)
        self.Stackplot.Draw("histo")
        if self.hideyLabels:
            self.Stackplot.GetYaxis().SetLabelSize(0)
        self.setXTitle(self.key,self.Stackplot)
        self.setYTitle(self.Stackplot)
        for ihisto,histo in enumerate(self.histos):
            if self.styles[ihisto] == "Line":
                histo.Draw("histo same")
        simul, cms = self.makeCMSstuff()
        if not self.noCMS:
            simul.Draw("same")
            cms.Draw("same")
        if self.nHistos > 1:
            legend.Draw("same")
        if samplestring is not None:
            samplelabel = self.makeSampletext(samplestring)
            samplelabel.Draw("same")
        if len(self.additionalLabels) > 0:
            for label in self.additionalLabels:
                label.Draw("same")
        c1.Update()
        canvas = c1
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)




def ScaletoInt(th1f):
    if th1f.GetNbinsX() != 1:
        th1f.Scale(1/float(th1f.Integral()))
