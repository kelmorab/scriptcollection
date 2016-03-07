import ROOT

def computeMutualInfo( TH2F ):
    
    integral = TH2F.Integral()
    if integral == 0:
        return -1
        
    h = ROOT.TH2F(TH2F)

    h.RebinX(2);
    h.RebinY(2);

    mutualinfo = 0
    maxBinX = h.GetNbinsX()
    maxBinY = h.GetNbinsY()
    for x in range(maxBinX+1):
        for y in range(maxBinY+1):
            pxy = h.GetBinContent(x,y)/integral
            px = h.Integral(x,x,1,maxBinY)/integral
            py = h.Integral(1,maxBinX,y,y)/integral
            if px > 0 and py > 0 and pxy > 0:
                mutualinfo = mutualinfo + pxy * ROOT.TMath.Log( pxy / (px*py))

    return mutualinfo
