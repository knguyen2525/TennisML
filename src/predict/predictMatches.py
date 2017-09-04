import sys
import numpy as np
from sklearn import linear_model

def train(trainingFileInput):
	dataTrain = np.genfromtxt(trainingFileInput, skip_header=1, delimiter=",")
	data = dataTrain[:,:-1]
	label = dataTrain[:,-1]
	lr = linear_model.LogisticRegression()
	lr.fit(data, label)
	return lr

def test(testingFileInput, lr):
	dataTest = np.genfromtxt(testingFileInput, skip_header=1, delimiter=",")
	data = dataTest[:,:-1]
	label = dataTest[:,-1]

	print "Predicting class lable for samples in X"
	print lr.predict(data)

	print "--------------------------"
	print "Predicting probability estimates in X"
	print lr.predict_proba(data)

	print "--------------------------"
	print "Predicting score/accuracy"
	print lr.score(data, label)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Error: Please specify:", "'trainingFile'", "'testingFile'"
		exit(0)

	home = "/Users/kevinnguyen/Projects/tennisml"

	# Gathering auxiliary data
	trainingFileInput = home + "/data/features/" + sys.argv[1]
	testingFileInput = home + "/data/features/" + sys.argv[2]

	lr = train(trainingFileInput)
	test(testingFileInput, lr)