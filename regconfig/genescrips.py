import sys
import os
import stat

def createScript(scriptname,inputfile,outputname,weightname,nTrees,shrinkage,nCuts,maxdepth,baggedsf,programpath,cuts,weightexp,variables):
    script="#!/bin/bash \n"
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+='cd '+config.cmsswpath+'/src\neval `scram  runtime -sh`\n'
    script+='cd - \n'
    script+='export INPUTFILE="'+inputfile+'"\n'
    script+='export OUTPUTFILE="'+outputname+'"\n'
    script+='export WEIGHTPREFIX="'+weightname+'"\n'
    script+='export REG_BDTG_NTREES="'+nTrees+'"\n'
    script+='export REG_BDTG_SHRINK="'+shrinkage+'"\n'
    script+='export REG_BDTG_MAXDEPTH="'+maxdepth+'"\n'
    script+='export REG_BDTG_NCUTS="'+nCuts+'"\n'
    script+='export REG_BDTG_BAGGEDSF="'+baggedsf+'"\n'
    script+='export REG_CUTS="'+cuts+'"\n'
    script+='export REG_WEIGHTEXP="'+weightexp+'"\n'
    script+='export REG_USEVAR00="'+variables[0]+'"\n'
    script+='export REG_USEVAR01="'+variables[1]+'"\n'
    script+='export REG_USEVAR02="'+variables[2]+'"\n'
    script+='export REG_USEVAR03="'+variables[3]+'"\n'
    script+='export REG_USEVAR04="'+variables[4]+'"\n'
    script+='export REG_USEVAR05="'+variables[5]+'"\n'
    script+='export REG_USEVAR06="'+variables[6]+'"\n'
    script+='export REG_USEVAR07="'+variables[7]+'"\n'
    script+='export REG_USEVAR08="'+variables[8]+'"\n'
    script+='export REG_USEVAR09="'+variables[9]+'"\n'
    script+='export REG_USEVAR10="'+variables[10]+'"\n'
    script+='export REG_USEVAR11="'+variables[11]+'"\n'
    script+='export REG_USEVAR12="'+variables[12]+'"\n'
    script+='export REG_USEVAR13="'+variables[13]+'"\n'
    script+='export REG_USEVAR14="'+variables[14]+'"\n'
    script+='export REG_USEVAR15="'+variables[15]+'"\n'
    script+='root -l -b '+programpath+'+'+'\n'
    f=open(scriptname,'w')
    f.write(script)
    f.close()
    st = os.stat(scriptname)
    os.chmod(scriptname, st.st_mode | stat.S_IEXEC)


#import config
if len(sys.argv) > 1:
    cfgname=sys.argv[1]
    assert cfgname[-3:]=='.py'
    config=__import__(cfgname[:-3])


#Set paths
outputpath = str(config.nfsroot)+str(config.outputfilefolder)
weightoutputpath = str(config.nfsroot)+str(config.outputfilefolder)+"weights/"
scriptpath = outputpath+"scripts/"

##############################################################################
if not os.path.exists(outputpath):
    os.makedirs(outputpath)
if not os.path.exists(scriptpath):
    os.makedirs(scriptpath)
if not os.path.exists(weightoutputpath):
    os.makedirs(weightoutputpath)
if not os.path.exists(outputpath+"/output/"):
    os.makedirs(outputpath+"/output/")
if not os.path.exists(config.cmsswpath):
    print 'WRONG CMSSW PATH!'
    print cmsswpath
    sys.exit()
##############################################################################



nTrees_list = []
if len(config.tree_list) == 0:
    for i in range(int(config.nTrees_end)/int(config.nTrees_steps) + 1):
        tmp = config.nTrees_start + i * config.nTrees_steps
        if tmp <= config.nTrees_end:
            nTrees_list.append(tmp)
else:
    nTrees_list = config.tree_list

Shrinkage_list = []
if len(config.shrink_list) == 0:
    for i in range(int(config.shrink_end/config.shrink_steps)+1):
        tmp = config.shrink_start + i * config.shrink_steps
        if tmp <= config.shrink_end:
            Shrinkage_list.append(tmp)
else:
    Shrinkage_list = config.shrink_list

MaxDepth_list = []
for i in range(int(config.MaxD_end)/int(config.MaxD_steps) + 1):
    tmp = config.MaxD_start + i * config.MaxD_steps
    if tmp <= config.MaxD_end:
        MaxDepth_list.append(tmp)

nCuts_list = []
for i in range(int(config.nCuts_end)/int(config.nCuts_steps) + 1):
    tmp = config.nCuts_start + i * config.nCuts_steps
    if tmp <= config.nCuts_end:
        nCuts_list.append(tmp)

baggedsf_list = config.bsf_list
inputsets_list = config.allinputsets
namelist = config.namelist

print "Output path:",outputpath
print "Weight path:",weightoutputpath
print "Script path:",scriptpath
print "Using cuts for training:",config.cuts
print "Generating",len(nTrees_list)*len(MaxDepth_list)*len(Shrinkage_list)*len(nCuts_list)*len(baggedsf_list)*len(inputsets_list),"scripts"


iscript = 0
for nTrees in nTrees_list:
    for shrink in Shrinkage_list:
        for maxdepth in MaxDepth_list:
            for nCuts in nCuts_list:
                for baggedsf in baggedsf_list:
                    i = 0
                    for varset in inputsets_list:
                        print "Generating script with nTrees:",nTrees,",shrinkage:",shrink,",nCuts:",nCuts,",maxdepth:",maxdepth,"and BaggedSampleFraction",baggedsf
                        if (len(namelist) > 0):
                            prefix = "script_"+str(nTrees)+"_"+str(shrink)+"_"+str(maxdepth)+"_"+str(nCuts)+"_"+str(baggedsf)+"_"+str(namelist[i])
                            i = i+1 
                        else:
                            prefix = "script_"+str(nTrees)+"_"+str(shrink)+"_"+str(maxdepth)+"_"+str(nCuts)+"_"+str(baggedsf)
                        createScript(scriptpath+prefix+".sh",
                                     str(config.nfsroot)+str(config.inputfiles),
                                     outputpath+"/output/"+prefix+".root",
                                     prefix,
                                     str(nTrees),str(shrink),str(nCuts),str(maxdepth),str(baggedsf),
                                     str(config.nfsroot)+str(config.program),
                                     config.cuts, config.weightexp, varset)
           
            
os.system("wget https://raw.githubusercontent.com/kit-cn-cms/BoostedAnalyzer_runscripts_NAF/master/published_samples/sup.py -O "+outputpath+"sup.py")

