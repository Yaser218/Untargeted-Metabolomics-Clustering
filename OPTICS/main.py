#encoding: UTF-8
"""
    OPTICS was tested as a pat of the our expermint
    in the papaer:
    'VOCCluster:Untargeted Metabolomics Feature clustering Approach for
    Clinical BreathGas Chromatography - Mass Spectrometry Data'
    OPTICS was designed to cluster same VOCs from a given number of metabolomics samples.
    It will not include more than one element in a cluster from the same sample.
    TO run OPTICS, a dataset is required in the format that is mentioned in the paper.
    The dataset that was used in the paper is included in the data folder.
    The main class takes 2 inputs which are epsilon and minPts.
    The main will process all of the required classes.
    The output will be a cluster list.
    Each value in the list indicates the cluster number corresponding to
    the same indexing in the dataset.
    @author: Yaser Alkhalifah, Jan - 2019
    """
import sys
import data_input
import optics


def main():
    if len(sys.argv) > 2:
        if float(sys.argv[1]) <= 1 and float(sys.argv[1]) > 0:
            if int(sys.argv[2]) > 0:
                load = data_input.DataLoad('Dataset')
                load.data_input()
                optics_ = optics.OPTICS(load.dataset, int(sys.argv[2]), float(sys.argv[1]))
                optics_.run()
                mylabels = optics_.label(float(sys.argv[1]))
                n_clusters_ = len(set(mylabels)) - (1 if -1 in mylabels else 0)
                print 'Estimated number of OPTICS clusters: %d' % n_clusters_
            else:
                print "Please enter valid minPts value"
        else:
            print "Please pass an eps between 0 to 1."
    else:
        print "Please enter epsilon and minPts values ..."


if __name__ == "__main__":
    main()
