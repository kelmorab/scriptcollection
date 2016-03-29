import ROOT
from rootutils import PDFPrinting


ROOT.gROOT.SetBatch(True)
path1 = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0317_testing/output/"

inputfile = ROOT.TFile(path1+"script_1200_0.1_5_30.root")
outputname = "fastplots"


tree = inputfile.Get("TestTree")

regpt = "BDTG"
partonpt = "Jet_PartonPt"

resprereg = ROOT.TH2F("resprereg","resprereg",100,0,300,100,-1,1)
respostreg = ROOT.TH2F("respostreg","respostreg",100,0,300,100,-1,1)

resprereg_mt = ROOT.TH2F("resprereg_mt","resprereg_mt",100,0,300,100,-1,1)
respostreg_mt = ROOT.TH2F("respostreg_mt","respostreg_mt",100,0,300,100,-1,1)

ptoverregpt = ROOT.TH2F("ptoverregpt","ptoverregpt",100,0,300,100,0,300)
mtoverregpt = ROOT.TH2F("mtoverregpt","mtoverregpt",100,0,300,100,0,300)
leadtrackoverregpt = ROOT.TH2F("leadtrackoverregpt","leadtrackoverregpt",50,0,100,100,0,300)
chmultoverregpt = ROOT.TH2F("chmultoverregpt","chmultoverregpt",50,1,51,100,0,300)

partonoverpt = ROOT.TH2F("partonoverpt","partonoverpt",100,0,300,100,0,300)
partonovermt = ROOT.TH2F("partonovermt","partonovermt",100,0,300,100,0,300)
partonovereta = ROOT.TH2F("partonovereta","partonovereta",100,0,300,50,-2.5,2.5)
partonoverchmult = ROOT.TH2F("partonoverchmult","partonoverchmult",100,0,300,50,1,51)
partonoverleadtrack = ROOT.TH2F("partonoverleadtrack","partonoverleadtrack",100,0,300,50,0,100)

histolist = [resprereg,respostreg,resprereg_mt,respostreg_mt,ptoverregpt,mtoverregpt,leadtrackoverregpt,chmultoverregpt,partonoverpt,partonovermt,partonovereta,partonoverchmult,partonoverleadtrack]



tree.Project("resprereg","(Jet_PartonPt - Jet_Pt)/Jet_Pt:Jet_Pt","","") 
tree.Project("respostreg","(Jet_PartonPt - "+regpt+")/"+regpt+":"+regpt,"","") 

tree.Project("resprereg_mt","(Jet_PartonPt - Jet_Pt)/Jet_Pt:Jet_Mt","","") 
tree.Project("respostreg_mt","(Jet_PartonPt - "+regpt+")/"+regpt+": Jet_Mt","","") 

tree.Project("ptoverregpt",regpt+":Jet_Pt","","")
tree.Project("mtoverregpt",regpt+":Jet_Mt","","")
tree.Project("leadtrackoverregpt",regpt+":Jet_leadTrackPt","","")
tree.Project("chmultoverregpt",regpt+":Jet_chargedMult","","")

tree.Project("partonoverpt","Jet_Pt :"+partonpt,"","")
tree.Project("partonovermt","Jet_Mt :"+partonpt,"","")
tree.Project("partonovereta","Jet_Eta :"+partonpt,"","")
tree.Project("partonoverchmult","Jet_chargedMult : "+partonpt,"","")
tree.Project("partonoverleadtrack","Jet_leadTrackPt:"+partonpt,"","")


pdfout = PDFPrinting(outputname)
outputfile = ROOT.TFile(outputname+".root","RECREATE")
outputfile.cd()
c1 = ROOT.TCanvas()    
c1.cd()


for histo in histolist:
    histo.Draw("colz")
    c1.Update
    pdfout.addCanvastoPDF(c1)


pdfout.closePDF()
