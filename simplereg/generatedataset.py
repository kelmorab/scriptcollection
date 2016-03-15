# python generatedataset.py outputname nEvents
import ROOT
import sys
from array import array

myrnd = ROOT.TRandom3()

nEvt = int(sys.argv[2])

#create outputfile
outputfile = ROOT.TFile(str(sys.argv[1])+".root","RECREATE")
outputfile.cd()


#Make tree for output
tree = ROOT.TTree("MVATree","MVATree")
var0 = array("f",[0])
var1 = array("f",[0])
var2 = array("f",[0])
var3 = array("f",[0])
var4 = array("f",[0])
target = array("f",[0])
Evt_Odd = array("i",[0])

tree.Branch("var0",var0,"var0/f")
tree.Branch("var1",var1,"var1/f")
tree.Branch("var2",var2,"var2/f")
tree.Branch("var3",var3,"var3/f")
tree.Branch("var4",var4,"var4/f")
#tree.Branch("var5",var4,"var5/f")
#tree.Branch("var6",var4,"var6/f")
tree.Branch("target",target,"target/f")
tree.Branch("Evt_Odd",Evt_Odd,"evt_odd/i")

scatter_0_target = ROOT.TH2F("th2f1","var0 vs. target",100,-1.2,1.2,100,-10,10)
scatter_0_1 = ROOT.TH2F("th2f3","var0 vs. var1",100,-1.2,1.2,100,-10,10)
scatter_1_target = ROOT.TH2F("th2f2","var1 vs. target",100,-10,10,100,-10,10)
histo1 = ROOT.TH1F("histo1","var0",100,-1,1)
histo2 = ROOT.TH1F("histo2","var1",100,-10,10)
histo3 = ROOT.TH1F("histo3","var2",100,-10,10)
histo5 = ROOT.TH1F("histo5","var3",100,-10,10)
histo6 = ROOT.TH1F("histo6","var4",100,-10,10)
#histo6 = ROOT.TH1F("histo6","var5",100,-10,10)
#histo6 = ROOT.TH1F("histo7","var6",100,-10,10)
histo4 = ROOT.TH1F("histo4","target",100,-10,10)


odd = 0
v1 = False
v2 = False
v3 = True
for i in range(nEvt):
    if v1:
        var0[0] = ROOT.gRandom.Uniform(-1,1)
        #var0[0] = ROOT.gRandom.Gaus(0,1)
        #while abs(var0[0]) > 1:
        #    var0[0] = ROOT.gRandom.Gaus(0,1)
        var2[0] = ROOT.gRandom.Gaus(6,1)
        target[0] = ROOT.gRandom.Gaus(1.,1.)
        var1[0] = target[0]+2*var0[0]
        #var1[0] = ROOT.gRandom.Gaus(1.+2*var0[0],1.)

    elif v2:
        target[0] = ROOT.gRandom.Gaus(1,0.5)
        var0[0] = ROOT.gRandom.Uniform(-1,1)
        #var2[0] = ROOT.gRandom.Uniform(-1,1)
        var2[0] = 0
        var1[0] = target[0]+0.5*var0[0]+1*var2[0]
    elif v3:
        target[0] = ROOT.gRandom.Gaus(1,0.5)
        var0[0] = ROOT.gRandom.Uniform(-1,1)
        var2[0] = ROOT.gRandom.Uniform(0.5,1)
        tmp0 = ROOT.gRandom.Uniform(0.8,1)
        tmp = ROOT.gRandom.Gaus(0,20)
        while abs(tmp) > 1:
            tmp = ROOT.gRandom.Gaus(0,20)
        var3[0] = var0[0] + (0.5 * tmp)
        if var2[0] < 0.75:
            var4[0] = var2[0] * tmp0
        else:
            var4[0] = var2[0] * tmp0
        #var2[0] = 1
        var1[0] = (target[0]+0.5*var0[0])+var2[0]
        
    Evt_Odd[0] = odd
    if odd == 0:
        odd = 1
    else:
        odd = 0
    #Fill plots
    scatter_0_target.Fill(var0[0],target[0])
    scatter_0_1.Fill(var0[0],var1[0])
    scatter_1_target.Fill(var1[0],target[0])
    histo1.Fill(var0[0])
    histo2.Fill(var1[0])
    histo3.Fill(var2[0])
    histo5.Fill(var3[0])
    histo6.Fill(var4[0])
    histo4.Fill(target[0])
    tree.Fill()


tree.Write()



#histo2.Add(histo3,1)


c1 = ROOT.TCanvas("c1","c1",600,900)
c1.Divide(3,2)
c1.cd(1)

scatter_0_target.Draw("colz")

c1.cd(2)

scatter_1_target.Draw("colz")

c1.cd(3)

scatter_0_1.Draw("colz")

c1.cd(4)

histo1.Draw()

c1.cd(5)

histo2.Draw()

c1.cd(6)

histo4.Draw()

#c1.Write()

raw_input("press ret")
