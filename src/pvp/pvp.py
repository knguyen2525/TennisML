import sys
sys.path.insert(0, "/Users/kevinnguyen/Projects/tennisml/src/util/")
from indexPlayers import getPlayerStats
from featureCreation import aggregate
from featureCreation import findStatsDifference
from featureCreation import getHandDifference
from featureCreation import getHeadToHeadDifference
from featureCreation import createFeatures
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
parser.add_argument("--cleanedAtpMatches", default="cleanedAtpMatches_1990_2017.csv", help="File with cleaned data")
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

	featureVector = [str(args.matchDate), str(statsDiff[0]), str(float(args.age1) - float(args.age2)), str(statsDiff[1]), str(statsDiff[2]), str(statsDiff[3]), str(statsDiff[4]), str(statsDiff[5]), str(statsDiff[6]), str(statsDiff[7]), str(statsDiff[8]), str(statsDiff[9]), str(statsDiff[10]), str(statsDiff[11]), str(statsDiff[12]), str(statsDiff[13]), str(handDiff), str(h2hDiff)]

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
	featureVector = getFeatureVector(players)

	print "creating features for training"
	features = createFeatures(inputFile, int(args.minYear), int(args.matchDate), args.type, players)

	# just create another file with no split for features
	# create a model training on all of this and pickel it
	# get that model in here and predict 1 row

	


