#include <iostream>
#include <string>
#include <sstream>

#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

using namespace std;

void MakeTreeforbReg(   ) 
{
  
  //Create file for output
  //TString outfilename("bRegTree.root");
  char* outfilename = getenv("OUTPUTFILE");
  TFile* outputFile = new TFile( outfilename, "RECREATE" );


  //Set up input tree
  TChain* InputChain = new TChain("MVATree");
  //TString fname = "/nfs/dust/cms/user/kschweig/JetRegression/testtrees/jetreg_0113_1_nominal_Tree.root";
  char* filenames = getenv("INPUTFILES");
  string buf;
  stringstream ss(filenames); 
  while (ss >> buf){
    InputChain->Add(buf.c_str());
  }


  int Event_Odd, NJets;
  float rho, Event_Weight;
  float Jet_pt[20],Jet_corr[20],Jet_Eta[20],Jet_M[20],Jet_leadTrackPt[20],Jet_Flav[20];
  float Jet_leptonPt[20],Jet_leptonPtRel[20],Jet_leptonDeltaR[20];
  float Jet_nHEFrac[20],Jet_nEMEFrac[20],Jet_chMult[20];
  float Jet_vtxPt[20],Jet_vtxMass[20],Jet_vtx3DVal[20],Jet_vtxNtracks[20],Jet_vtx3DSig[20];
  float Jet_PartonFlav[20],Jet_PartonPt[20];

  

  InputChain->SetBranchAddress("Evt_Odd",&Event_Odd);            
  InputChain->SetBranchAddress("N_Jets",&NJets);                      
  InputChain->SetBranchAddress("Evt_Rho",&rho);                       
  InputChain->SetBranchAddress("Weight",&Event_Weight);               

  InputChain->SetBranchAddress("Jet_Pt",&Jet_pt);                     
  InputChain->SetBranchAddress("Jet_corr",&Jet_corr);                 
  InputChain->SetBranchAddress("Jet_Eta",&Jet_Eta);                   
  InputChain->SetBranchAddress("Jet_M",&Jet_M);                       
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



  //Set up output tree
  outputFile->cd();
  TTree *OutputTree = new TTree("bRegTree","Tree for bJetRegression training");

  float E_Odd, E_Rho, E_Weight,J_Pt,J_corr,J_Eta,J_M,J_lTPt,J_Flav,J_lPt,J_lPtRel,J_lDR,J_nhef,J_nemef,J_chM,J_vPt,J_vM,J_vV,J_vNt,J_vS,J_PF,J_PPt;

  OutputTree->Branch("Evt_Odd",&E_Odd);                 
  OutputTree->Branch("Evt_Rho",&E_Rho);                       
  OutputTree->Branch("Weight",&E_Weight);               

  OutputTree->Branch("Jet_Pt",&J_Pt);                     
  OutputTree->Branch("Jet_corr",&J_corr);                 
  OutputTree->Branch("Jet_Eta",&J_Eta);                   
  OutputTree->Branch("Jet_M",&J_M);                       
  OutputTree->Branch("Jet_leadTrackPt",&J_lTPt);   
  OutputTree->Branch("Jet_Flav",&J_Flav);             

  OutputTree->Branch("Jet_leptonPt",&J_lPt);         
  OutputTree->Branch("Jet_leptonPtRel",&J_lPtRel);   
  OutputTree->Branch("Jet_leptonDeltaR",&J_lDR); 

  OutputTree->Branch("Jet_nHEFrac",&J_nhef);           
  OutputTree->Branch("Jet_nEmEFrac",&J_nemef);         
  OutputTree->Branch("Jet_chargedMult",&J_chM);        

  OutputTree->Branch("Jet_vtxPt",&J_vPt);               
  OutputTree->Branch("Jet_vtxMass",&J_vM);           
  OutputTree->Branch("Jet_vtx3DVal",&J_vV);         
  OutputTree->Branch("Jet_vtxNtracks",&J_vNt);     
  OutputTree->Branch("Jet_vtx3DSig",&J_vS);         

  OutputTree->Branch("Jet_PartonFlav",&J_PF);     
  OutputTree->Branch("Jet_PartonPt",&J_PPt);



  //Fill output tree
  long nEvents = InputChain->GetEntries();
  for(long i = 0; i<nEvents; i++) {
    
    InputChain->GetEvent(i);
    
    for(int j = 0; j < NJets; j++) {
      E_Odd = Event_Odd;
      E_Rho = rho;
      E_Weight = Event_Weight;  
      
      J_Pt = Jet_pt[j];
      J_corr = Jet_corr[j];
      J_Eta = Jet_Eta[j];
      J_M = Jet_M[j];
      J_lTPt = Jet_leadTrackPt[j];
      J_Flav = Jet_Flav[j];
      J_lPt = Jet_leptonPt[j];
      J_lPtRel = Jet_leptonPtRel[j];
      J_lDR = Jet_leptonDeltaR[j];
      J_nhef = Jet_nHEFrac[j];
      J_nemef = Jet_nEMEFrac[j];
      J_chM = Jet_chMult[j];
      J_vPt = Jet_vtxPt[j];
      J_vM = Jet_vtxMass[j];
      J_vV = Jet_vtx3DVal[j];
      J_vNt = Jet_vtxNtracks[j];
      J_vS = Jet_vtx3DSig[j];
      J_PF = Jet_PartonFlav[j];
      J_PPt = Jet_PartonPt[j];
      
      OutputTree->Fill();
    }
  }

  OutputTree->Write();

}


int main(   ) {
  MakeTreeforbReg();
}
