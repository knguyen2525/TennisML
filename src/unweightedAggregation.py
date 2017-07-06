# Reads in player stats over the years and averages the stats without any weights.

import os
import csv
from array import array

#pk,name1,name2,seed1,seed2,hand1,hand2,ht1,ht2,age1,age2,rank1,rank2,rank_points1,rank_points2,ace1,ace2,df1,df2,svpt1,svpt2,firstIn1,firstIn2,firstWon1,firstWon2,secondWon1,secondWon2,SvGms1,SvGms2,bpSaved1,bpSaved2,bpFaced1,bpFaced2,surface,tourney_date,result

def getPlayerStats(minYear, maxYear): 
	os.chdir("..")
	cwd = os.getcwd()
	input = cwd + "/features/atp_matches_" + str(minYear) + "-" + str(maxYear) + ".csv"

	players = {}

	with open(input, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for row in reader:
			if players.get(row["name1"]) is None: 
				players[row["name1"]] = []

			playerMatchData = {"ht": row["ht1"], "rank": row["rank1"], "rank_points": row["rank_points1"], "ace": row["ace1"], "df": row["df1"], "svpt": row["svpt1"], "firstIn": row["firstIn1"], "firstWon": row["firstWon1"], "secondWon": row["secondWon1"], "SvGms": row["SvGms1"], "bpSaved": row["bpSaved1"], "bpFaced": row["bpFaced1"], "tourney_date": row["tourney_date"]}
			players[row["name1"]].append(playerMatchData)

			if players.get(row["name2"]) is None: 
				players[row["name2"]] = []

			playerMatchData = {"ht": row["ht2"], "rank": row["rank2"], "rank_points": row["rank_points2"], "ace": row["ace2"], "df": row["df2"], "svpt": row["svpt2"], "firstIn": row["firstIn2"], "firstWon": row["firstWon2"], "secondWon": row["secondWon2"], "SvGms": row["SvGms2"], "bpSaved": row["bpSaved2"], "bpFaced": row["bpFaced2"], "tourney_date": row["tourney_date"]}
			players[row["name2"]].append(playerMatchData)

	return players

def timeToDays(time):
	year = time[:4]
	month = time[4:-2]
	day = time[-2:]

	return float(year)*365 + float(month)*30.42 + float(day)

def aggregatePlayerStats(players, minYear, currentYear):
	cwd = os.getcwd()
	output = cwd + "/features/unweighted/aggregated_stats_" + str(minYear) + "-" + str(currentYear) + ".csv"

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name", "ht", "rank", "rank_points", "ace", "df", "svpt", "firstIn", "firstWon", "secondWon", "SvGms", "bpSaved", "bpFaced"))

		for player in players:
			values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
			statsSum = array("f", values)
			statsCount = array("f", values)

			# ht, rank, rank_points, ace, df, svpt, firstIn, firstWon, secondWon, SvGms, bpSaved, bpFaced = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
			# htCount, rankCount, rank_pointsCount, aceCount, dfCount, svptCount, firstInCount, firstWonCount, secondWonCount, SvGmsCount, bpSavedCount, bpFacedCount = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
			for match in players[player]:
				if timeToDays(match["tourney_date"]) < timeToDays(str(currentYear*10000)):
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

if __name__ == "__main__":
	minYear = 2000
	maxYear = 2017

	print "gathering player data"
	players = getPlayerStats(2000, 2017)

	for year in range(minYear, maxYear):
		print 'generating unweighted training data up to year', str(year)
		aggregatePlayerStats(players, minYear, year)
		