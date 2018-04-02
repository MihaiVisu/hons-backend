
from sklearn.cluster import KMeans

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


import numpy as np


classifiers_dict = {
    'rf': RandomForestClassifier(random_state=0, n_estimators=50, n_jobs=-1),
    'svc': SVC(kernel="rbf", gamma="auto", probability=True),
    'knn': KNeighborsClassifier(n_neighbors=15),
    'mixed_model': 'mixed_model'
}



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
        means = np.zeros((cluster_no, len(cols)))
        # assign clustered_indices to dataframe
        b = np.zeros((len(data), len(cols) + 1))
        b[:, :-1] = data.values_list(*cols)
        b[:, -1] = indices
        # compute means of queried columns
        for index in np.unique(indices):
            means[index] = np.mean(b[b[:, -1] == index][:,:-1], axis=0)
        return means, indices

    # method to get the clusters of the environments corresponding
    # to the 5-6 environments based on
    # the queried columns and number of location clusters
    def get_environment_clusters(self, data, cluster_no, cols, number_environment_clusters):
        means, clustered_indices = self.__get_location_cluster_means(
            data, cluster_no, cols)
        # we have 5-6 clusters corresponding to 5 different environments
        environment_kmeans = KMeans(n_clusters=number_environment_clusters, random_state=0)
        # predict the cluster indices
        environment_indices = environment_kmeans.fit_predict(means)
        # sort the indices based on the means of the clusters
        idx = np.argsort(environment_kmeans.cluster_centers_.sum(axis=1))
        lut = np.zeros_like(idx)
        lut[idx] = np.arange(number_environment_clusters)
        # append the indices to the dataframe
        return lut[environment_indices][clustered_indices]
