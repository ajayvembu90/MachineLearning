__author__ = 'ajayvembu'

import urllib2

# read from an url
def readFileForKMean(fileName):
    testFile = urllib2.urlopen(fileName).read().split("\r")
    inputPointLables = testFile[0].split("\t")
    testFile.pop(0)
    testInstances = {}
    i = j = 0
    for line in testFile:
        eachTestLine = line.split("\t")
        testInstances[i] = {}
        for eachAttribute in eachTestLine:
            testInstances[i][str(inputPointLables[j])] = eachAttribute
            j += 1
        j = 0
        i += 1
    return testInstances

# write to a file (the id's of the points)
def writeToKMeaFile(fileName,results):
    file = open(fileName,"w")
    file.write("Cluster-Id\tList-of-points\n")
    for eachCluster in results.clusters:
        file.write(str(eachCluster))
        file.write("\t")
        file.write("\t")
        file.write("\t")
        idCount = 0
        for eachClusterPoint in results.clusters[eachCluster]:
            if idCount == len(results.clusters[eachCluster])-1:
                file.write(results.clusters[eachCluster][eachClusterPoint]["id"])
            else:
                file.write(results.clusters[eachCluster][eachClusterPoint]["id"])
                file.write(",")
            idCount += 1
        file.write("\n")



