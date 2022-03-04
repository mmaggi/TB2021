# TB2021

standard set up instruction 

```bash
cmsrel CMSSW_12_2_0_pre1
cd CMSSW_12_2_0_pre1/src
cmsenv
git cms-init -q
git cms-merge-topic jshlee:mapping_update_v0.5
git clone https://github.com/gem-sw/gemsw.git
scram b -j 10
```

Test Beam analysis set up
```bash
git clone https://github.com/mmaggi/TB2021
cd TB2021
scram b -j 10
```

Workflows:
```bash
cd Workflow/python
```

Step1, unpacking and local reconstruction
```bash
cmsRun gemTestBeamStep1.py inputFiles=file:filename maxEvents=Nevts
``` 

Step2, global reconstruction using the alignment db and track extrapolations to all tracking chambers (excluding the chamber to extrapolate) and track extrapolation to GE21
```bash
cmsRun gemTestBeamStep1.py inputFiles=file:filename maxEvents=Nevts
``` 

the two arguments are mandatory to set: inputFiles requires the file: protocol to to the filename including the entire path.
maxEvents requires an integer number representing the number of events to process, -1 in case all events shall be processed.

