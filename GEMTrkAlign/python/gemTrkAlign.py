import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TRALI',eras.phase2_muon)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.CondDBESSource_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('gemsw.Geometry.GeometryTestBeam_cff')


process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')

process.maxEvents.input = cms.untracked.int32(-1)

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)
process.gemTrkAli = cms.EDAnalyzer('GEMTrkAlign',
                                   gemRecHitLabel = cms.untracked.InputTag("gemRecHits"),
                                   extrackge21=cms.untracked.InputTag("ExtrapGE21","Extrapolated"),
                                   extrackgt01=cms.untracked.InputTag("ExtrapTrCh1","Extrapolated"),
                                   extrackgt02=cms.untracked.InputTag("ExtrapTrCh2","Extrapolated"),
                                   extrackgt03=cms.untracked.InputTag("ExtrapTrCh3","Extrapolated"),
                                   extrackgt04=cms.untracked.InputTag("ExtrapTrCh4","Extrapolated")
)

process.source = cms.Source("PoolSource",                           
  fileNames = cms.untracked.vstring('file:../../../gemsw/EventFilter/test/output_edm_track12.root'),
                            labelRawDataLikeMC = cms.untracked.bool(False)

)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tbAnalysis.root") )

process.tbtrali = cms.Path(process.gemTrkAli)
