---
title: High performance computing for microscopy data analysis

---


[[@anesCrystalPhaseMapping2018]]
## Data management on HPC
[[@alewijnse2017]][[@poger2023]] [[@assuncao2015]] [[@caplinsWorkflowImaging2D2019]]
- how to handle the large datasets? NAS? Cluster? What is available to us?
- Copy from 
- Preprocessing to handle only reduce files and compute woth original data/ full dataset once the script/code is set?

![[cluster.svg]]
> *Fig 0: a) cluster, pc, XNAS, compute nodes, login nodes etc.

**HPC OMNI Uni Siegen:**
- 439 nodes with 64 kernels and 256 GB RAM
- over 10 GPUs
- two smp nodes/fat nodes with 1536 gb ram and 4 cpus
- central file system/regular file system, 10TB; holds the home dirs


# Microscopy data anlaysis using py4DSTEM
[[@savitzkypy4DSTEMOpenSource2019]] [[@savitzkyArchitectureDevelopmentCycle2023]][[@bruefach2023]][[@ophus2022]]
- python is a general purpose programming language, increasingly popular in science, good for data analysis alongside R, AI, ML, etc.
- heavy processing needed because of the large amount of data
- basic features, provide screenshots/code snippets, maybe examples of the syntax with listings package

## Load data and examine the datacube

## Basic visualization and virtual imaging


## Reading, writing and file structure

![[filetree.svg|300]]
> *Fig 0: Example of a filestructure...*





