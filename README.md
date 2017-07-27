# TennisML

always player1 - player2
excluded = seed, match_num, entry, ioc, best_of, round, draw_size, tourney_level, minutes, score
pk = pk = tourney_id + tourney_name + player1_id + player2_id + tourney_date
round = round_of

1 = Right hand
2 = Left hand

1 = hard
2 = grass
3 = clay
4 = carpet

Stats that should not be aggregated for players:
Hand, Age

To generate training data:
1) Look at the matches and for a match in the training years, aggregate the players stats up to that match unweighted and weighted to generate the proper array.
Don't forget to subtract to get the proper vector.

Some things:
-Surface effect 
-weak player vs weak player stats padding
-common opponents
-upset factor?
-gen testing data ----
-gen training data ----
-head to head balancing ----
-hand effect ----

Thoughts:
-Use head to head as a weight? It will make more sense for players that havent played each other often
-The idea is if two players played each other alot then its easy to predict how they will do. If they havent, we need to connect them somehow via common opponents