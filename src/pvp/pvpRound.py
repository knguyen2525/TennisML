import sys
import pickle
import numpy as np
import csv
sys.path.insert(0, "/Users/kevinnguyen/Projects/tennisml/src/util/")
from indexPlayers import getPlayerStats
from featureCreation import aggregate
from featureCreation import findStatsDifference
from featureCreation import getHandDifference
from featureCreation import getHeadToHeadDifference
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--minYear", default="1990", help="Min date to gather data from")
parser.add_argument("--cleanedAtpMatches", default="cleaned_1990_2017.csv", help="File with cleaned data")
parser.add_argument("--cleanedTourneys", default="cleaned_1990_2017_tourney.csv", help="File containing tourney information")
parser.add_argument("--type", default="weighted", help="Weighted or unweighted features")
parser.add_argument("--round", required=True, help="Round of tourney of interest")
parser.add_argument("--tourneyID", required=True, help="Tourney ID")
args = parser.parse_args()

def getFeatureVector(players, match):
	player1AggStats = aggregate(players[match["name1"]], match["surface"], int(args.minYear), int(match["tourney_date"]), args.type)
	player2AggStats = aggregate(players[match["name2"]], match["surface"], int(args.minYear), int(match["tourney_date"]), args.type)

	# If could not find any stats before the current match then jump to next loop iteration
	if player1AggStats == 0 or player2AggStats == 0:
		print match 
		print "A players stats are 0"
		return 0

	# Find the difference between the two stats vectors
	statsDiff = findStatsDifference(player1AggStats, player2AggStats)

	# Find other stats such as player hands and head to head
	handDiff = getHandDifference(int(match["hand1"]), int(match["hand2"]))
	h2hDiff = getHeadToHeadDifference(match["name1"], match["name2"], players[match["name1"]], players[match["name2"]], int(args.minYear), int(match["tourney_date"]))

	featureVector = [float(statsDiff[0]), float(float(match["age1"]) - float(match["age2"])), float(statsDiff[1]), float(statsDiff[2]), float(statsDiff[3]), float(statsDiff[4]), float(statsDiff[5]), float(statsDiff[6]), float(statsDiff[7]), float(statsDiff[8]), float(statsDiff[9]), float(statsDiff[10]), float(statsDiff[11]), float(statsDiff[12]), float(statsDiff[13]), float(statsDiff[14]), float(handDiff), float(h2hDiff)]

	return featureVector

if __name__ == "__main__":
	print args
	
	# Gathering auxiliary data
	home = "/Users/kevinnguyen/Projects/tennisml"
	inputFile = home + "/data/cleanedData/" + args.cleanedAtpMatches
	tourneyFile = home + "/data/cleanedData/" + args.cleanedTourneys

	# Indexing player stats
	print "gathering player data"
	players = getPlayerStats(inputFile)

	# Loading models
	print "Loading models"
	f_in = open("models.p", "r")
	allModels = pickle.load(f_in)
	f_in.close()

	models = allModels["baseModels"]
	clr = allModels["stackedModels"]
	bestFeatureIndices = allModels["bestFeatureIndices"]

	# Creating variables
	correct = 0
	total = 0
	predictions = []
	nonPredictions = []
	wrongPredictions = []

	with open(tourneyFile, 'r') as f_in:
		reader = csv.DictReader(f_in)

		print "Looking for matches in round"
		for match in reader:
			if match["tourney_id"] == args.tourneyID and match["round"] == args.round and match["name1"] in players and match["name2"] in players:

				# Get latest feature vector for each player in each match
				print "generating feature vector"
				featureVector = getFeatureVector(players, match)
				if not isinstance(featureVector, basestring) and featureVector == 0:
					continue

				# Pick top features
				featureVector = np.reshape(np.array(featureVector), (1, 18))
				featureVector = featureVector[:, bestFeatureIndices]

				# Make base model predictions for feature vector
				baseModelPredictions = []
				for i in range(0, len(models)):
					prediction = models[i].predict(featureVector[0].reshape(1, -1))
					baseModelPredictions.append(prediction)

				# Concat base model predictions to feature vector
				baseModelPredictions = np.reshape(baseModelPredictions, (1, len(models)))
				finalVector = np.concatenate((featureVector, baseModelPredictions), axis=1)

				# Make prediction on match
				finalPrediction = clr.predict(finalVector)
				predictionProbability = clr.predict_proba(finalVector)

				# Store prediction outcome correctness
				if finalPrediction[0] == 1:
					if match["result"] == "1": correct += 1
					else: wrongPredictions.append(match["name1"] + " is predicted to win with " + str(predictionProbability[0][1] * 100) + " chance vs " + match["name2"])
					predictions.append(match["name1"] + " is predicted to win with " + str(predictionProbability[0][1] * 100) + " chance vs " + match["name2"])
				else:
					if match["result"] == "0": correct += 1
					else: wrongPredictions.append(match["name2"] + " is predicted to win with " + str(predictionProbability[0][0] * 100) + " chance vs " + match["name1"])
					predictions.append(match["name2"] + " is predicted to win with " + str(predictionProbability[0][0] * 100) + " chance vs " + match["name1"])

				total += 1
			elif match["tourney_id"] == args.tourneyID and match["round"] == args.round:
				if not match["name1"] in players and not match["name2"] in players:
					nonPredictions.append(match["name1"] + " and " + match["name2"] + " not in players")
				elif not match["name1"] in players:
					nonPredictions.append(match["name1"] + " not in players")
				else:
					nonPredictions.append(match["name2"] + " not in players")

	print "-----------------"
	print "Predictions"
	print "-----------------"
	for i in range(0, len(predictions)):
		print predictions[i]

	print "-----------------"
	print "Wrong Predictions"
	print "-----------------"
	for i in range(0, len(wrongPredictions)):
		print wrongPredictions[i]

	print "-----------------"
	print "Non-predictions"
	print "-----------------"
	for i in range(0, len(nonPredictions)):
		print nonPredictions[i]

	print "Matches predicted:", total
	print "Matches predicted correctly:", correct
	print "Prediction accuracy for this round:", (float(correct) / float(total)) * 100