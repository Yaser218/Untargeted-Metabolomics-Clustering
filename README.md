# Untargeted Metabolomics Feature Clustering - data folder

This page contains the supporting files for the paper *VOCCluster: Untargeted Metabolomics Feature Clustering Approach for Clinical Breath Gas Chromatography - Mass Spectrometry Data* by Alkhalifah et al. (2019).

The data folder contains the following files:

- **Dataset.csv**  contains all VOCs from all samples. Each row in the Dataset represents a VOC. Sample number, VOC number, RI and m/z intensities are required for each VOC. This file is used by all of the algorithms.

- **Cosine_Matrix.csv** contains the cosine distance similarity between all VOCs in the Dataset. This matrix can be generated after checking RIs alignments between samples. This can be done by running RI_Variation command which is located in VOCCluster folder. This file is used by all of the algorithms.

- **TargetedVOCs.csv** file is only required for VOCCluster, not the others. This file contains the targeted VOCs that are used to check the alignments of the RIs in the samples.

- **RI_Report.csv** is the generated file after running the  RI_Variation command. This file will help the operator to check the alignments of the RIs in all samples. If an error sample is noted, the sample must be corrected and the operation is repeated.

- **load.pkl** is the generated file after running the  RI_Variation command. This file will be used with VOCCluster to pass the delta RI and the calculated epsilon.



## Checking out the whole project

Use the following command to clone the whole repository. This will give you all the executables, input_data and evaluation scripts used in the paper.

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
