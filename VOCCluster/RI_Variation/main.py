#!/usr/bin/env python
"""
    This is the main script for calculating the variations between RIs.
    Input:
        Required:
            - Two data files must be entered.
            - One is the dataset file which contains all VOCs from all samples.
            - Second is the targeted VOCs file.
        Optional:
            - A threshold parameter which is used to cluster the targeted VOCs.
            - Default threshold = 0.98.
    Outputs:
        - A report will be generated containing:
            - Clusters of the targeted VOCs.
            - Minimum, maximum, delta and coefficient of variation
                for RIs in each cluster are calculated.
        - A pickle file for the process is generated in order to be used
            in building the distance matrix.
    Note:
        - The process should be repeated once alignments are not fulfiled the requirements.
    @author: Yaser Alkhalifah, Jan - 2019
"""
import os
import sys
import pickle
import targeted_extraction

def main():
    """
        The main function to start calling classes.
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '../data'))
    if len(sys.argv) > 2:
        if os.path.isfile('{0}/{1}'.format(path, sys.argv[1])):
            if os.path.isfile(path + '/' + '{0}'.format(sys.argv[2])):
                if len(sys.argv) > 3:
                    if float(sys.argv[3]) <= 1 and float(sys.argv[3]) > 0:
                        load = targeted_extraction.Targeted(sys.argv[1], sys.argv[2], path, float(sys.argv[3]))
                        load.extract_targeted()
                        pickle_out = open(path + '/' +'load.pkl', 'wb')
                        pickle.dump(load, pickle_out)
                    else:
                        print 'Please enter a threshold between 0 to 1'
                else:
                    load = targeted_extraction.Targeted(sys.argv[1], sys.argv[2], path)
                    load.extract_targeted()
                    pickle_out = open(path + '/' +'load.pkl', 'wb')
                    pickle.dump(load, pickle_out)
            else:
                print 'Please enter the right thargeted VOCs file name.'
        else:
            print 'Please enter the right dataset file name.'
    else:
        print "Please make sure that you entered:\n - The dataset file name and the targeted VOCs file name which are located in data folder.\n - Optional epsilon."

if __name__ == '__main__':
    main()
