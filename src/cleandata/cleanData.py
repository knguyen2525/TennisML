# Cleans tennis data given a min year and max year
# Matches are usually from the perspective of the winner in the raw data so this script takes half the matches
# and reverses the perspective to have an equal number of matches from the winner's perspective and loser's perspective

import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--minYear", default=1990, help="Min year for cleaning data")
parser.add_argument("--maxYear", default=2017, help="Max year for cleaning data")
args = parser.parse_args()

# Extracts row data and inverts data from a positive to negative labels on half the rows
# Writes output to file
def writeMatchData(row, player1, player2, result, f_out):
	# For each match, grab the stats for each player using player1 and player2 as winner and loser or loser and winner
	# If any stat is missing in the match, do not count the match
	pk = row["tourney_id"] + row["tourney_name"] + row["tourney_date"] + row[player1 + "_id"] + row[player2 + "_id"]
	name1 = row[player1 + "_name"]; name2 = row[player2 + "_name"]

	# 1 = right handed
	# 2 = left handed
	hand1 = ""; hand2 = ""
	if row[player1 + "_hand"] == "R": hand1 = "1"
	else: hand1 = "2"
	if row[player2 + "_hand"] == "R": hand2 = "1"
	else: hand2 = "2"
	if not row[player1 + "_hand"] or not row[player2 + "_hand"]: return 0

	# Get player's heights
	ht1 = row[player1 + "_ht"]; ht2 = row[player2 + "_ht"]
	if not ht1 or not ht2 or ht1 == "0" or ht2 == "0": return 0

	# Get player's ages
	age1 = row[player1 + "_age"]; age2 = row[player2 + "_age"]
	if not age1 or not age2 or age1 == "0" or age2 == "0": return 0

	# Get player's ages
	rank1 = row[player1 + "_rank"]; rank2 = row[player2 + "_rank"]
	if not rank1 or not rank2  or rank1 == "0" or rank2 == "0": return 0

	# Get player's rank points
	rank_points1 = row[player1 + "_rank_points"]; rank_points2 = row[player2 + "_rank_points"]
	if not rank_points1 or not rank_points2  or rank_points1 == "0" or rank_points2 == "0": return 0

	# Get player's aces
	ace1 = row[player1[:1] + "_ace"]; ace2 = row[player2[:1] + "_ace"]
	if not ace1 or not ace2: return 0

	# Get player's double faults
	df1 = row[player1[:1] + "_df"]; df2 = row[player2[:1] + "_df"]
	if not df1 or not df2: return 0

	# Get player's number of service points
	svpt1 = row[player1[:1] + "_svpt"]; svpt2 = row[player2[:1] + "_svpt"]
	if not svpt1 or not svpt2 or svpt1 == "0" or svpt2 == "0": return 0

	# Get player's number of first serves in
	firstIn1 = row[player1[:1] + "_1stIn"]; firstIn2 = row[player2[:1] + "_1stIn"]
	if not firstIn1 or not firstIn2: return 0

	# Get player's number of points won when first serve went in
	firstWon1 = row[player1[:1] + "_1stWon"]; firstWon2 = row[player2[:1] + "_1stWon"]
	if not firstWon1 or not firstWon2: return 0

	# Get player's number of points on when second serve went in
	secondWon1 = row[player1[:1] + "_2ndWon"]; secondWon2 = row[player2[:1] + "_2ndWon"]
	if not secondWon1 or not secondWon2: return 0

	# Get number of service games for each player
	SvGms1 = row[player1[:1] + "_SvGms"]; SvGms2 = row[player2[:1] + "_SvGms"]
	if not SvGms1 or not SvGms2 or SvGms1 == "0" or SvGms2 == "0": return 0

	# Get number of breakpoints saved by each player
	bpSaved1 = row[player1[:1] + "_bpSaved"]; bpSaved2 = row[player2[:1] + "_bpSaved"]
	if not bpSaved1 or not bpSaved2: return 0

	# Get number of breakpoints faced by each player
	bpFaced1 = row[player1[:1] + "_bpFaced"]; bpFaced2 = row[player2[:1] + "_bpFaced"]
	if not bpFaced1 or not bpFaced2: return 0

	# Get the surface information
	# 1 = hard
	# 2 = grass
	# 3 = clay
	# 4 = carpet
	if row["surface"] == "Hard": surface = "hard"
	elif row["surface"] == "Grass": surface = "grass"
	elif row["surface"] == "Clay": surface = "clay"
	elif row["surface"] == "Carpet": surface = "carpet"
	else: return 0

	# Get the date of the tourney
	tourney_date = row["tourney_date"]
	if not tourney_date: return 0

	# Check if match ended normally
	score = row["score"].strip()
	if score[-1:] != ")" and not score[-1:].isdigit(): return 0

	# Write stats out to file
	f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (pk, name1, name2, hand1, hand2, ht1, ht2, age1, age2, rank1, rank2, rank_points1, rank_points2, ace1, ace2, df1, df2, svpt1, svpt2, firstIn1, firstIn2, firstWon1, firstWon2, secondWon1, secondWon2, SvGms1, SvGms2, bpSaved1, bpSaved2, bpFaced1, bpFaced2, surface, tourney_date, result))

	return 1

# Reads in a file containing a years worth of matches to be cleaned
def clean(inputFile, f_out):
	invert = 0
	matchCounter = 0
	
	# Open file for year
	with open(inputFile, 'r') as f_in:
		reader = csv.DictReader(f_in)
		# For each row, write the match data to output csv
		# Invert winner and loser to clean data
		for row in reader:
			if invert == 0:
				result = writeMatchData(row, "winner", "loser", "1", f_out)
				if result == 1: matchCounter += 1
			else:
				result = writeMatchData(row, "loser", "winner", "0", f_out)
				if result == 1: matchCounter += 1

			invert = (invert + 1) % 2

	f_in.close()
	return matchCounter

if __name__ == "__main__":
	print args
	
	# Specifying year of matches we are interested in
	minYear = int(args.minYear)
	maxYear = int(args.maxYear)

	# Prepare the output file
	home = "/Users/kevinnguyen/Projects/tennisml"
	outputFile = home + "/data/cleanedData/cleaned_" + str(minYear) + "_" + str(maxYear) + ".csv"

	# Counter to keep track of matches obtained from cleaning
	matchCounter = 0

	# Opening output stream
	with open(outputFile, 'w') as f_out:
		# Writing header file for cleaned data
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("pk", "name1", "name2", "hand1", "hand2", "ht1", "ht2", "age1", "age2", "rank1", "rank2", "rank_points1", "rank_points2", "ace1", "ace2", "df1", "df2", "svpt1", "svpt2", "firstIn1", "firstIn2", "firstWon1", "firstWon2", "secondWon1", "secondWon2", "SvGms1", "SvGms2", "bpSaved1", "bpSaved2", "bpFaced1", "bpFaced2", "surface", "tourney_date", "result"))

		# For each year we are interested in, create a path for the file and clean the data
		# Keep a count of the number of matches cleaned
		for year in range(minYear, maxYear + 1):
			print "cleaning data for year", str(year)
			path = home + "/tennis_atp/atp_matches_" + str(year) + ".csv"
			numMatchesInYear = clean(path, f_out)
			matchCounter += numMatchesInYear

		print "Matches found from cleaning: " + str(matchCounter)

	f_out.close()




















