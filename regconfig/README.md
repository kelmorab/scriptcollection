#Scripts for testing different TMVA-Regression configurations

##Regressiontraining.C

Training script for b-Jet Regression

     export INPUTFILE="path/to/file.root"
     export WEIGHTPREFIX="prefix-of-weight-file" 
     export OUTPUTFILE="path/to/outputfile.root"
     export REG_CUTS="cuts"'
     export REG_BDTG_NTREES="nTrees"
     export REG_BDTG_SHRINK="Shrinkage"
     epxort REG_BDTG_MAXDEPTH="MaxDepth"
     root Regressiontraining.C+

##Training on NAF

1. Edit config.py
2. python genescrips.py config.py
3. change to outputdir and use sup.py to submit