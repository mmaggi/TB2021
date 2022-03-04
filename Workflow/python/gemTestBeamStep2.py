import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.register('include20x10',
                 False,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Include 20x10 chamber in the geometry")
options.parseArguments()

process = cms.Process("GEMTracker")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.options = cms.untracked.PSet(
    wantSummary=cms.untracked.bool(True),
    SkipEvent=cms.untracked.vstring('ProductNotFound'),
)

debug = False
#debug = True
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cout.threshold = cms.untracked.string('INFO')
process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
#process.MessageLogger.debugModules = cms.untracked.vstring('*')
#process.MessageLogger.suppressWarning= cms.untracked.vstring('GEMRawToDigiModule')
if debug:
    process.MessageLogger.cerr.threshold = "DEBUG"
    process.MessageLogger.debugModules = ["source", "muonGEMDigis"]
    process.maxEvents.input = cms.untracked.int32(100)
else:
    process.MessageLogger.cerr.FwkReport.reportEvery = 5000

#process.source = cms.Source("GEMStreamSource",
#                            fileNames=cms.untracked.vstring(
#                            options.inputFiles),   
#                            firstLuminosityBlockForEachRun=cms.untracked.VLuminosityBlockID({})
#)

process.source = cms.Source("PoolSource",                           
                            fileNames = cms.untracked.vstring(options.inputFiles),
                            labelRawDataLikeMC = cms.untracked.bool(False)
)
print(options.inputFiles)

# this block ensures that the output collection is named rawDataCollector, not source
process.rawDataCollector = cms.EDAlias(source=cms.VPSet(
    cms.PSet(type=cms.string('FEDRawDataCollection'))))

process.load('EventFilter.GEMRawToDigi.muonGEMDigis_cfi')
process.muonGEMDigis.InputLabel = cms.InputTag("rawDataCollector")
process.muonGEMDigis.fedIdStart = cms.uint32(1477)
process.muonGEMDigis.fedIdEnd = cms.uint32(1478)
process.muonGEMDigis.skipBadStatus = cms.bool(True)
process.muonGEMDigis.useDBEMap = True

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
if options.include20x10 :
    process.GlobalTag.toGet = cms.VPSet(cms.PSet(record=cms.string("GEMeMapRcd"),
                                                 tag=cms.string("GEMeMapTestBeam"),
                                                 connect=cms.string("sqlite_fip:gemsw/EventFilter/data/GEMeMap_TestBeam_with_20x10.db")))
else :
    process.GlobalTag.toGet = cms.VPSet(cms.PSet(record=cms.string("GEMeMapRcd"),
                                                 tag=cms.string("GEMeMapTestBeam"),
                                                 connect=cms.string("sqlite_fip:gemsw/EventFilter/data/GEMeMap_TestBeam.db")))

process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(
        record = cms.string('GEMAlignmentRcd'),
        tag = cms.string("TBGEMAlignment_test"),
        connect = cms.string("sqlite:MyAlignment_4_30g.db"),
    ),
    cms.PSet(
        record = cms.string('GEMAlignmentErrorExtendedRcd'),
        tag = cms.string("TBGEMAlignmentErrorExtended_test"),
        connect = cms.string("sqlite:MyAlignment_4_30g.db"),
    )
)

process.load('gemsw.Geometry.GeometryTestBeam_cff')
process.load('MagneticField.Engine.uniformMagneticField_cfi')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.MuonServiceProxy.ServiceParameters.Propagators.append('StraightLinePropagator')
process.load('TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi')
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.SteppingHelixPropagatorAny.useMagVolumes = cms.bool(False)

process.GEMTrackFinder = cms.EDProducer("GEMTrackFinder",
                                        process.MuonServiceProxy,
                                        gemRecHitLabel = cms.InputTag("gemRecHits"),
                                        maxClusterSize = cms.int32(10),
                                        minClusterSize = cms.int32(1),
                                        trackChi2 = cms.double(1000.0),
                                        skipLargeChamber = cms.bool(True),
                                        excludingChambers = cms.vint32(-1),
                                        use1DSeeds = cms.bool(False), 
                                        MuonSmootherParameters = cms.PSet(
                                           PropagatorAlong = cms.string('SteppingHelixPropagatorAny'),
                                           PropagatorOpposite = cms.string('SteppingHelixPropagatorAny'),
                                           RescalingFactor = cms.double(5.0)
                                        ),
)
process.GEMTrackFinder.ServiceParameters.GEMLayers = cms.untracked.bool(True)
process.GEMTrackFinder.ServiceParameters.CSCLayers = cms.untracked.bool(False)
process.GEMTrackFinder.ServiceParameters.RPCLayers = cms.bool(False)

