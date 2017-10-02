# Compacts player data into a players object with each player having an array of matches he participated in
# {
# 	"playerName": [
# 		{
# 			"pk": "$pk",
# 			"ht": "$ht",
# 			"rank": "$rank",
# 			"rank_points": "$rank_points"
# 			etc...
# 		}
# 		...
# 	],
# 	...
# }

import csv

# Extracts the player data from a given match for player 1 or player 2 in that match
def getPlayerMatchData(match, playerNum):
	# Extracting data from match based on playerNum 1 or 2
	playerMatchData = {"pk": match["pk"], "ht": match["ht" + playerNum], "rank": match["rank" + playerNum], "rank_points": match["rank_points" + playerNum], "ace": match["ace" + playerNum], "df": match["df" + playerNum], "svpt": match["svpt" + playerNum], "firstIn": match["firstIn" + playerNum], "firstWon": match["firstWon" + playerNum], "secondWon": match["secondWon" + playerNum], "SvGms": match["SvGms" + playerNum], "bpSaved": match["bpSaved" + playerNum], "bpFaced": match["bpFaced" + playerNum], "surface": match["surface"], "opponent": match["name" + str(((int(playerNum) % 2) + 1))], "tourney_date": match["tourney_date"]}

	# Quick math to see if player won that match based on match result and playerNum 1 or 2
	if int(playerNum) + int(match["result"]) == 2: playerMatchData["win"] = "1"
	else: playerMatchData["win"] = "0"

	return playerMatchData

# Extracts the surface from a given match for player 1 and 2 in a match
def getPlayerSurfaceData(match, playerNum):
	playerSurfaceData = {"surface": match["surface"], "tourney_date": match["tourney_date"]}

	# Quick math to see if player won that match based on match result and playerNum 1 or 2
	if int(playerNum) + int(match["result"]) == 2: playerSurfaceData["win"] = "1"
	else: playerSurfaceData["win"] = "0"

	return playerSurfaceData

# Generates a player object where players are linked to matches he has played as well as his stats for that match
def getPlayerStats(cleanedAtpMatches): 
	players = {}

	# Open cleaned matches file
	with open(cleanedAtpMatches, 'r') as f_in:
		reader = csv.DictReader(f_in)

		# For each match, create a hashmap between player name and stats
		for match in reader:
			# Create mapping if does not exists
			# Get player match for player 1 and append to player match array
			if players.get(match["name1"]) is None: players[match["name1"]] = []
			playerMatchData  = getPlayerMatchData(match, "1")
			players[match["name1"]].append(playerMatchData)

			# Repeat the above for player 2
			if players.get(match["name2"]) is None: players[match["name2"]] = []
			playerMatchData  = getPlayerMatchData(match, "2")
			players[match["name2"]].append(playerMatchData)

			# # Index player surface data to save time in feature creation later
			# if players.get(match["name1"] + "_" + match["surface"]) is None: players[match["name1"] + "_" + match["surface"]] = []
			# playerSurfaceData = getPlayerSurfaceData(match, "1")
			# players[match["name1"] + "_" + match["surface"]].append(playerSurfaceData)

			# if players.get(match["name2"] + "_" + match["surface"]) is None: players[match["name2"] + "_" + match["surface"]] = []
			# playerSurfaceData = getPlayerSurfaceData(match, "2")
			# players[match["name2"] + "_" + match["surface"]].append(playerSurfaceData)

	return players