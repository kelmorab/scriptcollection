#Usage 

import ROOT

ROOT.gStyle.SetOptStat(0);
ROOT.gROOT.SetBatch(True)


class sampleClass:
    def __init__ (self, sample):
        self.title = sample[0]
        self.color = sample[1]
        self.tfile = ROOT.TFile(str(sample[2]))
        self.ttree = self.tfile.Get(sample[3])

def plot1(nameprefix,plotvar,htitle,nbins,binbegin,binend,selection,samples):
    histos = []
    print samples
    for isample, sample in enumerate(samples):
        print "projecting sample",sample
        tmphisto = ROOT.TH1F(nameprefix+str(isample),htitle,nbins,binbegin,binend)
        tmphisto.SetLineColor(sample.color)
        sample.ttree.Project(tmphisto.GetName(),plotvar,selection)
        histos.append(tmphisto)
        del tmphisto
    print histos
    return histos


def drawline(x1,y1,x2,y2,width,color):
    line = ROOT.TLine(x1,y1,x2,y2)
    line.SetLineWidth(width)
    line.SetLineColor(color)
    line.Draw()
    


input_sample_noreg = ["ttbar niminal",ROOT.kBlack,"/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_nominal.root","MVATree"]

input_samples_reg=[["ttbar new Training 1",ROOT.kRed,"/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_evalbReg_nominal.root","bRegTree"],
                   ["ttbar new Training 2",ROOT.kGreen+3,"/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_bRegTree_0125_nominal.root","bRegTree"],
                   ["ttbar HV Training",ROOT.kBlue,"/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_nominal.root","MVATree"]]

outputfile = ROOT.TFile("compare_training-2.root","RECREATE")

sample_noreg = [sampleClass(input_sample_noreg)]
#print sample_noreg.tfile.Get("MVATree")
print sample_noreg[0].ttree
samples_reg = []
for input_sample in input_samples_reg:
    samples_reg.append(sampleClass(input_sample))


# define: [plotvar,histname, bin, binbegin, binend, selection, samples]
plots = [["Jetregpt_","Jet_regPt","p_T of b-Jets",200,0,400,"abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5",samples_reg],
         ["Jet_corr_","Jet_regPt/Jet_Pt","b-Jet Regession correction factor",40,0.6,1.6,"abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5",samples_reg],
         ["Jet_regpt-Ppt_","Jet_regPt/Jet_PartonPt","corrected b-Jet p_{T} / b-Quark p_{T}",70,0.2,1.8,"abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5",samples_reg],
         ["Jetpt_","Jet_Pt","p_T of b-Jets",200,0,400,"abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5",sample_noreg],
         ["Jet_pt-Ppt_","Jet_Pt/Jet_PartonPt","b-Jet p_{T} / b-Quark p_{T}",70,0.2,1.8,"abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5", sample_noreg]]



c1 = ROOT.TCanvas()

histoplots = []

outputfile.cd()

for plot in plots:
    histoplots.append(plot1(plot[0],plot[1],plot[2],plot[3],plot[4],plot[5],plot[6],plot[7]))

         
histoplots[0][0].Draw("histoe")
histoplots[0][1].Draw("same histoe")
histoplots[3][0].Draw("same histoe")

c1.Update()

c1.Write()

#raw_input("press ret")

histoplots[1][0].Draw("histoe")
histoplots[1][1].Draw("same histoe")

c1.Update()

c1.Write()

#raw_input("press ret")
drawopt = "histoe"
for i in range(len(plots[2][7])):
    print histoplots[2][i].GetName()
    histoplots[2][i].Draw(drawopt)
    if i == 0:
        histoplots[2][i].SetLineWidth(3)
    if drawopt == "histoe":
        drawopt = "same "+drawopt
histoplots[4][0].Draw(drawopt)
c1.Update()
#drawline(1,0,1,2000000,3,ROOT.kBlack)


line = ROOT.TLine(1,0,1,c1.GetUymax())
line.SetLineWidth(1)
line.SetLineStyle(2)
line.SetLineColor(ROOT.kBlack)
line.Draw("same")
c1.Update()

c1.Write()

#raw_input("press ret")

