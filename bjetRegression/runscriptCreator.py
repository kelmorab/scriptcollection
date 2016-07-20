#Modified from https://github.com/kit-cn-cms/cpp-plotscripts/blob/master/fatjet_data_mc/create_runscripts.py
#Usage = python runscriptCreator.py progampath scriptpath outpath 

import glob
import os
import sys
import stat
#import ROOT

programpath=sys.argv[1]

outpath=sys.argv[3]
scriptpath=sys.argv[2]
cmsswpath='/nfs/dust/cms/user/kschweig/CMSSW_7_6_3'

samples=[('ttbar','/nfs/dust/cms/user/kschweig/JetRegression/trees0718/ttbar_incl/')]

events_per_job= 1000000
files_per_job = 10

if not os.path.exists(scriptpath):
    os.makedirs(scriptpath)
if not os.path.exists(outpath):
    os.makedirs(outpath)
if not os.path.exists(cmsswpath):
    print 'WRONG CMSSW PATH!'
    print cmsswpath
    sys.exit()

def createScript(scriptname,programpath,processname,filenames,outfilename,maxevents,skipevents,suffix):
    script="#!/bin/bash \n"
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+='cd '+cmsswpath+'/src\neval `scram  runtime -sh`\n'
    script+='cd - \n'
    #script+='export PROCESSNAME="'+processname+'"\n'
    script+='export INPUTFILES="'+filenames+'"\n'
    script+='export OUTPUTFILE="'+outfilename+'"\n'
    #script+='export MAXEVENTS="'+str(maxevents)+'"\n'
    #script+='export SKIPEVENTS="'+str(skipevents)+'"\n'
    #script+='export SUFFIX="'+suffix+'"\n'
    script+='root -l -b '+programpath+'\(\)'+'\n'
    f=open(scriptname,'w')
    f.write(script)
    f.close()
    st = os.stat(scriptname)
    os.chmod(scriptname, st.st_mode | stat.S_IEXEC)

    
def createScriptsForSamples(samples,suffix,programpath):
    tmpsamples=[]
    for s in samples:
        allfiles=[]
        neventsperfile=[]
        print s[1]
        allfiles=sorted(glob.glob(s[1]+"*.root")) #get all root files in sampledirectory
        print allfiles
        tmpsamples.append((s[0],allfiles,neventsperfile))
    samples=tmpsamples

    for sample in samples:
        process=sample[0]
        files = sample[1]
        ijob=1
        nfiles=0
        files_in_job=[]
        for f in files:
            files_in_job.append(f)
            nfiles+=1
            if nfiles>=files_per_job or f == files[-1]:
                scriptname=scriptpath+'/'+process+suffix+'_'+str(ijob)+'.sh'
                filenames=' '.join(files_in_job)
                outfilename=outpath+'/'+process+suffix+'_'+str(ijob)+'.root'
                maxevents=9999999999
                skipevents=0
                print scriptname,filenames,outfilename,programpath
                createScript(scriptname,programpath,process,filenames,outfilename,maxevents,skipevents,suffix)
                ijob+=1
                nfiles=0
                files_in_job=[]

createScriptsForSamples(samples,'',programpath)
