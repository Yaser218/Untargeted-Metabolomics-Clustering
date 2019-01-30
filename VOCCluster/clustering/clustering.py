"""
    This is the VOCCluster clustering class. It will label all the dataset based on given thresholds.
    @author: Yaser Alkhalifah - Jan 2019
"""

class VOCCluster:
    """
        - This class takes a cosine_matrix (similarity distance for all neighbours of each victor (VOC) in the dataset),
        - It will returen a list of cluster labels. The lable 0 represents a noise.
        - The clusters are numbered starting from 1.
    """
    
    def __init__(self, cosine_matrix, dataset, samples_number, epsilon, min_pts):
        self.dataset = dataset
        self.min_pts = min_pts
        self.epsilon = epsilon
        self.samples_number = samples_number
        # The label list will hold the found cluster assignment for each victor in the dataset
        # The list will be filed by zeros which means that the victor has not considered yet.
        # Once the victor has been labled, it will have the labe value instad of zero.
        # If the victor did not attend any cluster, it will be assined as a noise (-1).
        self.label = [0]  * len(self.dataset)
        # voc_similarity is a list that contains cosine threshold value for each victor in the dataset that has been clustered.
        # The list will be filed by zeros which means that the victor has not considered yet.
        self.voc_similarity = [0] * len(cosine_matrix)
        self.cosine_matrix = cosine_matrix
        # number_of_clusters is the ID of the current cluster.
        self.number_of_clusters = 0
        self.vocs_branches = [[0, 0, 0, 0, 0]] * len(cosine_matrix)
        self.files_in_cluster = []

    def run(self):
        print 'Now start VOCCluster clustering technique'
        for P in range(0, len(self.dataset)):
            if self.label[P] == 0:
                neighbor_pts, x = self.region_query(P)
                if len(neighbor_pts) >= self.min_pts:
                    self.files_in_cluster = [[0, 0]] * self.samples_number
                    self.number_of_clusters += 1
                    print '*** New cluster ', self.number_of_clusters
                    self.new_custer(P, neighbor_pts)
        return self.label


    def new_custer(self, P, neighbor_pts):
        '''
            - This function is to start a new cluster.
            - It will search in all neighbours to find the high similarity points.
            - All of the found neighbours will be give the same cluster value.
            - Points that were pre-clustered and are close to this cluster will be moved to this cluster.
        '''
        # Give the established_point a cluster value.
        self.label[P] = self.number_of_clusters
        self.voc_similarity[P] = neighbor_pts[0][1]
        self.files_in_cluster[int(self.dataset[P][0])] = [P, neighbor_pts[0][1]]
        self.vocs_branches[P] = [P, 1, P, 1]
        while (neighbor_pts):
            # Extract the most similar neighbour.
            Pn = neighbor_pts.pop(0)
            if self.label[Pn[0]] == 0 and self.files_in_cluster[int(self.dataset[Pn[0]][0])] == [0, 0]:
                # If the extracted neighbour was not labelled yet,
                # find its neighbours and add them to the neighbours' list.
                # Give the extracted point the same cluster value.
                pn_neighbor_pts, combine = self.region_query(Pn[0], Pn[1], neighbor_pts, P)
                if pn_neighbor_pts != neighbor_pts or combine == 'Yes':
                    self.label[Pn[0]] = self.number_of_clusters
                    self.voc_similarity[Pn[0]] = Pn[1]
                    self.vocs_branches[Pn[0]] = Pn
                    self.files_in_cluster[int(self.dataset[Pn[0]][0])] = [Pn[0], Pn[1]]
                    neighbor_pts = pn_neighbor_pts
            elif self.label[Pn[0]] == 0 and (Pn[1] > self.files_in_cluster[int(self.dataset[Pn[0]][0])][1] and Pn[3] >= self.vocs_branches[self.files_in_cluster[int(self.dataset[Pn[0]][0])][0]][3]):
                if Pn[0] == self.files_in_cluster[int(self.dataset[Pn[0]][0])][0]:
                    self.voc_similarity[Pn[0]] = Pn[1]
                    self.vocs_branches[Pn[0]] = Pn
                    self.files_in_cluster[int(self.dataset[Pn[0]][0])] = [Pn[0], Pn[1]]
                else:
                    branches, neighbor_pts = self.release_free(self.files_in_cluster[int(self.dataset[Pn[0]][0])][0], neighbor_pts)
                    while (branches):
                        br = branches.pop(0)
                        branches2, neighbor_pts = self.release_free(br, neighbor_pts)
                        branches = branches + branches2

                    pn_neighbor_pts, combine = self.region_query(Pn[0], Pn[1], neighbor_pts, P)
                    if pn_neighbor_pts != neighbor_pts or combine == 'Yes':
                        self.label[Pn[0]] = self.number_of_clusters
                        self.voc_similarity[Pn[0]] = Pn[1]
                        self.vocs_branches[Pn[0]] = Pn
                        self.files_in_cluster[int(self.dataset[Pn[0]][0])] = [Pn[0], Pn[1]]
                        neighbor_pts = pn_neighbor_pts
            elif self.label[Pn[0]] != 0 and  ((Pn[1] > self.voc_similarity[Pn[0]] and  Pn[3] >= self.vocs_branches[Pn[0]][3]) or (Pn[1] >= self.voc_similarity[Pn[0]] and  Pn[3] > self.vocs_branches[Pn[0]][3])):
                # if the index in the cluster, just update its simi
                if Pn[0] == self.files_in_cluster[int(self.dataset[Pn[0]][0])][0]:
                    self.files_in_cluster[int(self.dataset[Pn[0]][0])][1] = Pn[1]
                    self.vocs_branches[Pn[0]] = Pn
                    self.voc_similarity[Pn[0]] = Pn[1]
                
                else:
                    if Pn[1] > self.files_in_cluster[int(self.dataset[Pn[0]][0])][1]:
                    
                        # if there is a clusrter index from same sample, remove it from the cluster with all its relevents
                        if self.files_in_cluster[int(self.dataset[Pn[0]][0])][0] != 0:

                            branches, neighbor_pts = self.release_free(self.files_in_cluster[int(self.dataset[Pn[0]][0])][0], neighbor_pts)
                            while (branches):
                                br = branches.pop(0)
                                branches2, neighbor_pts = self.release_free(br, neighbor_pts)
                                branches = branches + branches2
                        self.label[Pn[0]] = self.number_of_clusters
                        self.voc_similarity[Pn[0]] = Pn[1]
                        self.vocs_branches[Pn[0]] = Pn
                        self.files_in_cluster[int(self.dataset[Pn[0]][0])] = [Pn[0], Pn[1]]
                        branches = self.release(Pn[0])
                        while (branches):
                            br = branches.pop(0)
                            if self.files_in_cluster[int(self.dataset[br][0])] == [0, 0]:
                                row2 = self.cosine_matrix[br].split(',')
                                self.label[br] = self.number_of_clusters
                                self.files_in_cluster[int(self.dataset[br][0])] = [br, self.voc_similarity[br]]
                                self.vocs_branches[br][3] = float(row2[P])
                                branches = branches + self.release(br)
                            else:
                                branches = branches + self.release(br)
                                row2 = self.cosine_matrix[br].split(',')
                                brr = self.vocs_branches[br]
                                brr[3] = float(row2[P])
                                neighbor_pts.append(brr)
                                self.label[br] = 0
                                self.voc_similarity[br] = 0
                                self.vocs_branches[br] = [0, 0, 0, 0, 0]
                    else:
                        free_branch = self.release_free(Pn[0], para=1)
                        while (free_branch):
                            fb = free_branch.pop(0)
                            free_branch2 = self.release_free(fb, para=1)
                            free_branch = free_branch + free_branch2

    def release_free(self, p, neighbor_pts=[], para=0):
        branches = []
        self.label[int(p)] = 0
        self.voc_similarity[int(p)] = 0
        self.vocs_branches[int(p)] = [0, 0, 0, 0, 0]
        for i in range(0, len(self.vocs_branches)):
            if self.vocs_branches[i][2] == p:
                branches.append(self.vocs_branches[i][0])
        del_index = []
        for i in range(0, len(neighbor_pts)):
            if p != neighbor_pts[i][2]:
                del_index.append(neighbor_pts[i])
        if  para == 0:
            return branches, del_index
        else:
            return branches

    def release(self, p):
        branches = []
        for i in range(0, len(self.vocs_branches)):
            if self.vocs_branches[i][2] == p:
                branches.append(self.vocs_branches[i][0])
        return branches

    def region_query(self, point, core_distance=0, neighbor_pts=[], established_point=-1):
        # This function is to return neighbours for a given point.
        # Neighbours Index values, core_distance, point index value and established_distance are required for each neighbour.
        # The neighbours will be updated if the point was a neighbour.
        neighbors_all = neighbor_pts[:]
        index_in_neighbors_all = []
        # Once the point is the first point in the cluster, find all the neighbours >= epsilon.
        # Otherwise, update the neighbours.
        if established_point == -1:
            row = self.cosine_matrix[point].split(',')
            for index in range(len(row)-1):
                if float(row[index]) >= self.epsilon:
                    # core_point at this satge = established_point.
                    # Therfore, core_distance = established_distance
                    neighbors_all.append([index, float(row[index]), point, float(row[index])])
        else:
            # Get all the indexes of the neighbours.
            for index in neighbors_all:
                index_in_neighbors_all.append(index[0])
            # Get sample number for the established_point.
            established_sample_number = int(self.dataset[established_point][0])
            row = self.cosine_matrix[point].split(',')
            for index in range(len(row)-1):
                # update all points if they have existed in the neighbours,
                # or, add the neighbour that is not in.
                if self.dataset[index][0] == established_sample_number and float(row[index]) > core_distance  and index != established_point:
                    combine = 'no'
                    return neighbor_pts, combine
                elif float(row[index]) >= self.epsilon and self.dataset[index][0] != established_sample_number:
                    row2 = self.cosine_matrix[index].split(',')
                    if index not in index_in_neighbors_all:
                        neighbors_all.append([index, float(row[index]), point, float(row2[established_point])])
                        index_in_neighbors_all.append(index)
                    else:
                        for ww in range(0, len(neighbors_all)):
                            if index == neighbors_all[ww][0]:
                                if float(row[index]) > neighbors_all[ww][1] and float(row2[established_point]) != 0:
                                    neighbors_all[ww][1] = float(row[index])
                                    neighbors_all[ww][2] = point
                                    neighbors_all[ww][3] = float(row2[established_point])
                                break
        # Reorder the neighbours based on the core_distance value.
        neighbors_all.sort(key=lambda tup: tup[1], reverse=True)
        combine = 'Yes'
        return neighbors_all, combine
