import ROOT
from rootutils import PDFPrinting

def ScaletoInt(th1f):
    th1f.Scale(1/float(th1f.Integral()))

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);

inputfile1 = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttHbb.root")

tree1 = inputfile1.Get("MVATree")


histo_regcorr = ROOT.TH1F("regcorr","regcorr",60,0.4,1.8)
histo_partonpt = ROOT.TH1F("partonpt","partonpt",60,0,2.5)
histo_partonpt_noreg = ROOT.TH1F("partonpt_noreg","partonpt",60,0,2.5)
histo_partonpt_nob = ROOT.TH1F("partonpt_nob","partonpt_nob",60,0,2.5)
histo_partonregpt = ROOT.TH1F("partonregpt","partonregpt",60,0,2.5)
histo_partonpt_misstag = ROOT.TH1F("partonpt_misstag","partonpt_misstag",60,0,2.5)
histo_partonpt_noreg_misstag = ROOT.TH1F("partonpt_noreg_misstag","partonpt_misstag",60,0,2.5)


histo_regcorr.Sumw2()
histo_partonpt.Sumw2()
histo_partonpt_nob.Sumw2()
histo_partonregpt.Sumw2()
histo_partonpt_noreg.Sumw2()
histo_partonpt_misstag.Sumw2()
histo_partonpt_noreg_misstag.Sumw2()
isttH = True
german = False

pdfout = PDFPrinting("bregcontrol")

c1 = ROOT.TCanvas()


selection_Odd = "Evt_Odd == 0"


selection = "Jet_Pt > 0"
if isttH:
    selection = selection
else:
    selection = selection+" && "+selection_Odd


print "Projecting regcorr" 
tree1.Project("regcorr","Jet_regcorr",selection+" && Jet_regPt > 0")
print "Projecting Jet Pt / Paron pt for b-Jets" 
tree1.Project("partonpt","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt >0 && abs(Jet_PartonFlav) == 5 && Jet_regPt > 0")
print "Projecting non regressed Jet Pt / Paron pt for b-Jets" 
tree1.Project("partonpt_noreg","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt > 0 && abs(Jet_PartonFlav) == 5")
print "Projecting Jet Pt / Paron pt for non b-Jets" 
tree1.Project("partonpt_nob","Jet_Pt/Jet_PartonPt",selection+" && Jet_PartonPt > 0 && abs(Jet_PartonFlav) != 5")
print "Projecting regressed Jet pt / Parton Pt" 
tree1.Project("partonregpt","Jet_regPt/Jet_PartonPt",selection+" && Jet_PartonPt >0 && abs(Jet_PartonFlav) == 5 && Jet_regPt > 0")
print "Projection regressed Jet Pt / Parton Pt for misstagged with matchedParton"
tree1.Project("partonpt_misstag","Jet_regPt/Jet_PartonPt",selection+" && Jet_regPt > 0 && Jet_PartonPt >= 0 && abs(Jet_Flav) != 5")
print "Projection Jet Pt / Parton Pt for misstagged with matchedParton"
tree1.Project("partonpt_noreg_misstag","Jet_Pt/Jet_PartonPt",selection+" && Jet_regPt > 0 && Jet_PartonPt >= 0 && abs(Jet_Flav) != 5")




histo_regcorr.SetLineColor(ROOT.kRed)
histo_partonpt.SetLineColor(ROOT.kBlue)
histo_partonpt_noreg.SetLineColor(ROOT.kBlue)
histo_partonpt_nob.SetLineColor(ROOT.kViolet-5)
histo_partonregpt.SetLineColor(ROOT.kRed)
histo_partonpt_misstag.SetLineColor(ROOT.kRed)
histo_partonpt_noreg_misstag.SetLineColor(ROOT.kBlue)


leg1=ROOT.TLegend(0.6,0.74,0.89,0.89)
leg1.AddEntry(histo_partonpt_noreg,"b-Jets")
leg1.AddEntry(histo_partonpt_nob,"u/d/s/c-Jets")


