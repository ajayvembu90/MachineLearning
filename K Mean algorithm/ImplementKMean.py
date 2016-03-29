__author__ = 'ajayvembu'

import ReadFile
import KMeanAlgorithmUpdatedV1
import ValidateKMean
import sys

numberOfClusters = int(sys.argv[1])
testFileName = str(sys.argv[2])
outPutFileName = str(sys.argv[3])

testData = ReadFile.readFileForKMean(testFileName)
KMeanResult = KMeanAlgorithmUpdatedV1.KMeanAlgorithm(testData,numberOfClusters)
sSE = ValidateKMean.squaredErrorFunction(KMeanResult.clusters,KMeanResult.centroids)
ReadFile.writeToKMeaFile(outPutFileName,KMeanResult)
print sSE