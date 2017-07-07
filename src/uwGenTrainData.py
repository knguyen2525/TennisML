# Reads in player stats over the years and averages the stats without any weights.

import sys
import os
import csv
from array import array

#pk,name1,name2,seed1,seed2,hand1,hand2,ht1,ht2,age1,age2,rank1,rank2,rank_points1,rank_points2,ace1,ace2,df1,df2,svpt1,svpt2,firstIn1,firstIn2,firstWon1,firstWon2,secondWon1,secondWon2,SvGms1,SvGms2,bpSaved1,bpSaved2,bpFaced1,bpFaced2,surface,tourney_date,result

def getPlayerStats(): 
	os.chdir("..")
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_2000-2017.csv"

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

def aggregatePlayerStats(players, minYear, testingYear):
	cwd = os.getcwd()
	output = cwd + "/features/trainingData" + str(minYear) + "-" + str(testingYear-1) + "UW.csv"

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name", "ht", "rank", "rank_points", "ace", "df", "svpt", "firstIn", "firstWon", "secondWon", "SvGms", "bpSaved", "bpFaced"))

		for player in players:
			values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
			statsSum = array("f", values)
			statsCount = array("f", values)

			for match in players[player]:
				if timeToDays(match["tourney_date"]) < timeToDays(str(testingYear*10000)) and timeToDays(match["tourney_date"]) >= timeToDays(str(minYear*10000)):
					if float(match["ht"]) != 0:
						statsSum[0] += float(match["ht"])
						statsCount[0] += 1.0

					if float(match["rank"]) != 0:
						statsSum[1] += float(match["rank"])
						statsCount[1] += 1.0

					if float(match["rank_points"]) != 0:
						statsSum[2] += float(match["rank_points"])
						statsCount[2] += 1.0

					if float(match["ace"]) != 0:
						statsSum[3] += float(match["ace"])
						statsCount[3] += 1.0

					if float(match["df"]) != 0:
						statsSum[4] += float(match["df"])
						statsCount[4] += 1.0

					if float(match["svpt"]) != 0:
						statsSum[5] += float(match["svpt"])
						statsCount[5] += 1.0

					if float(match["firstIn"]) != 0:
						statsSum[6] += float(match["firstIn"])
						statsCount[6] += 1.0

					if float(match["firstWon"]) != 0:
						statsSum[7] += float(match["firstWon"])
						statsCount[7] += 1.0

					if float(match["secondWon"]) != 0:
						statsSum[8] += float(match["secondWon"])
						statsCount[8] += 1.0

					if float(match["SvGms"]) != 0:
						statsSum[9] += float(match["SvGms"])
						statsCount[9] += 1.0

					if float(match["bpSaved"]) != 0:
						statsSum[10] += float(match["bpSaved"])
						statsCount[10] += 1.0

					if float(match["bpFaced"]) != 0:
						statsSum[11] += float(match["bpFaced"])
						statsCount[11] += 1.0

			averageStats = [0.0] * 12
			for i in range(0, len(statsSum)):
				if statsCount[i] != 0.0:
					averageStats[i] = statsSum[i]/statsCount[i]
				else:
					averageStats[i] = 0.0

			if sum(statsCount) != 0:		
				f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (player, str(averageStats[0]), str(averageStats[1]), str(averageStats[2]), str(averageStats[3]), str(averageStats[4]), str(averageStats[5]), str(averageStats[6]), str(averageStats[7]), str(averageStats[8]), str(averageStats[9]), str(averageStats[10]), str(averageStats[11])))

def generateTrainingData(players, minYear, testingYear):
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_2000-2017.csv"

	with open(input, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for match in reader:
			if timeToDays(match["tourney_date"]) < timeToDays(str(testingYear*10000)) and timeToDays(match["tourney_date"]) >= timeToDays(str(minYear*10000)):
				name1 = match["name1"]; name2 = match["name2"]
				player1AverageStats = aggregatePlayerStats(players[name1])
				player2AverageStats = aggregatePlayerStats(players[name2])

				#subtract them, concat with match info, write out to file


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

	# print 'generating unweighted training data for year', str(testingYear)
	# aggregatePlayerStats(players, minYear, testingYear)
