import os
import sys
import stat
import glob

cmsswpath = "/nfs/dust/cms/user/kschweig/CMSSW_7_6_3"
scriptnameprefix = "bscript_"
outputprefix = "output_"
inputpath = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarbReg0318_testing/output/"
programpath = "/nfs/dust/cms/user/kschweig/Code/scriptcollection/bjetRegression/breg_performance.py"
filesperjob = 1

filelist = glob.glob(inputpath+"*.root")

print len(filelist)

if (len(filelist)/filesperjob)*filesperjob < len(filelist):
    nscripts = (len(filelist)/filesperjob) + 1
else:
    nscripts = (len(filelist)/filesperjob)
print nscripts

for i in range(nscripts):
    jobfiles = filelist[i*filesperjob:(i*filesperjob)+1]
    scriptname = scriptnameprefix+str(i)+'.sh'
    script="#!/bin/bash \n"
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+='cd '+cmsswpath+'/src\neval `scram  runtime -sh`\n'
    script+='cd - \n'
    script+='python '+programpath+' '+outputprefix+' '+str(i+1)+' '
    for i in range(len(jobfiles)):
        script+=jobfiles[i]+' '
    script+='\n'    
    f=open(scriptname,'w')
    f.write(script)
    f.close()
    st = os.stat(scriptname)
    os.chmod(scriptname, st.st_mode | stat.S_IEXEC)
    del script
