# Holds functions responsible for aggregating player stats within a time period
# Takes care of weighing stats based on certain factors (time, surface, hand)

import csv
from array import array
from timeUtil import isDateInRange
from generateWeights import getWeightFactor

# Loops through matches and generates features for each match in cleaned data
def createFeatures(inputFile, minYear, maxYear, featureType, players):
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

				featureVector = [int(match["tourney_date"]), str(statsDiff[0]), str(float(match["age1"]) - float(match["age2"])), str(statsDiff[1]), str(statsDiff[2]), str(statsDiff[3]), str(statsDiff[4]), str(statsDiff[5]), str(statsDiff[6]), str(statsDiff[7]), str(statsDiff[8]), str(statsDiff[9]), str(statsDiff[10]), str(statsDiff[11]), str(statsDiff[12]), str(statsDiff[13]), str(statsDiff[14]), str(handDiff), str(h2hDiff), match["result"]]
				features.append(featureVector)

				if len(features) % 1000 == 0 and len(features) != 0: print "generated feature vectors for: " + str(len(features)) + " matches"

		print "generated feature vectors for: " + str(len(features)) + " matches"
		
	f_in.close()
	return features

# Given a players matches, creates average stats vector for a player
def aggregate(playersMatches, matchSurface, minYear, currentMatchTime, featureType):
	statsSum = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	weightSum = 0.0
	surfaceWinWeightCount = 0.0
	surfaceMatchWeightSum = 0.0

	for match in playersMatches:
		# If match is in the range we care about
		if isDateInRange(match["tourney_date"], minYear * 1000, currentMatchTime):
			# you are doing this loop twice
			wfactor = 0.0

			# Get the weights if we are doing weighted
			if featureType == "weighted": wfactor = getWeightFactor(match, playersMatches, minYear, currentMatchTime)
			else: wfactor = 1.0

			# Sum up the stats while keeping track of weighted sum. Basic Stats
			statsSum[0] += wfactor * float(match["ht"])
			statsSum[1] += wfactor * float(match["rank"])
			statsSum[2] += wfactor * float(match["rank_points"])
			statsSum[3] += wfactor * float(match["ace"])
			statsSum[4] += wfactor * float(match["df"])
			statsSum[5] += wfactor * float(match["svpt"])
			statsSum[6] += wfactor * float(match["firstIn"])
			statsSum[7] += wfactor * float(match["firstWon"])
			statsSum[8] += wfactor * float(match["secondWon"])
			statsSum[9] += wfactor * float(match["SvGms"])
			statsSum[10] += wfactor * float(match["bpSaved"])
			statsSum[11] += wfactor * float(match["bpFaced"])

			# Break points lost stats
			statsSum[12] += wfactor * float(int(match["bpFaced"]) - int(match["bpSaved"]))

			# Service aptitude
			statsSum[13] += wfactor * float(int(match["firstWon"]) + int(match["secondWon"]) - int(match["bpFaced"])) / float(match["svpt"])

			# Surface stats
			surfaceWin, surfaceMatch = getSurfaceStats(matchSurface, match)
			surfaceWinWeightCount += wfactor * surfaceWin
			surfaceMatchWeightSum += wfactor * surfaceMatch

			weightSum += wfactor

	# If we did not find any matches to aggregate before the current match
	if weightSum == 0.0: return 0

	# Get the average of all the stats found
	averageStats = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	for i in range(0, len(statsSum)):
		averageStats[i] = statsSum[i] / weightSum

	# Adding surface feature. If not matches played on surface than append 0.5
	if surfaceMatchWeightSum == 0.0: averageStats.append(0.5)
	else: averageStats.append(surfaceWinWeightCount / surfaceMatchWeightSum)

	return averageStats

# Takes the difference of states between two players averages
def findStatsDifference(player1AverageStats, player2AverageStats):
	statsDiff = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	for i in range(0, len(player1AverageStats)):
		statsDiff[i] = player1AverageStats[i] - player2AverageStats[i]

	return statsDiff

# Returns the hand difference between two players
def getHandDifference(hand1, hand2):
	return int(hand1) - int(hand2)

# Gathers head to head data between two players
def getHeadToHeadDifference(name1, name2, player1Matches, player2Matches, minYear, currentMatchTime):
	matchCount = 0
	wins = 0

	# Finds all matches with player 1 and player 2. Finds the wins of player 1 and returns wins - losses from player 1's perspective
	for match in player1Matches:
		if match["opponent"] == name2 and isDateInRange(match["tourney_date"], minYear * 1000, currentMatchTime):
			matchCount += 1
			if match["win"] == "1":
				wins += 1

	return wins - (matchCount - wins)

# Passing in surface of match in question. Checking current match if same surface and if win or not
def getSurfaceStats(matchSurface, match):
	if matchSurface == match["surface"]:
		if match["win"] == "1":
			return 1.0, 1.0
		else:
			return 0.0, 1.0
	else:
		return 0.0, 0.0








