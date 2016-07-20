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
  float rho, Event_Weight, PU_Weight, LeptonSF;
  float Jet_pt[20],Jet_rawpt[20],Jet_corr[20],Jet_corr_raw[20],Jet_Eta[20],Jet_M[20],Jet_Mt[20],Jet_leadTrackPt[20],Jet_Flav[20],Jet_PFlav[20],Jet_regcorr;
  float Jet_leptonPt[20],Jet_leptonPtRel[20],Jet_leptonDeltaR[20];
  float Jet_nHEFrac[20],Jet_cHEFrac[20], Jet_chMult[20];
  float Jet_nEMEFrac[20],Jet_JESnEMEFrac[20],Jet_JESandRnEMEFrac[20],Jet_rawEnEMEFrac[20],Jet_idnEMEFrac[20];
  float Jet_totHEFrac[20],Jet_JEStotHEFrac[20],Jet_JESandRtotHEFrac[20],Jet_rawEtotHEFrac[20],Jet_idtotHEFrac[20];
  float Jet_vtxPt[20],Jet_vtxMass[20],Jet_vtx3DVal[20],Jet_vtxNtracks[20],Jet_vtx3DSig[20];
  float Jet_PartonFlav[20],Jet_PartonPt[20],Jet_PartonDeltaR[20];
  float Jet_helperL1[20], Jet_helperL3[20], Jet_helperJER[20];
  float Jet_GenJetPt[20];


  InputChain->SetBranchAddress("Evt_Odd",&Event_Odd);
  InputChain->SetBranchAddress("N_RegJets",&NJets);
  InputChain->SetBranchAddress("Weight",&Event_Weight);
  InputChain->SetBranchAddress("Weight_PU",&PU_Weight);
  InputChain->SetBranchAddress("N_PrimaryVertices", &NPV);
  InputChain->SetBranchAddress("Weight_LeptonSF", &LeptonSF);


  InputChain->SetBranchAddress("RegJet_preregPt",&Jet_pt);
  InputChain->SetBranchAddress("RegJet_corr",&Jet_corr);
  InputChain->SetBranchAddress("RegJet_regcorr",&Jet_regcorr);
  InputChain->SetBranchAddress("RegJet_Eta",&Jet_Eta);
  InputChain->SetBranchAddress("RegJet_M",&Jet_M);
  InputChain->SetBranchAddress("RegJet_Mt",&Jet_Mt);
  InputChain->SetBranchAddress("RegJet_leadTrackPt",&Jet_leadTrackPt);
  InputChain->SetBranchAddress("RegJet_Flav",&Jet_Flav);
  InputChain->SetBranchAddress("RegJet_PartonFlav",&Jet_PFlav);

  InputChain->SetBranchAddress("RegJet_leptonPt",&Jet_leptonPt);
  InputChain->SetBranchAddress("RegJet_leptonPtRel",&Jet_leptonPtRel);
  InputChain->SetBranchAddress("RegJet_leptonDeltaR",&Jet_leptonDeltaR);

  InputChain->SetBranchAddress("RegJet_nHEFrac",&Jet_nHEFrac);
  InputChain->SetBranchAddress("RegJet_cHEFrac",&Jet_cHEFrac);
  InputChain->SetBranchAddress("RegJet_chargedMult",&Jet_chMult);

  InputChain->SetBranchAddress("RegJet_nEmEFrac",&Jet_nEMEFrac);

  InputChain->SetBranchAddress("RegJet_totHEFrac",&Jet_totHEFrac);

  InputChain->SetBranchAddress("RegJet_vtxPt",&Jet_vtxPt);
  InputChain->SetBranchAddress("RegJet_vtxMass",&Jet_vtxMass);
  InputChain->SetBranchAddress("RegJet_vtx3DVal",&Jet_vtx3DVal);
  InputChain->SetBranchAddress("RegJet_vtxNtracks",&Jet_vtxNtracks);
  InputChain->SetBranchAddress("RegJet_vtx3DSig",&Jet_vtx3DSig);

  InputChain->SetBranchAddress("RegJet_MatchedPartonFlav",&Jet_PartonFlav);
  InputChain->SetBranchAddress("RegJet_MatchedPartonPt",&Jet_PartonPt);
  InputChain->SetBranchAddress("RegJet_MatchedPartonDeltaR",&Jet_PartonDeltaR);
  InputChain->SetBranchAddress("RegJet_MatchedGenJetwNuPt",&Jet_GenJetPt);

  //Set up output tree
  outputFile->cd();
  TTree *OutputTree = new TTree("bRegTree","Tree for bJetRegression training");

  float E_Odd, E_Rho, N_PV, LSF, E_Weight,P_Weight,J_Pt,J_rawPt,J_corr,J_corr_raw,J_Eta,J_M,J_Mt,J_lTPt,J_Flav,J_lPt,J_lPtRel,J_lDR,J_nhef,J_chef,J_nemef,J_chM,J_vPt,J_vM,J_vV,J_vNt,J_vS,J_PF,J_PPt, J_RPJ, J_RLJ, J_RVJ,J_PDR,J_PFlav,J_tothef,J_JEStothef,J_JESandRtothef,J_rawEtothef,J_idtothef,J_JESnemef,J_JESandRnemef,J_rawEnemef,J_idnemef,J_helperL1,J_helperL3,J_corrhelper,J_corrhelperJESandR, J_GJPt;

  OutputTree->Branch("Evt_Odd",&E_Odd);
  OutputTree->Branch("Weight",&E_Weight);
  OutputTree->Branch("Weight_PU",&P_Weight);
  OutputTree->Branch("Weight_LeptonSF",&LSF);

  OutputTree->Branch("N_PrimaryVertices",&N_PV);

  OutputTree->Branch("Jet_Pt",&J_Pt);
  OutputTree->Branch("Jet_corr",&J_corr);
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
  OutputTree->Branch("Jet_chargedMult",&J_chM);

  OutputTree->Branch("Jet_totHEFrac", &J_tothef);

  OutputTree->Branch("Jet_nEmEFrac",&J_nemef);

  OutputTree->Branch("Jet_vtxPt",&J_vPt);
  OutputTree->Branch("Jet_vtxMass",&J_vM);
  OutputTree->Branch("Jet_vtx3DVal",&J_vV);
  OutputTree->Branch("Jet_vtxNtracks",&J_vNt);
  OutputTree->Branch("Jet_vtx3DSig",&J_vS);

  OutputTree->Branch("Jet_MatchedPartonFlav",&J_PF);
  OutputTree->Branch("Jet_MatchedPartonPt",&J_PPt);
  OutputTree->Branch("Jet_MatchedPartonDeltaR",&J_PDR);
  OutputTree->Branch("Jet_MatchedGenJetwNuPt",&J_GJPt);

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
      LSF = LeptonSF;

      J_Pt = Jet_pt[j];
      J_corr = Jet_corr[j];
      J_Eta = Jet_Eta[j];
      J_M = Jet_M[j]/Jet_regcorr[j];
      J_Mt = Jet_Mt[j]/Jet_regcorr[j];
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

      J_tothef = Jet_totHEFrac[j];
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
      J_GJPt = Jet_GenJetPt[j];

      OutputTree->Fill();
    }
  }

  OutputTree->Write();

}


int main(   ) {
  MakeTreeforbReg();
}
