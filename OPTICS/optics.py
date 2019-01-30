"""
    OPTICS is class will start clustering the dataset file which is located in the data folder.
    It uses the cousin matrix file which is in the data folder.
    The cosine matrix contains all similarity distances between all VOCs that is precalculated.
    The output will be a list.
    The list contains a cluster value for each VOC.
    Non cluster VOC is given a -1 value.
    @author: Yaser Alkhalifah, Jan - 2019
"""
import os

class OPTICS:
    def __init__(self, dataset, min_pts, eps):
        self.dataset = dataset
        self.min_pts = min_pts
        self.eps = eps
        self.cd = [0]  * len(self.dataset)  # core distance
        self.rd = [0]  * len(self.dataset)     # reachability distance
        self.processed = [0]  * len(self.dataset)  # Does this point has been processed?
        self.ordered = []
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        if os.path.isfile('{0}/{1}'.format(path, 'Cosine_Matrix.csv')):
            print 'Cosine distance has been calculated and now is being loaded...............'
            cosine_file = open('{0}/{1}'.format(path, 'Cosine_Matrix.csv'), 'r')
            self.cosine_matrix = list(cosine_file)
        else:
            print 'Error: cosine matrix is not exist'
            exit()
    def run(self):
        print 'Now starting OPTICS clustering ...'
        # for each unprocessed point (p)...
        for p in range(0, len(self.dataset)):
            if self.processed[p] == 0:
                data_files = []
                # mark p as processed
                self.processed[p] = 1
                self.ordered.append(p)
                data_files.append(self.dataset[p][0])
                # find p's neighbors
                point_neighbors = self.neighbors(p)
                # if p has a core_distance, i.e has min_cluster_size - 1 neighbors
                if self._core_distance(p, point_neighbors) != 0:
                    seeds = []
                    self._update(point_neighbors, p, seeds)
                    # as long as we have unprocessed neighbors...
                    while(seeds):
                        # find the neighbor n with smallest reachability distance
                        seeds.sort(key=lambda tup: tup[1], reverse=True)
                        n = seeds.pop(0)
                        if self.dataset[n[0]][0] not in data_files:
                            self.rd[n[0]] = n[1]
                            data_files.append(self.dataset[n[0]][0])
                            # mark n as processed
                            self.processed[n[0]] = 1
                            self.ordered.append(n[0])
                            # find n's neighbors
                            n_neighbors = self.neighbors(n[0])
                            # if n has a core_distance...
                            if self._core_distance(n[0], n_neighbors) != 0:
                                self._update(n_neighbors, n[0], seeds)
        return self.ordered
    def _core_distance(self, point, _neighbors):
    
        if self.cd[point] != 0: return self.cd[point]
        if len(_neighbors) >= self.min_pts:
            self.cd[point] = _neighbors[self.min_pts - 1][1]
        
        return self.cd[point]
    def _update(self, _neighbors, point, seeds):
        
        # for each of point's unprocessed neighbors n...
        for n in _neighbors:
            if self.processed[n[0]] == 0:
                # find new reachability distance new_rd
                # if rd is 0, keep new_rd and add n to the seed list
                new_rd = min(self.cd[point], n[1])
                if self.rd[n[0]] == 0:
                    #self.rd[n[0]] = new_rd
                    seeds.append([n[0], new_rd])
                # otherwise if new_rd > old rd, means that object
                # is already in the queue.  Object is moved further
                # to the top of the queue if their new reachability-distance
                # is smaller than their previous reachability-distance.
                elif new_rd > self.rd[n[0]]:
                    if [n[0], self.rd[n[0]]] in seeds:
                        seeds.remove([n[0], self.rd[n[0]]])
                        #self.rd[n[0]] = new_rd
                        seeds.append([n[0], new_rd])
                    else:
                       #self.rd[n[0]] = new_rd
                        #self.ordered.remove(n[0])
                        seeds.append([n[0], new_rd])

    def label(self, cluster_threshold):
        labels = [-1]  * len(self.dataset)
        cluster_id = 0
        for object in range(len(self.ordered)):
        
            if self.rd[self.ordered[object]] < cluster_threshold:
                if self.cd[self.ordered[object]] >= cluster_threshold:
                    cluster_id = cluster_id +1
                    labels[self.ordered[object]] = cluster_id
            else:
                 labels[self.ordered[object]] = cluster_id
    
        return labels
    def neighbors(self, p):
        _neighbors = []
        data_files = []
        neighbors_all = []
        row = self.cosine_matrix[p].split(',')
        for index in range(len(row)-1):
            if float(row[index]) >= self.eps and self.processed[index] == 0:
                neighbors_all.append([index, float(row[index])])
        neighbors_all.sort(key=lambda tup: tup[1], reverse=True)
        for index in range(len(neighbors_all)):
            if self.dataset[neighbors_all[index][0]][0] not in data_files:
                data_files.append(self.dataset[neighbors_all[index][0]][0])
                _neighbors.append(neighbors_all[index])
        return _neighbors
