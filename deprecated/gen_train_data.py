# generates training data in libsvm format
import os
import sys
import csv

# global averages of all stats
def aggregate_player_info(year, years_and_players, weighted=True):
    
    # find input csv file for given year
    cwd = os.getcwd()

    if weighted == True:
        filename = cwd + '/w_agg_files/weighted_player_agg_stats_' + str(year) + '.csv'
    else:
        filename = cwd + '/uw_agg_files/unweighted_player_agg_stats_' + str(year) + '.csv'
    

    years_and_players[year] = {}

    with open(filename, 'r') as f_in:
        # read input as csv dictionary
        reader = csv.DictReader(f_in)
        for row in reader:
            years_and_players[year][row['name']] = row

def generate_training_data(years_and_players, min_year, max_year):
    # find input csv file
    cwd = os.getcwd()
    filename = cwd + '/atp_matches_features.csv'
    output = cwd + "/uw_train_data/train_data_" + str(min_year) + "-" + str(max_year) + ".csv"

    with open(output, 'w') as f_out:
        f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name1", "name2", "surface", "date", "minutes", "best_of", "draw_size", "avg_seed1", "avg_seed2", "avg_ht1", "avg_ht2", "avg_age1", "avg_age2", "avg_rank1", "avg_rank2", "avg_rank_pts1", "avg_rank_pts2", "avg_aces1", "avg_aces2", "avg_dfs1", "avg_dfs2", "avg_svpts1", "avg_svpts2", "avg_1stIn1", "avg_1stIn2", "avg_1stWon1", "avg_1stWon2", "avg_2ndWon1", "avg_2ndWon2", "avg_SvGms1", "avg_SvGms2", "avg_bpSaved1", "avg_bpSaved2", "avg_bpFaced1", "avg_bpFaced2", "hand1", "hand2", "wfactor1", "wfactor2", "result"))

        with open(filename, 'r') as f_in:
            # read input as csv dictionary
            reader = csv.DictReader(f_in)

            for row in reader:
                year = int(row['date']) / 10000

                if year > max_year:
                    break

                player1Data = years_and_players[year][row['name']]
                player2Data = years_and_players[year][row['o_name']]

                name1 = row['name']
                name2 = row['o_name']
                surface = row['surface']
                date = row['date']
                minutes = row['minutes']
                best_of = row['best_of']
                draw_size = row['draw_size']
                result = row['result']
                avg_seed1 = player1Data['avg_seed']
                avg_seed2 = player2Data['avg_seed']
                avg_ht1 = player1Data['avg_ht']
                avg_ht2 = player2Data['avg_ht']
                avg_age1 = player1Data['avg_age']
                avg_age2 = player2Data['avg_age']
                avg_rank1 = player1Data['avg_rank']
                avg_rank2 = player2Data['avg_rank']
                avg_rank_pts1 = player1Data['avg_rank_pts']
                avg_rank_pts2 = player2Data['avg_rank_pts']
                avg_aces1 = player1Data['avg_aces']
                avg_aces2 = player2Data['avg_aces']
                avg_dfs1 = player1Data['avg_dfs']
                avg_dfs2 = player2Data['avg_dfs']
                avg_svpts1 = player1Data['avg_svpts']
                avg_svpts2 = player2Data['avg_svpts']
                avg_1stIn1 = player1Data['avg_1stIn']
                avg_1stIn2 = player2Data['avg_1stIn']
                avg_1stWon1 = player1Data['avg_1stWon']
                avg_1stWon2 = player2Data['avg_1stWon']
                avg_2ndWon1 = player1Data['avg_2ndWon']
                avg_2ndWon2 = player2Data['avg_2ndWon']
                avg_SvGms1 = player1Data['avg_SvGms']
                avg_SvGms2 = player2Data['avg_SvGms']
                avg_bpSaved1 = player1Data['avg_bpSaved']
                avg_bpSaved2 = player2Data['avg_bpSaved']
                avg_bpFaced1 = player1Data['avg_bpFaced']
                avg_bpFaced2 = player2Data['avg_bpFaced']
                hand1 = player1Data['hand']
                hand2 = player2Data['hand']
                wfactor1 = player1Data['wfactor']
                wfactor2 = player2Data['wfactor']

                f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (name1, name2, surface, date, minutes, best_of, draw_size, avg_seed1, avg_seed2, avg_ht1, avg_ht2, avg_age1, avg_age2, avg_rank1, avg_rank2, avg_rank_pts1, avg_rank_pts2, avg_aces1, avg_aces2, avg_dfs1, avg_dfs2, avg_svpts1, avg_svpts2, avg_1stIn1, avg_1stIn2, avg_1stWon1, avg_1stWon2, avg_2ndWon1, avg_2ndWon2, avg_SvGms1, avg_SvGms2, avg_bpSaved1, avg_bpSaved2, avg_bpFaced1, avg_bpFaced2, hand1, hand2, wfactor1, wfactor2, result))

if __name__ == '__main__':
    years_and_players = {}

    for year in range(2000, 2017):
        print 'gathering player data for year', str(year)
        aggregate_player_info(int(year), years_and_players, False)

    print 'generating train data per match'
    generate_training_data(years_and_players, 2000, 2016)



# for each match, get the year than find the players in that year avg stats and concatenate winners + losers vector

