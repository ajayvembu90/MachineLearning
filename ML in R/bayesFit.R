# the package used to test Naive Bayes
library(e1071)
args <- commandArgs(TRUE)
# to read the input set
totalInputSet <- read.csv(file=args[1],header = TRUE, sep = ",")
# change the target as factor variable
totalInputSet$class <- as.factor(totalInputSet$class)
i = 1
totalAccuracy = 0
# get 10 different samples of the data to get the avearge accuracy
while(i <= 10){
  # split the data as train and test into 80:20 ratio respectively
  trainSamples <- sample(1:768,691)
  # train the naive bayes - a generative model
  bayesFit <- naiveBayes(class ~ nOfTimesPreg + plasmaGlucoseCon + diolBP + tricepsThickness + X2HrSerIns + bMI + diabPedigreeFunc + age, data = totalInputSet, subset = trainSamples)
  # predict the test data
  bayesPredictResult <- predict(bayesFit, totalInputSet[-trainSamples,])
  # tabulate the final result to get the confidance matrix
  finalResult <- table(bayesPredictResult, totalInputSet[-trainSamples,]$class)
  # compute the ovearll accuracy
  currentAccuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2])) * 100
  cat("Accuracy for experiment : " , i ," ", currentAccuracy,"\n")
  totalAccuracy <- totalAccuracy + currentAccuracy
  i = i + 1
}
  # compute the average accuracy
averageAccuracy <- totalAccuracy / 10
cat("The overall accuracy for Bayes method is ",averageAccuracy,"\n")
