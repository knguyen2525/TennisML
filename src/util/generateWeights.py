# Has functions that generate all weights to be considered

# Generates a weight factor based on time from the current match
def getTimeWeight(matchTime, maxTime):
	timeHyperParameter = 0.9999
	return timeHyperParameter ** (int(maxTime) - int(matchTime))

# Returns all weights to be used on match data
def getWeightFactor(matchTime, maxTime):
	return getTimeWeight(matchTime, maxTime)