# Generates a weight factor based on time from the current match
def getTimeWeight(matchTime, currentMatchTime):
	timeHyperParameter = 0.9999
	return timeHyperParameter ** (int(currentMatchTime) - int(matchTime))

# Returns all weights to be used on match data
def getWeightFactor(match, playersMatches, minYear, currentMatchTime):
	timeWeight = getTimeWeight(match["tourney_date"], currentMatchTime)
	return timeWeight