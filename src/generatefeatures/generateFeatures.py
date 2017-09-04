# Reads in player stats over the years and averages the stats without any weights.

# import math
import sys
sys.path.append("/Users/kevinnguyen/Projects/tennisml/src/util/")
import csv
from indexPlayers import getPlayerStats
from timeUtil import isDateInRange
from compilePlayerStats import aggregate
from compilePlayerStats import findStatsDifference
from compilePlayerStats import getHandDifference
from compilePlayerStats import getHeadToHeadDifference

# Loops through matches and generates features for each match in cleaned data
def generateFeatures(outputFile, minYear, maxYear, featureType, players):
	# Write header of output file
	with open(outputFile, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "handDiff", "h2hDiff", "result"))

		# Reading in match data from cleaned data
	 	with open(inputFile, 'r') as f_in:
	 		reader = csv.DictReader(f_in)
	 		matchCounter = 0

	 		# For each match, aggregate player stats based on previous matches and output feature vector for that match
	 		print "aggregating player data and generating features"
			for match in reader:
	 			if isDateInRange(match["tourney_date"], minYear * 10000, maxYear * 10000):
	 				# Aggregating general player stats. Also weighs if weighted parameter is passed in
	 				player1AggStats = aggregate(players[match["name1"]], minYear, match["tourney_date"], featureType)
	 				player2AggStats = aggregate(players[match["name2"]], minYear, match["tourney_date"], featureType)

	 				# If could not find any stats before the current match then jump to next loop iteration
	 				if player1AggStats == 0 or player2AggStats == 0: continue

	 				# Find the difference between the two stats vectors
					statsDiff = findStatsDifference(player1AggStats, player2AggStats)

					# Find other stats such as player hands and head to head
	 				handDiff = getHandDifference(match["hand1"], match["hand2"])
	 				h2hDiff = getHeadToHeadDifference(match["name1"], match["name2"], players[match["name1"]], players[match["name2"]], minYear, match["tourney_date"])

	 				# Write difference vector to output feature file
	 				f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(statsDiff[0]), str(float(match["age1"]) - float(match["age2"])), str(statsDiff[1]), str(statsDiff[2]), str(statsDiff[3]), str(statsDiff[4]), str(statsDiff[5]), str(statsDiff[6]), str(statsDiff[7]), str(statsDiff[8]), str(statsDiff[9]), str(statsDiff[10]), str(statsDiff[11]), str(handDiff), str(h2hDiff), match["result"]))

	 				if matchCounter % 1000 == 0 and matchCounter != 0: print "generated feature vectors for: " + str(matchCounter) + " matches"
	 				matchCounter += 1

	 		print "generated feature vectors for: " + str(matchCounter) + " matches"
	 		
	 	f_in.close()
 	f_out.close()


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
	outputFile = home + "/data/features/" + featureType + "_" + str(minYear) + "-" + str(maxYear) + ".csv"
	generateFeatures(outputFile, minYear, maxYear, featureType, players)






