process.GEMTrackFinderAl1 =process.GEMTrackFinder.clone()
process.GEMTrackFinderAl1.excludingChambers = cms.vint32(0)
process.GEMTrackFinderAl2 =process.GEMTrackFinder.clone()
process.GEMTrackFinderAl2.excludingChambers = cms.vint32(1)
process.GEMTrackFinderAl3 =process.GEMTrackFinder.clone()
process.GEMTrackFinderAl3.excludingChambers = cms.vint32(2)
process.GEMTrackFinderAl4 =process.GEMTrackFinder.clone()
process.GEMTrackFinderAl4.excludingChambers = cms.vint32(3)


process.ExtrapGE21 = cms.EDProducer("GEMTrakExtrapoler", 
                                    process.MuonServiceProxy,
                                    trackLabel=cms.InputTag("GEMTrackFinder"),
                                    recHitLabel = cms.InputTag("gemRecHits"),
                                    doprint = cms.bool(False)
)

process.ExtrapTrCh1 = cms.EDProducer("GTRTrakExtrapoler", 
                                     process.MuonServiceProxy,
                                     trackLabel=cms.InputTag("GEMTrackFinderAl1"),
                                     TrackChamber=cms.uint32(1),                                     
                                     recHitLabel = cms.InputTag("gemRecHits"),
                                     doprint = cms.bool(False)                                     
)
process.ExtrapTrCh2=process.ExtrapTrCh1.clone()
process.ExtrapTrCh2.trackLabel=cms.InputTag("GEMTrackFinderAl2")
process.ExtrapTrCh2.TrackChamber=cms.uint32(2)
process.ExtrapTrCh2.doprint = cms.bool(False)

process.ExtrapTrCh3=process.ExtrapTrCh1.clone()
process.ExtrapTrCh3.trackLabel=cms.InputTag("GEMTrackFinderAl3")
process.ExtrapTrCh3.TrackChamber=cms.uint32(3)
process.ExtrapTrCh3.doprint = cms.bool(False)

process.ExtrapTrCh4=process.ExtrapTrCh2.clone()
process.ExtrapTrCh4.trackLabel=cms.InputTag("GEMTrackFinderAl4")
process.ExtrapTrCh4.TrackChamber=cms.uint32(4)
process.ExtrapTrCh4.doprint = cms.bool(False)



process.load("CommonTools.UtilAlgos.TFileService_cfi")
process.TFileService.fileName = cms.string("AnalysisTB.root") 
process.TestBeamTrackAnalyzer = cms.EDAnalyzer("TestBeamTrackAnalyzer",
                                               gemRecHitLabel = cms.InputTag("gemRecHits"),
                                               tracks = cms.InputTag("GEMTrackFinder"),
                                               )
process.perTrFilter = cms.EDFilter("PerfTrack",
                                       recHitLabel = cms.InputTag("gemRecHits")
)
#process.perTrPath = cms.Path(process.perTrFilter)

process.output = cms.OutputModule("PoolOutputModule",
                                  outputCommands=cms.untracked.vstring(
                                      "keep *_*_*_*",
                                      "drop FEDRawDataCollection_source_*_*"
                                  ),
                                  fileName=cms.untracked.string(
                                      'output_edm_track_4_30g.root'),
#                                  SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('reco'))

)

#process.load("DQM.Integration.config.environment_cfi")
#process.load('DQM.GEM.GEMDQM_cff')

#process.dqmEnv.subSystemFolder = "GEM"
#process.dqmEnv.eventInfoFolder = "EventInfo"
#process.dqmSaver.path = ""
#process.dqmSaver.tag = "GEM"

#process.unpack = cms.Path(process.muonGEMDigis)
#process.reco = cms.Path(process.gemRecHits * process.perTrFilter)# * process.GEMTrackFinder)
process.track = cms.Path(process.GEMTrackFinder*process.GEMTrackFinderAl1*process.GEMTrackFinderAl2*process.GEMTrackFinderAl3*process.GEMTrackFinderAl4*process.ExtrapGE21*process.ExtrapTrCh1*process.ExtrapTrCh2*process.ExtrapTrCh3*process.ExtrapTrCh4)
#process.track_ana = cms.Path(process.TestBeamTrackAnalyzer)
#process.dqm = cms.Path(process.GEMDQM)
#process.dqm.remove(process.GEMDAQStatusSource)
#process.dqmout = cms.EndPath(process.dqmEnv + process.dqmSaver)
process.outpath = cms.EndPath(process.output)
#process.sched = cms.Schedule(process.muonGEMDigis,process.gemRecHits,process.outpath)
