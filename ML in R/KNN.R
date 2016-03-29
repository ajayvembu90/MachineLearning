# the package used for K- Nearest Neighbor
library(class)
args <- commandArgs(TRUE)
totalInputSet <- read.csv(file=args[1],header = TRUE, sep = ",")
totalInputSet$class <- as.factor(totalInputSet$class)
i = 1
j = 1
totalAccuracy = 0
allKs = c(3,5,7,9,11)
# iterate for all the kernels
while(j <= length(allKs)){
  # run ten times 
  while(i <= 10){
  	# split the input data into 80:20 for train and test respectively
    trainSamples <- sample(1:768,691)
    trainingSetKnn <- totalInputSet[trainSamples,]
    testSetKnn <- totalInputSet[-trainSamples,]
    # train the model
    testResultForKNN <- knn(train = trainingSetKnn[,c(1,2,3,4,5,6,7,8)], test = testSetKnn[,c(1,2,3,4,5,6,7,8)], k = allKs[j], cl = trainingSetKnn[,9])
    # confidence matrix
    finalResult <- table(testResultForKNN, testSetKnn$class)
    # accuracy
    currentAccuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2])) * 100
    totalAccuracy <- totalAccuracy + currentAccuracy
    i = i + 1
  }
  # average accuracy for all the kernels
  averageAccuracy <- totalAccuracy / 10
  cat("k = ",allKs[j]," has an accuracy of ",averageAccuracy,"\n")
  totalAccuracy = 0
  i = 1
  j = j + 1
}
