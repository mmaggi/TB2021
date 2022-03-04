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

