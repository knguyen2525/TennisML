# Reads in player stats over the years and averages the stats without any weights.

import os
import csv

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

			playerData = {"seed": row["seed1"], "ht": row["ht1"], "rank": row["rank1"], "rank_points": row["rank_points1"], "ace": row["ace1"], "df": row["df1"], "svpt": row["svpt1"], "firstIn": row["firstIn1"], "firstWon": row["firstWon1"], "secondWon": row["secondWon1"], "SvGms": row["SvGms1"], "bpSaved": row["bpSaved1"], "bpFaced": row["bpFaced1"]}
			players[row["name1"]].append(playerData)

			if players.get(row["name2"]) is None: 
				players[row["name2"]] = []

			playerData = {"seed": row["seed2"], "ht": row["ht2"], "rank": row["rank2"], "rank_points": row["rank_points2"], "ace": row["ace2"], "df": row["df2"], "svpt": row["svpt2"], "firstIn": row["firstIn2"], "firstWon": row["firstWon2"], "secondWon": row["secondWon2"], "SvGms": row["SvGms2"], "bpSaved": row["bpSaved2"], "bpFaced": row["bpFaced2"]}
			players[row["name2"]].append(playerData)

	return players

def aggregatePlayerStats(players, minYear, year):
	cwd = os.getcwd()
	output = cwd + "/features/atp_matches_" + str(minYear) + "-" + str(year) + ".csv"

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name", "seed", "ht", "rank", "rank_points", "ace", "df", "svpt", "firstIn", "firstWon", "secondWon", "SvGms", "bpSaved", "bpFaced"))

		for player in players:
			

if __name__ == "__main__":
	minYear = 2000
	maxYear = 2017

	print "gathering player data"
	players = getPlayerStats(minYear, maxYear)

	for year in range(minYear, maxYear):
		print 'generating unweighted training data up to year', str(year)
		aggregatePlayerStats(players, minYear, year)
		