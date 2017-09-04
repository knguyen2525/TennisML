# Functions for anything related to time

# Makes sure that a date of a match is within the range of interest
def isDateInRange(matchDate, minTime, maxTime):
	return int(minTime) <= int(matchDate) and int(matchDate) < int(maxTime)

# Turns a given date to time in days
def timeToDays(time):
	year = time[:4]
	month = time[4:-2]
	day = time[-2:]
	return float(year)*365 + float(month)*30.42 + float(day)