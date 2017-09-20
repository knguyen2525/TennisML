# Counts number of matches given input files

import sys
import csv

def countMatches(inputFile):
	matchCount = 0
	with open(inputFile, 'r') as f_in:
		reader = csv.DictReader(f_in)
		for row in reader:
			matchCount += 1

		f_in.close()
	return matchCount

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Error: Please specify", "'minYear'", "'maxYear'"
		exit(0)

	# Specifying year of matches we are interested in
	minYear = int(sys.argv[1])
	maxYear = int(sys.argv[2])

	# Prepare the output file
	home = "/Users/kevinnguyen/Projects/tennisml"
	matchCount = 0

	for year in range(minYear, maxYear + 1):
		path = home + "/tennis_atp/atp_matches_" + str(year) + ".csv"
		matchCount += countMatches(path)

	print "Matches counted: " + str(matchCount)
