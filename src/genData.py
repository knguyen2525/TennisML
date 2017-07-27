# Reads in player stats over the years and averages the stats without any weights.

import math
import sys
import os
import csv
from array import array

weighted = 0
testingYear = int(sys.argv[2])

def timeToDays(time):
	year = time[:4]
	month = time[4:-2]
	day = time[-2:]
	return float(year)*365 + float(month)*30.42 + float(day)

def getWeightFactor(matchDate, maxT):
	hyperParam = 0.9999
	return hyperParam ** (int(testingYear) * 10000 - int(matchDate))

def getHandDiff(hand1, hand2):
	return int(hand1) - int(hand2)

def getHead2Head(name1, name2, minT, maxT, players):
	matchCount = 0
	wins = 0

	for match in players[name1]:
		if match["opponent"] == name2 and isInDateRange(match["tourney_date"], minT, maxT):
			matchCount += 1
			if match["win"] == "1":
				wins += 1

	return wins - (matchCount - wins)

def isInDateRange(date, minT, maxT):
	return int(date) <= (int(maxT)*10000) and int(date) >= (int(minT)*10000) and int(date) < (testingYear*100000)

def diffStats(player1AverageStats, player2AverageStats):
	statsDiff = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	for i in range(0, len(player1AverageStats)):
		statsDiff[i] = player1AverageStats[i] - player2AverageStats[i]

	return statsDiff

def getCommonOpponents(name1, name2, minT, maxT, players):
	#does it make a copy or just create a pointer?

	#([], [])
	commonOpp = {}

	for match1 in players[name1]:
		for match2 in players[name2]:
			if match1["opponent"] == match2["opponent"] and isInDateRange(match1["tourney_date"], minT, maxT) and isInDateRange(match2["tourney_date"], minT, maxT):
				if commonOpp[match1["opponent"]] is None:
					commonOpp[match1["opponent"]] = ([], [])
				commonOpp[match1["opponent"]][0].append(match1)
				commonOpp[match1["opponent"]][1].append(match2)

def getPlayerStats(): 
	os.chdir("..")
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_1990-2018.csv"

	players = {}

	with open(input, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for match in reader:
			if players.get(match["name1"]) is None: 
				players[match["name1"]] = []

			playerMatchData = {"pk": match["pk"], "ht": match["ht1"], "rank": match["rank1"], "rank_points": match["rank_points1"], "ace": match["ace1"], "df": match["df1"], "svpt": match["svpt1"], "firstIn": match["firstIn1"], "firstWon": match["firstWon1"], "secondWon": match["secondWon1"], "SvGms": match["SvGms1"], "bpSaved": match["bpSaved1"], "bpFaced": match["bpFaced1"], "tourney_date": match["tourney_date"], "surface": match["surface"], "opponent": match["name2"], "tourney_date": match["tourney_date"]}

			if match["result"] == "1": 
				playerMatchData["win"] = "1"
			else:
				playerMatchData["win"] = "0"

			players[match["name1"]].append(playerMatchData)

			if players.get(match["name2"]) is None: 
				players[match["name2"]] = []

			playerMatchData = {"pk": match["pk"], "ht": match["ht2"], "rank": match["rank2"], "rank_points": match["rank_points2"], "ace": match["ace2"], "df": match["df2"], "svpt": match["svpt2"], "firstIn": match["firstIn2"], "firstWon": match["firstWon2"], "secondWon": match["secondWon2"], "SvGms": match["SvGms2"], "bpSaved": match["bpSaved2"], "bpFaced": match["bpFaced2"], "tourney_date": match["tourney_date"], "surface": match["surface"], "opponent": match["name1"], "tourney_date": match["tourney_date"]}

			if match["result"] == "1": 
				playerMatchData["win"] = "0"
			else:
				playerMatchData["win"] = "1"

			players[match["name2"]].append(playerMatchData)

	return players

def aggPlayerStats(matches, minT, maxT):
	statsSum = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	weightSum = 0.0

	for match in matches:
		if isInDateRange(match["tourney_date"], minT, maxT):
			wfactor = getWeightFactor(match["tourney_date"], maxT)
			if weighted == 0:
				wfactor = 1
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

	averageStats = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

	for i in range(0, len(statsSum)):
		averageStats[i] = statsSum[i]/weightSum

	return averageStats

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Error: Please specify", "minT", "maxT", "weighted"
		exit(0)

	minT = int(sys.argv[1])
	maxT = int(sys.argv[2])
	weighted = int(sys.argv[3])

	print "gathering player data"
	players = getPlayerStats()

	print "aggregating player data for matches"
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_1990-2018.csv"
	output = ""

	if weighted == 1: output = cwd + "/features/wData" + str(minT) + "-" + str(maxT-1) + ".csv"
	else: output = cwd + "/features/uwData" + str(minT) + "-" + str(maxT-1) + ".csv"

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "handDiff", "h2hDiff", "result"))

		with open(input, 'r') as f_in:
			reader = csv.DictReader(f_in)
			matchCounter = 0

			for match in reader:
				if isInDateRange(match["tourney_date"], minT, maxT):
					player1AggStats = aggPlayerStats(players[match["name1"]], minT, match["tourney_date"])
					player2AggStats = aggPlayerStats(players[match["name2"]], minT, match["tourney_date"])
					statsDiff = diffStats(player1AggStats, player2AggStats)

					handDiff = getHandDiff(match["hand1"], match["hand2"])
					h2hDiff = getHead2Head(match["name1"], match["name2"], minT, match["tourney_date"], players)

					f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(statsDiff[0]), str(float(match["age1"]) - float(match["age2"])), str(statsDiff[1]), str(statsDiff[2]), str(statsDiff[3]), str(statsDiff[4]), str(statsDiff[5]), str(statsDiff[6]), str(statsDiff[7]), str(statsDiff[8]), str(statsDiff[9]), str(statsDiff[10]), str(statsDiff[11]), str(handDiff), str(h2hDiff), match["result"]))

					if matchCounter % 1000 == 0 and matchCounter != 0: print "generated training data for: " + str(matchCounter) + " matches"
					matchCounter += 1

			print "generated training data for: " + str(matchCounter) + " matches"






























