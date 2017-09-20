import sys
import math
import numpy as np
from train import trainModels
from train import trainStackedModel
from predict import setPredictionsTrain
from predict import setPredictionsTest
from predict import testStackedModel

# Give different sections of data fold IDs to handle "rolling" training
def divideDataset(trainingFileInput, numFolds):
	data = np.genfromtxt(trainingFileInput, skip_header=1, delimiter=",")

	# Separate labels from data
	labels = data[:,-1]
	data = np.delete(data, np.s_[-1:], axis=1)

	#Delete date column
	data = np.delete(data, np.s_[0:1], axis=1)

	# Creating fold ID column
	foldIDs = np.zeros(data.shape[0])

	# Finding size of each fold
	foldSize = int(math.floor(data.shape[0] / (numFolds + 2)))
	foldID = 0

	# Assign fold IDs from first to last data chronologically
	for i in range(0, data.shape[0]):
		if i % foldSize == 0 and i != 0 and foldID != numFolds + 1:
			foldID += 1
		foldIDs[i] = foldID
	
	return foldIDs, data, labels, foldSize

# Retrieve training data relelvant to a current fold
def getTrainingSet(foldIDs, data, labels, currTestFold):
	tempTrainData = []
	tempTrainLabels = []

	# Gather feature vectors and the labels for those vectors for training
	for i in range(0, foldIDs.shape[0]):
		if foldIDs[i] < currTestFold:
			tempTrainData.append(data[i])
			tempTrainLabels.append(labels[i])

	return tempTrainData, tempTrainLabels

# Deletes the data for fold 0 as this is unused data
def deleteFirstFoldRows(data, labels, baseModelPredictionsTrain, foldSize):
	data = np.delete(data, range(0, foldSize), axis=0)
	labels = np.delete(labels, range(0, foldSize), axis=0)
	baseModelPredictionsTrain = np.delete(baseModelPredictionsTrain, range(0, foldSize), axis=0)
	return data, labels, baseModelPredictionsTrain

# Util function for printing base model accuracy
def printBaseModelAccuracy(trainData, trainLabels, testData, testLabels):
	models = trainModels(trainData, trainLabels)
	for model in models:
		print model
		print "Predicting class lable for samples in X"
		print model.predict(testData)

		print "--------------------------"
		print "Predicting score/accuracy"
		print model.score(testData, testLabels)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Error: Please specify:", "'trainingFile'", "'testingFile'", "'numFolds'"
		exit(0)

	home = "/Users/kevinnguyen/Projects/tennisml"

	# Gathering auxiliary data
	trainingFileInput = home + "/data/features/" + sys.argv[1]
	testingFileInput = home + "/data/features/" + sys.argv[2]
	numFolds = int(sys.argv[3])
	numBaseModels = 2

	# Assign foldIDs to vectors based on numFolds
	foldIDs, data, labels, foldSize = divideDataset(trainingFileInput, numFolds)
	baseModelPredictionsTrain = np.zeros(shape=(data.shape[0], numBaseModels))

	# For each test fold, train on the previous data and test on the currTestFold
	for currTestFold in range(1, numFolds + 2):
		print "Creating predictions for test fold", currTestFold
		# Get training set based on test fold
		tempTrainData, tempTrainLabels = getTrainingSet(foldIDs, data, labels, currTestFold)
		# Train models based on training set
		models = trainModels(tempTrainData, tempTrainLabels)

		# Get predictions for current test fold
		for i in range(0, numBaseModels):
			baseModelPredictionsTrain = setPredictionsTrain(foldIDs, data, baseModelPredictionsTrain, currTestFold, models[i], i)

		print "================================="

	print "Prepping training data"
	# Delete the rows for fold 0 that were used to predict fold 1
	trainData, trainLabels, baseModelPredictionsTrain = deleteFirstFoldRows(data, labels, baseModelPredictionsTrain, foldSize)

	# Create the training set with original features and predictions from base models
	trainingDataset = np.concatenate((trainData, baseModelPredictionsTrain), axis=1)

	print "Prepping testing data"
	# Now train base models on entire training set to predict testing set
	models = trainModels(data, labels)

	# Set the predictions matrix for the test data
	testData, testLabels, baseModelPredictionsTest = setPredictionsTest(testingFileInput, models)
	testingDataset = np.concatenate((testData, baseModelPredictionsTest), axis=1)

	print "================================="
	print "Printing base model accuracies"
	printBaseModelAccuracy(trainData, trainLabels, testData, testLabels)
	
	print "================================="
	print "Training and testing stacked model"
	# Train stacked model and predict
	clr = trainStackedModel(trainingDataset, trainLabels)
	testStackedModel(clr, testingDataset, testLabels)













