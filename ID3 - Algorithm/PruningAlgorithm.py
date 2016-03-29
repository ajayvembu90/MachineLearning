__author__ = 'ajayvembu'

import readFile2
import copy
import random
import bintree

# get the accuracy percentage of a data set in O(B) time

def findAccuracy(decisionTree,validationSet):
    winCount = 0
    totalCount = 0
    for eachSet in validationSet:
        if eachSet != "testedAttributes":
          actualClass = validationSet[eachSet]["Class"]
          predictedClass = classFoundByDecisionTree(decisionTree,validationSet[eachSet])
          if str(predictedClass) == str(actualClass):
              winCount += 1
          totalCount += 1

    return ( float(winCount) / float(totalCount) ) * 100.0


# the class found by the decision tree

def classFoundByDecisionTree(tree,eachSet):
    if bool(tree):
      if str(tree.testAttrForCurrentNode) == "Class":
          if tree.label == "+":
             return 1
          else:
             return 0
      elif eachSet[str(tree.testAttrForCurrentNode)] == "1":
          return classFoundByDecisionTree(tree.left,eachSet)
      else:
          return classFoundByDecisionTree(tree.right,eachSet)
    else:
      return 0

# to get all the internal nodes in O(N)

def getAllInternalNodes(tempNode,internalNodeArray):
    if bool(tempNode):
      if tempNode.testAttrForCurrentNode != "Class":
          internalNodeArray.append(tempNode)
          getAllInternalNodes(tempNode.left,internalNodeArray)
          getAllInternalNodes(tempNode.right,internalNodeArray)



# the below pruning algorithm runs in O(LMB) time
# L and M are random parameters

def pruningAlgorithm(decisionTree,L,K,validationFile):
   decisionTreeBest = copy.deepcopy(decisionTree)
   max = findAccuracy(decisionTree,validationFile.trainingSetValues)
   i = 0
   while i < L:
     currentDecsionTree = copy.deepcopy(decisionTree)
     internalNodeArray = []
     # get all the internal nodes in the tree and store it in the internalNodeArray
     getAllInternalNodes(currentDecsionTree,internalNodeArray)
     M = random.randint(1,K)
     j = 0
     while j < M:
         N = len(internalNodeArray)
         P = random.randint(0,N-1)

         internalNodeArray[P].left = bintree.BinTreeForDesTree()
         internalNodeArray[P].right = bintree.BinTreeForDesTree()
         internalNodeArray[P].left.testAttrForCurrentNode = "Class"
         internalNodeArray[P].right.testAttrForCurrentNode = "Class"

         posCount = 0
         negCount = 0
         # use the data set stored while the tree was constructed
         for eachSet in internalNodeArray[P].dataForPruning:
             if eachSet != "testedAttributes":
               if internalNodeArray[P].dataForPruning[eachSet]["Class"] == "1":
                   posCount += 1
               else:
                   negCount += 1

         if posCount > negCount:
          internalNodeArray[P].left.label = "+"
          internalNodeArray[P].right.label = "+"
         else:
          internalNodeArray[P].left.label = "-"
          internalNodeArray[P].right.label = "-"
         j += 1
     # get the accuracy
     currentTreeAccuracy = findAccuracy(currentDecsionTree,validationFile.trainingSetValues)

     if max < currentTreeAccuracy:
         max = currentTreeAccuracy
         decisionTreeBest = copy.deepcopy(currentDecsionTree)
     i += 1

   return decisionTreeBest





















