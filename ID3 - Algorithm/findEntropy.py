__author__ = 'ajayvembu'

import math

# to get the entropy of a data set
# runs in O(B) time where B - number of instances

def findentropy(inputValues):

    pos = 0
    neg = 0

    cloneInput = inputValues.copy()
    for key1 in cloneInput:
        if key1 != "testedAttributes":
          if int(inputValues[key1]["Class"]) == 1:
              pos += 1
          else:
              neg += 1
    # get the proportions
    ppos = float(pos) / float(pos+neg)
    pneg = float(neg) / float(pos+neg)

    if ppos == 0 or pneg == 0:
        return 0.0
    # find the entropy
    return -ppos*math.log10(ppos) - pneg*math.log10(pneg)


# get the proportion which runs in O(B)
def findProportion(inputSet):
    count = 0

    cloneInput = inputSet.copy()
    for key1 in cloneInput:
        if key1 != "testedAttributes":
          count += 1

    return count

# find the gain
# runs in O(B) time
def findGain(parentSetEntropy,leftSet,rightSet):
    # get the proportions
    leftCount = findProportion(leftSet)
    rightCount = findProportion(rightSet)
    leftSetEntropy = rightSetEntropy = 0

    # get the left child and right child entropy

    if bool(leftSet):
     leftSetEntropy = findentropy(leftSet)
    if bool(rightSet):
     rightSetEntropy = findentropy(rightSet)

    # return the information gain
    return float(parentSetEntropy) - (float(leftCount) / float(leftCount+rightCount))*float(leftSetEntropy) - (float(rightCount) / float(leftCount+rightCount))*float(rightSetEntropy)





