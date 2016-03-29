__author__ = 'ajayvembu'


# to find the SE of the data set in O(CB) time
def squaredErrorFunction(clusters,centroids):
    sSE = 0
    for eachCluster in clusters:
        for eachPoints in clusters[eachCluster]:
            sSE += (float(clusters[eachCluster][eachPoints]["x"]) - float(centroids[eachCluster]["x"]))**2 + (float(clusters[eachCluster][eachPoints]["y"]) - float(centroids[eachCluster]["y"]))**2
    return sSE

