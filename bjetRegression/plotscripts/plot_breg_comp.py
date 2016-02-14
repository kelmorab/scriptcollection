import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);

inputfile1 = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_nominal.root")

tree1 = inputfile1.Get("MVATree")
inputfile2 = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_evalbReg_0125_nominal.root")

tree2 = inputfile2.Get("bRegTree")
histo_noreg = ROOT.TH1F("noreg","Jet p_{T}/Parton p_{T}",70,0.2,1.8)
histo_reg_HV = ROOT.TH1F("reg-HV","Jet p_{T}/p_{T, parton}",70,0.2,1.8)
histo_reg_ttH = ROOT.TH1F("reg-ttH","Jet p_{T}/p_{T, parton}",70,0.2,1.8)

c1 = ROOT.TCanvas()

selection_PartonFlav = "abs(Jet_PartonFlav) == 5"
selection_Flav = "abs(Jet_Flav) == 5"
selection_Odd = "Evt_Odd == 0"


selection = selection_PartonFlav+" && "+selection_Flav+" && "+selection_Odd

print "Projecting to  noreg" 
tree1.Project("noreg","Jet_Pt/Jet_PartonPt",selection)
print "Projecting to  reg-HV" 
tree1.Project("reg-HV","Jet_regPt/Jet_PartonPt",selection)
print "Projecting to  reg-ttH" 
tree2.Project("reg-ttH","Jet_regPt/Jet_PartonPt",selection)

histo_noreg.SetLineColor(ROOT.kBlue)
histo_reg_HV.SetLineColor(ROOT.kRed)
histo_reg_ttH.SetLineColor(ROOT.kGreen+2)


fit_noreg = ROOT.TF1("Fit_noreg","gaus",0.8,1.1)
fit_noreg.SetParameter(0,1)
fit_noreg.SetParameter(1,1)
fit_noreg.SetParameter(2,1.5)
fit_noreg.SetLineWidth(2)
fit_noreg.SetLineColor(ROOT.kBlue)
fit_reg_HV = ROOT.TF1("Fit_reg_HV","gaus",0.85,1.135)
fit_reg_HV.SetParameter(0,1)
fit_reg_HV.SetParameter(1,1)
fit_reg_HV.SetParameter(2,1.5)
fit_reg_HV.SetLineWidth(2)
fit_reg_HV.SetLineColor(ROOT.kRed)
fit_reg_ttH = ROOT.TF1("Fit_reg_ttH","gaus",0.85,1.135)
fit_reg_ttH.SetParameter(0,1)
fit_reg_ttH.SetParameter(1,1)
fit_reg_ttH.SetParameter(2,1.5)
fit_reg_ttH.SetLineWidth(2)
fit_reg_ttH.SetLineColor(ROOT.kGreen+2)


histo_noreg.Fit("Fit_noreg","","",0.85,1.1)
histo_reg_HV.Fit("Fit_reg_HV","","",0.9,1.11)
histo_reg_ttH.Fit("Fit_reg_ttH","","",0.9,1.11)


leg=ROOT.TLegend(0.6,0.54,0.89,0.89)
leg.AddEntry(histo_noreg,"Before Regression")
leg.AddEntry(0,"Fit: #mu="+str(fit_noreg.GetParameter(1))[:6]+"#pm"+str(fit_noreg.GetParError(1))[:6],"")
leg.AddEntry(0,"     #sigma="+str(fit_noreg.GetParameter(2))[:6]+"#pm"+str(fit_noreg.GetParError(2))[:6],"")
leg.AddEntry(histo_reg_HV,"After Regression HV Training")
leg.AddEntry(0,"Fit: #mu="+str(fit_reg_HV.GetParameter(1))[:6]+"#pm"+str(fit_reg_HV.GetParError(1))[:6],"")
leg.AddEntry(0,"     #sigma="+str(fit_reg_HV.GetParameter(2))[:6]+"#pm"+str(fit_reg_HV.GetParError(2))[:6],"")
leg.AddEntry(histo_reg_ttH,"After Regression our Training")
leg.AddEntry(0,"Fit: #mu="+str(fit_reg_ttH.GetParameter(1))[:6]+"#pm"+str(fit_reg_ttH.GetParError(1))[:6],"")
leg.AddEntry(0,"     #sigma="+str(fit_reg_ttH.GetParameter(2))[:6]+"#pm"+str(fit_reg_ttH.GetParError(2))[:6],"")

#histo_noreg.GetYaxis().SetRangeUser(0,)

histo_noreg.Draw()
fit_noreg.Draw("same")
histo_reg_HV.Draw("same")
fit_reg_HV.Draw("same")
histo_reg_ttH.Draw("same")
fit_reg_ttH.Draw("same")
leg.Draw("same")
c1.Update()
line = ROOT.TLine(1,0,1,c1.GetUymax())
line.SetLineWidth(1)
line.SetLineStyle(2)
line.SetLineColor(ROOT.kBlack)
line.Draw("same")

c1.Update()

c1.Print("compreg.pdf","title")

raw_input("Press ret")
