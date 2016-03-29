__author__ = 'ajayvembu'

import readFile2
import PruningAlgorithm
import bintree
import ID3Algortihm

# driver program

fileResult = readFile2.readFile("training_set.csv")
validationFile = readFile2.readFile("validation_set.csv")
testSet = readFile2.readFile("test_set.csv")
printInd = "yes"
L = 5
K = 3
targetAttribute = fileResult.inputAttributes[-1]
del(fileResult.inputAttributes[-1])
root = ID3Algortihm.ID3Algorithm(fileResult.trainingSetValues,fileResult.inputAttributes,bintree.BinTreeForDesTree(),targetAttribute)

print PruningAlgorithm.findAccuracy(root,validationFile.trainingSetValues)
bestTree = PruningAlgorithm.pruningAlgorithm(root,L,K,validationFile)

print PruningAlgorithm.findAccuracy(bestTree,validationFile.trainingSetValues)

if printInd == "yes":
    ID3Algortihm.printTree(root,"")
else:
    print "Indicated not to print the decision tree"

