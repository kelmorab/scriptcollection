
#include <cstdlib>
#include <iostream>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Reader.h"



using namespace std;

void evalReg(   )
{
  char* inputfilenames = getenv("INPUTFILES");
  char* inputweights = getenv("INPUTWEIGHT");
  char* outputname = getenv("OUTPUTFILE");
  
  TChain* InputChain = new TChain("bRegTree");
  
  string buf;
  stringstream ss(inputfilenames); 
  while (ss >> buf){
    InputChain->Add(buf.c_str());
  }
  
  TFile* outputFile = new TFile(outputname, "RECREATE");


  int Event_Odd, NJets;
  float rho, Event_Weight;
  float Jet_pt, Jet_corr, Jet_Eta, Jet_M,Jet_Mt, Jet_leadTrackPt, Jet_Flav;
  float Jet_leptonPt, Jet_leptonPtRel, Jet_leptonDeltaR;
  float Jet_nHEFrac, Jet_nEMEFrac, Jet_chMult;
  float Jet_vtxPt, Jet_vtxMass, Jet_vtx3DVal, Jet_vtxNtracks, Jet_vtx3DSig;
  float Jet_PartonFlav, Jet_PartonPt;

  cout << "Setting up Branches in Inputchain"  << endl;
  InputChain->SetBranchAddress("Evt_Odd",&Event_Odd);            
  //InputChain->SetBranchAddress("N_Jets",&NJets);                      
  InputChain->SetBranchAddress("Evt_Rho",&rho);                       
  InputChain->SetBranchAddress("Weight",&Event_Weight);               

  InputChain->SetBranchAddress("Jet_Pt",&Jet_pt);                     
  InputChain->SetBranchAddress("Jet_corr",&Jet_corr);                 
  InputChain->SetBranchAddress("Jet_Eta",&Jet_Eta);                   
  InputChain->SetBranchAddress("Jet_M",&Jet_M);                       
  InputChain->SetBranchAddress("Jet_Mt",&Jet_Mt);                       

  InputChain->SetBranchAddress("Jet_leadTrackPt",&Jet_leadTrackPt);   
  InputChain->SetBranchAddress("Jet_Flav",&Jet_Flav);                 

  InputChain->SetBranchAddress("Jet_leptonPt",&Jet_leptonPt);         
  InputChain->SetBranchAddress("Jet_leptonPtRel",&Jet_leptonPtRel);   
  InputChain->SetBranchAddress("Jet_leptonDeltaR",&Jet_leptonDeltaR); 

  InputChain->SetBranchAddress("Jet_nHEFrac",&Jet_nHEFrac);           
  InputChain->SetBranchAddress("Jet_nEmEFrac",&Jet_nEMEFrac);         
  InputChain->SetBranchAddress("Jet_chargedMult",&Jet_chMult);        

  InputChain->SetBranchAddress("Jet_vtxPt",&Jet_vtxPt);               
  InputChain->SetBranchAddress("Jet_vtxMass",&Jet_vtxMass);           
  InputChain->SetBranchAddress("Jet_vtx3DVal",&Jet_vtx3DVal);         
  InputChain->SetBranchAddress("Jet_vtxNtracks",&Jet_vtxNtracks);     
  InputChain->SetBranchAddress("Jet_vtx3DSig",&Jet_vtx3DSig);         

  InputChain->SetBranchAddress("Jet_PartonFlav",&Jet_PartonFlav);     
  InputChain->SetBranchAddress("Jet_PartonPt",&Jet_PartonPt);  
  

  /*
  //Create Histograms to fill later
  //Input Variables:
  TH1F *hrho = new TH1F("hrho","Regression Input: Rho",30,0,60);

  TH1F *hjetpT = new TH1F("hjetpT","Regression Input: Jet pT",160,0,1600);
  TH1F *hjetcorr = new TH1F("hjetcorr","Regression Input: Jet corr",25,0.75,1.25);
  TH1F *hjeteta = new TH1F("hjeteta","Regression Input: Jet #eta",20,-5,5);
  TH1F *hjetmass = new TH1F("hjetmass","Regression Input: Jet Mass",160,0,1600);
  TH1F *hjetleadtrackpt = new TH1F("hjetleadtrackpt","Regression Input: Jet leading Track pT",60,0,600);

  TH1F *hjetleptonpt = new TH1F("hjetleptonpt","Regression Input: Jet Lepton pT",60,0,120);
  TH1F *hjetleptonptrel = new TH1F("hjetleptonptrel","Regression Input: Jet Lepton pT Rel ",30,0,60);
  TH1F *hjetleptondeltar = new TH1F("hjetleptondeltar","Regression Input: Jet Lepton DeltaR ",10,0,0.5);
  
  TH1F *hjetnhefrac = new TH1F("hjetnhefrac","Regression Input: Jet nHEFraction ",20,0,1);
  TH1F *hjetnemefrac = new TH1F("hjetnemefrac","Regression Input: Jet nEmEFraction ",20,0,1);
  TH1F *hjetchmult = new TH1F("hjetchmult","Regression Input: Jet charged Mult",35,0,70);

  TH1F *hjetvtxpt = new TH1F("hjetvtxpt","Regression Input: Jet vtx pT ",100,0,200);
  TH1F *hjetvtxmass = new TH1F("hjetvtxmass","Regression Input: Jet vtx Mass ",14,0,7);
  TH1F *hjetvtxntracks = new TH1F("hjetvtxntracks","Regression Input: Jet vtx N_{tracks}",13,-0.5,12.5);
  TH1F *hjetvtxval = new TH1F("hjetvtxval","Regression Input: Jet vtx 3D Val",30,0,15);
  TH1F *hjetvtxsig = new TH1F("hjetvtxsig","Regression Input: Jet vtx 3D Sig",150,0,300);
  
  //Output Variables
  TH1F *hjetptreg = new TH1F("hjetptreg","Regression Output: Jet pT",160,0,1600);
  */
  
  outputFile->cd();
  
  float Jet_regPt;

  //Set up new Tree, with the same branches as to inputtree, but without entries
  cout << "Setting up new Tree" << endl;
  TTree *newTree = InputChain->CloneTree(0);
  
  cout << "Setting up new Branch in Outputtree" << endl;
  TBranch *RegpT = newTree->Branch("Jet_regPt",&Jet_regPt,"Jet_regPt/F");

  //Initialize Regression
  cout << "Initializing TMVA::Reader" << endl;
  reader = new TMVA::Reader();

  reader->AddVariable("Jet_Pt",&Jet_pt ); 
  reader->AddVariable("Jet_corr",&Jet_corr );
  reader->AddVariable("Evt_Rho",&rho);
  reader->AddVariable("Jet_Eta",&Jet_Eta );
  reader->AddVariable("Jet_Mt",&Jet_Mt ); 
  reader->AddVariable("Jet_leadTrackPt",&Jet_leadTrackPt ); 
  reader->AddVariable("Jet_leptonPtRel",&Jet_leptonPtRel );
  reader->AddVariable("Jet_leptonPt",&Jet_leptonPt ); 
  reader->AddVariable("Jet_leptonDeltaR",&Jet_leptonDeltaR );
  //reader->AddVariable("Jet_nHEFrac",&Jet_nHEFrac ); 
  //reader->AddVariable("Jet_nEmEFrac",&Jet_nEMEFrac );
  reader->AddVariable("Jet_chargedMult",&Jet_chMult );
  reader->AddVariable("Jet_vtxPt",&Jet_vtxPt );
  reader->AddVariable("Jet_vtxMass",&Jet_vtxMass );
  reader->AddVariable("Jet_vtx3DVal",&Jet_vtx3DVal );
  reader->AddVariable("Jet_vtxNtracks",&Jet_vtxNtracks );
  reader->AddVariable("Jet_vtx3DSig",&Jet_vtx3DSig );
  
  cout << "Booking MVA" << endl;
  reader->BookMVA("BDTG",inputweights);


  //Loop over all Events and fill new Branch with regressed pT
  long nentries = InputChain->GetEntries();
  for(long i = 0; i < nentries; i++) {
    InputChain->GetEvent(i);
    
    if(abs(Jet_PartonFlav) == 5 && abs(Jet_Flav) == 5) {
      Jet_regPt = reader->EvaluateRegression("BDTG").at(0);
    }
    else {
      Jet_regPt = -99;
    }
   
    newTree->Fill();
  }

  outputFile->Write();
}

