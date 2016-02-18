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
                self.addCanvastoPDF(tmpcanvas)
            tmpcanvas = ROOT.TCanvas()
            self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
        else:
            print "Init PDFPrinting"
            tmpcanvas = ROOT.TCanvas()
            self.openclosePDF(tmpcanvas, self.name, False)
            print "PDF "+self.name+ " opened"

    def openclosePDF(self,canvas, pdfname, open = True):
        if not open:
            canvas.Print(pdfname+".pdf[")
            self.PDFopened = True
        if open:
            canvas.Print(pdfname+".pdf]")
            
    def addCanvastoPDF(self, canvas):
        canvas.Print(self.name+".pdf")
    
    def closePDF(self):
        tmpcanvas = ROOT.TCanvas()
        self.openclosePDF(tmpcanvas, self.name, self.PDFopened)
        print "PDF "+self.name+ " closed"
    


#KIT Color Definitions
def convertColor(intval):
    if floatval == 255:
        return 1
    else:
        return 

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

