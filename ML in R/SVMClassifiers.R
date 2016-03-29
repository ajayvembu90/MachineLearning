# package for SVM classification
library(e1071)
args <- commandArgs(TRUE)
totalInputSet <- read.csv(file=args[1],header = TRUE, sep = ",")
totalInputSet$class <- as.factor(totalInputSet$class)
i = 1
j = 1
totalAccuracy = 0
# for all the kernel functions
allKernels = c("","linear","polynomial","radial","sigmoid")
while(j <= length(allKernels)){
  while(i <= 10){
  	# split the data into 80:20 for train and test respectively
    trainSamples <- sample(1:768,691)
    # train the model - discriminative 
    if (allKernels[j] == ""){
      svmClassifier <- svm(class ~ nOfTimesPreg + plasmaGlucoseCon + diolBP + tricepsThickness + X2HrSerIns + bMI + diabPedigreeFunc + age, data = totalInputSet, subset = trainSamples)
    }
    else{
      svmClassifier <- svm(class ~ nOfTimesPreg + plasmaGlucoseCon + diolBP + tricepsThickness + X2HrSerIns + bMI + diabPedigreeFunc + age, data = totalInputSet, subset = trainSamples, kernel = allKernels[j])
    }
    # predict for test data
    svmPredictResult <- predict(svmClassifier, totalInputSet[-trainSamples,])
    # tabulate the result - confidence matrix
    finalResult <- table(svmPredictResult, totalInputSet[-trainSamples,]$class)
    # compute the accuracy
    currentAccuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2])) * 100
    totalAccuracy <- totalAccuracy + currentAccuracy
    i = i + 1
  }
  # overall average accuracy for every kernel function
  averageAccuracy <- totalAccuracy / 10
  if (allKernels[j] == ""){
    cat("Default has accuracy of ",averageAccuracy,"\n")
  }
  else{
    cat(allKernels[j]," has accuracy of ",averageAccuracy,"\n")
  }
  
  totalAccuracy = 0
  i = 1
  j = j + 1
}
