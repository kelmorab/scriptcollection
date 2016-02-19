#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"


#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Factory.h"
#endif

using namespace TMVA;


void Regressiontraining(   )
{
  TMVA::Tools::Instance();
  
  // to get access to the GUI and all tmva macro
  /*TString tmva_dir(TString(gRootDir) + "/tmva");
  if(gSystem->Getenv("TMVASYS"))
    tmva_dir = TString(gSystem->Getenv("TMVASYS"));
  gROOT->SetMacroPath(tmva_dir + "/test/:" + gROOT->GetMacroPath() );
  gROOT->ProcessLine(".L TMVARegGui.C");
  */
  
  char* outfileName = getenv("OUTPUTFILE");
  TFile* outputFile = TFile::Open( outfileName, "RECREATE" );
  
  char* jobname = getenv("WEIGHTPREFIX");
  TMVA::Factory *factory = new TMVA::Factory( jobname, outputFile,"V:!Silent:Color:DrawProgressBar" );
   
   //Add Variables to factory
   factory->AddVariable("Jet_Pt","Jet_pt","units", 'F'); 
   factory->AddVariable("Jet_corr","Jet_corr","units", 'F');
   factory->AddVariable("Evt_Rho","rho","units", 'F');
   factory->AddVariable("Jet_Eta","Jet_eta","units", 'F');
   factory->AddVariable("Jet_Mt","Jet_mt","units", 'F'); 
   factory->AddVariable("Jet_leadTrackPt","Jet_leadTrackPt","units", 'F'); 
   factory->AddVariable("Jet_leptonPtRel","Jet_leptonPtRel","units", 'F');
   factory->AddVariable("Jet_leptonPt","Jet_leptonPt","units", 'F'); 
   factory->AddVariable("Jet_leptonDeltaR","Jet_leptonDeltaR","units", 'F');
   //factory->AddVariable("Jet_nHEFrac","Jet_neHEF","units", 'F'); 
   //factory->AddVariable("Jet_nEmEFrac","Jet_neEmEF","units", 'F');
   factory->AddVariable("Jet_chargedMult","Jet_chargedMult","units", 'F');
   factory->AddVariable("Jet_vtxPt","Jet_vtxPt","units", 'F');
   factory->AddVariable("Jet_vtxMass","Jet_vtxMass","units", 'F');
   factory->AddVariable("Jet_vtx3DVal","Jet_vtx3dL","units", 'F');
   factory->AddVariable("Jet_vtxNtracks","Jet_vtxNtrk","units", 'F');
   factory->AddVariable("Jet_vtx3DSig","Jet_vtx3deL","units", 'F');
   

   factory->AddTarget( "Jet_PartonPt" ); 
   
   //factory->AddSpectator( "Jet_PartonFlav" );
   //factory->AddSpectator( "Jet_Flav" );
   //factory->AddSpectator( "Evt_Odd" );
   

   
   std::cout << "before fname" << endl;
   //Root file for Training
   TFile *input(0);
   TString fname = getenv("INPUTFILE");
   //TString fname = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbarforbReg0211.root";
   //   TString fname = "/nfs/dust/cms/user/kschweig/JetRegression/trees0113/ttbar_nominal.root";
   std::cout << "after fname" << endl;

   if (!gSystem->AccessPathName( fname )) {
     input = TFile::Open( fname ); // check if file in local directory exists
   }
   if (!input) {
     std::cout << "ERROR: could not open data file" << std::endl;
     exit(1);
   }

   std::cout << "--- TMVARegression           : Using input file: " << input->GetName() << std::endl;

   TTree *Tree = (TTree*)input->Get("bRegTree");
   Double_t regWeight = 1.0;

   std::cout << "Add RegressionTree" << endl;
   factory->AddRegressionTree( Tree, regWeight );
   
   //std::cout << "Add weight expression" << endl;
   //factory->SetWeightExpression("1","Regression");

   //Cut on on samples
   //TCut mycut = "Evt_Odd == 1 && abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5";
   TCut mycut = getenv("REG_CUTS");
   
   std::cout << "Prepare Training" << endl;
   factory->PrepareTrainingAndTestTree( mycut, "V:VerboseLevel=Debug:nTrain_Regression=100000:nTest_Regression=1000000:SplitMode=Random:NormMode=NumEvents:!V" );
   //factory->PrepareTrainingAndTestTree( mycut, "nTrain_Regression=0:nTest_Regression=0:SplitMode=Random:NormMode=NumEvents:!V" );
   
   bool usebdt = true;

   if (usebdt) {
     std::cout << "Book BTDG" << endl;

     TString nTrees    = getenv("REG_BDTG_NTREES");
     TString shrinkage = getenv("REG_BDTG_SHRINK");
     TString maxdepth  = getenv("REG_BDTG_MAXDEPTH");
     TString ncuts     = getenv("REG_BDTG_NCUTS");
     
     TString bookmethodstring = "!H:NTrees="+nTrees+"::BoostType=Grad:Shrinkage="+shrinkage+":UseBaggedBoost:BaggedSampleFraction=0.5:nCuts="+ncuts+":MaxDepth="+maxdepth+":PruneMethod=costcomplexity:PruneStrength=30:GradBaggingFraction=0.5";
     
     factory->BookMethod( TMVA::Types::kBDT, "BDTG", bookmethodstring);
     }
   else {
     std::cout << "Book ANN" << endl;
     factory->BookMethod( TMVA::Types::kMLP, "MLP_ANN", "");
   }

   // Train MVAs using the set of training events
   std::cout << "Train MVA" << endl;
   factory->TrainAllMethods();

   // ---- Evaluate all MVAs using the set of test events
   std::cout << "Test MVA" << endl;
   factory->TestAllMethods();

   // ----- Evaluate and compare performance of all configured MVAs
   std::cout << "Eval MVA" << endl;
   factory->EvaluateAllMethods(); 

   outputFile->Close();

   std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
   std::cout << "==> TMVARegression is done!" << std::endl;      

   delete factory;

}
