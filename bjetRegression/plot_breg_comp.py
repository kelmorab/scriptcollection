import ROOT
#ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);


inputfile = ROOT.TFile("testtrees/jetreg_0112_2_nominal_Tree.root")

tree = inputfile.Get("MVATree")

histo_noreg = ROOT.TH1F("noreg","Jet p_{T}/Parton p_{T}",70,0.2,1.8)
histo_reg = ROOT.TH1F("reg","Jet p_{T}/p_{T, parton}",70,0.2,1.8)

c1 = ROOT.TCanvas()

tree.Project("noreg","Jet_Pt/Jet_PartonPt","abs(Jet_PartonFlav) == 5 && abs(Jet_Flav) == 5")
tree.Project("reg","Jet_regPt/Jet_PartonPt","abs(Jet_PartonFlav) == 5 && abs(Jet_Flav) == 5")

histo_noreg.SetLineColor(ROOT.kBlue)
histo_reg.SetLineColor(ROOT.kRed)

fit_noreg = ROOT.TF1("Fit_noreg","gaus",0.8,1.1)
fit_noreg.SetParameter(0,1)
fit_noreg.SetParameter(1,1)
fit_noreg.SetParameter(2,1.5)
fit_noreg.SetLineWidth(2)
fit_noreg.SetLineColor(ROOT.kBlue)
fit_reg = ROOT.TF1("Fit_reg","gaus",0.85,1.135)
fit_reg.SetParameter(0,1)
fit_reg.SetParameter(1,1)
fit_reg.SetParameter(2,1.5)
fit_reg.SetLineWidth(2)
fit_reg.SetLineColor(ROOT.kRed)

histo_noreg.Fit("Fit_noreg","","",0.85,1.1)
histo_reg.Fit("Fit_reg","","",0.9,1.11)


leg=ROOT.TLegend(0.6,0.54,0.89,0.89)
leg.AddEntry(histo_noreg,"Before Regression")
leg.AddEntry(0,"Fit: #mu="+str(fit_noreg.GetParameter(1))[:6]+"#pm"+str(fit_noreg.GetParError(1))[:6],"")
leg.AddEntry(0,"     #sigma="+str(fit_noreg.GetParameter(2))[:6]+"#pm"+str(fit_noreg.GetParError(2))[:6],"")
leg.AddEntry(histo_reg,"After Regression")
leg.AddEntry(0,"Fit: #mu="+str(fit_reg.GetParameter(1))[:6]+"#pm"+str(fit_reg.GetParError(1))[:6],"")
leg.AddEntry(0,"     #sigma="+str(fit_reg.GetParameter(2))[:6]+"#pm"+str(fit_reg.GetParError(2))[:6],"")

histo_noreg.GetYaxis().SetRangeUser(0,800)

histo_noreg.Draw()
fit_noreg.Draw("same")
histo_reg.Draw("same")
fit_reg.Draw("same")
leg.Draw("same")

c1.Update()

raw_input("Press ret")
