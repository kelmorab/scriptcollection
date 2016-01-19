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

using namespace std;

void MakeTreeforbReg(   ) 
{
  
  TString outfilename("bRegTree.root");
  TFile* outputFile = new TFile( outfilename, "RECREATE" );
  
  TFile *input(0);
  TString fname = "/nfs/dust/cms/user/kschweig/JetRegression/testtrees/jetreg_0113_1_nominal_Tree.root";
   
  if (!gSystem->AccessPathName( fname )) {
    input = TFile::Open( fname ); // check if file in local directory exists
  }
  if (!input) {
    std::cout << "ERROR: could not open data file" << std::endl;
    exit(1);
  }


  //Set up Input Tree
  TTree *InputTree = (TTree*)input->Get("MVATree");

  int Event_Odd, NJets;
  float rho, Event_Weight;
  float Jet_pt[20],Jet_corr[20],Jet_Eta[20],Jet_M[20],Jet_leadTrackPt[20],Jet_Flav[20];
  float Jet_leptonPt[20],Jet_leptonPtRel[20],Jet_leptonDeltaR[20];
  float Jet_nHEFrac[20],Jet_nEMEFrac[20],Jet_chMult[20];
  float Jet_vtxPt[20],Jet_vtxMass[20],Jet_vtx3DVal[20],Jet_vtxNtracks[20],Jet_vtx3DSig[20];
  float Jet_PartonFlav[20],Jet_PartonPt[20];

  

  InputTree->SetBranchAddress("Evt_Odd",&Event_Odd);            
  InputTree->SetBranchAddress("N_Jets",&NJets);                      
  InputTree->SetBranchAddress("Evt_Rho",&rho);                       
  InputTree->SetBranchAddress("Weight",&Event_Weight);               

  InputTree->SetBranchAddress("Jet_Pt",&Jet_pt);                     
  InputTree->SetBranchAddress("Jet_corr",&Jet_corr);                 
  InputTree->SetBranchAddress("Jet_Eta",&Jet_Eta);                   
  InputTree->SetBranchAddress("Jet_M",&Jet_M);                       
  InputTree->SetBranchAddress("Jet_leadTrackPt",&Jet_leadTrackPt);   
  InputTree->SetBranchAddress("Jet_Flav",&Jet_Flav);                 

  InputTree->SetBranchAddress("Jet_leptonPt",&Jet_leptonPt);         
  InputTree->SetBranchAddress("Jet_leptonPtRel",&Jet_leptonPtRel);   
  InputTree->SetBranchAddress("Jet_leptonDeltaR",&Jet_leptonDeltaR); 

  InputTree->SetBranchAddress("Jet_nHEFrac",&Jet_nHEFrac);           
  InputTree->SetBranchAddress("Jet_nEmEFrac",&Jet_nEMEFrac);         
  InputTree->SetBranchAddress("Jet_chargedMult",&Jet_chMult);        

  InputTree->SetBranchAddress("Jet_vtxPt",&Jet_vtxPt);               
  InputTree->SetBranchAddress("Jet_vtxMass",&Jet_vtxMass);           
  InputTree->SetBranchAddress("Jet_vtx3DVal",&Jet_vtx3DVal);         
  InputTree->SetBranchAddress("Jet_vtxNtracks",&Jet_vtxNtracks);     
  InputTree->SetBranchAddress("Jet_vtx3DSig",&Jet_vtx3DSig);         

  InputTree->SetBranchAddress("Jet_PartonFlav",&Jet_PartonFlav);     
  InputTree->SetBranchAddress("Jet_PartonPt",&Jet_PartonPt);         



  //Set up Output Tree
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



  //Fill Output Tree
  int nEvents = InputTree->GetEntries();
  for(int i = 0; i<nEvents; i++) {
    
    InputTree->GetEvent(i);
    
    for(int j = 0; j < NJets; j++) {
      E_Odd = Event_Odd;
      E_Rho = rho;
      E_Weight = Event_Weight;  
      
      J_Pt = Jet_pt[j];
      if (J_Pt == 0) {
	cout << J_Pt << endl;
      }
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

  OutputTree->Write("bRegTree.root");
  
  

}
