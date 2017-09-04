# Holds functions responsible for aggregating player stats within a time period
# Takes care of weighing stats based on certain factors (time, surface, hand)

from array import array
from timeUtil import isDateInRange
from generateWeights import getWeightFactor

# Given a players matches, creates average stats vector for a player
def aggregate(playersMatches, minYear, currentMatchTime, featureType):
	statsSum = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	weightSum = 0.0

	for match in playersMatches:
		# If match is in the range we care about
		if isDateInRange(match["tourney_date"], minYear * 1000, currentMatchTime):
			wfactor = 0

			# Get the weights if we are doing weighted
			if featureType == "weighted": wfactor = getWeightFactor(match["tourney_date"], currentMatchTime)
			else: wfactor = 1

			# Sum up the stats while keeping track of weighted sum
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
			weightSum += wfactor

	# If we did not find any matches to aggregate before the current match
	if weightSum == 0: return 0
	
	# Get the average of all the stats found
	averageStats = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	for i in range(0, len(statsSum)):
		averageStats[i] = statsSum[i]/weightSum

	return averageStats

# Takes the difference of states between two players averages
def findStatsDifference(player1AverageStats, player2AverageStats):
	statsDiff = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
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