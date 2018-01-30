
from sklearn.cluster import KMeans

import numpy as np


class KmeansClassifier(object):

    # method to get the cluster means of the data points based on coordinates
    # and the queried columns
    @staticmethod
    def __get_location_cluster_means(data, cluster_no, cols):
        # obtain indices of clusters
        kmeans = KMeans(n_clusters=cluster_no, random_state=0)
        # get the indices of the location based clusters
        coordinates = data.values_list('latitude', 'longitude')
        indices = kmeans.fit_predict(coordinates)
        # initialise means of queried columns
        means = np.zeros((cluster_no, len(cols)+1))
        # assign clustered_indices to dataframe
        b = np.zeros((len(data), len(cols)+1))
        b[:,:-1] = data.values_list(*cols)
        b[:,-1] = indices
        # compute means of queried columns
        for index in np.unique(indices):
            means[index] = np.mean(b[b[:,-1]==index][:-1], axis=0)
        return means, indices


    # method to get the clusters of the environments corresponding to the 5 environments based on
    # the queried columns and number of location clusters
    def get_environment_clusters(self, data, cluster_no, cols):
        means, clustered_indices = self.__get_location_cluster_means(data, cluster_no, cols)
        # we have 5 clusters corresponding to 5 different environments
        environment_kmeans = KMeans(n_clusters=5, random_state=0)
        # predict the cluster indices
        environment_indices = environment_kmeans.fit_predict(means)
        # sort the indices based on the means of the clusters
        idx = np.argsort(environment_kmeans.cluster_centers_.sum(axis=1))
        lut = np.zeros_like(idx)
        lut[idx] = np.arange(5)
        # append the indices to the dataframe
        return lut[environment_indices][clustered_indices]
