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

	# cwd = os.getcwd()
	# output = cwd + "/features/trainingData" + str(minYear) + "-" + str(testingYear-1) + "UW.csv"

	# with open(output, 'w') as f_out:
	# 	f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name", "ht", "rank", "rank_points", "ace", "df", "svpt", "firstIn", "firstWon", "secondWon", "SvGms", "bpSaved", "bpFaced"))

	with open(input, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for match in reader:
			if timeToDays(match["tourney_date"]) < timeToDays(str(testingYear*10000)) and timeToDays(match["tourney_date"]) >= timeToDays(str(minYear*10000)):
				name1 = match["name1"]; name2 = match["name2"]
				player1AverageStats = aggregatePlayerStats(players[name1], minYear, testingYear)
				player2AverageStats = aggregatePlayerStats(players[name2], minYear, testingYear)

				statsDiff = array("f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
				for i in range(0, len(player1AverageStats)):
					if match["result"] == "1":
						statsDiff[i] = player1AverageStats - player2AverageStats
					else:
						statsDiff[i] = player2AverageStats - player1AverageStats

				#concat with match info then write to file


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
