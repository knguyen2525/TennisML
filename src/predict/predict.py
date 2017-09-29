import numpy as np

# Sets the predictions for the base models for the current test fold
def setPredictionsTrain(foldIDs, data, labels, baseModelPredictionsTrain, currTestFold, model, currentModelIndex):
	numCorrectPredictions = 0
	numPredictions = 0
	for i in range(0, data.shape[0]):
		if foldIDs[i] == currTestFold:
			#use row to predict a 1 or 0, set data last column i as the 1 or 0
			prediction = model.predict(data[i].reshape(1, -1))
			baseModelPredictionsTrain[i][currentModelIndex] = prediction
			if prediction == labels[i]:
				numCorrectPredictions += 1
			numPredictions += 1

	return baseModelPredictionsTrain, numCorrectPredictions, numPredictions

# Sets the predictions for the base models on the test data
def setPredictionsTest(testingFileInput, models):
	data = np.genfromtxt(testingFileInput, skip_header=1, delimiter=",")

	# Separate labels from data
	labels = data[:,-1]
	data = np.delete(data, np.s_[-1:], axis=1)
	#Delete date column
	data = np.delete(data, np.s_[0:1], axis=1)

	baseModelPredictionsTest = np.zeros(shape=(data.shape[0], len(models)))

	# Set the predictions for each base model 
	for i in range(0, len(models)):
		for j in range(0, data.shape[0]):
			baseModelPredictionsTest[j][i] = models[i].predict(data[j].reshape(1, -1))

	return data, labels, baseModelPredictionsTest

# Test stacked model
def testStackedModel(clr, data, labels):
	print "Predicting class lable for samples in X"
	print clr.predict(data)

	print "--------------------------"
	print "Predicting probability estimates in X"
	print clr.predict_proba(data)

	print "--------------------------"
	print "Predicting score/accuracy"
	print clr.score(data, labels)

