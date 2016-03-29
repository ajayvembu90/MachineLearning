__author__ = 'ajayvembu'

import findEntropy
import bintree
import random

# the result of find best attribute method

class BestAttributeResult:
    decisionAttribute = ""
    leftSet = {}
    rightSet = {}


# the ID3 alogrithm in the tom mitchell book
# the algorithm runs in O(BN^2) time
# where B - the number of records in the training set
# N - the number of attributes to be tested

def ID3Algorithm(trainingSetValues,inputAttributes,tempNode,targetAttribute):

    positiveCount = 0
    negativeCount = 0
    totalCount = 0
    inputSetToCheckCount = trainingSetValues.copy()

    # to get the positive and negative counts

    for key1 in inputSetToCheckCount:
      if key1 != "testedAttributes":
        if inputSetToCheckCount[key1]["Class"] == '1':
           positiveCount += 1
        else:
           negativeCount += 1
        totalCount += 1

    # if the data set only has positive class then the label is +

    if positiveCount == totalCount:
        tempNode.testAttrForCurrentNode = "Class"
        tempNode.label = "+"
        return tempNode

    # if the data set only has negative class then the label is -

    elif negativeCount == totalCount:
        tempNode.testAttrForCurrentNode = "Class"
        tempNode.label = "-"
        return tempNode

    # if the length of the tested attributes equals the input set attributes then it means all the attributes are exhausted
    # then do the count check again

    elif len(trainingSetValues["testedAttributes"]) == len(inputAttributes):
        inputSetToCheckCount = trainingSetValues.copy()
        positiveCount = 0
        negativeCount = 0
        for key1 in inputSetToCheckCount:
           if key1 != "testedAttributes":
             if inputSetToCheckCount[key1]["Class"] == '1':
                positiveCount += 1
             else:
                negativeCount += 1
        if positiveCount > negativeCount:
             tempNode.testAttrForCurrentNode = "Class"
             tempNode.label = "+"
        else:
             tempNode.testAttrForCurrentNode = "Class"
             tempNode.label = "-"
        return tempNode

    # else find the best attribute in the current data set and branch the resultant data set as left and right with 1's in the left
    # and 0's in the right, the 1's and 0's are the test of the current best attribute
    else:
        # find the best attribute
        resultOfBestAttribute = findBestAttribute(trainingSetValues,inputAttributes)
        tempNode.testAttrForCurrentNode = resultOfBestAttribute.decisionAttribute
        tempNode.dataForPruning = trainingSetValues.copy()

        # branch to left if there is a data set for 1's
        if bool(resultOfBestAttribute.leftSet):
            tempNode.left = bintree.BinTreeForDesTree()
            ID3Algorithm(resultOfBestAttribute.leftSet,inputAttributes,tempNode.left,targetAttribute)

        # branch to left if there is a data set for 0's
        if bool(resultOfBestAttribute.rightSet):
            tempNode.right = bintree.BinTreeForDesTree()
            ID3Algorithm(resultOfBestAttribute.rightSet,inputAttributes,tempNode.right,targetAttribute)

    return tempNode


# the method to find the best attribute
# runs in O(BN) time

def findBestAttribute(inputSet,inputAttributes):
    entropyOfParent = findEntropy.findentropy(inputSet)
    maxGain = 0
    bestAttribute = ""
    testedAttributes = {}
    result = None
    i = 0
    # find the best attribute with the maximum gain
    for eachAttribute in inputAttributes:
        if eachAttribute not in testedAttributes.values() and eachAttribute not in inputSet["testedAttributes"].values() and eachAttribute != "Class":
            currentSet = inputSet.copy()
            leftSet = {}
            rightSet = {}
            leftSetIndex = 0
            rightSetIndex = 0
            for eachSet in currentSet:
                if eachSet != "testedAttributes":
                   if currentSet[eachSet][eachAttribute] == "1":
                       leftSet[leftSetIndex] = {}
                       leftSet[leftSetIndex] = currentSet[eachSet].copy()
                       leftSetIndex += 1
                   else:
                       rightSet[rightSetIndex] = {}
                       rightSet[rightSetIndex] = currentSet[eachSet].copy()
                       rightSetIndex += 1
            currentGain = findEntropy.findGain(entropyOfParent,leftSet,rightSet)
            if maxGain < currentGain:
                result = BestAttributeResult()
                maxGain = currentGain
                bestAttribute = eachAttribute
                result.decisionAttribute = bestAttribute
                result.leftSet = leftSet
                result.rightSet = rightSet
            testedAttributes[i] = eachAttribute
            i += 1

    # to handle the case if there are no result that is if there are no best attribute
    # repeat the same procedure as in the ID3
    if not bool(result):
        attrIndex = random.randint(0,len(testedAttributes)-1)
        currentAttribute = testedAttributes[attrIndex]
        currentSet = inputSet.copy()
        leftSet = {}
        rightSet = {}
        leftSetIndex = 0
        rightSetIndex = 0
        result = BestAttributeResult()
        for eachSet in currentSet:
            if eachSet != "testedAttributes":
                if currentSet[eachSet][currentAttribute] == "1":
                    leftSet[leftSetIndex] = {}
                    leftSet[leftSetIndex] = currentSet[eachSet].copy()
                    leftSetIndex += 1
                else:
                    rightSet[rightSetIndex] = {}
                    rightSet[rightSetIndex] = currentSet[eachSet].copy()
                    rightSetIndex += 1
        result.decisionAttribute = currentAttribute
        result.leftSet = leftSet
        result.rightSet = rightSet

    # set that node's decision attribute as the best attribute
    if bool(result.leftSet):
        result.leftSet["testedAttributes"] = inputSet["testedAttributes"].copy()
        result.leftSet["testedAttributes"][len(result.leftSet["testedAttributes"])] = result.decisionAttribute
    if bool(result.rightSet):
        result.rightSet["testedAttributes"] = inputSet["testedAttributes"].copy()
        result.rightSet["testedAttributes"][len(result.rightSet["testedAttributes"])] = result.decisionAttribute

    return result

# to print the final decision tree runs in O(N) time

def printTree(tempNode,spaceVal):
    if bool(tempNode):
     if tempNode.testAttrForCurrentNode == "Class":
         if str(tempNode.label) == "+":
             print str(spaceVal) + " : 1"
         else:
             print str(spaceVal) + " : 0"
         return
     print str(spaceVal)+str(tempNode.testAttrForCurrentNode)+str(" : 1")
     printTree(tempNode.left,spaceVal+" | ")
     print str(spaceVal)+str(tempNode.testAttrForCurrentNode)+str(" : 0")
     printTree(tempNode.right,spaceVal+" | ")


# to find the class of a particular tes instance
def findClass(eachSet,decisionTree,spaceVal):
    if bool(decisionTree):
      if str(decisionTree.testAttrForCurrentNode) == "Class":
            if decisionTree.label == "+":
               print str(spaceVal)+" : 1"
            else:
               print spaceVal+" : 0"
      elif eachSet[str(decisionTree.testAttrForCurrentNode)] == "1":
            print str(spaceVal)+str(decisionTree.testAttrForCurrentNode) + " : 1"
            return findClass(eachSet,decisionTree.left,spaceVal+' ')
      else:
            print str(spaceVal)+str(decisionTree.testAttrForCurrentNode) + " : 0"
            return findClass(eachSet,decisionTree.right,spaceVal+' ')



















