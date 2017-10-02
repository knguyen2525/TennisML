import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--minYear", default=1990, help="Min year for cleaning data")
parser.add_argument("--maxYear", default=2017, help="Max year for cleaning data")
args = parser.parse_args()

def writeMatchData(row, player1, player2, result, f_out):
	name1 = row[player1 + "_name"]; name2 = row[player2 + "_name"]

	# 1 = right handed
	# 2 = left handed
	hand1 = ""; hand2 = ""
	if row[player1 + "_hand"] == "R": hand1 = "1"
	else: hand1 = "2"
	if row[player2 + "_hand"] == "R": hand2 = "1"
	else: hand2 = "2"
	if not row[player1 + "_hand"] or not row[player2 + "_hand"]: return 0

	# Get player's ages
	age1 = row[player1 + "_age"]; age2 = row[player2 + "_age"]
	if not age1 or not age2 or age1 == "0" or age2 == "0": return 0

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

	# Get tourney ID
	tourney_id = row["tourney_id"]
	if not tourney_id: return 0

	# Get round
	round = row["round"]
	if not round: return 0

	# Write stats out to file
	f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (name1, name2, hand1, hand2, age1, age2, surface, tourney_date, tourney_id, round, result))

	f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name1", "name2", "hand1", "hand2", "age1", "age2", "surface", "tourney_date", "tourney_id", "round", "result"))

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
	outputFile = home + "/data/cleanedData/cleaned_" + str(minYear) + "_" + str(maxYear) + "_tourney.csv"

	# Counter to keep track of matches obtained from cleaning
	matchCounter = 0

	# Opening output stream
	with open(outputFile, 'w') as f_out:
		# Writing header file for cleaned data
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name1", "name2", "hand1", "hand2", "age1", "age2", "surface", "tourney_date", "tourney_id", "round", "result"))

		# For each year we are interested in, create a path for the file and clean the data
		# Keep a count of the number of matches cleaned
		for year in range(minYear, maxYear + 1):
			print "cleaning data for year", str(year)
			path = home + "/tennis_atp/atp_matches_" + str(year) + ".csv"
			numMatchesInYear = clean(path, f_out)
			matchCounter += numMatchesInYear

		print "Matches found from cleaning: " + str(matchCounter)

	f_out.close()
