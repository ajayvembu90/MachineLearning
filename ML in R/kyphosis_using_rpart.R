#to create the factor variable,
#The kyphosis data set has a factored in itself

# below code to construct the decision tree

kyphosisFit <- rpart( Kyphosis ~ Age + Number + Start, parms = list(split = "information"), data = kyphosis, method = "class")

#below code create a post of the decision tree in a file with the filename #“output.ps”

post(kyphosisFit, filename = "output.ps", 
     title = "Classification Tree for Kyphosis")

#the important attributes in the decision tree are 
# start with highest priority and age with medium priority and number with    # the lowest priority

summary (kyphosisFit)

#the below code to find the best pruning parameter and the best cp parameter # is 0.01000

printcp(kyphosisFit)

#create a pruned tree using the below code

prunedTree <- prune(kyphosisFit, cp = 0.010000)

#80 percent data

#test data counter set

testDataKyphosisCounter <- c(sample(1:81,64))

#fit with test data

kyphosisTestDatFit <- rpart( Kyphosis ~ Age + Number + Start, parms = list(split = "information"), data = kyphosis, method = "class", subset = testDataKyphosisCounter)

#prune with test data fit

kyphosisTestDatPrunedTree <- prune(kyphosisTestDatFit , cp = 0.010000)

#prediction for the test data and the post pruning accuracy for the test data is around 85 #percent

predict(kyphosisTestDatPrunedTree,kyphosis[-testDataKyphosisCounter,], type = "class")

#90 percent test data

testDataKyphosisCounterNinty <- sample(1:81,73)

#decision tree

kyphosisTestDatFitNinty <- rpart( Kyphosis ~ Age + Number + Start, parms = list(split = "information"), data = kyphosis, method = "class", subset = testDataKyphosisCounterNinty)

#pruned tree

kyphosisTestDatFitPrunedNinty <- prune(kyphosisTestDatFitNinty , cp = 0.0100)

#predict on test data and the post pruning accuracy for the test data is around 71 #percent


predict(kyphosisTestDatPrunedTree,kyphosis[-testDataKyphosisCounterNinty,], type = "class")





