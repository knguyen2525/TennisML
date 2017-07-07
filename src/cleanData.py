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
	# if not ht1: ht1 = 0
	# if not ht2: ht2 = 0
	if not ht1 or not ht2: return

	age1 = row[player1 + "_age"]; age2 = row[player2 + "_age"]
	# if not age1: age1 = 0
	# if not age2: age2 = 0
	if not age1 or not age2: return

	rank1 = row[player1 + "_rank"]; rank2 = row[player2 + "_rank"]
	# if not rank1: rank1 = 0
	# if not rank2: rank2 = 0
	if not rank1 or not rank2: return

	rank_points1 = row[player1 + "_rank_points"]; rank_points2 = row[player2 + "_rank_points"]
	# if not rank_points1: rank_points1 = 0
	# if not rank_points2: rank_points2 = 0
	if not rank_points1 or not rank_points2: return

	ace1 = row[player1[:1] + "_ace"]; ace2 = row[player2[:1] + "_ace"]
	# if not ace1: ace1 = 0
	# if not ace2: ace2 = 0
	if not ace1 or not ace2: return

	df1 = row[player1[:1] + "_df"]; df2 = row[player2[:1] + "_df"]
	# if not df1: df1 = 0
	# if not df2: df2 = 0
	if not df1 or not df2: return

	svpt1 = row[player1[:1] + "_svpt"]; svpt2 = row[player2[:1] + "_svpt"]
	# if not svpt1: svpt1 = 0
	# if not svpt2: svpt2 = 0
	if not svpt1 or not svpt2: return

	firstIn1 = row[player1[:1] + "_1stIn"]; firstIn2 = row[player2[:1] + "_1stIn"]
	# if not firstIn1: firstIn1 = 0
	# if not firstIn2: firstIn2 = 0
	if not firstIn1 or not firstIn2: return

	firstWon1 = row[player1[:1] + "_1stWon"]; firstWon2 = row[player2[:1] + "_1stWon"]
	# if not firstWon1: firstWon1 = 0
	# if not firstWon2: firstWon2 = 0
	if not firstWon1 or not firstWon2: return

	secondWon1 = row[player1[:1] + "_2ndWon"]; secondWon2 = row[player2[:1] + "_2ndWon"]
	# if not secondWon1: secondWon1 = 0
	# if not secondWon2: secondWon2 = 0
	if not secondWon1 or not secondWon2: return

	SvGms1 = row[player1[:1] + "_SvGms"]; SvGms2 = row[player2[:1] + "_SvGms"]
	# if not SvGms1: SvGms1 = 0
	# if not SvGms2: SvGms2 = 0
	if not SvGms1 or not SvGms2: return

	bpSaved1 = row[player1[:1] + "_bpSaved"]; bpSaved2 = row[player2[:1] + "_bpSaved"]
	# if not bpSaved1: bpSaved1 = 0
	# if not bpSaved2: bpSaved2 = 0
	if not bpSaved1 or not bpSaved2: return

	bpFaced1 = row[player1[:1] + "_bpFaced"]; bpFaced2 = row[player2[:1] + "_bpFaced"]
	# if not bpFaced1: bpFaced1 = 0
	# if not bpFaced2: bpFaced2 = 0
	if not bpFaced1 or not bpFaced2: return

	if row["surface"] == "Hard": surface = 1
	elif row["surface"] == "Grass": surface = 2
	elif row["surface"] == "Clay": surface = 3
	elif row["surface"] == "Carpet": surface = 4
	else: return

	tourney_date = row["tourney_date"]
	# if not tourney_date: tourney_date = 0
	if not tourney_date: return

	f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (pk, name1, name2, hand1, hand2, ht1, ht2, age1, age2, rank1, rank2, rank_points1, rank_points2, ace1, ace2, df1, df2, svpt1, svpt2, firstIn1, firstIn2, firstWon1, firstWon2, secondWon1, secondWon2, SvGms1, SvGms2, bpSaved1, bpSaved2, bpFaced1, bpFaced2, surface, tourney_date, result))

# Reads in rows from dataset and toggles inverting of labels
def clean(year, path, f_out):
	with open(path, 'r') as f_in:
		invert = 0
		reader = csv.DictReader(f_in)
		for row in reader:
			if invert == 0:
				writeMatchData(row, "winner", "loser", "1", f_out)
				invert = 1
			else:
				writeMatchData(row, "loser", "winner", "0", f_out)
				invert = 0

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Error: Please specify", "minYear", "maxYear"
		exit(0)

	minYear = int(sys.argv[1])
	maxYear = int(sys.argv[2])

	os.chdir("..")
	cwd = os.getcwd()
	output = cwd + "/features/atp_matches_" + str(minYear) + "-" + str(maxYear) + ".csv"

	with open(output, 'w') as f_out:
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("pk", "name1", "name2", "hand1", "hand2", "ht1", "ht2", "age1", "age2", "rank1", "rank2", "rank_points1", "rank_points2", "ace1", "ace2", "df1", "df2", "svpt1", "svpt2", "firstIn1", "firstIn2", "firstWon1", "firstWon2", "secondWon1", "secondWon2", "SvGms1", "SvGms2", "bpSaved1", "bpSaved2", "bpFaced1", "bpFaced2", "surface", "tourney_date", "result"))

		for year in range(minYear, maxYear):
			print "cleaning data for year", str(year)
			path = cwd + "/data/atp_matches_" + str(year) + ".csv"
			clean(int(year), path, f_out)




















