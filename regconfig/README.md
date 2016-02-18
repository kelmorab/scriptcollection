#Scripts for testing different TMVA-Regression configurations

##Regressiontraining.C

     export INPUTFILES="path/to/file1.root [path/to/file2.root ..]"
     export WEIGHTPREFIX="prefix-of-weight-file" 
     export OUTPUTFILE="path/to/outputfile.root"
     export REG_BDTG_NTREES="nTrees"
     export REG_BDTG_SHRINK="Shrinkage"
     epxort REG_BDTG_MAXDEPTH="MaxDepth"
     root Regressiontraining.C\(\)
