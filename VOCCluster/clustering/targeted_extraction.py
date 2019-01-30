#!/usr/bin/env python2
#encoding: UTF-8
"""
    - This class will upload the dataset and targeted VOCs files which are located in the data folder.
    - It will search in the dataset about all of the targeted VOCs.
    - It uses threashold = 0.98 unless a different value has been passed.
    - At the end, a report will be generated and located in the data folder.
    @author: Yaser Alkhalifah, Jan - 2019
"""
import os
import numpy as np
import cosine_calculations


class Targeted:

    def __init__(self, data_file, targ_file, path, threshold=0.98):
        self.data_file = path + '/' + data_file
        self.targ_file = path + '/' + targ_file
        self.path = path
        self.threshold = threshold
        print 'Used threshold = ', self.threshold
        self.loaded_samples = []
        self.label = []
        self.retention_index = []
        self.ri_vary = []
        self.samples = []
        self.epsilon = 1
        # Load dataset, which includes heading and values
        f = open('{0}'.format(self.data_file), 'r')
        f = list(f)
        number_of_vocs = sum(1 for row in f)-1 # -1 heading
        number_of_columns = len(f[0].split(','))
        self.first_m_z = int(f[0].split(',')[3])
        self.last_m_z = int(f[0].split(',')[-1])
        print 'dataset includes ', number_of_vocs, 'VOCs in all samples '
        print 'dataset includes ', number_of_columns, ' Columns, ', 'm/z values start from ', self.first_m_z, 'and end ', self.last_m_z
        # Create a matrix with a shape of (number_of_vocs X number_of_columns) filled with zeros.
        self.dataset = np.zeros((number_of_vocs,
                                 number_of_columns))
        # Fill in the matrix with the values.
        print 'Now uploading the targeted VOCs File.....'
        for line in range(1, len(f)):
            if int(float(f[line].strip().split(',')[0])) not in self.loaded_samples:
                self.loaded_samples.append(int(float(f[line].strip().split(',')[0])))
            for column in range(number_of_columns):
                self.dataset[line-1][column] = int(float(f[line].strip().split(',')[column]))
        # Load Targeted VOCs into the targeted_vocs array
        f = open('{0}'.format(self.targ_file), 'r')
        f = list(f)
        number_of_targeted = sum(1 for row in f)
        print   'Number of targeted VOCs that have been uploaded : ', number_of_targeted
        self.targeted_vocs = np.zeros((number_of_targeted, 4))
        for line in range(number_of_targeted):
            for column in range(4):
                self.targeted_vocs[line][column] = int(float(f[line].strip().split(',')[column]))




    ##################################################################
    # This function to start clustering targeted compounds and stared in label(contains VOC index + cosine distance value). Then calculate Delta RI for each segment. The segmented RI points and Delta RI are then stored in self.ri_vary.
    def extract_targeted(self):
        """
            This function to extract all targeted VOCs from all samples.
        """
        print 'Searching about targeted VOCs ...'
        cosine = cosine_calculations.Cosine(self.dataset)
        for targ in range(len(self.targeted_vocs)):
            for voc_index in range(len(self.dataset)):# Find the targeted VOC
                if self.targeted_vocs[targ][0] == self.dataset[voc_index][0] and self.targeted_vocs[targ][1] == self.dataset[voc_index][1]:
                    self.label.append([voc_index])
                    self.samples.append([self.targeted_vocs[targ][0]])
                    self.retention_index.append([int(self.targeted_vocs[targ][2])])
                    break
            while True: # Extract all similar VOCs from all samples and clusrter them...
                no_update = 0
                for voc_index in range(len(self.dataset)):
                    local_targeted_compound = []
                    if self.dataset[voc_index][0] not in self.samples[targ] and self.dataset[voc_index][2] in range(int(self.targeted_vocs[targ][2]), int(self.targeted_vocs[targ][3])):
                        for local_index in range(voc_index, len(self.dataset)):# extract all VOCs in particular sample and cluster the highest cosine VOC
                            if self.dataset[local_index][2] in range(int(self.targeted_vocs[targ][2]), int(self.targeted_vocs[targ][3])):
                                compared_m_z = cosine.normalisation(local_index)
                                for clu in range(len(self.label[targ])):
                                    targ_m_z = cosine.normalisation(self.label[targ][clu])
                                    if cosine.cosine_similarity(targ_m_z, compared_m_z) >= self.threshold:
                                        local_targeted_compound.append([local_index, cosine.cosine_similarity(targ_m_z, compared_m_z)])
                            else:
                                break
                    if len(local_targeted_compound) >= 1:
                        no_update == 1
                        local_targeted_compound.sort(key=lambda tup: tup[1], reverse=True)
                        self.label[targ].append(local_targeted_compound[0][0])
                        self.samples[targ].append(self.dataset[local_targeted_compound[0][0]][0])
                        self.retention_index[targ].append(int(self.dataset[local_targeted_compound[0][0]][2]))
                if no_update == 0:
                    print 'VOC ', targ, ' was found in samples = ', len(self.label[targ]), ' Max RI = ', max(self.retention_index[targ]), ', min = ', min(self.retention_index[targ]), ' and delta RI = ', max(self.retention_index[targ]) -  min(self.retention_index[targ])
                    break
        # Now testing all the clusters to find the max distance between 2 VOCs from the same cluster,and fill in self.ri_vary.
        for clu in range(len(self.label)):
            if clu == len(self.label)-1:
                self.ri_vary.append([(max(self.retention_index[clu-1])+ min(self.retention_index[clu]))/2, max(self.retention_index[clu]) -  min(self.retention_index[clu])])
            else:
                self.ri_vary.append([(max(self.retention_index[clu])+ min(self.retention_index[clu+1]))/2, max(self.retention_index[clu]) -  min(self.retention_index[clu])])

            for in_clust in range(len(self.label[clu])):
                for in_clust2 in range(len(self.label[clu])):
                    if in_clust != in_clust2:
                        if cosine.cosine_similarity(cosine.normalisation(self.label[clu][in_clust]), cosine.normalisation(self.label[clu][in_clust2])) < self.epsilon:
                            self.epsilon = cosine.cosine_similarity(cosine.normalisation(self.label[clu][in_clust]), cosine.normalisation(self.label[clu][in_clust2]))
        print 'Epsilon = ', self.epsilon
        self.ri_vary.sort(key=lambda tup: tup[0], reverse=False)
        self.ri_variation_report()
    # Create a CSV report contains all Targeted clusters...
    def ri_variation_report(self):
        """
            All targeted VOCs that have been found will be reported in
            a CSV file in order to check the alignment.
            """
        result_file = open(self.path + '/' + 'RI_Report.csv', 'w')
        result_file.write('Sample#'+",")
        result_file.write('VOC#'+",")
        result_file.write('RI'+",")
        for m_z in range(self.first_m_z, self.last_m_z+1):
            result_file.write(str(m_z)+",")
        result_file.write("\n")
        for clu in range(len(self.label)):
            for in_clust in range(len(self.label[clu])):
                result_file.write(str(self.dataset[int(self.label[clu][in_clust])][0])+",")
                result_file.write(str(self.dataset[int(self.label[clu][in_clust])][1])+",")
                result_file.write(str(self.dataset[int(self.label[clu][in_clust])][2])+",")
                for voc in range(3, len(self.dataset[self.label[clu][in_clust]])):
                    result_file.write(str(self.dataset[int(self.label[clu][in_clust])][voc])+",")
                result_file.write("\n")
            result_file.write('##########################################################')
            result_file.write("\n")
            result_file.write(''+",")
            result_file.write('MaxRI'+",")
            result_file.write(str(max(self.retention_index[clu]))+",")
            result_file.write("\n")
            result_file.write(''+",")
            result_file.write('MinRI'+",")
            result_file.write(str(min(self.retention_index[clu]))+",")
            result_file.write("\n")
            result_file.write(''+",")
            result_file.write('Delta RI'+",")
            result_file.write(str(max(self.retention_index[clu])-min(self.retention_index[clu]))+",")
            result_file.write("\n")
            result_file.write(''+",")
            result_file.write('RI COV %'+",")
            result_file.write(str(np.std(self.retention_index[clu])/np.mean(self.retention_index[clu])*100)+",")
            result_file.write("\n")
            result_file.write('##########################################################')
            result_file.write("\n")
        result_file.close()
