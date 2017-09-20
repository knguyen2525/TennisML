# Reads in player stats over the years and averages the stats without any weights.

# import math
import sys
sys.path.append("/Users/kevinnguyen/Projects/tennisml/src/util/")
import csv
import math
from operator import itemgetter
from indexPlayers import getPlayerStats
from timeUtil import isDateInRange
from featureCreation import aggregate
from featureCreation import findStatsDifference
from featureCreation import getHandDifference
from featureCreation import getHeadToHeadDifference

# Loops through matches and generates features for each match in cleaned data
def generateFeatures(outputFile, minYear, maxYear, featureType, players):
	features = []

	# Reading in match data from cleaned data
	with open(inputFile, 'r') as f_in:
		reader = csv.DictReader(f_in)

		# For each match, aggregate player stats based on previous matches and output feature vector for that match
		print "aggregating player data and generating features"
		for match in reader:
			if isDateInRange(match["tourney_date"], minYear * 10000, maxYear * 10000):
				# Aggregating general player stats. Also weighs if weighted parameter is passed in
				player1AggStats = aggregate(players[match["name1"]], match["surface"], minYear, match["tourney_date"], featureType)
				player2AggStats = aggregate(players[match["name2"]], match["surface"], minYear, match["tourney_date"], featureType)

				# If could not find any stats before the current match then jump to next loop iteration
				if player1AggStats == 0 or player2AggStats == 0: continue

				# Find the difference between the two stats vectors
				statsDiff = findStatsDifference(player1AggStats, player2AggStats)

				# Find other stats such as player hands and head to head
				handDiff = getHandDifference(match["hand1"], match["hand2"])
				h2hDiff = getHeadToHeadDifference(match["name1"], match["name2"], players[match["name1"]], players[match["name2"]], minYear, match["tourney_date"])


				featureVector = [int(match["tourney_date"]), str(statsDiff[0]), str(float(match["age1"]) - float(match["age2"])), str(statsDiff[1]), str(statsDiff[2]), str(statsDiff[3]), str(statsDiff[4]), str(statsDiff[5]), str(statsDiff[6]), str(statsDiff[7]), str(statsDiff[8]), str(statsDiff[9]), str(statsDiff[10]), str(statsDiff[11]), str(statsDiff[12]), str(statsDiff[13]), str(handDiff), str(h2hDiff), match["result"]]
				features.append(featureVector)

				if len(features) % 1000 == 0 and len(features) != 0: print "generated feature vectors for: " + str(len(features)) + " matches"

		print "generated feature vectors for: " + str(len(features)) + " matches"
		
	f_in.close()
	return features

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Error: Please specify:", "'minYear'", "'maxYear'", "'cleanedAtpMatchesFileName'", "'weighted|unweighted'"
		exit(0)

	# Gathering auxiliary data
	minYear = int(sys.argv[1])
	maxYear = int(sys.argv[2])
	home = "/Users/kevinnguyen/Projects/tennisml"
	inputFile = home + "/data/cleanedData/" + sys.argv[3]
	featureType = sys.argv[4]

	# Indexing player stats
	print "gathering player data"
	players = getPlayerStats(inputFile)

	# Calling generateFeatures to create feature vectors
	outputFile = home + "/data/features/" + featureType + "_" + str(minYear) + "_" + str(maxYear)
	features = generateFeatures(outputFile, minYear, maxYear, featureType, players)

	# Finding training/testing split 70/30
	numTrainingFeatures = int(math.ceil(0.7 * len(features))) - 1
	print "Training vectors is " + str(numTrainingFeatures)
	print "Testing vectors is " + str(len(features) - numTrainingFeatures)

	# Sorting features by tourney date
	print "Sorting features by tourney_date"
	sortedFeatures = sorted(features)

	# Write features to file after sorting by date
	print "Writing training data to file"
	with open(outputFile + "_training.csv", 'w') as f_out:
		# Write header of output file
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("tourney_date", "htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "bpLostDiff", "surfaceWinsDiff", "handDiff", "h2hDiff", "result"))

		for i in range(0, numTrainingFeatures):
			# Write difference vector to output feature file
			f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (sortedFeatures[i][0], sortedFeatures[i][1], sortedFeatures[i][2], sortedFeatures[i][3], sortedFeatures[i][4], sortedFeatures[i][5], sortedFeatures[i][6], sortedFeatures[i][7], sortedFeatures[i][8], sortedFeatures[i][9], sortedFeatures[i][10], sortedFeatures[i][11], sortedFeatures[i][12], sortedFeatures[i][13], sortedFeatures[i][14], sortedFeatures[i][15], sortedFeatures[i][16], sortedFeatures[i][17], sortedFeatures[i][18]))

		f_out.close()

	# Write features to file after sorting by date
	print "Writing testing data to file"
	with open(outputFile + "_testing.csv", 'w') as f_out:
		# Write header of output file
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("tourney_date", "htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "bpLostDiff", "surfaceWinsDiff", "handDiff", "h2hDiff", "result"))

		for i in range(numTrainingFeatures, len(features)):
			# Write difference vector to output feature file
			f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(sortedFeatures[i][0]), sortedFeatures[i][1], sortedFeatures[i][2], sortedFeatures[i][3], sortedFeatures[i][4], sortedFeatures[i][5], sortedFeatures[i][6], sortedFeatures[i][7], sortedFeatures[i][8], sortedFeatures[i][9], sortedFeatures[i][10], sortedFeatures[i][11], sortedFeatures[i][12], sortedFeatures[i][13], sortedFeatures[i][14], sortedFeatures[i][15], sortedFeatures[i][16], sortedFeatures[i][17], sortedFeatures[i][18]))

		f_out.close()