leg2=ROOT.TLegend(0.6,0.75,0.89,0.89)
if german:
    leg2.AddEntry(histo_partonpt,"Vor Regression")
    leg2.AddEntry(histo_partonregpt,"Nach Regression")
else:
    leg2.AddEntry(histo_partonpt,"Before Regression")
    leg2.AddEntry(histo_partonregpt,"After Regression")

simul = ROOT.TLatex(0.125, 0.908, 'CMS simulation')
simul.SetTextFont(42)
simul.SetTextSize(0.045)
simul.SetNDC()

cms = ROOT.TLatex(0.125, 0.86, 'work in progress')
cms.SetTextFont(42)
cms.SetTextSize(0.045)
cms.SetNDC()

label = ROOT.TLatex(0.6275,0.908, 'Sample: t#bar{t}H , H #rightarrow b#bar{b}')
label.SetTextFont(42)
label.SetTextSize(0.045)
label.SetNDC()

#RegCorr Plot:

histo_regcorr.Draw("histoe")
#Make Style
histo_regcorr.SetTitle("")
ScaletoInt(histo_regcorr)
histo_regcorr.GetXaxis().SetTitle("p_{T, reg} / p_{T}")
histo_regcorr.GetXaxis().SetTitleSize(0.05)
histo_regcorr.GetXaxis().SetTitleOffset(0.75)
if german:
    histo_regcorr.GetYaxis().SetTitle("Beliebige Einheiten")
else:
    histo_regcorr.GetYaxis().SetTitle("arbitrary units")
histo_regcorr.GetYaxis().SetTitleSize(0.05)
histo_regcorr.GetYaxis().SetTitleOffset(0.8)
histo_regcorr.GetYaxis().SetRangeUser(0,histo_regcorr.GetBinContent(histo_regcorr.GetMaximumBin())*1.1)

cms.Draw("same")
simul.Draw("same")
label.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()

pdfout.addCanvastoPDF(c1)

#raw_input("Press Ret")



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
histo_partonregpt.GetXaxis().SetTitle("p_{T, Jet} / p_{T, Parton}")
histo_partonregpt.GetXaxis().SetTitleSize(0.055)
histo_partonregpt.GetXaxis().SetTitleOffset(0.7)
if german:
    histo_partonregpt.GetYaxis().SetTitle("Beliebige Einheiten")
else:
    histo_partonregpt.GetYaxis().SetTitle("arbitrary units")
histo_partonregpt.GetYaxis().SetTitleSize(0.05)
histo_partonregpt.GetYaxis().SetTitleOffset(0.8)
histo_partonregpt.GetYaxis().SetRangeUser(0,histo_partonregpt.GetBinContent(histo_partonregpt.GetMaximumBin())*1.1)


histo_partonpt.Draw("histoe same")

leg2.Draw("same")
cms.Draw("same")
simul.Draw("same")
label.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()
pdfout.addCanvastoPDF(c1)

#raw_input("Press ret")


histo_partonpt_noreg.Draw("histoe")
#Make Style
histo_partonpt_noreg.SetTitle("")
ScaletoInt(histo_partonpt_nob)
ScaletoInt(histo_partonpt_noreg)
histo_partonpt_noreg.GetXaxis().SetTitle("p_{T, Jet} / p_{T, Parton}")
histo_partonpt_noreg.GetXaxis().SetTitleSize(0.055)
histo_partonpt_noreg.GetXaxis().SetTitleOffset(0.7)
if german:
    histo_partonpt_noreg.GetYaxis().SetTitle("Beliebige Einheiten")
else:
    histo_partonpt_noreg.GetYaxis().SetTitle("arbitrary units")
histo_partonpt_noreg.GetYaxis().SetTitleSize(0.05)
histo_partonpt_noreg.GetYaxis().SetTitleOffset(0.8)
histo_partonpt_noreg.GetYaxis().SetRangeUser(0,histo_partonpt_noreg.GetBinContent(histo_partonpt_noreg.GetMaximumBin())*1.1)
histo_partonpt_nob.Draw("histoe same")

