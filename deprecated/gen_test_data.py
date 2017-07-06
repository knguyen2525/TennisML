import os
import sys
import glob
import csv
import math

def gen_test_data(a_year, weighted=True):
    
    # find input csv files and output files
    cwd = os.getcwd()
    if weighted == True:
        path = cwd + "/w_agg_files/weighted_player_agg_stats_" + str(a_year) + ".csv"
    else:
        path = cwd + "/uw_agg_files/unweighted_player_agg_stats_" + str(a_year) + ".csv"

    data = cwd + "/atp_matches_features.csv"
    output = cwd + "/uw_test_data/test_data_" + str(a_year) + ".csv"
    player = {}

    # read all csv file and store in dictionary
    for filename in glob.glob(path):
        with open(filename, 'r') as f_in:
            reader = csv.DictReader(f_in)
            for row in reader:
                name = row['name']
                player[name] = row

    with open(output, 'w') as f_out:
        f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name1", "name2", "surface", "date", "minutes", "best_of", "draw_size", "avg_seed1", "avg_seed2", "avg_ht1", "avg_ht2", "avg_age1", "avg_age2", "avg_rank1", "avg_rank2", "avg_rank_pts1", "avg_rank_pts2", "avg_aces1", "avg_aces2", "avg_dfs1", "avg_dfs2", "avg_svpts1", "avg_svpts2", "avg_1stIn1", "avg_1stIn2", "avg_1stWon1", "avg_1stWon2", "avg_2ndWon1", "avg_2ndWon2", "avg_SvGms1", "avg_SvGms2", "avg_bpSaved1", "avg_bpSaved2", "avg_bpFaced1", "avg_bpFaced2", "hand1", "hand2", "wfactor1", "wfactor2", "result"))

        for filename in glob.glob(data):
            with open(filename, 'r') as f_in:
                reader = csv.DictReader(f_in)
                for row in reader:
                    year = int(row['date']) / 10000
                    if year == a_year:
                        name1 = row['name']
                        name2 = row['o_name']
                        surface = row['surface']
                        date = row['date']
                        minutes = row['minutes']
                        best_of = row['best_of']
                        draw_size = row['draw_size']
                        result = row['result']
                        avg_seed1 = player[name1]['avg_seed']
                        avg_seed2 = player[name2]['avg_seed']
                        avg_ht1 = player[name1]['avg_ht']
                        avg_ht2 = player[name2]['avg_ht']
                        avg_age1 = player[name1]['avg_age']
                        avg_age2 = player[name2]['avg_age']
                        avg_rank1 = player[name1]['avg_rank']
                        avg_rank2 = player[name2]['avg_rank']
                        avg_rank_pts1 = player[name1]['avg_rank_pts']
                        avg_rank_pts2 = player[name2]['avg_rank_pts']
                        avg_aces1 = player[name1]['avg_aces']
                        avg_aces2 = player[name2]['avg_aces']
                        avg_dfs1 = player[name1]['avg_dfs']
                        avg_dfs2 = player[name2]['avg_dfs']
                        avg_svpts1 = player[name1]['avg_svpts']
                        avg_svpts2 = player[name2]['avg_svpts']
                        avg_1stIn1 = player[name1]['avg_1stIn']
                        avg_1stIn2 = player[name2]['avg_1stIn']
                        avg_1stWon1 = player[name1]['avg_1stWon']
                        avg_1stWon2 = player[name2]['avg_1stWon']
                        avg_2ndWon1 = player[name1]['avg_2ndWon']
                        avg_2ndWon2 = player[name2]['avg_2ndWon']
                        avg_SvGms1 = player[name1]['avg_SvGms']
                        avg_SvGms2 = player[name2]['avg_SvGms']
                        avg_bpSaved1 = player[name1]['avg_bpSaved']
                        avg_bpSaved2 = player[name2]['avg_bpSaved']
                        avg_bpFaced1 = player[name1]['avg_bpFaced']
                        avg_bpFaced2 = player[name2]['avg_bpFaced']
                        hand1 = player[name1]['hand']
                        hand2 = player[name2]['hand']
                        wfactor1 = player[name1]['wfactor']
                        wfactor2 = player[name2]['wfactor']

                        f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (name1, name2, surface, date, minutes, best_of, draw_size, avg_seed1, avg_seed2, avg_ht1, avg_ht2, avg_age1, avg_age2, avg_rank1, avg_rank2, avg_rank_pts1, avg_rank_pts2, avg_aces1, avg_aces2, avg_dfs1, avg_dfs2, avg_svpts1, avg_svpts2, avg_1stIn1, avg_1stIn2, avg_1stWon1, avg_1stWon2, avg_2ndWon1, avg_2ndWon2, avg_SvGms1, avg_SvGms2, avg_bpSaved1, avg_bpSaved2, avg_bpFaced1, avg_bpFaced2, hand1, hand2, wfactor1, wfactor2, result))



if __name__ == "__main__":
    gen_test_data(2017, False)

