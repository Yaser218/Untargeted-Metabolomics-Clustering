"""
    dbscan is class will start clustering the dataset file which is located in the data folder.
    It uses the cousin matrix file which is in the data folder.
    The cosine matrix contains all similarity distances between all VOCs that is precalculated.
    The output will be a list.
    The list contains a cluster value for each VOC.
    Non cluster VOC is given a -1 value.
    @author: Yaser Alkhalifah, Jan - 2019
"""
import os
import numpy

class Dbscan:
    def __init__(self, dataset, min_pts, eps):
        self.dataset = dataset
        self.min_pts = min_pts
        self.eps = eps
        self.labels = [0]  * len(self.dataset)
        self.voc_similarity = [0]  * len(self.dataset)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        if os.path.isfile('{0}/{1}'.format(path, 'Cosine_Matrix.csv')):
            print 'Cosine distance has been calculated and now is being loaded...............'
            cosine_file = open('{0}/{1}'.format(path, 'Cosine_Matrix.csv'), 'r')
            self.cosine_matrix = list(cosine_file)
        else:
            print 'Error: cosine matrix is not exist'
            exit()
    def DBSCAN(self):
        print 'Start DBSCAN clustering...'
        self.C = 0
        for P in range(0, len(self.dataset)):
            if not (self.labels[P] == 0):
                continue
            neighbor_pts = self.region_query(P)
            if len(neighbor_pts) < self.min_pts:
                self.labels[P] = -1
            else:
                self.C += 1
                self.grow_custer(P, neighbor_pts)

        return self.labels
    def grow_custer(self, P, neighbor_pts):
        self.labels[P] = self.C
        cluster_files = []
        cluster_files.append(self.dataset[P][0])
        i = 0
        while i < len(neighbor_pts):
            Pn = neighbor_pts[i]
            if self.dataset[Pn][0] not in cluster_files:
                if self.labels[Pn] == -1:
                    self.labels[Pn] = self.C
                    cluster_files.append(self.dataset[Pn][0])
                
                elif self.labels[Pn] == 0:
                    self.labels[Pn] = self.C
                    cluster_files.append(self.dataset[Pn][0])
                    Pnneighbor_pts = self.region_query(Pn)
                    if len(Pnneighbor_pts) >= self.min_pts:
                        neighbor_pts = neighbor_pts + Pnneighbor_pts
            i += 1
    def region_query(self, P):
        neighbors = []
        data_files = []
        neighbors_all = []
        row = self.cosine_matrix[P].split(',')
        for index in range(len(row)-1):
            if float(row[index]) >= self.eps and self.labels[index] <= 0:
                neighbors_all.append([index, float(row[index])])
        neighbors_all.sort(key=lambda tup: tup[1], reverse=True)
        for index in range(len(neighbors_all)):
            if self.dataset[neighbors_all[index][0]][0] not in data_files:
                data_files.append(self.dataset[neighbors_all[index][0]][0])
                neighbors.append(neighbors_all[index][0])
        return neighbors
