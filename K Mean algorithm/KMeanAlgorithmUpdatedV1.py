__author__ = 'ajayvembu'

import random
import math
import KMeanResult

# K mean algorithm
# runs in O(KBC)
# where K - num of iterations for convergence
# B - number of testing instances
# C - number of clusters


def KMeanAlgorithm(testData,numberOfClusters):
    # get random index for points as initial cluster points
    randomPoints = random.sample(range(0,len(testData)-1),numberOfClusters)
    centroids = {}
    allClusters = {}
    finalOutPutClusters = {}
    i = 0
    # assign all the inital cluster points
    while i < numberOfClusters:
       centroids[i] = testData[randomPoints[i]]
       allClusters[i] = {}
       i += 1
    i = 0
    # arbitrarily 25 iterations exits either after 25 iterations or until reaching convergence
    while i < 25:
        for eachTestInstance in testData:
           # get the cluster index for the current test data
           clusterIndexOfAPoint = findClusterIndex(testData[eachTestInstance],centroids)
           allClusters[clusterIndexOfAPoint][len(allClusters[clusterIndexOfAPoint])] = testData[eachTestInstance]
        # recompute the centroid after assigning each point to a corresponding cluster
        newCentroids = recomputeCentroids(allClusters)
        j = 0
        testForCentroidEquality = True
        while j < numberOfClusters:
           if not (abs(float(newCentroids[j]["x"]) - float(centroids[j]["x"])) <= 0.001 and abs(float(newCentroids[j]["y"]) - float(centroids[j]["y"])) <= 0.001):
               testForCentroidEquality = False
           j += 1
        if testForCentroidEquality:
           break
        centroids = newCentroids
        allClusters = {}
        finalOutPutClusters = allClusters
        k = 0
        while k < numberOfClusters:
            allClusters[k] = {}
            k += 1
        i += 1
    results = KMeanResult.KMeanResults()
    results.clusters = finalOutPutClusters
    results.centroids = centroids
    return results

# get the cluster index of a test instance in O(C) time
# uses the distance metric to find the relevance between a point and its centroid
def findClusterIndex(testInstance,centroids):
    i = 0
    clusterIndex = 0
    minDistance = float("inf")
    while i < len(centroids):
        currentDistance = math.sqrt((float(testInstance["x"]) - float(centroids[i]["x"]))**2 + (float(testInstance["y"]) - float(centroids[i]["y"]))**2)
        if currentDistance < minDistance:
            minDistance = currentDistance
            clusterIndex = i
        i += 1
    return clusterIndex

# to recompute the centroids in worst case O(CB)
# the resulting centroid point may or may not be in the data set
def recomputeCentroids(allClusters):
    newCentroids = {}
    for eachCluster in allClusters:
        denom = 1
        allSumOfX = 0
        allSumOfY = 0
        for eachPointInACluster in allClusters[eachCluster]:
            allSumOfX += float(allClusters[eachCluster][eachPointInACluster]["x"])
            allSumOfY += float(allClusters[eachCluster][eachPointInACluster]["y"])
            denom += 1
        newCentroids[eachCluster] = {}
        newCentroids[eachCluster]["x"] = str(float(allSumOfX / denom))
        newCentroids[eachCluster]["y"] = str(float(allSumOfY / denom))
    return newCentroids
