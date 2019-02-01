# Untargeted Metabolomics Feature Clustering

This page contains the supporting files for the paper *VOCCluster: Untargeted Metabolomics Feature Clustering Approach for Clinical Breath Gas Chromatography - Mass Spectrometry Data* by Alkhalifah et al. (2019).

- **data**  contains the files that are required to be uploaded into the VOCCluster, DBSCAN and OPTICS. Generated files from the algorithms are stored in the data folder.

- **DBSCAN** contains DBSCAN algorithm that is coded in Python. DBSCAN has been tuned to cluster deconvoluted GCMS data. It will not cluster more than one VOC from a sample in a cluster.

- **OPTICS** contains OPTICS algorithm that is coded in Python. OPTICS has been tuned to cluster deconvoluted GCMS data. It will not cluster more than one VOC from a sample in a cluster.

- **VOCCluster** contains VOCCluster algorithm that is coded in Python. It is a novel clustering technique that is able to cluster similar VOCs from different deconvoluted DCMS breath data.

- Note: All of the algorithms read the required files from data folder to generate clusters for the given data.



## Checking out the whole project

Use the following command to clone the whole repository. This will give you all the executables, input_data and evaluation scripts used in the paper.


```
git clone https://github.com/Yaser218/Untargeted-Metabolomics-Clustering.git
```
