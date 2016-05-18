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
  //TString outfilename("test.root");
  char* outfilename = getenv("OUTPUTFILE");
  TFile* outputFile = new TFile( outfilename, "RECREATE" );
  

  //Set up input tree
  TChain* InputChain = new TChain("MVATree");
  //TString filenames = "/nfs/dust/cms/user/kschweig/JetRegression/trees0209/ttbar_nominal.root";
  char* filenames = getenv("INPUTFILES");
  string buf;
  stringstream ss(filenames); 
  while (ss >> buf){
    InputChain->Add(buf.c_str());  
  }


  int Event_Odd, NJets, NPV;
  float rho, Event_Weight, PU_Weight;
  float Jet_pt[20],Jet_rawpt[20],Jet_corr[20],Jet_corr_raw[20],Jet_Eta[20],Jet_M[20],Jet_Mt[20],Jet_leadTrackPt[20],Jet_Flav[20],Jet_PFlav[20];
  float Jet_leptonPt[20],Jet_leptonPtRel[20],Jet_leptonDeltaR[20];
  float Jet_nHEFrac[20],Jet_cHEFrac[20],Jet_nEMEFrac[20],Jet_totHEFrac[20], Jet_chMult[20];
  float Jet_vtxPt[20],Jet_vtxMass[20],Jet_vtx3DVal[20],Jet_vtxNtracks[20],Jet_vtx3DSig[20];
  float Jet_PartonFlav[20],Jet_PartonPt[20],Jet_PartonDeltaR[20];

  

  InputChain->SetBranchAddress("Evt_Odd",&Event_Odd);            
  InputChain->SetBranchAddress("N_Jets",&NJets);                      
  InputChain->SetBranchAddress("Evt_Rho",&rho);                       
  InputChain->SetBranchAddress("Weight",&Event_Weight);
  InputChain->SetBranchAddress("Weight_PU",&PU_Weight);
  InputChain->SetBranchAddress("N_PrimaryVertices", &NPV);

  InputChain->SetBranchAddress("Jet_Pt",&Jet_pt);                     
  InputChain->SetBranchAddress("Jet_rawPt",&Jet_rawpt);                     
  InputChain->SetBranchAddress("Jet_corr",&Jet_corr);                 
  InputChain->SetBranchAddress("Jet_corr_rawJet",&Jet_corr_raw);                 
  InputChain->SetBranchAddress("Jet_Eta",&Jet_Eta);                   
  InputChain->SetBranchAddress("Jet_M",&Jet_M);                       
  InputChain->SetBranchAddress("Jet_Mt",&Jet_Mt);                       
  InputChain->SetBranchAddress("Jet_leadTrackPt",&Jet_leadTrackPt);   
  InputChain->SetBranchAddress("Jet_Flav",&Jet_Flav);                 
  InputChain->SetBranchAddress("Jet_PartonFlav",&Jet_PFlav);                 

  InputChain->SetBranchAddress("Jet_leptonPt",&Jet_leptonPt);         
  InputChain->SetBranchAddress("Jet_leptonPtRel",&Jet_leptonPtRel);   
  InputChain->SetBranchAddress("Jet_leptonDeltaR",&Jet_leptonDeltaR); 

  InputChain->SetBranchAddress("Jet_nHEFrac",&Jet_nHEFrac);           
  InputChain->SetBranchAddress("Jet_cHEFrac",&Jet_cHEFrac);
  InputChain->SetBranchAddress("Jet_totHEFrac",&Jet_totHEFrac);           
  InputChain->SetBranchAddress("Jet_nEmEFrac",&Jet_nEMEFrac);         
  InputChain->SetBranchAddress("Jet_chargedMult",&Jet_chMult);        

  InputChain->SetBranchAddress("Jet_vtxPt",&Jet_vtxPt);               
  InputChain->SetBranchAddress("Jet_vtxMass",&Jet_vtxMass);           
  InputChain->SetBranchAddress("Jet_vtx3DVal",&Jet_vtx3DVal);         
  InputChain->SetBranchAddress("Jet_vtxNtracks",&Jet_vtxNtracks);     
  InputChain->SetBranchAddress("Jet_vtx3DSig",&Jet_vtx3DSig);         

  InputChain->SetBranchAddress("Jet_MatchedPartonFlav",&Jet_PartonFlav);     
  InputChain->SetBranchAddress("Jet_MatchedPartonPt",&Jet_PartonPt);         
  InputChain->SetBranchAddress("Jet_MatchedPartonDeltaR",&Jet_PartonDeltaR);         



  //Set up output tree
  outputFile->cd();
  TTree *OutputTree = new TTree("bRegTree","Tree for bJetRegression training");

  float E_Odd, E_Rho, N_PV,  E_Weight,P_Weight,J_Pt,J_rawPt,J_corr,J_corr_raw,J_Eta,J_M,J_Mt,J_lTPt,J_Flav,J_lPt,J_lPtRel,J_lDR,J_nhef,J_chef,J_nemef,J_chM,J_vPt,J_vM,J_vV,J_vNt,J_vS,J_PF,J_PPt, J_RPJ, J_RLJ, J_RVJ,J_PDR,J_PFlav,J_tothef;

  OutputTree->Branch("Evt_Odd",&E_Odd);                 
  OutputTree->Branch("Evt_Rho",&E_Rho);                       
  OutputTree->Branch("Weight",&E_Weight);          
  OutputTree->Branch("Weight_PU",&P_Weight);          
  
  OutputTree->Branch("N_PrimaryVertices",&N_PV);

  OutputTree->Branch("Jet_Pt",&J_Pt);                     
  OutputTree->Branch("Jet_rawPt",&J_rawPt);                     
  OutputTree->Branch("Jet_corr",&J_corr);                 
  OutputTree->Branch("Jet_corr_rawJet",&J_corr_raw);                 
  OutputTree->Branch("Jet_Eta",&J_Eta);                   
  OutputTree->Branch("Jet_M",&J_M);                       
  OutputTree->Branch("Jet_Mt",&J_Mt);                       
  OutputTree->Branch("Jet_leadTrackPt",&J_lTPt);   
  OutputTree->Branch("Jet_Flav",&J_Flav);             
  OutputTree->Branch("Jet_PartonFlav",&J_PFlav);             

  OutputTree->Branch("Jet_leptonPt",&J_lPt);         
  OutputTree->Branch("Jet_leptonPtRel",&J_lPtRel);   
  OutputTree->Branch("Jet_leptonDeltaR",&J_lDR); 

  OutputTree->Branch("Jet_nHEFrac",&J_nhef);           
  OutputTree->Branch("Jet_cHEFrac",&J_chef);           
  OutputTree->Branch("Jet_totHEFrac", &J_tothef);
  OutputTree->Branch("Jet_nEmEFrac",&J_nemef);         
  OutputTree->Branch("Jet_chargedMult",&J_chM);        

  OutputTree->Branch("Jet_vtxPt",&J_vPt);               
  OutputTree->Branch("Jet_vtxMass",&J_vM);           
  OutputTree->Branch("Jet_vtx3DVal",&J_vV);         
  OutputTree->Branch("Jet_vtxNtracks",&J_vNt);     
  OutputTree->Branch("Jet_vtx3DSig",&J_vS);         

  OutputTree->Branch("Jet_MatchedPartonFlav",&J_PF);     
  OutputTree->Branch("Jet_MatchedPartonPt",&J_PPt);
  OutputTree->Branch("Jet_MatchedPartonDeltaR",&J_PDR);

  OutputTree->Branch("Jet_PtRatioPartonJet",&J_RPJ);
  OutputTree->Branch("Jet_PtRatioLeptonJet",&J_RLJ);
  OutputTree->Branch("Jet_PtRatioVertexJet",&J_RVJ);

  //Fill output tree
  long nEvents = InputChain->GetEntries();
  for(long i = 0; i<nEvents; i++) {
    
    InputChain->GetEvent(i);
    
    float tottmp;

    for(int j = 0; j < NJets; j++) {
      E_Odd = Event_Odd;
      E_Rho = rho;
      E_Weight = Event_Weight;  
      P_Weight = PU_Weight;
      N_PV = NPV;
      J_Pt = Jet_pt[j];
      J_rawPt = Jet_rawpt[j];
      J_corr = Jet_corr[j];
      J_corr_raw = Jet_corr_raw[j];
      J_Eta = Jet_Eta[j];
      J_M = Jet_M[j];
      J_Mt = Jet_Mt[j];
      J_lTPt = Jet_leadTrackPt[j];
      J_Flav = Jet_Flav[j];
      J_PFlav = Jet_PFlav[j];
      J_lPt = Jet_leptonPt[j];
      J_lPtRel = Jet_leptonPtRel[j];
      J_lDR = Jet_leptonDeltaR[j];
      J_nhef = Jet_nHEFrac[j];
      J_chef = Jet_cHEFrac[j];
      J_nemef = Jet_nEMEFrac[j];
      if (J_nemef > 1) {  J_nemef = 1;  }
      tottmp = J_nhef + J_chef;
      if (tottmp >= 1) {  J_tothef = 1;  }
      else {  J_tothef = tottmp;  }
      J_chM = Jet_chMult[j];
      J_vPt = Jet_vtxPt[j];
      J_vM = Jet_vtxMass[j];
      J_vV = Jet_vtx3DVal[j];
      J_vNt = Jet_vtxNtracks[j];
      J_vS = Jet_vtx3DSig[j];
      J_PF = Jet_PartonFlav[j];
      J_PPt = Jet_PartonPt[j];
      J_PDR = Jet_PartonDeltaR[j];
      J_RPJ = Jet_PartonPt[j] / Jet_pt[j];
      J_RLJ = Jet_leptonPt[j] / Jet_pt[j];
      J_RVJ = Jet_vtxPt[j] / Jet_pt[j];

      OutputTree->Fill();
    }
  }

  OutputTree->Write();

}


int main(   ) {
  MakeTreeforbReg();
}
