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

Ideas:
Upset factor
Time decay
Common opponents
Surface factor

Stats that should not be aggregated for players:
Hand, Age

To generate training data:
1) Look at the matches and for a match in the training years, aggregate the players stats up to that match unweighted and weighted to generate the proper array.
Don't forget to subtract to get the proper vector.