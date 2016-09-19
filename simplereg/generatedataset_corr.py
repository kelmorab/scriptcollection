###################################################################################################################
#-----------------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------------# 
# Script for generating datasets for testing multivariate regression on a based on morphed gaussian distributions #
#-----------------------------------------------------------------------------------------------------------------# 
#            >>>>>>>> usage: python generatedataset_corr.py [outputname] [nEvents] <<<<<<<<                       #
#-----------------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------------#
###################################################################################################################
import ROOT
import sys
import math
from array import array

myrnd = ROOT.TRandom3()

nEvt = int(sys.argv[2])

#create outputfile
outputfile = ROOT.TFile(str(sys.argv[1])+".root","RECREATE")
outputfile.cd()

tree = ROOT.TTree("MVATree","MVATree")


#Regression Inputs
var0 = array("f",[0])
var1 = array("f",[0])
var2 = array("f",[0])
var3 = array("f",[0])
var4 = array("f",[0])
var5 = array("f",[0])
var6 = array("f",[0])
#Regression targets
target = array("f",[0])
var0_smearing_upup = array("f",[0])
var0_smearing_up = array("f",[0])
var0_smearing_down = array("f",[0])
var0_smearing_downdown = array("f",[0])
var0_offset_upup = array("f",[0])
var0_offset_up = array("f",[0])
var0_offset_down = array("f",[0])
var0_offset_downdown = array("f",[0])
#Misc
Evt_Odd = array("i",[0])
#Morphed variables
var3_morphed = array("f",[0])
var4_morphed = array("f",[0])
#Setting up tree

tree.Branch("target",target,"target/f")
tree.Branch("var1",var1,"var1/f")
tree.Branch("var2",var2,"var2/f")
tree.Branch("var3",var3,"var3/f")
tree.Branch("var4",var4,"var6/f")
tree.Branch("var5",var4,"var6/f")
tree.Branch("var0",var0,"var0/f")
tree.Branch("var0_smearing_upup",var0_smearing_upup,"var0 uni up/f")
tree.Branch("var0_smearing_up",var0_smearing_up,"var0 uni up/f")
tree.Branch("var0_smearing_down",var0_smearing_down,"var0 uni down/f")
tree.Branch("var0_smearing_downdown",var0_smearing_downdown,"var0 uni down/f")
tree.Branch("var0_offset_upup",var0_offset_upup,"var0 gaus up/f")
tree.Branch("var0_offset_up",var0_offset_up,"var0 gaus up/f")
tree.Branch("var0_offset_down",var0_offset_down,"var0 gaus down/f")
tree.Branch("var0_offset_downdown",var0_offset_downdown,"var0 gaus down/f")

tree.Branch("Evt_Odd",Evt_Odd,"evt_odd/i")

odd = 0
for iev in range(nEvt):
    #Generate random variables
    target[0] = ROOT.gRandom.Gaus(1,0.5) #Basic Gaus shape
    var1[0] = ROOT.gRandom.Uniform(-0.5,0.5) #Smearing 
    var2[0] = ROOT.gRandom.Uniform(0.5) #Offset
    #var3[0] = ROOT.gRandom.Uniform(-2,2) #Uniform smearing for correlation study
    #var4[0] = ROOT.gRandom.Gaus(2,0.75) #Gaussion peak for correlation study

    
    #Compute morphed dist.
    xtile = 1.5
    var0[0] = (target[0]+xtile*var1[0])+var2[0] #Target for inputvariables study
    var4[0] = (target[0]+xtile*var1[0]) #Target for inputvariables study
    var5[0] = (target[0])+var2[0] #Target for inputvariables study


    # ------------------------------------------------------------------------------
    # ----------------- Targets for correlation study ------------------------------
    xshift = 0.5
    var0_smearing_upup[0] = ( target[0]+((xtile + 1.5*xshift)*var1[0]) ) + var2[0]
    var0_smearing_up[0] = ( target[0]+((xtile + xshift)*var1[0]) ) + var2[0] 
    var0_smearing_down[0] = ( target[0]+((xtile - xshift)*var1[0]) ) + var2[0]
    var0_smearing_downdown[0] = ( target[0]+((xtile - 1.5*xshift)*var1[0]) ) + var2[0]
    # -----------------------------------------------------------------------------
    var0_offset_upup[0] = ( target[0]+(0.5*var1[0]) ) + ( 1.75 * var2[0] )
    var0_offset_up[0] = ( target[0]+(0.5*var1[0]) ) + ( 1.5 * var2[0] )
    var0_offset_down[0] = ( target[0]+(0.5*var1[0]) ) + ( 0.5 * var2[0] )
    var0_offset_downdown[0] = ( target[0]+(0.5*var1[0]) ) + ( 0.25 * var2[0] )
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    Evt_Odd[0] = odd
    if odd == 0:
        odd = 1
    else:
        odd = 0

    var = -10
    while var == -10:
        var = ROOT.gRandom.Gaus(0,4)
        if var > -1 and var < 1:
            var3[0] = var
        else:
            var = -10
            
    tree.Fill()


tree.Write()    
