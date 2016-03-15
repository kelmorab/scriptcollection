from __future__ import division

import ROOT
from math import sqrt



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

def getIntegralDiviation( h1, h2 ):
    i1 = h1.Integral()
    i2 = h2.Integral()
    div = i1 - i2
    if div < 0:
        div = i2 - i1
    return div


def getBinnedDiviation( h1, h2 ):
    nb1 = h1.GetXaxis().GetNbins()
    nb2 = h2.GetXaxis().GetNbins()
    if nb1 != nb2:
        print "h1 and h2 don't have same number of bins"
        exit()
    divs = []
    for b in range(nb1):
        h1bc = h1.GetBinContent(b)
        h2bc = h2.GetBinContent(b)
        if h1bc != 0:
            div =  (h1bc-h2bc)/h1bc
        else:
            div = 0
        #print h1bc,h2bc, div 
        divs.append(div)
    sum_ = 0
    #print divs
    for e in range(len(divs)):
        #print sum_
        sum_ = sum_ + divs[e] 
    print "Average binned Diviation:",sum_/float(len(divs))

def runtest( h1, h2 ):
    nb1 = h1.GetXaxis().GetNbins()
    nb2 = h2.GetXaxis().GetNbins()
    if nb1 != nb2:
        print "h1 and h2 don't have same number of bins"
        exit()
    maxup = 0
    maxdown = 0.1
    nfluc = 0
    ldiv = 0
    a = False
    b = False
    lasta = False
    lastb = False
    na = 0
    nb = 0
    r = 0
    n = 0
    for b in range(nb1):
        h1bc = h1.GetBinContent(b)
        h2bc = h2.GetBinContent(b)        
        n = n + 1
        if h2bc < h1bc: 
            b = True
            a = False
            if lastb != b:
                r = r + 1
        elif h2bc >= h1bc:
            b = False
            a = True
            if lasta != a:
                r = r + 1
        if a:
            na = na + 1
        elif b:
            nb = nb + 1
        lasta = a
        lastb = b

        div = h1bc-h2bc
        if (div < 0 and ldiv > 0) or (div > 0 and ldiv < 0):
            nfluc = nfluc + 1
        if div >= maxup:
            maxup = div
        if div <= maxdown:
            maxdown = div
        ldiv = div
    r_exp = 1+((2*na*nb)/(na+nb))
    var_r = (((r_exp - 1)*(r_exp - 2))/(float(na+nb-1)))
    sig_r = sqrt(var_r)
    print "Max upward fluctuation:",maxup
    print "Max downward fluctuation:",maxdown
    print "r_obs:",r,"r_exp:",r_exp
    print "r diviation:",(abs(r-r_exp)/sig_r),"sigma"


def getChi2( h1, h2 ):
    return h1.Chi2Test(h2)


def getKSvalue( h1, h2 ):
    KSvalue = h1.KolmogorovTest(h2)
    return KSvalue

def getDiviationtests( h1, h2 , doint = True, dobinned = True, doKS = True, dochi2 = False):
    print "\n\n"
    print "Printing Regression Diviations:"
    if doint:
        print "Diviation of Integrals:",getIntegralDiviation( h1, h2 )
    if dobinned:
        getBinnedDiviation( h1, h2 )
    if dochi2:
        print "Chi2 test value:",getChi2( h1, h2 )
    if doKS:
        print "KS-Value:", getKSvalue( h1, h2 )
        print "KS-Value:", getKSvalue( h2, h1 )
    runtest( h1, h2 )


class Errors():
    def __init__(self, useloss = ["squared","abs"]):
        self.squaredtesterr = 0
        self.abstesterr = 0
        self.nabs = 0
        self.nsquared = 0
        self.RSS = 0
        self.TSS = -1
        self.R2 = -1
        self.abssum = 0
        self.eventvals = []
        if "squared" in useloss:
            self.usesquared = True
        else:
            self.usesquared = False
        if "abs" in useloss:
            self.useabs = True
        else:
            self.useabs = False
        
    def computeloss(self,x,y,func):
        if func == "squared":
            self.RSS = self.RSS + (y-x)*(y-x)
            self.nsquared = self.nsquared + 1 
        if func == "abs":
            self.abssum = self.abssum + abs(y-x)
            self.nabs = self.nabs + 1

    def addevent(self,x,y):
        self.eventvals.append([x,y])
        if self.usesquared:
            self.computeloss(x,y,"squared")
        if self.useabs:
            self.computeloss(x,y,"abs")
    
    def geteventmean(self):
        x_mean = 0
        y_mean = 0
        for i in range(len(self.eventvals)):
            x_mean = x_mean + self.eventvals[i][0]
            y_mean = y_mean + self.eventvals[i][1]
        x_mean = x_mean / len(self.eventvals)
        y_mean = y_mean / len(self.eventvals)
        return x_mean, y_mean

    def computeerr(self,lossfunc = ["squared","abs"]):
        if "squared" in lossfunc:
            self.squaredtesterr = (1/self.nsquared)*self.RSS
        if "abs" in lossfunc:
            self.abstesterr = (1/self.nabs)*self.abssum
    
    def computeTSS(self):
        x_mean, y_mean = self.geteventmean()
        tmp_sum = 0
        for i in range(len(self.eventvals)):
            tmp_sum = tmp_sum + ((self.eventvals[i][1] - y_mean)*(self.eventvals[i][1] - y_mean))
        self.TSS = tmp_sum

    def calculateR2(self):
        self.computeTSS()
        self.R2 = 1 - (self.RSS/self.TSS)

    def printerr(self, lossfunc = ["squared","abs"]):
        if "squared" in lossfunc:
            self.computeTSS()
            self.calculateR2()
            print "Residual sum of squares (RSS):",self.RSS
            print "Residual standard error (RSE):",sqrt((1/(self.nsquared - 2)) * self.RSS)
            print "Total sum of squares (TSS)   :",self.TSS
            print "R^2 statistic                :",self.R2
            print "Error with squared Error loss function:",self.squaredtesterr
        if "abs" in lossfunc:
            print "Error with absolute Error loss function:",self.abstesterr
