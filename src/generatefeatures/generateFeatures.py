# Reads in player stats over the years and averages the stats without any weights.

# import math
import sys
sys.path.append("/Users/kevinnguyen/Projects/tennisml/src/util/")
import math
from indexPlayers import getPlayerStats
from featureCreation import createFeatures
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--minYear", default=1990, help="Min year for cleaning data")
parser.add_argument("--maxYear", default=2017, help="Max year for cleaning data")
parser.add_argument("--cleanedAtpMatches", default="cleaned_1990_2017.csv", help="File with cleaned data")
parser.add_argument("--type", default="weighted", help="Weighted or unweighted features")
parser.add_argument("--pvp", default=True, help="Create features for all or 70/30 split")
args = parser.parse_args()

if __name__ == "__main__":
	print args
	
	# Gathering auxiliary data
	minYear = int(args.minYear)
	maxYear = int(args.maxYear)
	home = "/Users/kevinnguyen/Projects/tennisml"
	inputFile = home + "/data/cleanedData/" + args.cleanedAtpMatches
	featureType = args.type

	# Indexing player stats
	print "gathering player data"
	players = getPlayerStats(inputFile)

	# Calling generateFeatures to create feature vectors
	outputFile = home + "/data/features/" + featureType + "_" + str(minYear) + "_" + str(maxYear)
	features = createFeatures(inputFile, minYear, maxYear, featureType, players)

	# Sorting features by tourney date
	print "Sorting features by tourney_date"
	sortedFeatures = np.array(sorted(features))

	# Finding training/testing split 70/30
	numTrainingFeatures = int(math.ceil(0.7 * len(features))) - 1
	print "Training vectors is " + str(numTrainingFeatures)
	print "Testing vectors is " + str(len(features) - numTrainingFeatures)

	# Write features to file after sorting by date
	print "Writing training data to file"
	with open(outputFile + "_training.csv", 'w') as f_out:
		# Write header of output file
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("tourney_date", "htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "bpLostDiff", "svgAptDiff", "surfaceWinsDiff", "handDiff", "h2hDiff", "result"))

		for i in range(0, numTrainingFeatures):
			# Write difference vector to output feature file
			f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (sortedFeatures[i][0], sortedFeatures[i][1], sortedFeatures[i][2], sortedFeatures[i][3], sortedFeatures[i][4], sortedFeatures[i][5], sortedFeatures[i][6], sortedFeatures[i][7], sortedFeatures[i][8], sortedFeatures[i][9], sortedFeatures[i][10], sortedFeatures[i][11], sortedFeatures[i][12], sortedFeatures[i][13], sortedFeatures[i][14], sortedFeatures[i][15], sortedFeatures[i][16], sortedFeatures[i][17], sortedFeatures[i][18], sortedFeatures[i][19]))

		f_out.close()

	# Write features to file after sorting by date
	print "Writing testing data to file"
	with open(outputFile + "_testing.csv", 'w') as f_out:
		# Write header of output file
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("tourney_date", "htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "bpLostDiff", "svgAptDiff", "surfaceWinsDiff", "handDiff", "h2hDiff", "result"))

		for i in range(numTrainingFeatures, len(features)):
			# Write difference vector to output feature file
			f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(sortedFeatures[i][0]), sortedFeatures[i][1], sortedFeatures[i][2], sortedFeatures[i][3], sortedFeatures[i][4], sortedFeatures[i][5], sortedFeatures[i][6], sortedFeatures[i][7], sortedFeatures[i][8], sortedFeatures[i][9], sortedFeatures[i][10], sortedFeatures[i][11], sortedFeatures[i][12], sortedFeatures[i][13], sortedFeatures[i][14], sortedFeatures[i][15], sortedFeatures[i][16], sortedFeatures[i][17], sortedFeatures[i][18], sortedFeatures[i][19]))

		f_out.close()

	if args.pvp == True:
		# Write all features to one training file
		print "Writing training data to one file"
		print "Training vectors is " + str(len(features))
		
		with open(outputFile + "_training_all.csv", 'w') as f_out:
			# Write header of output file
			f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("tourney_date", "htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "bpLostDiff", "svgAptDiff", "surfaceWinsDiff", "handDiff", "h2hDiff", "result"))

			for i in range(0, len(features)):
				# Write difference vector to output feature file
				f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (sortedFeatures[i][0], sortedFeatures[i][1], sortedFeatures[i][2], sortedFeatures[i][3], sortedFeatures[i][4], sortedFeatures[i][5], sortedFeatures[i][6], sortedFeatures[i][7], sortedFeatures[i][8], sortedFeatures[i][9], sortedFeatures[i][10], sortedFeatures[i][11], sortedFeatures[i][12], sortedFeatures[i][13], sortedFeatures[i][14], sortedFeatures[i][15], sortedFeatures[i][16], sortedFeatures[i][17], sortedFeatures[i][18], sortedFeatures[i][19]))

			f_out.close()


