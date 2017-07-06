import os
import sys
import glob
import csv

# "w" stands for winner and "l" stands for loser

def parser():

	# find input csv files and output files
	owd = os.getcwd()
	os.chdir("..")
	cwd = os.getcwd()
	path = cwd + "/tennis_atp/atp_matches_2[0-9]*.csv"
	output = owd + "/atp_matches_features.csv"

	match_count = 0
	#score

	# read all csv files
	with open(output, 'w') as f_out:
		# write first row of output csv file
		f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("key", "name", "o_name", "id", "o_id", "seed", "o_seed","ht", "o_ht", "age", "o_age", "rank", "o_rank", "rank_pts", "o_rank_pts", "ace", "o_ace", "df", "o_df", "svpt", "o_svpt", "1stIn", "o_1stIn", "1stWon", "o_1stWon", "2ndWon", "o_2ndWon", "SvGms", "o_SvGms", "bpSaved", "o_bpSaved", "bpFaced", "o_bpFaced", "age_diff", "rank_diff", "rank_point_diff", "date", "surface", "minutes", "result", "hand", "o_hand", "score", "o_score", "round_of", "best_of", "draw_size", "tourney_level"))

		for filename in glob.glob(path):
			print 'processing ', filename
			with open(filename, 'r') as f_in:
				# read input as csv dictionary
				reader = csv.DictReader(f_in)
				for row in reader:
					#Tourney information
					round_of = row['round']
					best_of = row['best_of']
					draw_size = row['draw_size']
					tourney_level = row['tourney_level']

					#Creating loser scores			
					w_score = row['score']
					l_score = ''
					setScores = w_score.split(' ')
  
  					#Reversing scores for loser
					for setScore in setScores:
						if setScore in {'RET','Walkover','W/O','DEF', 'Default', 'Played', 'In', '', 'Unfinished'}:
							w_score = ''
							l_score = ''
							break

						if setScore[-1] == ')':
							l_score = l_score + setScore[2] + '-' + setScore[0] + '(' + setScore[-2] + ') '
						else:
							l_score = l_score + setScore[2] + '-' + setScore[0] + ' '

					l_score = l_score[:-1]

					w_hand = row['winner_hand']
					l_hand = row['loser_hand']
					
					# create key for each row of csv file
					w_key = row['tourney_date'] + row['tourney_name'] + row['winner_id'] + row['loser_id']
					l_key = row['tourney_date'] + row['tourney_name'] + row['loser_id'] + row['winner_id']
					
					# handle empty cells for age
					if not row['winner_age'].strip() or not row['loser_age'].strip():
					    w_age_diff = 0
					else:
					    w_age_diff = int(float(row['winner_age'])) - int(float(row['loser_age']))
					
					w_id = row['winner_id']; l_id = row['loser_id']
					w_name = row['winner_name']; l_name = row['loser_name']
					w_seed = row['winner_seed']; l_seed = row['loser_seed']
					if not w_seed: w_seed = 0
					if not l_seed: l_seed = 0
					
					w_ht = row['winner_ht']; l_ht = row['loser_ht']
					if not w_ht: w_ht = 0
					if not l_ht: l_ht = 0
					
					w_age = row['winner_age']; l_age = row['loser_age']
					if not w_age: w_age = 0
					if not l_age: l_age = 0
					
					w_rank = row['winner_rank']; l_rank = row['loser_rank']
					if not w_rank: w_rank = 0
					if not l_rank: l_rank = 0
					
					w_rank_pts = row['winner_rank_points']
					l_rank_pts = row['loser_rank_points']
					if not w_rank_pts: w_rank_pts = 0
					if not l_rank_pts: l_rank_pts = 0
					
					w_ace = row['w_ace']; l_ace = row['l_ace']
					if not w_ace: w_ace = 0
					if not l_ace: l_ace = 0
					
					w_df = row['w_df']; l_df = row['l_df']
					if not w_df: w_df = 0
					if not l_df: l_df = 0
					
					w_svpt = row['w_svpt']; l_svpt = row['l_svpt']
					if not w_svpt: w_svpt = 0
					if not l_svpt: l_svpt = 0
					
					w_1stIn = row['w_1stIn']; l_1stIn = row['l_1stIn']
					if not w_1stIn: w_1stIn = 0
					if not l_1stIn: l_1stIn = 0
					
					w_1stWon = row['w_1stWon']; l_1stWon = row['l_1stWon']
					if not w_1stWon: w_1stWon = 0
					if not l_1stWon: l_1stWon = 0
					
					w_2ndWon = row['w_2ndWon']; l_2ndWon = row['l_2ndWon']
					if not w_2ndWon: w_2ndWon = 0
					if not l_2ndWon: l_2ndWon = 0
					
					w_SvGms = row['w_SvGms']; l_SvGms = row['l_SvGms']
					if not w_SvGms: w_SvGms = 0
					if not l_SvGms: l_SvGms = 0
					
					w_bpSaved = row['w_bpSaved']; l_bpSaved = row['l_bpSaved']
					if not w_bpSaved: w_bpSaved = 0
					if not l_bpSaved: l_bpSaved = 0
					
					w_bpFaced = row['w_bpFaced']; l_bpFaced = row['l_bpFaced']
					if not w_bpFaced: w_bpFaced = 0
					if not l_bpFaced: l_bpFaced = 0
					
					w_rank_diff = int(w_rank) - int(l_rank)
					if w_rank == 0 or l_rank == 0:
					    w_rank_diff = 0
					
					w_rank_point_diff = int(w_rank_pts) - int(l_rank_pts)
					if w_rank_pts == 0 or l_rank_pts == 0:
					    w_rank_point_diff = 0
					
					date = row['tourney_date']

					# 0 = hard
					# 1 = grass
					# 2 = clay
					# 3 = carpet
					if row['surface'] == 'Hard':
						surface = 1
					elif row['surface'] == 'Grass':
						surface = 2
					elif row['surface'] == 'Clay':
						surface = 3
					else:
						surface = 4
					
					minutes = row['minutes']
					if not minutes: minutes = 0
					
					# write output; 1 for win, 0 for loss
					f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (w_key, w_name, l_name, w_id, l_id, w_seed, l_seed, w_ht, l_ht, w_age, l_age, w_rank, l_rank, w_rank_pts, l_rank_pts, w_ace, l_ace, w_df, l_df, w_svpt, l_svpt, w_1stIn, l_1stIn, w_1stWon, l_1stWon, w_2ndWon, l_2ndWon, w_SvGms, l_SvGms, w_bpSaved, l_bpSaved, w_bpFaced, l_bpFaced, w_age_diff, w_rank_diff, w_rank_point_diff, date, surface, minutes, "1", w_hand, l_hand, w_score, l_score, round_of, best_of, draw_size, tourney_level))
					f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (l_key, l_name, w_name, l_id, w_id, l_seed, w_seed, l_ht, w_ht, l_age, w_age, l_rank, w_rank, l_rank_pts, w_rank_pts, l_ace, w_ace, l_df, w_df, l_svpt, w_svpt, l_1stIn, w_1stIn, l_1stWon, w_1stWon, l_2ndWon, w_2ndWon, l_SvGms, w_SvGms, l_bpSaved, w_bpSaved, l_bpFaced, w_bpFaced, -w_age_diff, -w_rank_diff, -w_rank_point_diff, date, surface, minutes, "0", l_hand, w_hand, l_score, w_score, round_of, best_of, draw_size, tourney_level))

if __name__ == "__main__":
	parser()
