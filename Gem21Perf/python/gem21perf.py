import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TRALI',eras.phase2_muon)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.CondDBESSource_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('gemsw.Geometry.GeometryTestBeam_cff')
#process.load("Geometry.GEMGeometryBuilder.gemGeometryDB_cfi")

from RecoMuon.TrackingTools.MuonServiceProxy_cff import MuonServiceProxy
MuonServiceProxy.ServiceParameters.Propagators.append('StraightLinePropagator')
MuonServiceProxy.ServiceParameters.GEMLayers = cms.bool(True)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')

process.maxEvents.input = cms.untracked.int32(-1)

process.gemTBGE21 = cms.EDAnalyzer('CheckTracks',
                                  gemRecHitLabel = cms.InputTag("gemRecHits"),
                                  extRecHitLabel = cms.InputTag("ExtrapolationFinder1"),
)

process.source = cms.Source("PoolSource",                           
  fileNames = cms.untracked.vstring('file:output_edm_track.root'),
                            labelRawDataLikeMC = cms.untracked.bool(False)

)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tbAnalysis.root") )

process.tbge21 = cms.Path(process.gemTBGE21)
