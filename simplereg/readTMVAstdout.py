#usage: python readTMVAstdout.py inputfile.txt ninputvars
import sys
import re

def makerankingtable(rankinglist,rankingstring):
    print '\\begin{table}[c]'
    print '\\begin{tabular}{c c}'
    print '\\toprule'
    print '& '+rankingstring+' \\'+'\\'
    print '\midrule'
    for element in rankinglist:
        print element[0],'&\SI{',element[1],'}{} \\'+'\\'
    print '\\bottomrule'
    print '\end{tabular}'
    print '\end{table}'

def makerestable(reslist):
    caption = ["Test Sample","Training Sample"]
    for ir,res in enumerate(reslist):
        print '\\begin{table}[c]'
        print '\\caption{'+caption[ir]+'}'
        print '\\vspace{5pt}'
        print '\\begin{tabular}{ c c c c c c}'
        print '\\toprule'
        print 'Bias & Bias (T) & RMS & RMS (T) & Mutual Info & Mutual Info (T)'+' \\'+'\\'
        print '\midrule'
        tmpstring = ""
        for element in res:
            tmpstring +="\SI{ "+element+"}{} & "
        print tmpstring[:-2]+ ' \\'+'\\'
        print '\\bottomrule'
        print '\end{tabular}'
        print '\end{table}'




charset = sys.getfilesystemencoding()

lines = []
try:
    open(str(sys.argv[1]), 'r')
except IOError:
    print "Inputfile does not exist"
    exit()
with open(str(sys.argv[1]), 'r') as f:
    inputfile = f.read()
    lines = inputfile.split("\n")
    lines.pop()

nicelines = []
printflag = False
for line in lines:
    if line.startswith("--- DataSetInfo              : Correlation matrix (Regression):"):
        printflag = True
    if line.startswith("--- DataSetFactory           :"):
        printflag = False
    if line.startswith("--- TFHandler_Factory        : Variable        Mean        RMS   [        Min        Max ]"):
        printflag = True
    if line.startswith("--- TFHandler_Factory        : Plot event variables for Id"):
        printflag = False
    if line.startswith("--- TFHandler_Factory        : Ranking input variables (method unspecific)..."):
        printflag = True
    if line.startswith("--- Factory                  : Train all methods for Regression ..."):
        printflag = False
    if line.startswith("--- TFHandler_BDTG           : Plot event variables for BDTG"):
        printflag = True
    if line.startswith("--- TFHandler_BDTG           : Create scatter and profile plots in target-file directory"):
        printflag = False
    if line.startswith("--- Factory                  : MVA Method:        <Bias>   <Bias_T>    RMS    RMS_T  |  MutInf MutInf_T"):
        printflag = True
    if line.startswith("--- Factory                  : Evaluation results ranked by smallest RMS on training sample:"):
        printflag = False
    if line.startswith("--- Dataset:Default          : Created tree 'TestTree' with"):
        printflag = False
    if printflag:
        nicelines.append(line)

ranking_corr = []
ranking_mutinf = []
ranking_ratio = []
ranking_ratio_T = []

res = []

for il, line in enumerate(nicelines):
    if line.startswith("--- IdTransformation"):
        if line.endswith("|Correlation with target|"):
            for i in range(int(sys.argv[2])):
                a =  nicelines[il+2+i].replace(" ","")
                a = a.split(":")
                ranking_corr.append([a[-2],a[-1]])
        if line.endswith("Mutual information"):
            for i in range(int(sys.argv[2])):
                a =  nicelines[il+2+i].replace(" ","")
                a = a.split(":")
                ranking_mutinf.append([a[-2],a[-1]])        
        if line.endswith("Correlation Ratio"):
            for i in range(int(sys.argv[2])):
                a =  nicelines[il+2+i].replace(" ","")
                a = a.split(":")
                ranking_ratio.append([a[-2],a[-1]])
        if line.endswith("Correlation Ratio (T)"):
            for i in range(int(sys.argv[2])):
                a =  nicelines[il+2+i].replace(" ","")
                a = a.split(":")
                ranking_ratio_T.append([a[-2],a[-1]])
    if line.startswith("--- Factory                  : BDTG"):
        tmp = line.split(" ")
        outvars = []
        #print tmp
        for t in tmp:
            if len(t) > 1 and t != "---":
                flag = True
                try :
                    int(t[0])
                except ValueError:
                    flag = False
                t = t.split(":")
                #print t
                if len(t) > 1:
                    t  = t[1]
                else:
                    t  = t[0]
                #print t
                if t[0] == "-" or flag:
                    #print t
                    nm = 0
                    slast = "k"
                    for s in t:
                        if s == "-" and slast != "e":
                            nm = nm + 1
                        slast = s
                        #print t
                    if nm >= 1:
                        isplit = -1
                        slast = "k"
                        if t[0] == "-" and nm == 1:
                            outvars.append(t)
                        else:
                            for i,s in enumerate(t):
                                if s == "-" and slast != "e" and i != 0:
                                    isplit = i
                                slast = s
                            outvars.append(t[0:isplit])
                            outvars.append(t[isplit::])
                    else:
                        #print t
                        outvars.append(t)
        res.append(outvars)        

print res
print ranking_corr, ranking_mutinf, ranking_ratio, ranking_ratio_T 



makerankingtable(ranking_corr,"$|$Correlation with target$|$")
makerankingtable(ranking_mutinf,"Mutual Information")
makerankingtable(ranking_ratio,"Correlation Ratio")
makerankingtable(ranking_ratio_T,"Correlation Ratio (T)")
makerestable(res)

