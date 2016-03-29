from __future__ import division

import ROOT
from math import sqrt




class Tests():
    def __init__(self):
        #Set variables
        self.mutualinfo = -1
        self.avbinneddiv = 0
        self.maxupabs = 0
        self.maxuppercent = 0
        self.maxdownabs = 0
        self.maxdownpercent = 0
        self.r_exp = 0
        self.r = 0
        self.r_div_sig = 0
        self.chi2 = 0
        self.KS = 0
        self.testdone = False

    def computeMutualInfo(self,  TH2F ):

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

        self.mutualinfo =  mutualinfo

    def getBinnedDiviation(self,  h1, h2 ):
        nb1 = h1.GetXaxis().GetNbins()
        nb2 = h2.GetXaxis().GetNbins()
        if nb1 != nb2:
            print "h1 and h2 don't have same number of bins"
            self.avbinneddiv = -1
            return False
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
        self.avbinneddiv = sum_/float(len(divs))
        return True

    def doruntest(self, h1, h2 ):
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

            div = h2bc-h1bc
            if h1bc == 0:
                h1bc_ = 1
            else:
                h1bc_ = h1bc
            if (div < 0 and ldiv > 0) or (div > 0 and ldiv < 0):
                nfluc = nfluc + 1
            if div >= maxup:
                maxup = div
                maxuppercent = maxup/h1bc_
            if div <= maxdown:
                maxdown = div
                maxdownpercent = maxdown/h1bc_
            ldiv = div
        r_exp = 1+((2*na*nb)/(na+nb))
        var_r = (((r_exp - 1)*(r_exp - 2))/(float(na+nb-1)))
        sig_r = sqrt(var_r)
        self.maxupabs = maxup
        self.maxdownabs = maxdown
        self.maxuppercent = maxuppercent
        self.maxdownpercent = maxdownpercent
        self.r_exp = r_exp
        self.r = r
        self.r_div_sig = (abs(r-r_exp)/sig_r)

        """
        print "Max upward fluctuation:",maxup,", div from target:", maxuppercent
        print "Max downward fluctuation:",maxdown,", div from target:", maxdownpercent
        print "r_obs:",r,"r_exp:",r_exp
        print "r diviation:",(abs(r-r_exp)/sig_r),"sigma"
        """

    def getChi2(self,  h1, h2 ):
        self.chi2 =  h1.Chi2Test(h2)


    def getKSvalue(self,  h1, h2 ):
        KSvalue = h1.KolmogorovTest(h2)
        self.KS = KSvalue

    def runDiviationtests(self,  h1, h2 ):
        self.getBinnedDiviation( h1, h2 )    
        self.getChi2( h1, h2 )
        self.getKSvalue( h1, h2 )
        self.doruntest( h1, h2 )
        self.testdone = True
        
    def getvalues(self):
        return {"runtest-r" : self.r,
                "runtest-r_exp" : self.r_exp,
                "runtest-r_div_sig" : self.r_div_sig, 
                "max_div_abs_up" : self.maxupabs, 
                "max_div_abs_down" :self.maxdownabs, 
                "max_div_percent_up" : self.maxuppercent,
                "max_div_percent_down" : self.maxdownpercent,
                "chi2" : self.chi2,
                "KS" : self.KS,
                "Binned_div" : self.avbinneddiv,
                "mutualinfo" : self.mutualinfo}

    def getvaluenames(self):
        return ["runtest-r",
                "runtest-r_exp",
                "runtest-r_div_sig", 
                "max_div_abs_up", 
                "max_div_abs_down", 
                "max_div_percent_up",
                "max_div_percent_down",
                "chi2",
                "KS",
                "Binned_div",
                "mutualinfo"]

    def printtests(self, dobinned = True, doKS = True, dochi2 = False, doRun = True):
        if self.testdone:
            print "\n\n"
            print "Printing Regression Diviations:"
            if dobinned:
                print "Average binnend diviation:",self.avbinneddiv
            if dochi2:
                print "Chi2 test value:",self.chi2
            if doKS:
                print "KS-Value:", self.KS
            if doRun:
                print "Runtest:",self.r,"when",self.r_exp,"where expected ->",self.r_div_sig,"sigma diviation"
                print "Maximum upward fluctuation:  ",self.maxupabs,"->",self.maxuppercent
                print "Maximum downward fluctuation:",self.maxdownabs,"->",self.maxdownpercent
            if self.mutualinfo != -1:
                print "Mutual information:",self.mutualinfo
        else:
            print "Execute runDiviationtests() first!"


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

    def getvalues(self):
        return {"RSS" : self.RSS,
                "RSE" : (sqrt((1/(self.nsquared - 2)) * self.RSS)),
                "TSS" : self.TSS,
                "R^2" : self.R2,
                "err_squared_loss" : self.squaredtesterr,
                "err_abs_loss" : self.abstesterr }
        
    def getvaluenames(self):
       return ["RSS",
               "RSE",
               "TSS",
               "R^2",
               "err_squared_loss",
               "err_abs_loss"]
        



def writevaluetable(objdic, filename, sampleprefix, values = [] ):
    lines = []
    for key in objdic:
        valdic = objdic[key].getvalues()
        t = "&"
        for val in objdic[key].getvaluenames():
            if val in values or values[0] == "all":
                t = t + str(val) + " &"
        title = t[:-1]+"\\\\"
        l = str(key)+" & "
        for val in objdic[key].getvaluenames():
            if val in values or values[0] == "all":
                tmp =str(valdic[val])
                if not tmp.startswith(sampleprefix):
                    tmp = "\SI{"+tmp+"}{}"
                l = l + tmp +" &"
        lines.append(l[:-1]+"\\\\")
    with open(filename+'.txt', 'w') as f:
        f.write(title+"\n")
        for line in lines:
            f.write(line+"\n")
    f.close()
    out =[ filename,title+"\n"]+lines
    return out

def writevaluetopy(objdic, filename):
    lines = ["alldic = {"]
    samples = "samplelist = ["
    values = "vallist = ["
    valuesset = False
    for key in objdic:
        samples += '"'+str(key)+'",'
        valdic = objdic[key].getvalues()
        for valkey in valdic:
            if not valuesset:
                values += '"'+str(valkey)+'",'
            lines.append('"'+str(key)+"_"+str(valkey)+'"'+" : "+str(valdic[valkey])+",")
        if not valuesset:
            values = values[:-1] + "]"
            valuesset = True
    lines.append("}")
    samples = samples[:-1]+"]"
    with open(filename+'.py','w') as f:
        f.write(samples+"\n")
        f.write(values+"\n")
        for line in lines:
            f.write(line+"\n")
    f.close()
    out = [ filename,samples+"\n",values+"\n"]+lines
    return out

    
