import sys
import pickle
import numpy as np
sys.path.insert(0, "/Users/kevinnguyen/Projects/tennisml/src/util/")
from indexPlayers import getPlayerStats
from featureCreation import aggregate
from featureCreation import findStatsDifference
from featureCreation import getHandDifference
from featureCreation import getHeadToHeadDifference
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name1", required=True, help="Name of player 1")
parser.add_argument("--name2", required=True, help="Name of player 2")
parser.add_argument("--hand1", required=True, help="Hand of player 1. 1=R, 2=L")
parser.add_argument("--hand2", required=True, help="Hand of player 2. 1=R, 2=L")
parser.add_argument("--age1", required=True, help="Age of player 1")
parser.add_argument("--age2", required=True, help="Age of player 2")
parser.add_argument("--matchDate", required=True, help="Date of match to be predicted. Format: YearMonthDay")
parser.add_argument("--matchSurface", required=True, help="Surface of play")
parser.add_argument("--minYear", default="1990", help="Min date to gather data from")
parser.add_argument("--cleanedAtpMatches", default="cleaned_1990_2017.csv", help="File with cleaned data")
parser.add_argument("--type", default="weighted", help="Weighted or unweighted features")
args = parser.parse_args()

def getFeatureVector(players):
	player1AggStats = aggregate(players[args.name1], args.matchSurface, int(args.minYear), int(args.matchDate), args.type)
	player2AggStats = aggregate(players[args.name2], args.matchSurface, int(args.minYear), int(args.matchDate), args.type)

	# If could not find any stats before the current match then jump to next loop iteration
	if player1AggStats == 0 or player2AggStats == 0: 
		print "A players stats are 0"
		sys.exit(0)

	# Find the difference between the two stats vectors
	statsDiff = findStatsDifference(player1AggStats, player2AggStats)

	# Find other stats such as player hands and head to head
	handDiff = getHandDifference(int(args.hand1), int(args.hand2))
	h2hDiff = getHeadToHeadDifference(args.name1, args.name2, players[args.name1], players[args.name2], int(args.minYear), int(args.matchDate))

	featureVector = [float(statsDiff[0]), float(float(args.age1) - float(args.age2)), float(statsDiff[1]), float(statsDiff[2]), float(statsDiff[3]), float(statsDiff[4]), float(statsDiff[5]), float(statsDiff[6]), float(statsDiff[7]), float(statsDiff[8]), float(statsDiff[9]), float(statsDiff[10]), float(statsDiff[11]), float(statsDiff[12]), float(statsDiff[13]), float(statsDiff[14]), float(handDiff), float(h2hDiff)]

	return featureVector

if __name__ == "__main__":
	print args
	
	# Gathering auxiliary data
	home = "/Users/kevinnguyen/Projects/tennisml"
	inputFile = home + "/data/cleanedData/" + args.cleanedAtpMatches

	# Indexing player stats
	print "gathering player data"
	players = getPlayerStats(inputFile)

	print "generating feature vector"
	featureVector = np.array(getFeatureVector(players))

	f_in = open("models.p", "r")
	allModels = pickle.load(f_in)
	f_in.close()

	models = allModels["baseModels"]
	clr = allModels["stackedModels"]
	bestFeatureIndices = allModels["bestFeatureIndices"]

	featureVector = np.reshape(featureVector, (1, 18))
	featureVector = featureVector[:, bestFeatureIndices]

	baseModelPredictions = []
	for i in range(0, len(models)):
		prediction = models[i].predict(featureVector[0].reshape(1, -1))
		baseModelPredictions.append(prediction)

	baseModelPredictions = np.reshape(baseModelPredictions, (1, len(models)))
	finalVector = np.concatenate((featureVector, baseModelPredictions), axis=1)

	finalPrediction = clr.predict(finalVector)

	predictionProbability = clr.predict_proba(finalVector)

	if finalPrediction[0] == 1:
		print args.name1 + " is predicted to win with " + str(predictionProbability[0][1] * 100) + " chance!"
	else:
		print args.name2 + " is predicted to win with " + str(predictionProbability[0][0] * 100) + " chance!"
	