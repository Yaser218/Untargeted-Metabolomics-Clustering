# VOCCluster algoritherm - cosin matrix and clustering

This page contains the supporting files for the paper *VOCCluster: Untargeted Metabolomics Feature Clustering Approach for Clinical Breath Gas Chromatography - Mass Spectrometry Data* by Alkhalifah et al. (2019).

- **main.py**  is the main executable script to generate the cosine matrix and the clustering preocess. It has been implemented in Python. It reads two files from data folderh are Dataset.csv and load.pkl.


- **cosine_matrix_generation.py** contains a script to calculate the similarty between VOCs based on a RI range for each one. It will generate a matrix which is stored in the data folder.


- **cosine_calculations.py** contains a script of cosine similarity calculation. This class is imported by cosine_matrix_generation.


- **clustering.py** contains a script of the VOCCluster clustering concept. The clustering will take place afer the similarty matrix is generated.



## Required libraries

The program depends on the following Python library:

* os
* numpy
* math
* pickle
* multiprocessing

## Required data files

Clustering requires two data files to be located in the data folder which are:
*   Dataset file which is a file that contains all VOCs from all samples. Dataset file must contain sample#, VOC#, RI and m/z (e.g. 40:450) for each VOC.
*   load file which is a file that contains RI varation and the calculated epsilon. 

## Getting Started

DBSCAN can be run using  on your local machine by typing the following on terminal:
```python main.py Dataset.csv TargetedVOCs.csv   # where dataset and TargetedVOCs are the used files name in the data folder. this command will set the default epsilon value = 0.98
```
```python main.py Dataset.csv TargetedVOCs.csv epsilon   # where dataset and TargetedVOCs are the used files name in the data folder. epsilon is the preferred value > 0 and <= 1.
```
## Output

The output here is a report that is generated and stored in the data folder.

