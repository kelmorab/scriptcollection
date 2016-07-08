import ROOT
from rootutils import PDFPrinting


ROOT.gROOT.SetBatch(True)
path1 = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/"

files = ["BReg_0329_newVars.root","BReg_0329_oldVars.root","BReg_0330_newVars.root","BReg_0330_oldVars.root"]
regpt_list = ["BDTG","BDTG","BDTG * Jet_Pt","BDTG * Jet_Pt"]
target_list = ["Jet_MatchedPartonPt","Jet_MatchedPartonPt","Jet_MatchedPartonPt_D_Jet_Pt","Jet_MatchedPartonPt_D_Jet_Pt"]

binning_outputdiv_target = [[250,0,700],[250,0,700],[150,0,4.6],[150,0,4.5]]
binning_outputdiv_div = [[400,-400,300],[400,-400,300],[200,-4,0.7],[200,-4,0.7]]

binning_outputdiv_zoom_target = [[100,30,150],[100,30,150],[100,0.6,1.5],[100,0.6,1.5]]
binning_outputdiv_zoom_div = [[100,-50,50],[100,-50,50],[100,-0.4,0.4],[100,-0.4,0.4]]


for i,f in enumerate(files):
    inputfile = ROOT.TFile(path1+f)
    outputname = "fastplots_"+str(i)
    
    regpt = regpt_list[i]
    target = target_list[i]

    tree = inputfile.Get("TestTree")

    regpt = regpt_list[i]
    partonpt = "Jet_MatchedPartonPt"

    resprereg = ROOT.TH2F("resprereg","resprereg",100,0,300,100,-1,1)
    respostreg = ROOT.TH2F("respostreg","respostreg",100,0,300,100,-1,1)
    outputdif_full = ROOT.TH2F("outputdif_full","outputdif_full",binning_outputdiv_target[i][0],binning_outputdiv_target[i][1],binning_outputdiv_target[i][2],binning_outputdiv_div[i][0],binning_outputdiv_div[i][1],binning_outputdiv_div[i][2])
    outputdif_zoom = ROOT.TH2F("outputdif_zoom","outputdif_zoom",binning_outputdiv_zoom_target[i][0],binning_outputdiv_zoom_target[i][1],binning_outputdiv_zoom_target[i][2],binning_outputdiv_zoom_div[i][0],binning_outputdiv_zoom_div[i][1],binning_outputdiv_zoom_div[i][2])



    histolist = [resprereg,respostreg,outputdif_full,outputdif_zoom]



    tree.Project("resprereg","(Jet_MatchedPartonPt - Jet_Pt)/Jet_Pt:Jet_Pt","","") 
    tree.Project("respostreg","(Jet_MatchedPartonPt - ("+regpt+"))/("+regpt+"):("+regpt+")","","") 
    tree.Project("outputdif_full","( BDTG - "+target+") : "+target,"","")
    tree.Project("outputdif_zoom","( BDTG - "+target+") : "+target,"","")



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

    del histolist,resprereg,respostreg,outputdif_full,outputdif_zoom,inputfile,tree,pdfout