leg1.Draw("same")
cms.Draw("same")
simul.Draw("same")
label.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()
pdfout.addCanvastoPDF(c1)


histo_partonpt_noreg_misstag.Draw("histoe")
#Make Style
histo_partonpt_noreg_misstag.SetTitle("")
ScaletoInt(histo_partonpt_misstag)
ScaletoInt(histo_partonpt_noreg_misstag)
histo_partonpt_noreg_misstag.GetXaxis().SetTitle("p_{T, Jet} / p_{T, Parton}")
histo_partonpt_noreg_misstag.GetXaxis().SetTitleSize(0.055)
histo_partonpt_noreg_misstag.GetXaxis().SetTitleOffset(0.7)
if german:
    histo_partonpt_noreg_misstag.GetYaxis().SetTitle("Beliebige Einheiten")
else:
    histo_partonpt_noreg_misstag.GetYaxis().SetTitle("arbitrary units")
histo_partonpt_noreg_misstag.GetYaxis().SetTitleSize(0.05)
histo_partonpt_noreg_misstag.GetYaxis().SetTitleOffset(0.8)
histo_partonpt_noreg_misstag.GetYaxis().SetRangeUser(0,histo_partonpt_noreg.GetBinContent(histo_partonpt_noreg.GetMaximumBin())*1.1)
histo_partonpt_misstag.Draw("histoe same")

dofit = True

if dofit:
    noreg_left = 0.8
    noreg_right = 1.2
    reg_left = 0.85
    reg_right = 1.25


    fit_noreg = ROOT.TF1("Fit_noreg","gaus",noreg_left,noreg_right)
    fit_noreg.SetParameter(0,1)
    fit_noreg.SetParameter(1,1)
    fit_noreg.SetParameter(2,1.5)
    fit_noreg.SetLineWidth(2)
    fit_noreg.SetLineColor(ROOT.kBlue)
    fit_reg = ROOT.TF1("Fit_reg","gaus",reg_left,reg_right)
    fit_reg.SetParameter(0,1)
    fit_reg.SetParameter(1,1)
    fit_reg.SetParameter(2,1.5)
    fit_reg.SetLineWidth(2)
    fit_reg.SetLineColor(ROOT.kRed)


    histo_partonpt_noreg_misstag.Fit("Fit_noreg","","",noreg_left,noreg_right)
    histo_partonpt_misstag.Fit("Fit_reg","","",reg_left,reg_right)
    
    fit_reg.Draw("same")
    fit_noreg.Draw("same")
    


leg_misstag=ROOT.TLegend(0.55,0.45,0.89,0.89)
if german:
    leg_misstag.AddEntry(histo_partonpt_noreg_misstag,"Vor Regression")    
else:
    leg_misstag.AddEntry(histo_partonpt_noreg_misstag,"Before Regression")
if dofit:
    leg_misstag.AddEntry(0,"Fit: #mu="+str(fit_noreg.GetParameter(1))[:6]+"#pm"+str(fit_noreg.GetParError(1))[:6],"")
    leg_misstag.AddEntry(0,"     #sigma="+str(fit_noreg.GetParameter(2))[:6]+"#pm"+str(fit_noreg.GetParError(2))[:6],"")
if german:
    leg_misstag.AddEntry(histo_partonpt_misstag,"Nach Regression")
else:
    leg_misstag.AddEntry(histo_partonpt_misstag,"After Regression")
if dofit:
    leg_misstag.AddEntry(0,"Fit: #mu="+str(fit_reg.GetParameter(1))[:6]+"#pm"+str(fit_reg.GetParError(1))[:6],"")
    leg_misstag.AddEntry(0,"     #sigma="+str(fit_reg.GetParameter(2))[:6]+"#pm"+str(fit_reg.GetParError(2))[:6],"")



leg_misstag.Draw("same")
cms.Draw("same")
simul.Draw("same")
label.Draw("same")
c1.Update()

drawLine = True
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(2)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")

c1.Update()
pdfout.addCanvastoPDF(c1)


pdfout.closePDF()
#raw_input("Press ret")
