# DBSCAN clustering algoritherm

This page contains the supporting files for the paper *VOCCluster: Untargeted Metabolomics Feature Clustering Approach for Clinical Breath Gas Chromatography - Mass Spectrometry Data* by Alkhalifah et al. (2019).

- **main.py**  is the main executable script for the DBSCAN. It has been implemented in Python. DBSCAN requires two parameters to be entered which are epsilon and minPts.


- **data_input.py** contains a script to load the data from the file Dataset.csv which is located in the data folder. The Dataset file has to be formatted as in the file and also will be explained down.

- **dbscan.py** contains a script of DBSCAN algorithm. It clusters the input dataset based on the concept of the algorithm by taking into account that no more than one point from the same sample has to be in a cluster.


## Required libraries

The program depends on the following Python library:
* sys
* os
* numpy

## Required data files

DBSCAN requires two data files to be located in the data folder which are:
*   Dataset file which is a file that contains all VOCs from all samples. Dataset file must contain sample#, VOC#, RI and m/z (e.g. 40:450) for each VOC.
*   Cosine_Matrix file which is a file that contains the distance similarity between VOCs. The cosine function was used to calculate the similarity between VOCs. The matrix shape should be m*m, where m is the number of VOCs in the Dataset file.

## Getting Started

DBSCAN can be run using  on your local machine by typing the following on terminal:
```
python main.py epsilon minPts    # where epsilon and minPts are the preferred values.
```
## Output

This algorithm will label all VOCs in the dataset. Similar VOCs are given same cluster value where the non-cluster VOC will be given a -1 label.

