import sys

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Error: Please specify:", "'trainingFile'", "'testingFile'"
		exit(0)

	home = "/Users/kevinnguyen/Projects/tennisml"

	# Gathering auxiliary data
	trainingFileInput = home + "/data/features/" + sys.argv[1]
	testingFileInput = home + "/data/features/" + sys.argv[2]

	