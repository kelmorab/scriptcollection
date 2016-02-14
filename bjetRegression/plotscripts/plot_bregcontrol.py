import ROOT
ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0);

inputfile1 = ROOT.TFile("ttHbb.root")

tree1 = inputfile1.Get("MVATree")


histo_regcorr = ROOT.TH1F("regcorr","regcorr",60,0.4,1.8)
#histo_regpt = ROOT.TH1F("regpt","regpt",200,0,600)
#histo_pt = ROOT.TH1F("pt","pt",200,0,600)
histo_partonpt = ROOT.TH1F("partonpt","partonpt",60,0,3)
histo_partonregpt = ROOT.TH1F("partonregpt","partonregpt",60,0,3)

isttH = True

c1 = ROOT.TCanvas()


selection_Odd = "Evt_Odd == 0"


selection = "Jet_regPt > 0"
if isttH:
    selection = selection
else:
    selection = selection+" && "+selection_Odd


print "Projecting to regcorr" 
tree1.Project("regcorr","Jet_regcorr",selection)
print "Projecting to Parton Pt / Jet pt" 
tree1.Project("partonpt","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt > 0 && abs(Jet_PartonFlav) == 5 && Jet_regPt > 0")
print "Projecting to Parton Pt / regressed Jet pt" 
tree1.Project("partonregpt","Jet_regPt/Jet_PartonPt",selection+" && Jet_PartonPt > 0 && abs(Jet_PartonFlav) == 5 && Jet_regPt > 0")


histo_regcorr.SetLineColor(ROOT.kRed)
histo_partonpt.SetLineColor(ROOT.kBlue)
histo_partonregpt.SetLineColor(ROOT.kRed)

leg1=ROOT.TLegend(0.6,0.54,0.89,0.89)
leg1.AddEntry(histo_regcorr,"Vor Regression")


leg2=ROOT.TLegend(0.6,0.75,0.89,0.89)
leg2.AddEntry(histo_partonpt,"Vor Regression")
leg2.AddEntry(histo_partonregpt,"Nach Regression")


cms = ROOT.TLatex(0.15, 0.92, 'CMS private work')
cms.SetTextFont(42)
cms.SetTextSize(0.05)
cms.SetNDC()


#RegCorr Plot:

histo_regcorr.Draw("histoe")
#Make Style
histo_regcorr.SetTitle("")
histo_regcorr.GetXaxis().SetTitle("Regressed Jet p_{T} / Jet p_{T}")
histo_regcorr.GetXaxis().SetTitleSize(0.05)
histo_regcorr.GetXaxis().SetTitleOffset(0.75)
histo_regcorr.GetYaxis().SetTitle("Ereignisse")
histo_regcorr.GetYaxis().SetTitleSize(0.05)
histo_regcorr.GetYaxis().SetTitleOffset(0.8)


cms.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()

raw_input("Press Ret")

c1.Print("bregcontrol_regcorr.pdf","title1")

#parton pt plot

histo_partonregpt.Draw("histoe")
#Make Style
histo_partonregpt.SetTitle("")
histo_partonregpt.GetXaxis().SetTitle("p_{T, Lepton} / Jet p_{T, Jet}")
histo_partonregpt.GetXaxis().SetTitleSize(0.06)
histo_partonregpt.GetXaxis().SetTitleOffset(0.7)
histo_partonregpt.GetYaxis().SetTitle("Ereignisse")
histo_partonregpt.GetYaxis().SetTitleSize(0.05)
histo_partonregpt.GetYaxis().SetTitleOffset(0.8)

histo_partonpt.Draw("histoe same")

leg2.Draw("same")
cms.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()


c1.Print("bregcontrol_partonpt.pdf","title2")


raw_input("Press ret")
