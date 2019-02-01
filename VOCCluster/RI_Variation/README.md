# VOCCluster algoritherm - RI Variation

This page contains the supporting files for the paper *VOCCluster: Untargeted Metabolomics Feature Clustering Approach for Clinical Breath Gas Chromatography - Mass Spectrometry Data* by Alkhalifah et al. (2019).

- **main.py**  is the main executable script to calculate the RI variations. It has been implemented in Python. It requires the files name to be entered which are Dataset.csv and TargetedVOCs.csv. Epsilon is an optional third parameter can be entered after the files name. Default epsilon is applied if the epsilon is not entered which is equal to 0.98.


- **targeted_extraction.py** contains a script to load the data from the file Dataset.csv and the targeted VOCs which are located in the data folder. Clusters of targeted VOCs are extracted by calculating the cosine similarity between VOCs.


- **cosine_calculations.py** contains a script of cosine similarity calculation.



## Required libraries

The program depends on the following Python library:
* sys
* os
* numpy
* math
* pickle

## Required data files

RI Variation requires two data files to be located in the data folder which are:
*   Dataset file which is a file that contains all VOCs from all samples. Dataset file must contain sample#, VOC#, RI and m/z (e.g. 40:450) for each VOC.
*   Targeted VOCs file which is a file that contains an example of the targeted VOCs which are required to be extracted from all samples.

## Getting Started

DBSCAN can be run on your local machine by typing the following on terminal:
```
python main.py Dataset.csv TargetedVOCs.csv   # where dataset and TargetedVOCs are the used files name in the data folder.
                                              # The command will set the default epsilon value = 0.98
```
```
python main.py Dataset.csv TargetedVOCs.csv epsilon   # where dataset and TargetedVOCs are the used files name in the data folder. epsilon is the preferred value > 0 and <= 1.
```
## Output

The output here is a report that is generated and stored in the data folder.

