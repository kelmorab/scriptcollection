#Scripts for b-Jet Regression

## MakeTreeforbReg.C

Root script, that converts output Trees form the [BoostedTTH Framework](https://github.com/cms-ttH/BoostedTTH) to Trees for usage in a TMVA Regression training.
     
     export INPUTFILES="path/to/file1.root [path/to/file2.root ..]" 
     export OUTPUTFILE="path/to/outputfile.root"
     root MakeTreeforbReg.C\(\)

## runscriptCreator.py

Create shell scripts for parallel usage of MakeTreeforbReg.C on BIRDCluster at NAF. 
       
       python runscriptCreator.py path/to/MakeTreeforbReg.C path/to/scriptfolder path/to/outputfolder

Submission can be done with [sup.py](https://github.com/kit-cn-cms/BoostedAnalyzer_runscripts_NAF/blob/master/published_samples/sup.py).

       wget https://raw.githubusercontent.com/kit-cn-cms/BoostedAnalyzer_runscripts_NAF/master/published_samples/sup.py
       python sup.py path/to/scripts/*.sh  

