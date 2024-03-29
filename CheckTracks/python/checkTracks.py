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
# Get alignment from local db

#process.GlobalTag.toGet = cms.VPSet(
#    cms.PSet(
#        record = cms.string('GEMAlignmentRcd'),
#        tag = cms.string("TBGEMAlignment_test"),
#        connect = cms.string("sqlite:MyAlignment.db"),
#    ),
#    cms.PSet(
#        record = cms.string('GEMAlignmentErrorExtendedRcd'),
#        tag = cms.string("TBGEMAlignmentErrorExtended_test"),
#        connect = cms.string("sqlite:MyAlignment.db"),
#    )
#)


#process.load('Configuration.Geometry.GeometryExtended2026D87Reco_cff')

process.maxEvents.input = cms.untracked.int32(10)

process.gemTrAli = cms.EDAnalyzer('CheckTracks',
                                  gemRecHitLabel = cms.InputTag("gemRecHits"),
                                  track1=cms.InputTag("GEMTrackFinder1"),
                                  track2=cms.InputTag("GEMTrackFinder2"),
                                  track3=cms.InputTag("GEMTrackFinder3"),
                                  track4=cms.InputTag("GEMTrackFinder4")
)

process.source = cms.Source("PoolSource",                           
#  fileNames = cms.untracked.vstring('file:../../../gemsw/EventFilter/test/output2_edm.root'),
  fileNames = cms.untracked.vstring('file:../../../gemsw/EventFilter/test/output_edm_track.root'),
                            labelRawDataLikeMC = cms.untracked.bool(False)

)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tbAnalysis.root") )

process.tbtrali = cms.Path(process.gemTrAli)
