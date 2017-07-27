import numpy as np
import os
from sklearn import linear_model
from sklearn.metrics import accuracy_score

def train(filename):
	os.chdir("..")
	cwd = os.getcwd()
	input = cwd + "/features/" + filename

	data = np.genfromtxt(input, skip_header=1, delimiter=",")

	lr = linear_model.LogisticRegression(C=10)

	X = data[:,:-1]
	Y = data[:,-1]

	print len(X), len(Y)

	print lr.fit_transform(X, Y)

	print lr
	# # The output is always 1 or 0, not a probability number.
	result = lr.predict(X)
	print result

	print lr.predict_proba(X)[:,1]

	print accuracy_score(Y, result)

	print accuracy_score(Y, result, normalize=False), "wah"

if __name__ == "__main__":
	train("uwData1990-2016.csv")