import ROOT

class PDFPrinting():
    def __init__(self, pdfname, convertROOTfile = False, rootfile = 'name'):
        self.name = pdfname
        self.PDFopened = False
        if convertROOTfile:
            if type(rootfile) is str: 
                inputfile = ROOT.TFile(rootfile)
            else:
                inputfile = rootfile
            #tmpcanvas = ROOT.TCanvas()
            #self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
            nkeys = 0
            for key in inputfile.GetListOfKeys():
                nkeys = nkeys + 1
            tmpcanvas = ROOT.TCanvas()
            self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
            for ikey, key in enumerate(inputfile.GetListOfKeys()):
                tmpcanvas = inputfile.Get(key.GetName())
                #if not self.PDFopened:
                #    self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
                #elif ikey == nkeys-1:
                #    self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
                #else:
                self.addCanvastoPDF(tmpcanvas,pdfname)
            tmpcanvas = ROOT.TCanvas()
            self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
    def openclosePDF(self,canvas, pdfname, open = True):
        if not open:
            canvas.Print(pdfname+".pdf[")
            self.PDFopened = True
        if open:
            canvas.Print(pdfname+".pdf]")
            
    def addCanvastoPDF(self, canvas, pdfname):
        canvas.Print(pdfname+".pdf")

        
#KIT Color Definitions


def convertColor(intval):
    if floatval == 255:
        return 1
    else:
        return 
"""
KIT_Gruen = ROOT.TColor()
KIT_Blau = ROOT.TColor()
KIT_MaiGruen = ROOT.TColor()
KIT_Gelb = ROOT.TColor()
KIT_Orange = ROOT.TColor()
KIT_Braun = ROOT.TColor()
KIT_Rot = ROOT.TColor()
KIT_Lila = ROOT.TColor()
KIT_Cyan_Blau = ROOT.TColor()

KIT_Gruen.SetRGB(0/256.0,150/256.0,130/256.0)
KIT_Blau.SetRGB(70/256.0,100/256.0,170/256.0)
KIT_MaiGruen.SetRGB(140/256.0,182/256.0,60/256.0)
KIT_Gelb.SetRGB(252/256.0,229/256.0,0/256.0)
KIT_Orange.SetRGB(223/256.0,155/256.0,27/256.0)
KIT_Braun.SetRGB(167/256.0,130/256.0,46/256.0)
KIT_Rot.SetRGB(162/256.0,34/256.0,35/256.0)
KIT_Lila.SetRGB(163/256.0,16/256.0,124/256.0)
KIT_Cyan_Blau.SetRGB(35/256.0,161/256.0,224/256.0)


\definecolor{KIT-Gruen}{RGB}{0,150,130}
\definecolor{KIT-Blau}{RGB}{70,100,170}
\definecolor{KIT-MaiGruen}{RGB}{140,182,60}
\definecolor{KIT-Gelb}{RGB}{252,229,0}
\definecolor{KIT-Orange}{RGB}{223,155,27}
\definecolor{KIT-Braun}{RGB}{167,130,46}
\definecolor{KIT-Rot}{RGB}{162,34,35}
\definecolor{KIT-Lila}{RGB}{163,16,124}
\definecolor{KIT-Cyan-Blau}{RGB}{35,161,224}
"""


KIT_Gruen_ = ROOT.TColor(1001 ,0/256.0,150/256.0,130/256.0)
KIT_Blau_ = ROOT.TColor(1002 ,70/256.0,100/256.0,170/256.0)
KIT_MaiGruen_ = ROOT.TColor(1003 ,140/256.0,182/256.0,60/256.0)
KIT_Gelb_ = ROOT.TColor(1004 ,252/256.0,229/256.0,0/256.0)
KIT_Orange_ = ROOT.TColor(1005 ,223/256.0,155/256.0,27/256.0)
KIT_Braun_ = ROOT.TColor(1006 ,167/256.0,130/256.0,46/256.0)
KIT_Rot_ = ROOT.TColor(1007 ,162/256.0,34/256.0,35/256.0)
KIT_Lila_ = ROOT.TColor(1008 ,163/256.0,16/256.0,124/256.0)
KIT_Cyan_Blau_ = ROOT.TColor(1009 ,35/256.0,161/256.0,224/256.0)



KIT_Gruen = 1001
KIT_Blau = 1002
KIT_MaiGruen = 1003
KIT_Gelb = 1004
KIT_Orange = 1005
KIT_Braun = 1006
KIT_Rot = 1007
KIT_Lila = 1008
KIT_Cyan_Blau = 1009


"""
KIT_Gruen_ = ROOT.TColor(0,150,130)
KIT_Blau_ = ROOT.TColor(70,100,170)
KIT_MaiGruen_ = ROOT.TColor(140,182,60)
KIT_Gelb_ = ROOT.TColor(252,229,0)
KIT_Orange_ = ROOT.TColor(223,155,27)
KIT_Braun_ = ROOT.TColor(167,130,46)
KIT_Rot_ = ROOT.TColor(162,34,35)
KIT_Lila_ = ROOT.TColor(163,16,124)
KIT_Cyan_Blau_ = ROOT.TColor(35,161,224)

"""
