from sklearn.feature_selection import f_classif
from sklearn.feature_selection import SelectKBest

def voteOnFeatures(data, labels, keep, fScores):
	fit = SelectKBest(f_classif, k=keep).fit(data, labels)
	scores = fit.scores_
	for i in range(0, scores.shape[0]):
		fScores[i] += scores[i]

	return fScores




