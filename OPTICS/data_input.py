"""
    data_load is class will upload the dataset file which is located in data folder.
    @author: Yaser Alkhalifah, Jan - 2019
"""
import os
import numpy as np

class DataLoad:
    def __init__(self, data_file):
        self.data_file = data_file
        self.loaded_samples = []
        self.samples = []
    def data_input(self):
        """
            This function to load dataset into dataset array.
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        if not os.path.isfile('{0}/{1}.csv'.format(path, self.data_file)):
            print 'Error: Dataset file is not exist.'
            exit()
        # Uplead Dataset.csv file.
        f = open('{0}/{1}.csv'.format(path, self.data_file), 'r')
        print 'Now uploading dataset File.....'
        f = list(f)
        # The Dataset contains heading, number of lines - heading
        self.number_of_VOCs = sum(1 for row in f)-1
        # Count number of columns, last column's value is empty, that is why -1.
        self.number_of_columns = len(f[0].split(',')) -1
        self.first_m_z = int(f[0].split(',')[3])    # find the first m/z value.
        self.last_m_z = int(f[0].split(',')[-2])    # find the last m/z value.
        print 'dataset includes ', self.number_of_VOCs, 'VOCs in all samples '
        print ('dataset includes ', self.number_of_columns, ' Columns, ',
               'm/z values start from ', self.first_m_z,
               'and end ', self.last_m_z)
        # Create a matrix with a shape of (number_of_VOCs X number_of_columns) filled with zeros.
        self.dataset = np.zeros((self.number_of_VOCs,
                                 self.number_of_columns))
        for line in range(1, len(f)):
            if int(float(f[line].strip().split(',')[0])) not in self.loaded_samples:
                self.loaded_samples.append(int(float(f[line].strip().split(',')[0])))
            for column in range(self.number_of_columns):
                self.dataset[line-1][column] = int(float(f[line].strip().split(',')[column]))
