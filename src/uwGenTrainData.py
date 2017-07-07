# Reads in player stats over the years and averages the stats without any weights.

import sys
import os
import csv
from array import array

def getPlayerStats(): 
	os.chdir("..")
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_1990-2017.csv"

	players = {}

	with open(input, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for match in reader:
			if players.get(match["name1"]) is None: 
				players[match["name1"]] = []

			playerMatchData = {"ht": match["ht1"], "rank": match["rank1"], "rank_points": match["rank_points1"], "ace": match["ace1"], "df": match["df1"], "svpt": match["svpt1"], "firstIn": match["firstIn1"], "firstWon": match["firstWon1"], "secondWon": match["secondWon1"], "SvGms": match["SvGms1"], "bpSaved": match["bpSaved1"], "bpFaced": match["bpFaced1"], "tourney_date": match["tourney_date"]}
			players[match["name1"]].append(playerMatchData)

			if players.get(match["name2"]) is None: 
				players[match["name2"]] = []

			playerMatchData = {"ht": match["ht2"], "rank": match["rank2"], "rank_points": match["rank_points2"], "ace": match["ace2"], "df": match["df2"], "svpt": match["svpt2"], "firstIn": match["firstIn2"], "firstWon": match["firstWon2"], "secondWon": match["secondWon2"], "SvGms": match["SvGms2"], "bpSaved": match["bpSaved2"], "bpFaced": match["bpFaced2"], "tourney_date": match["tourney_date"]}
			players[match["name2"]].append(playerMatchData)

	return players

def timeToDays(time):
	year = time[:4]
	month = time[4:-2]
	day = time[-2:]

	return float(year)*365 + float(month)*30.42 + float(day)

def aggregatePlayerStats(matches, minYear, testingYear):
	statsSum = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	count = 0.0

	for match in matches:
		if timeToDays(match["tourney_date"]) < timeToDays(str(testingYear*10000)) and timeToDays(match["tourney_date"]) >= timeToDays(str(minYear*10000)):
			statsSum[0] += float(match["ht"])
			statsSum[1] += float(match["rank"])
			statsSum[2] += float(match["rank_points"])
			statsSum[3] += float(match["ace"])
			statsSum[4] += float(match["df"])
			statsSum[5] += float(match["svpt"])
			statsSum[6] += float(match["firstIn"])
			statsSum[7] += float(match["firstWon"])
			statsSum[8] += float(match["secondWon"])
			statsSum[9] += float(match["SvGms"])
			statsSum[10] += float(match["bpSaved"])
			statsSum[11] += float(match["bpFaced"])
			count += 1

	averageStats = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	for i in range(0, len(statsSum)):
		averageStats[i] = statsSum[i]/count

	return averageStats

def generateTrainingData(players, minYear, testingYear):
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_1990-2017.csv"

	cwd = os.getcwd()
	output = cwd + "/features/uwTrainingData" + str(minYear) + "-" + str(testingYear-1) + ".csv"

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("htDiff", "ageDiff", "rankDiff", "rank_pointsDiff", "aceDiff", "dfDiff", "svptDiff", "firstInDiff", "firstWonDiff", "secondWonDiff", "SvGmsDiff", "bpSavedDiff", "bpFacedDiff", "result"))

		with open(input, 'r') as f_in:
			reader = csv.DictReader(f_in)
			matchCounter = 0

			for match in reader:
				if timeToDays(match["tourney_date"]) < timeToDays(str(testingYear*10000)) and timeToDays(match["tourney_date"]) >= timeToDays(str(minYear*10000)):

					player1AverageStats = aggregatePlayerStats(players[match["name1"]], minYear, testingYear)
					player2AverageStats = aggregatePlayerStats(players[match["name2"]], minYear, testingYear)

					statsDiff = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
					for i in range(0, len(player1AverageStats)):
						if match["result"] == "1":
							statsDiff[i] = player1AverageStats[i] - player2AverageStats[i]
						else:
							statsDiff[i] = player2AverageStats[i] - player1AverageStats[i]

					f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(statsDiff[0]), str(float(match["age1"]) - float(match["age2"])), str(statsDiff[1]), str(statsDiff[2]), str(statsDiff[3]), str(statsDiff[4]), str(statsDiff[5]), str(statsDiff[6]), str(statsDiff[7]), str(statsDiff[8]), str(statsDiff[9]), str(statsDiff[10]), str(statsDiff[11]), match["result"]))

					if matchCounter % 1000 == 0 and matchCounter != 0: print "Generated training data for: " + str(matchCounter) + " matches"
					matchCounter += 1

			print "Generated training data for: " + str(matchCounter) + " matches"

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Error: Please specify", "minYear", "testingYear"
		exit(0)

	minYear = int(sys.argv[1])
	testingYear = int(sys.argv[2])

	print "gathering player data"
	players = getPlayerStats()

	print "aggregating player data for matches"
	generateTrainingData(players, minYear, testingYear)
