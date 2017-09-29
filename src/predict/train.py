from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn import neighbors
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import tree
from sklearn import svm

# Train perceptron model
def trainPerceptron(data, labels):
	clr = linear_model.Perceptron()
	clr.fit(data, labels)
	return clr

# Train knn
def trainKnn(data, labels):
	clr = neighbors.KNeighborsClassifier()
	clr.fit(data, labels)
	return clr

# Train random forest
def trainRandomForest(data, labels):
	clr = ensemble.RandomForestClassifier()
	clr.fit(data, labels)
	return clr

# Train gradient boosting
def trainGradientBoosting(data, labels):
	clr = ensemble.GradientBoostingClassifier()
	clr = clr.fit(data, labels)
	return clr

# Train decision tree
def trainDecisionTree(data, labels):
	clr = tree.DecisionTreeClassifier()
	clr.fit(data, labels)
	return clr

# Train svm
def trainSVM(data, labels):
	clr = svm.SVC()
	clr.fit(data, labels)
	return clr

# Train base models used in stacking
def trainModels(data, labels):
	print "Training perceptron"
	perceptron_model = trainPerceptron(data, labels)

	print "Training k-nearest neighbors"
	knn_model = trainKnn(data, labels)

	print "Training random forest"
	random_forest_model = trainRandomForest(data, labels)

	print "Training gradient boosting"
	gradient_boosting_model = trainGradientBoosting(data, labels)

	print "Training decision tree"
	decisionTree_model = trainDecisionTree(data, labels)

	print "Training svm"
	svm_model = trainSVM(data, labels)

	models = list()
	models.append(perceptron_model)
	models.append(knn_model)
	models.append(random_forest_model)
	models.append(gradient_boosting_model)
	models.append(decisionTree_model)
	models.append(svm_model)

	return models

# Train logistic regression stacked model
def trainStackedModel(data, labels):
	parameters = {
		"C": [0.001, 0.01, 0.1, 1, 10, 100, 1000], 
		"solver": ["lbfgs", "liblinear"],
		"max_iter": [1000, 10000]
	}

	lr = linear_model.LogisticRegression(penalty="l2")
	clr = GridSearchCV(lr, parameters)
	clr.fit(data, labels)
	return clr
