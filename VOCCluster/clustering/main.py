#!/usr/bin/env python
"""
    - Clustering class will be used to cluster all similar VOCs in the dataset.
    - input:
        -   load.pkl which is generated from RI_Variation class and stored in the data folder.
        -   Cosine_Matrix.csv which is generated from Generate_cosine_matrix class and stored in data folder.
    - output:
        - cluster list.
        - Each value in the list indicates the cluster number corresponding to
        the same indexing in the dataset.
    @author: Yaser Alkhalifah, Jan - 2019
"""
import os
import pickle
import cosine_matrix_generation
import clustering

def main():
    """
        The main function to start calling clustering classes.
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'data'))
    if os.path.isfile('{0}/{1}'.format(path, 'load.pkl')):
        pickle_in = open('{0}/{1}'.format(path, 'load.pkl'), 'rb')
        load = pickle.load(pickle_in)
        #cosine_matrix_generation.Matrix_generator(load, path)
        if not os.path.isfile('{0}/{1}'.format(path, 'Cosine_Matrix.csv')):
            print 'Error: cosine matrix has to be calculated and stored in data folder.'
            exit()
        cosine_file = open('{0}/{1}'.format(path, 'Cosine_Matrix.csv'), 'r')
        cosine_matrix = list(cosine_file)
        results = clustering.VOCCluster(cosine_matrix, load.dataset, len(load.loaded_samples), load.epsilon, 2)
        my_labels = results.run()
        print my_labels
        n_clusters_ = len(set(my_labels)) - (1 if 0 in my_labels else 0)
        print ('Estimated number of VOCCluster clusters: %d' % n_clusters_)
    else:
        print 'Please run VOC_neighbours before running the clustering code'
        exit()

if __name__ == '__main__':
    main()
