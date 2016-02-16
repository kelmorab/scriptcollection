import ROOT
import rootutils

def ScaletoInt(th1f):
    th1f.Scale(1/float(th1f.Integral()))

ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0);

inputfile1 = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root")

tree1 = inputfile1.Get("MVATree")


histo_regcorr = ROOT.TH1F("regcorr","regcorr",60,0.4,1.8)
histo_partonpt = ROOT.TH1F("partonpt","partonpt",60,0,3)
histo_partonpt_noreg = ROOT.TH1F("partonpt_noreg","partonpt",60,0,3)
histo_partonpt_nob = ROOT.TH1F("partonpt_nob","partonpt_nob",60,0,3)
histo_partonregpt = ROOT.TH1F("partonregpt","partonregpt",60,0,3)

histo_regcorr.Sumw2()
histo_partonpt.Sumw2()
histo_partonpt_nob.Sumw2()
histo_partonregpt.Sumw2()
histo_partonpt_noreg.Sumw2()

isttH = True

c1 = ROOT.TCanvas()


selection_Odd = "Evt_Odd == 0"


selection = "Jet_Pt > 0"
if isttH:
    selection = selection
else:
    selection = selection+" && "+selection_Odd


print "Projecting to regcorr" 
tree1.Project("regcorr","Jet_regcorr",selection+" && Jet_regPt > 0")
print "Projecting to Parton Pt / Jet pt" 
tree1.Project("partonpt","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt >0 && abs(Jet_PartonFlav) == 5 && Jet_regPt > 0")
print "Projecting to Parton Pt / Jet pt" 
tree1.Project("partonpt_noreg","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt > 0 && abs(Jet_PartonFlav) == 5")
print "Projecting to Parton Pt / Jet pt" 
tree1.Project("partonpt_nob","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt > 0 && abs(Jet_PartonFlav) != 5")
print "Projecting to Parton Pt / regressed Jet pt" 
tree1.Project("partonregpt","Jet_regPt/Jet_PartonPt",selection+" && Jet_PartonPt >0 && abs(Jet_PartonFlav) == 5 && Jet_regPt > 0")


histo_regcorr.SetLineColor(ROOT.kRed)
histo_partonpt.SetLineColor(ROOT.kBlue)
histo_partonpt_nob.SetLineColor(ROOT.kViolet)
histo_partonregpt.SetLineColor(ROOT.kRed)

leg1=ROOT.TLegend(0.6,0.74,0.89,0.89)
leg1.AddEntry(histo_partonpt,"b-Jets")
leg1.AddEntry(histo_partonpt_nob,"u/d/s/c-Jets")


leg2=ROOT.TLegend(0.6,0.75,0.89,0.89)
leg2.AddEntry(histo_partonpt,"Vor Regression")
leg2.AddEntry(histo_partonregpt,"Nach Regression")


simul = ROOT.TLatex(0.125, 0.908, 'CMS simulation')
simul.SetTextFont(42)
simul.SetTextSize(0.045)
simul.SetNDC()

cms = ROOT.TLatex(0.125, 0.86, 'work in progress')
cms.SetTextFont(42)
cms.SetTextSize(0.045)
cms.SetNDC()

#RegCorr Plot:

histo_regcorr.Draw("histoe")
#Make Style
histo_regcorr.SetTitle("")
ScaletoInt(histo_regcorr)
histo_regcorr.GetXaxis().SetTitle("Regressed Jet p_{T} / Jet p_{T}")
histo_regcorr.GetXaxis().SetTitleSize(0.05)
histo_regcorr.GetXaxis().SetTitleOffset(0.75)
histo_regcorr.GetYaxis().SetTitle("Beliebige Einheiten")
histo_regcorr.GetYaxis().SetTitleSize(0.05)
histo_regcorr.GetYaxis().SetTitleOffset(0.8)
histo_regcorr.GetYaxis().SetRangeUser(0,histo_regcorr.GetBinContent(histo_regcorr.GetMaximumBin())*1.1)

cms.Draw("same")
simul.Draw("same")
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



"""
histo_partonpt_noreg.Draw("histoe")
#Make Style
histo_partonpt_noreg.SetTitle("")
ScaletoInt(histo_partonpt)
ScaletoInt(histo_partonpt_nob)
histo_partonpt_noreg.GetXaxis().SetTitle("Jet p_{T, Jet} / p_{T, Parton}")
histo_partonpt_noreg.GetXaxis().SetTitleSize(0.055)
histo_partonpt_noreg.GetXaxis().SetTitleOffset(0.7)
histo_partonpt_noreg.GetYaxis().SetTitle("Beliebige Einheiten")
histo_partonpt_noreg.GetYaxis().SetTitleSize(0.05)
histo_partonpt_noreg.GetYaxis().SetTitleOffset(0.8)
histo_partonpt_noreg.GetYaxis().SetRangeUser(0,histo_partonpt.GetBinContent(histo_partonpt.GetMaximumBin())*1.1)
histo_partonpt_nob.Draw("histoe same")

leg1.Draw("same")
cms.Draw("same")
simul.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()


raw_input("Press ret")
"""

#parton pt plot

histo_partonregpt.Draw("histoe")
#Make Style
histo_partonregpt.SetTitle("")
ScaletoInt(histo_partonregpt)
ScaletoInt(histo_partonpt)
histo_partonregpt.GetXaxis().SetTitle("Jet p_{T, Jet} / p_{T, Parton}")
histo_partonregpt.GetXaxis().SetTitleSize(0.055)
histo_partonregpt.GetXaxis().SetTitleOffset(0.7)
histo_partonregpt.GetYaxis().SetTitle("Beliebige Einheiten")
histo_partonregpt.GetYaxis().SetTitleSize(0.05)
histo_partonregpt.GetYaxis().SetTitleOffset(0.8)
histo_partonregpt.GetYaxis().SetRangeUser(0,histo_partonregpt.GetBinContent(histo_partonregpt.GetMaximumBin())*1.1)


histo_partonpt.Draw("histoe same")

leg2.Draw("same")
cms.Draw("same")
simul.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()


raw_input("Press ret")


histo_partonpt.Draw("histoe")
#Make Style
histo_partonpt.SetTitle("")
ScaletoInt(histo_partonpt)
ScaletoInt(histo_partonpt_nob)
histo_partonpt.GetXaxis().SetTitle("Jet p_{T, Jet} / p_{T, Parton}")
histo_partonpt.GetXaxis().SetTitleSize(0.055)
histo_partonpt.GetXaxis().SetTitleOffset(0.7)
histo_partonpt.GetYaxis().SetTitle("Beliebige Einheiten")
histo_partonpt.GetYaxis().SetTitleSize(0.05)
histo_partonpt.GetYaxis().SetTitleOffset(0.8)
histo_partonpt.GetYaxis().SetRangeUser(0,histo_partonpt.GetBinContent(histo_partonpt.GetMaximumBin())*1.1)
histo_partonpt_nob.Draw("histoe same")

leg1.Draw("same")
cms.Draw("same")
simul.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()


raw_input("Press ret")
