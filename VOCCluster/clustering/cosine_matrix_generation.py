#!/usr/bin/env python2
#encoding: UTF-8
"""
    This class will be called once the alignments are accepted.
    Here, VOCCluster will start calculating the similarity of the VOCs
    that appear at the same RI range.
    @author: Yaser Alkhalifah, Jan - 2019
"""

import os
import multiprocessing
import cosine_calculations

class Matrix_generator:

    def __init__(self, load, path):
        self.load = load
        self.path = path
        self.cosine = cosine_calculations.Cosine(self.load.dataset)
        self.load_matrix()

    def multi_process(self, st, ed, name):
        """
            - Create a process to calculate cosine similarity for a selected number of samples.
            - Store the values into CSV file.
        """
        result_file = open(self.path + '/' + '{0}.csv'.format(name), 'w')
        for sample in range(st, ed):
            print 'sample number  ', sample
            for voc_index in range(len(self.load.dataset)):
                if self.load.dataset[voc_index][0] == sample:
                    targ_m_z = self.cosine.normalisation(voc_index)
                    delta = 0
                    # To find delta RI based on VOC RI
                    for find_delta in range(len(self.load.ri_vary)):
                        if self.load.dataset[voc_index][2] in range(0, self.load.ri_vary[0][0]):
                            delta = self.load.ri_vary[0][1]
                            break
                        elif find_delta == len(self.load.ri_vary) - 1:
                            delta = self.load.ri_vary[find_delta][1]
                            break
                        elif self.load.dataset[voc_index][2] in range(self.load.ri_vary[find_delta][0], self.load.ri_vary[find_delta+1][0]):
                            delta = self.load.ri_vary[find_delta][1]
                            break
                    for voc_index2 in range(len(self.load.dataset)):
                        if self.load.dataset[voc_index2][0] != sample:
                            if self.load.dataset[voc_index2][2] in range(int(self.load.dataset[voc_index][2] - delta), int(self.load.dataset[voc_index][2] + delta)):
                                compared_m_z = self.cosine.normalisation(voc_index2)
                                result_file.write(str(self.cosine.cosine_similarity(targ_m_z, compared_m_z)) + ",")

                            else:
                                result_file.write(str('0') + ",")
                        else:
                            result_file.write(str('0') + ",")
                    result_file.write("\n")

        result_file.close()

    # load distance matrix into a CSV file .
    def load_matrix(self):
        """
            Calculate the PC's core number and take 75% of the cores to create processes.
            Each process will calculate the cosine similarity for a number of samples.
            Each process will create a (Cosine_TableX.CSV) file, where X is the process number.
            Finally, All of the processes files will be combined into a single file called (Cosine_Matrix.csv).
        """
        cores_number = multiprocessing.cpu_count()
        cores_required = int(cores_number * 0.75)
        samples_per_process = len(self.load.loaded_samples) / cores_required
        print 'Number of cors are  ', cores_number
        p_process = []
        process_num = 0
        first_sample = 0
        last_sample = 0
        while True:
            process_num += 1
            first_sample = last_sample
            if process_num == cores_required:
                last_sample = len(self.load.loaded_samples)
            else:
                last_sample = first_sample + samples_per_process
            P = multiprocessing.Process(target=self.multi_process, args=(first_sample, last_sample, 'Cosine_Table{0}'.format(first_sample)))
            p_process.append(P)
            if process_num == cores_required:
                break
        for i in p_process:
            i.start()
        for i in p_process:
            i.join()
        result_file = open(self.path + '/' + 'Cosine_Matrix.csv', 'w')
        first_sample = 0
        last_sample = 0
        while True:
            first_sample = last_sample
            last_sample = first_sample + samples_per_process
            if os.path.isfile(self.path + '/' + 'Cosine_Table{0}.csv'.format(first_sample)):
                print 'The cosine table is loading...... ', 'Cosine_Table{0}.csv'.format(first_sample)
                f = open(self.path+ '/' + 'Cosine_Table{0}.csv'.format(first_sample), 'rb')
                for row in f:
                    result_file.write(row)
                f.close()
                os.remove(self.path + '/' + 'Cosine_Table{0}.csv'.format(first_sample))
            else:
                result_file.close()
                break
