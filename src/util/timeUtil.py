# Functions for anything related to time

# Makes sure that a date of a match is within the range of interest
def isDateInRange(matchDate, minTime, maxTime):
	return int(minTime) <= int(matchDate) and int(matchDate) < int(maxTime)

# Turns a given date to time in days
def timeToDays(time):
	year = float(str(time)[:4])
	month = float(str(time)[4:-2])
	day = float(str(time)[-2:])
	return year*365 + month*30.42 + day