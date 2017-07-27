# Cleans data and converts positive labeled matches to negative labled matches
# Removes statistics that will not be used

import sys
import os
import csv

# Extracts row data and inverts data from a positive to negative label on half the rows.
# Writes output to file
def writeMatchData(row, player1, player2, result, f_out):
	pk = row["tourney_id"] + row["tourney_name"] + row["tourney_date"] + row[player1 + "_id"] + row[player2 + "_id"]
	name1 = row[player1 + "_name"]; name2 = row[player2 + "_name"]

	hand1 = ""; hand2 = ""
	if row[player1 + "_hand"] == "R" or not row[player1 + "_hand"]: hand1 = "1"
	else: hand1 = "2"
	if row[player2 + "_hand"] == "R" or not row[player2 + "_hand"]: hand2 = "1"
	else: hand2 = "2"

	ht1 = row[player1 + "_ht"]; ht2 = row[player2 + "_ht"]
	if not ht1 or not ht2: return 0

	age1 = row[player1 + "_age"]; age2 = row[player2 + "_age"]
	if not age1 or not age2: return 0

	rank1 = row[player1 + "_rank"]; rank2 = row[player2 + "_rank"]
	if not rank1 or not rank2: return 0

	rank_points1 = row[player1 + "_rank_points"]; rank_points2 = row[player2 + "_rank_points"]
	if not rank_points1 or not rank_points2: return 0

	ace1 = row[player1[:1] + "_ace"]; ace2 = row[player2[:1] + "_ace"]
	if not ace1 or not ace2: return 0

	df1 = row[player1[:1] + "_df"]; df2 = row[player2[:1] + "_df"]
	if not df1 or not df2: return 0

	svpt1 = row[player1[:1] + "_svpt"]; svpt2 = row[player2[:1] + "_svpt"]
	if not svpt1 or not svpt2: return 0

	firstIn1 = row[player1[:1] + "_1stIn"]; firstIn2 = row[player2[:1] + "_1stIn"]
	if not firstIn1 or not firstIn2: return 0

	firstWon1 = row[player1[:1] + "_1stWon"]; firstWon2 = row[player2[:1] + "_1stWon"]
	if not firstWon1 or not firstWon2: return 0

	secondWon1 = row[player1[:1] + "_2ndWon"]; secondWon2 = row[player2[:1] + "_2ndWon"]
	if not secondWon1 or not secondWon2: return 0

	SvGms1 = row[player1[:1] + "_SvGms"]; SvGms2 = row[player2[:1] + "_SvGms"]
	if not SvGms1 or not SvGms2: return 0

	bpSaved1 = row[player1[:1] + "_bpSaved"]; bpSaved2 = row[player2[:1] + "_bpSaved"]
	if not bpSaved1 or not bpSaved2: return 0

	bpFaced1 = row[player1[:1] + "_bpFaced"]; bpFaced2 = row[player2[:1] + "_bpFaced"]
	if not bpFaced1 or not bpFaced2: return 0

	if row["surface"] == "Hard": surface = 1
	elif row["surface"] == "Grass": surface = 2
	elif row["surface"] == "Clay": surface = 3
	elif row["surface"] == "Carpet": surface = 4
	else: return 0

	tourney_date = row["tourney_date"]
	if not tourney_date: return 0

	f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (pk, name1, name2, hand1, hand2, ht1, ht2, age1, age2, rank1, rank2, rank_points1, rank_points2, ace1, ace2, df1, df2, svpt1, svpt2, firstIn1, firstIn2, firstWon1, firstWon2, secondWon1, secondWon2, SvGms1, SvGms2, bpSaved1, bpSaved2, bpFaced1, bpFaced2, surface, tourney_date, result))
	return 1

# Reads in rows from dataset and toggles inverting of labels
def clean(year, path, f_out):
	with open(path, 'r') as f_in:
		invert = 0
		matchCounter = 0

		reader = csv.DictReader(f_in)
		for row in reader:
			if invert == 0:
				result = writeMatchData(row, "winner", "loser", "1", f_out)
				if result == 1: matchCounter += 1
				invert = 1
			else:
				result = writeMatchData(row, "loser", "winner", "0", f_out)
				if result == 1: matchCounter += 1
				invert = 0

		return matchCounter

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Error: Please specify", "minYear", "maxYear"
		exit(0)

	minYear = int(sys.argv[1])
	maxYear = int(sys.argv[2])

	os.chdir("..")
	cwd = os.getcwd()
	output = cwd + "/features/atp_matches_" + str(minYear) + "-" + str(maxYear) + ".csv"

	matchCounter = 0

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("pk", "name1", "name2", "hand1", "hand2", "ht1", "ht2", "age1", "age2", "rank1", "rank2", "rank_points1", "rank_points2", "ace1", "ace2", "df1", "df2", "svpt1", "svpt2", "firstIn1", "firstIn2", "firstWon1", "firstWon2", "secondWon1", "secondWon2", "SvGms1", "SvGms2", "bpSaved1", "bpSaved2", "bpFaced1", "bpFaced2", "surface", "tourney_date", "result"))

		for year in range(minYear, maxYear):
			print "cleaning data for year", str(year)
			path = cwd + "/tennis_atp/atp_matches_" + str(year) + ".csv"
			result = clean(int(year), path, f_out)
			matchCounter += result

		print "Matches found from cleaning: " + str(matchCounter)




















