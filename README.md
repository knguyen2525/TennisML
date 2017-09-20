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

70-30 split at 1990-2008, 2008-2017
20550 matches in testing
48738 matches in training

Features:
-Time weighing ----
-Basic stats ----
-Surface effect ----
-head to head balancing ----
-hand effect ----
-Number of times broken ----
-weak player vs weak player stats padding
-avg rank per round?
-service game prowess

Training/Testing:
-Feature extraction
-Logistic regression and stacking (knn, decision tree, perceptron, and try others)
	1991+ has data we want
	rolling k folds cross validation
	use entire training set to make predictions on test for each model. Keep as features for lr
	train 1987-1990, test 1990-1993
	train 1990-1993, test 1993-1996
	train 1990-1996, test 1996-1999
	train 1990-1999, test 1999-2002
	train 1990-2002, test 2002-2005
	train 1990-2005, test 2005-2008

	We are losing some data for initial training

	train 1994-2008 with base models. Predict on 2008-2017. Save predictions
	stacking model train on 1994-2008 with base model predictions. Predict on testing set with base model predictions 


-Roll through data to make folds
-Exhaustive grid search for hyper parameters


