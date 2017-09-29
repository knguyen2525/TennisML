# Counts number of matches given input files

import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--minYear", default=1990, help="Min year for cleaning data")
parser.add_argument("--maxYear", default=2017, help="Max year for cleaning data")
args = parser.parse_args()

def countMatches(inputFile):
	matchCount = 0
	with open(inputFile, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for row in reader:
			matchCount += 1

		f_in.close()
	return matchCount

if __name__ == "__main__":
	print args
	
	# Specifying year of matches we are interested in
	minYear = int(args.minYear)
	maxYear = int(args.maxYear)

	# Prepare the output file
	home = "/Users/kevinnguyen/Projects/tennisml"
	matchCount = 0

	for year in range(minYear, maxYear + 1):
		path = home + "/tennis_atp/atp_matches_" + str(year) + ".csv"
		matchCount += countMatches(path)

	print "Matches counted: " + str(matchCount)
