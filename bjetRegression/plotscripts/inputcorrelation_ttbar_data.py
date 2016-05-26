import ROOT
import itertools
from rootutils import PDFPrinting
myrnd = ROOT.TRandom3()

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)

rootpath = "/nfs/dust/cms/user/kschweig/JetRegression/"

sel_singleel="(N_LooseMuons==0) && (Jet_regPt > 0)"

input_data = rootpath+"trees0418/mu.root"
input_ttbar = rootpath+"trees0413/ttbar_nominal.root"

inputs = [input_data, input_ttbar]

inputvariables = ["Jet_Pt","Jet_Mt","Jet_Eta","Jet_leadTrackPt","Jet_corr","Jet_leptonPt","Jet_leptonPtRel","Jet_leptonDeltaR","Jet_totHEFrac","Jet_nEmEFrac","Jet_vtxPt","Jet_vtx3DVal","Jet_vtx3DSig","Jet_vtxMass","Jet_vtxNtracks","N_PrimaryVertices"]

inputbinning = {"Jet_Pt":[200,0,600],
                "Jet_Mt":[200,0,600],
                "Jet_Eta":[50,-2.5,2.5],
                "Jet_leadTrackPt":[50,0,150],
                "Jet_corr":[100,0.8,1.2],
                "Jet_leptonPt":[60,0,120],
                "Jet_leptonPtRel":[20,0,30],
                "Jet_leptonDeltaR":[20,0,0.5],
                "Jet_totHEFrac":[20,0,1],
                "Jet_nEmEFrac":[20,0,1],
                "Jet_vtxPt":[20,0,100],
                "Jet_vtx3DVal":[30,0,15],
                "Jet_vtx3DSig":[50,0,200],
                "Jet_vtxMass":[14,0,7],
                "Jet_vtxNtracks":[13,-0.5,12.5],
                "N_PrimaryVertices":[26,-.5,25.5],
                "Jet_leptonEta": [50,-2.5,2.5] }

c1 = ROOT.TCanvas()
c1.cd()
        
postfix = "regressed_"

inputcombinations = itertools.combinations(inputvariables,2)
inputfile_data = ROOT.TFile(input_data)
inputfile_ttbar = ROOT.TFile(input_ttbar)


pdfout_data = PDFPrinting("output_"+postfix+str(input_data.split("/")[-1])[0:-5])    
outputfile_data = ROOT.TFile("output_"+postfix+str(input_data.split("/")[-1]),"RECREATE")

pdfout_ttbar = PDFPrinting("output_"+postfix+str(input_ttbar.split("/")[-1])[0:-5])    
outputfile_ttbar = ROOT.TFile("output_"+postfix+str(input_ttbar.split("/")[-1]),"RECREATE")

pdfout_scatter = PDFPrinting("output_"+postfix+(str(input_ttbar.split("/")[-1])[0:-5])+"_"+(str(input_data.split("/")[-1])[0:-5]))


tree_data = inputfile_data.Get("MVATree")
tree_ttbar = inputfile_ttbar.Get("MVATree")

mcweight="(Evt_Odd == 0) * 2 * 2.68 * Weight_PU && (Jet_regPt > 0)"

for comb in inputcombinations:
    var0 = comb[0]
    var1 = comb[1]

    rannum_data = ROOT.gRandom.Integer(10000)
    rannum_ttbar = ROOT.gRandom.Integer(10000)

    htmp_data = ROOT.TH2F(str(rannum_data),var0+"_"+var1+str(rannum_data),inputbinning[var0][0],inputbinning[var0][1],inputbinning[var0][2],inputbinning[var1][0],inputbinning[var1][1],inputbinning[var1][2])
    htmp_ttbar = ROOT.TH2F(str(rannum_ttbar),var0+"_"+var1+str(rannum_ttbar),inputbinning[var0][0],inputbinning[var0][1],inputbinning[var0][2],inputbinning[var1][0],inputbinning[var1][1],inputbinning[var1][2])


    tree_data.Project(str(rannum_data),var1+":"+var0,"")
    tree_ttbar.Project(str(rannum_ttbar),var1+":"+var0,mcweight)
    
    htmp_data.GetXaxis().SetTitle(var0)
    htmp_data.GetYaxis().SetTitle(var1)
    htmp_data.Draw("colz")
    c1.Update()
    pdfout_data.addCanvastoPDF(c1)
    outputfile_data.cd()
    htmp_data.Write()

    htmp_ttbar.GetXaxis().SetTitle(var0)
    htmp_ttbar.GetYaxis().SetTitle(var1)
    htmp_ttbar.Draw("colz")
    c1.Update()
    pdfout_ttbar.addCanvastoPDF(c1)
    outputfile_ttbar.cd()
    htmp_ttbar.Write()

    htmp_data.SetMarkerColor(ROOT.kRed)
    htmp_data.Draw()
    htmp_ttbar.Draw("same")
    c1.Update()
    pdfout_scatter.addCanvastoPDF(c1)

    del htmp_data,htmp_ttbar

pdfout_data.closePDF()
pdfout_ttbar.closePDF()
pdfout_scatter.closePDF()

