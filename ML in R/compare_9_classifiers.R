args <- commandArgs(TRUE)
dataURL<-as.character(args[1])
header<-as.logical(args[2])
d<-read.csv(dataURL,header = header)
d[d=="?"] <- 0
classIndex <- as.integer(args[3])
d[,classIndex]<-as.factor(d[,classIndex])
levels(d[,classIndex]) <- c(0,1)
set.seed(123)
library(rpart)
library(e1071)
library(class)
library(adabag)
library(randomForest)
library(mlbench)
library(ada)
library("ipred")
library("MASS")
library("nnet")
accuracyDT = accuracySVM = accuracyNB = accuracyKNN = accuracyLR = accuracyNN = accuracyRF = accuracyBG = accuracyBOS = 0 
options(warn=-1)
for(i in 1:10) {
  cat("Running sample ",i,"\n")
  sampleInstances<-sample(1:nrow(d),size = 0.9*nrow(d))
  trainingData<-d[sampleInstances,]
  testData<-d[-sampleInstances,]
  
  
  #Decision Tree
  cfit  <- rpart( trainingData[,classIndex] ~ ., data = trainingData[,-classIndex],parms = list(split = 'information'),control = rpart.control(minsplit = 1,minbucket = 1),method = 'class')
  prunedTree <- prune(cfit, cp = 0.01)
  finalResult <- table(predict(prunedTree, testData,type = "class"),testData[,classIndex])
  accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracyDT <- accuracyDT + accuracy
  cat("Method = Decision Tree"," and Accuracy = ",accuracy,"\n")
  
  
  
  #SVM
  svmClassifier <- svm(trainingData[,classIndex] ~ ., data = trainingData[,-classIndex])
  finalResult <- table(predict(svmClassifier, testData), testData[,classIndex])
  accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracySVM <- accuracySVM + accuracy
  cat("Method = SVM"," and Accuracy = ",accuracy,"\n")
  
  
  #Naive Bayessian
  bayesFit <- naiveBayes(trainingData[,classIndex] ~ ., data = trainingData[,-classIndex])
  finalResult <- table(predict(bayesFit, testData), testData[,classIndex])
  accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracyNB <- accuracyNB + accuracy
  cat("Method = Naive Bayes"," and Accuracy = ",accuracy,"\n")
  
  
  #KNN
  cl <- factor(trainingData[,classIndex])
  testResultForKNN <- knn(train = trainingData[,-classIndex], test = testData[,-classIndex], cl ,prob = TRUE)
  finalResult <- table(testResultForKNN, testData[,classIndex])
  accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracyKNN <- accuracyKNN + accuracy
  cat("Method = KNN"," and Accuracy = ",accuracy,"\n")
  
  
  #Logistic Regression
  mylogit <- glm(trainingData[,classIndex] ~ .,  data = trainingData[,-classIndex], family = "binomial")
  p<-predict(mylogit, newdata=testData, type="response")
  threshold=0.65
  prediction<-sapply(p, FUN=function(x) if (x>threshold) 1 else 0)
  finalResult <- table(prediction,testData[,classIndex])
  actual <- testData[,classIndex]
  accuracy <- sum(actual == prediction) / length(actual)
  accuracyLR <- accuracyLR + accuracy
  cat("Method = Logistic Regression"," and Accuracy = ",accuracy,"\n")
  
  
  #Neural Networks
  neuralNetworkClassifier <- nnet( trainingData[,classIndex] ~ ., data=trainingData[,-classIndex],size = 4,maxit=1000,decay=.01)
  neuralNetworkClassifier <- nnet( trainingData[,classIndex] ~ ., data=trainingData[,-classIndex],size = 4,maxit=1000,decay=.01)
  prediction <- predict(neuralNetworkClassifier,newdata = testData)
  prediction <- round(prediction)
  accuracy <- sum(prediction == testData[,classIndex] ) / length(prediction )
  accuracyNN <- accuracyNN + accuracy
  cat("Method = Neural Networks"," and Accuracy = ",accuracy,"\n")
  
  #Random Forest
  randomForest <- randomForest(trainingData[,classIndex] ~ ., data=trainingData[,-classIndex], importance=TRUE,proximity=TRUE)
  finalResult <- table(predict(randomForest, newdata=testData,), testData[,classIndex])
  accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracyRF <- accuracyRF + accuracy
  cat("Method = Random Forest"," and Accuracy = ",accuracy,"\n")
  
  
  #Bagging
  baggingClassifier <- bagging(trainingData[,classIndex] ~ ., data=trainingData[,-classIndex], coob=TRUE)
  #baggingClassifier <- bagging(trainingData[,classIndex] ~ ., data=trainingData[,-classIndex], coob=TRUE)
  finalResult <- table(predict(baggingClassifier,testData),testData[,classIndex])
  predictValueBagging <- predict(baggingClassifier,testData)
  levels(predictValueBagging) <- levels(testData[,classIndex])
  accuracy <- sum(predictValueBagging == testData[,classIndex]) / length(predictValueBagging)
  #accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracyBG <- accuracyBG + accuracy
  cat("Method = Bagging"," and Accuracy = ",accuracy,"\n")
  
  
  #Boosting
  boostingClassifier <- ada(trainingData[,classIndex] ~ ., data = trainingData[,-classIndex], iter=20, nu=1, type="discrete")
  finalResult <- table(predict(boostingClassifier,testData),testData[,classIndex])
  accuracy <- ((finalResult[1,1] + finalResult[2,2]) / (finalResult[1,1] + finalResult[1,2] + finalResult[2,1] + finalResult[2,2]))
  accuracyBOS <- accuracyBOS + accuracy
  cat("Method = Boosting"," and Accuracy = ",accuracy,"\n")
  
  
}
options(warn=0)
print("Overall Accuracy")
cat("Decsion Tree = ",accuracyDT / 10,"\n")
cat("SVM = ",accuracySVM / 10,"\n")
cat("Naive Bayes = ",accuracyNB / 10,"\n")
cat("KNN = ",accuracyKNN / 10,"\n")
cat("Logistic Regression = ",accuracyLR /10,"\n")
cat("Neural Nets = ",accuracyNN/10,"\n")
cat("Random Forest = ",accuracyRF/10,"\n")
cat("Bagging = ",accuracyBG/10,"\n")
cat("Boosting = ",accuracyBOS/10,"\n")
  
  


