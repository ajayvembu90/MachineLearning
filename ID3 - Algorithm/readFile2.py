__author__ = 'ajayvembu'

def readFile(fileName):
 trainingFile = open(fileName,"r")
 firstLine = trainingFile.readline()

 inputAttributes = firstLine[:-1].split(',')
 trainingSetValues = {}
 j = 0

 for line in trainingFile:
    eachInputSet = line[:-1].split(',')
    i=0
    trainingSetValues[j] = {}
    while i < len(eachInputSet):
       trainingSetValues[j][str(inputAttributes[i])] = eachInputSet[i]
       i += 1
    j += 1
 trainingSetValues["testedAttributes"] ={}
 result = FileResult()
 result.trainingSetValues = trainingSetValues
 result.inputAttributes = inputAttributes

 return result


class FileResult:
    trainingSetValues = {}
    inputAttributes = ""


















