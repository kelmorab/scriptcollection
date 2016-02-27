import ROOT

def exporthistos(outputname, histolist):
    outfile = ROOT.TFile(outputname+".root","RECREATE")
    outfile.cd()
    for histo in histolist:
        if histo.__class__.__name__ == 'normPlots': #ask histo for the name of its class
            hlist = histo.getHistos()
            name = histo.getKey() #Get name for dir
            outfile.mkdir('normPlots'+name) #Create dir
            outfile.cd('normPlots'+name) #switch to dir
            for h in hlist:
                h.Write()
            outfile.cd() #switch back to root
            
        elif histo.__class__.__name__ == 'CatPlots': #ask histo for the name of its class
            hlist = histo.getHistos()
            if len(hlist) == 1:
                hlist[0].Write()
    print "Histos exported to",outputname+".root"
