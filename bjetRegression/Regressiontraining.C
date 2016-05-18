
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
  TString tmva_dir(TString(gRootDir) + "/tmva");
  if(gSystem->Getenv("TMVASYS"))
    tmva_dir = TString(gSystem->Getenv("TMVASYS"));
  gROOT->SetMacroPath(tmva_dir + "/test/:" + gROOT->GetMacroPath() );
  gROOT->ProcessLine(".L TMVARegGui.C");
  
   
   TString outfileName( "BReg_0330_oldVars.root" );
   TFile* outputFile = TFile::Open( outfileName, "RECREATE" );
   

   TMVA::Factory *factory = new TMVA::Factory( "TMVARegression_0330_oldVars", outputFile,"V:!Silent:Color:DrawProgressBar" );
   
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
   //factory->AddVariable("Jet_chargedMult","Jet_chargedMult","units", 'F');
   factory->AddVariable("Jet_vtxPt","Jet_vtxPt","units", 'F');
   factory->AddVariable("Jet_vtxMass","Jet_vtxMass","units", 'F');
   factory->AddVariable("Jet_vtx3DVal","Jet_vtx3dL","units", 'F');
   factory->AddVariable("Jet_vtxNtracks","Jet_vtxNtrk","units", 'F');
   factory->AddVariable("Jet_vtx3DSig","Jet_vtx3deL","units", 'F');
   
   factory->AddTarget( "Jet_MatchedPartonPt / Jet_Pt" ); 

   factory->AddSpectator( "Jet_MatchedPartonPt");
   factory->AddSpectator( "Jet_MatchedPartonFlav" );
   factory->AddSpectator( "Jet_Flav" );
   factory->AddSpectator( "Evt_Odd" );
   factory->AddSpectator("N_PrimaryVertices");
   factory->AddSpectator("Jet_totHEFrac"); 
   factory->AddSpectator("Jet_nEmEFrac");
   
   std::cout << "before fname" << endl;
   //Root file for Training
   TFile *input(0);
   TString fname = "/nfs/dust/cms/user/kschweig/JetRegression/trees0329/ttbarinclforbReg0329.root";
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
   
   std::cout << "Add weight expression" << endl;
   factory->SetWeightExpression("Weight","Regression");

   //Cut on on samples
   TCut mycut = "Evt_Odd == 1 && abs(Jet_Flav) == 5 && abs(Jet_MatchedPartonFlav) == 5 && Jet_Eta <= 2.4";
   
   std::cout << "Prepare Training" << endl;
   factory->PrepareTrainingAndTestTree( mycut, "V:VerboseLevel=Debug:nTrain_Regression=100000:nTest_Regression=300000:SplitMode=Random:NormMode=NumEvents:!V" );
   //factory->PrepareTrainingAndTestTree( mycut, "nTrain_Regression=0:nTest_Regression=0:SplitMode=Random:NormMode=NumEvents:!V" );
   
   bool usebdt = true;

   if (usebdt) {
     std::cout << "Book BTDG" << endl;
     //factory->BookMethod( TMVA::Types::kBDT, "BDTG","!H:V:VerbosityLevel=Debug:NTrees=1000::BoostType=Grad:Shrinkage=0.1:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=5:PruneMethod=costcomplexity:PruneStrength=30:GradBaggingFraction=0.5:UseBaggedBoost=True" );
     factory->BookMethod( TMVA::Types::kBDT, "BDTG","!H:V:VerbosityLevel=Debug:NTrees=1200::BoostType=Grad:Shrinkage=0.1:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=30:MaxDepth=5:PruneMethod=costcomplexity:PruneStrength=30:GradBaggingFraction=0.5:UseBaggedBoost=True:VarTransform=U(Jet_leptonDeltaR)" );
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
