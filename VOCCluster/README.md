# VOCCluster algorithm

This page contains the supporting files for the paper *VOCCluster: Untargeted Metabolomics Feature Clustering Approach for Clinical Breath Gas Chromatography - Mass Spectrometry Data* by Alkhalifah et al. (2019).


This algorithm contains two processes. Each process has been allocated in a folder:
- **RI_Variation**  folder contains a process to calculate the RI variations between samples. This process requires two inputs which are Daraset and TargetedVOCs. The output of this preocess will be a report that is checked by the operator before running the next process.

- **clustering** folder contains a process to build the cosine matrix and the clustering. The matrix will be stored in the data folder.
