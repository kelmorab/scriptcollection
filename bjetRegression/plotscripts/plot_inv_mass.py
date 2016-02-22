import ROOT
from rootutils import PDFPrinting
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0);

isttH = False
german = False
leptons = "two" # all, two, one, none

if isttH:
    inputfile1 = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0218/ttHbb.root")
else:
    inputfile1 = ROOT.TFile("/nfs/dust/cms/user/kschweig/JetRegression/trees0214/ttbar.root")

tree1 = inputfile1.Get("MVATree")

if isttH:
    histo_noreg = ROOT.TH1F("noreg","bbMass_noreg",125,50,250)
    histo_noreg.Sumw2()
    histo_reg = ROOT.TH1F("reg","bbMass_reg",125,50,250)
    histo_reg.Sumw2()
else:
    histo_noreg = ROOT.TH1F("noreg","hadtopmass_noreg",150,100,300)
    histo_noreg.Sumw2()
    histo_reg = ROOT.TH1F("reg","hadtopmass_reg",150,100,300)
    histo_reg.Sumw2()


if isttH:
    pdfout = PDFPrinting("bbMass_ger_"+leptons)
else:
    pdfout = PDFPrinting("thadMass")

c1 = ROOT.TCanvas()

selection_Odd = "Evt_Odd == 0"
if leptons is "all":
    selection_ttH = "Evt_bbMass > 0"
elif leptons is "two":
    selection_ttH = "Evt_bbMass2Lep > 0"
elif leptons is "one":
    selection_ttH = "Evt_bbMass1Lep > 0"
elif leptons is "none":
    selection_ttH = "Evt_bbMass0Lep > 0"
else:
    print "error with leptons"
    exit()

selection_ttbar = "Evt_hadtopmass > 0"


selection = "1"
if isttH:
    selection = selection+ " && "+selection_ttH
    if leptons is "all":
        variable_noreg = "Evt_bbMass"
        variable_reg = "Evt_regbbMass"
    elif leptons is "two":
        variable_noreg = "Evt_bbMass2Lep"
        variable_reg = "Evt_regbbMass2Lep"
    elif leptons is "one":
        variable_noreg = "Evt_bbMass1Lep"
        variable_reg = "Evt_regbbMass1Lep"
    elif leptons is "none":
        variable_noreg = "Evt_bbMass0Lep"
        variable_reg = "Evt_regbbMass0Lep"

else:
    selection = selection+ " && "+selection_Odd+" && "+selection_ttbar
    variable_noreg = "Evt_hadtopmass"
    variable_reg = "Evt_reghadtopmass"


print "Projecting to noreg" 
tree1.Project("noreg",variable_noreg,selection)
print "Projecting to  reg" 
tree1.Project("reg",variable_reg,selection)

histo_noreg.SetLineColor(ROOT.kBlue)
histo_noreg.SetLineWidth(1)
histo_noreg.Scale(1/float(histo_noreg.Integral()))
#histo_noreg.SetLineColor(ROOT.kBlue)
histo_reg.SetLineColor(ROOT.kRed)
histo_reg.SetLineWidth(1)
histo_reg.Scale(1/float(histo_reg.Integral()))
dofit = True


if dofit:
    if isttH:
        noreg_left = 90
        noreg_right = 142
        reg_left = 100
        reg_right = 150
    else:
        noreg_left = 145
        noreg_right = 195
        reg_left = 155
        reg_right = 200

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


    histo_noreg.Fit("Fit_noreg","","",noreg_left,noreg_right)
    histo_reg.Fit("Fit_reg","","",reg_left,reg_right)


leg=ROOT.TLegend(0.55,0.45,0.89,0.89)
if german:
    leg.AddEntry(histo_noreg,"Vor Regression")    
else:
    leg.AddEntry(histo_noreg,"Before Regression")
if dofit:
    leg.AddEntry(0,"Fit: #mu="+str(fit_noreg.GetParameter(1))[:6]+"#pm"+str(fit_noreg.GetParError(1))[:6],"")
    leg.AddEntry(0,"     #sigma="+str(fit_noreg.GetParameter(2))[:6]+"#pm"+str(fit_noreg.GetParError(2))[:6],"")
if german:
    leg.AddEntry(histo_reg,"Nach Regression")
else:
    leg.AddEntry(histo_reg,"After Regression")
if dofit:
    leg.AddEntry(0,"Fit: #mu="+str(fit_reg.GetParameter(1))[:6]+"#pm"+str(fit_reg.GetParError(1))[:6],"")
    leg.AddEntry(0,"     #sigma="+str(fit_reg.GetParameter(2))[:6]+"#pm"+str(fit_reg.GetParError(2))[:6],"")


#histo_noreg.GetYaxis().SetRangeUser(0,)


simul = ROOT.TLatex(0.125, 0.908, 'CMS simulation')
simul.SetTextFont(42)
simul.SetTextSize(0.045)
simul.SetNDC()

cms = ROOT.TLatex(0.125, 0.86, 'work in progress')
cms.SetTextFont(42)
cms.SetTextSize(0.045)
cms.SetNDC()
if isttH:
    label = ROOT.TLatex(0.6275,0.908, 'Sample: t#bar{t}H , H #rightarrow b#bar{b}')
else:
    label = ROOT.TLatex(0.77,0.908, 'Sample: t#bar{t}')
label.SetTextFont(42)
label.SetTextSize(0.045)
label.SetNDC()

histo_reg.Draw("histoe")
#Make Style
histo_reg.SetTitle("")
if isttH:
    histo_reg.GetXaxis().SetTitle("m(H #rightarrow b#bar{b}) (GeV)")
    histo_reg.GetYaxis().SetTitleOffset(0.9)
    histo_reg.GetXaxis().SetTitleOffset(0.7)
else:
    histo_reg.GetXaxis().SetTitle("m(t_{had}) (GeV)")   
    histo_reg.GetYaxis().SetTitleOffset(0.9)
    histo_reg.GetXaxis().SetTitleOffset(0.75)

histo_reg.GetXaxis().SetTitleSize(0.05)
if german:
    histo_reg.GetYaxis().SetTitle("Beliebige Einheiten")
else:
    histo_reg.GetYaxis().SetTitle("arbitrary units")

histo_reg.GetYaxis().SetTitleSize(0.05)
histo_reg.GetYaxis().SetRangeUser(0,histo_reg.GetBinContent(histo_reg.GetMaximumBin())*1.1)



histo_noreg.Draw("same histoe")

if dofit:
    fit_noreg.Draw("same")
    fit_reg.Draw("same")
leg.Draw("same")
cms.Draw("same")
simul.Draw("same")
label.Draw("same")
c1.Update()



drawLine = False
if drawLine:
    line = ROOT.TLine(1,0,1,c1.GetUymax())
    line.SetLineWidth(1)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("same")


c1.Update()

pdfout.addCanvastoPDF(c1)

pdfout.closePDF()
#raw_input("Press ret")
