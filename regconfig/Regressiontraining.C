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
  
  TString useVar00 = getenv("REG_USEVAR00");
  TString useVar01 = getenv("REG_USEVAR01");
  TString useVar02 = getenv("REG_USEVAR02");
  TString useVar03 = getenv("REG_USEVAR03");
  TString useVar04 = getenv("REG_USEVAR04");
  TString useVar05 = getenv("REG_USEVAR05");
  TString useVar06 = getenv("REG_USEVAR06");
  TString useVar07 = getenv("REG_USEVAR07");
  TString useVar08 = getenv("REG_USEVAR08");
  TString useVar09 = getenv("REG_USEVAR09");
  TString useVar10 = getenv("REG_USEVAR10");
  TString useVar11 = getenv("REG_USEVAR11");
  TString useVar12 = getenv("REG_USEVAR12");
  TString useVar13 = getenv("REG_USEVAR13");
  TString useVar14 = getenv("REG_USEVAR14");
  TString useVar15 = getenv("REG_USEVAR15");
  
  //Add Variables to factory
  if( useVar00 == "True" ){  factory->AddVariable("Jet_Pt","Jet_pt","units", 'F'); }
  if( useVar01 == "True" ){  factory->AddVariable("Jet_corr","Jet_corr","units", 'F'); }
  if( useVar02 == "True" ){  factory->AddVariable("N_PrimaryVertices","N_PrimaryVertices","units", 'F'); }
  if( useVar03 == "True" ){  factory->AddVariable("Jet_Eta","Jet_eta","units", 'F'); }
  if( useVar04 == "True" ){  factory->AddVariable("Jet_Mt","Jet_mt","units", 'F');  }
  if( useVar05 == "True" ){  factory->AddVariable("Jet_leadTrackPt","Jet_leadTrackPt","units", 'F');  }
  if( useVar06 == "True" ){  factory->AddVariable("Jet_leptonPtRel","Jet_leptonPtRel","units", 'F'); }
  if( useVar07 == "True" ){  factory->AddVariable("Jet_leptonPt","Jet_leptonPt","units", 'F');  }
  if( useVar08 == "True" ){  factory->AddVariable("Jet_leptonDeltaR","Jet_leptonDeltaR","units", 'F'); }
  if( useVar09 == "True" ){  factory->AddVariable("Jet_totHEFrac","Jet_totHEFrac","units", 'F');  }
  if( useVar10 == "True" ){  factory->AddVariable("Jet_nEmEFrac","Jet_neEmEF","units", 'F'); }
  if( useVar11 == "True" ){  factory->AddVariable("Jet_vtxPt","Jet_vtxPt","units", 'F'); }
  if( useVar12 == "True" ){  factory->AddVariable("Jet_vtxMass","Jet_vtxMass","units", 'F'); }
  if( useVar13 == "True" ){  factory->AddVariable("Jet_vtx3DVal","Jet_vtx3dL","units", 'F'); }
  if( useVar14 == "True" ){  factory->AddVariable("Jet_vtxNtracks","Jet_vtxNtrk","units", 'F'); }
  if( useVar15 == "True" ){  factory->AddVariable("Jet_vtx3DSig","Jet_vtx3deL","units", 'F'); }
  
  factory->AddTarget( "Jet_MatchedPartonPt" );
  //factory->AddTarget( "Jet_MatchedPartonPt / Jet_Pt" );
   

   
   std::cout << "before fname" << endl;
   //Root file for Training
   TFile *input(0);
   TString fname = getenv("INPUTFILE");
   std::cout << fname << std::endl;
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
   TString Weightexp = getenv("REG_WEIGHTEXP");

   factory->SetWeightExpression(Weightexp,"Regression");
   
   //Cut on on samples
   //TCut mycut = "Evt_Odd == 1 && abs(Jet_Flav) == 5 && abs(Jet_PartonFlav) == 5";
   TCut mycut = getenv("REG_CUTS");
   
   std::cout << "Prepare Training" << endl;
   factory->PrepareTrainingAndTestTree( mycut, "V:VerboseLevel=Debug:nTrain_Regression=100000:nTest_Regression=100000:SplitMode=Random:NormMode=NumEvents:!V" );
   //factory->PrepareTrainingAndTestTree( mycut, "nTrain_Regression=0:nTest_Regression=0:SplitMode=Random:NormMode=NumEvents:!V" );
   
   bool usebdt = true;

   if (usebdt) {
     std::cout << "Book BTDG" << endl;

     TString nTrees    = getenv("REG_BDTG_NTREES");
     TString shrinkage = getenv("REG_BDTG_SHRINK");
     TString maxdepth  = getenv("REG_BDTG_MAXDEPTH");
     TString ncuts     = getenv("REG_BDTG_NCUTS");
     TString BaggedSF  = getenv("REG_BDTG_BAGGEDSF");

     
     TString bookmethodstring = "!H:NTrees="+nTrees+"::BoostType=Grad:Shrinkage="+shrinkage+":UseBaggedBoost:BaggedSampleFraction="+BaggedSF+":nCuts="+ncuts+":MaxDepth="+maxdepth+":PruneMethod=costcomplexity:PruneStrength=30";
     
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
