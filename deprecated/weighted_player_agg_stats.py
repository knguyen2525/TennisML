import os
import sys
import glob
import csv
import math


# global averages of all stats
def analyze_weighted(a_year):
    
    # find input csv files and output files
    cwd = os.getcwd()
    path = cwd + "/atp_matches_features.csv"
    output = cwd + "/weighted_player_agg_stats_" + str(a_year) + ".csv"
    result = {}
    
    # read all csv files
    with open(output, 'w') as f_out:
        f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("name", "avg_seed", "avg_ht", "avg_age", "avg_rank", "avg_rank_pts", "avg_aces", "avg_dfs", "avg_svpts", "avg_1stIn", "avg_1stWon", "avg_2ndWon", "avg_SvGms", "avg_bpSaved", "avg_bpFaced", "hand", "wfactor"))

        for filename in glob.glob(path):
            with open(filename, 'r') as f_in:
                # read input as csv dictionary
                reader = csv.DictReader(f_in)
                for row in reader:
                    gm_year = int(row['date']) / 10000
                    if gm_year >= a_year:
                        pass

                    fact = math.exp((a_year - gm_year) / 5.0)
                    wseed = fact*float(row['seed'])
                    wht = fact*float(row['ht'])
                    wage = fact*float(row['age'])
                    wrank = fact*float(row['rank'])
                    wrank_pts = fact*float(row['rank_pts'])
                    wace = fact*float(row['ace'])
                    wdf = fact*float(row['df'])
                    wsvpt = fact*float(row['svpt'])
                    w1stIn = fact*float(row['1stIn'])
                    w1stWon = fact*float(row['1stWon'])
                    w2ndWon = fact*float(row['2ndWon'])
                    wSvGms = fact*float(row['SvGms'])
                    wbpSaved = fact*float(row['bpSaved'])
                    wbpFaced = fact*float(row['bpFaced'])
                    whand = ''
              
                    if row['hand'] == 'R':
                        whand = '1'
                    else:
                        whand = '2'

                    # add player to dictionary
                    if result.get(row['name']) is None:
                        result[row['name']] = {'count': fact, 'seed': wseed, 'ht': wht, 'age': wage, 'rank': wrank, 'rank_pts': wrank_pts, 'ace': wace, 'df': wdf, 'svpt': wsvpt, '1stIn': w1stIn, '1stWon': w1stWon, '2ndWon': w2ndWon, 'SvGms': wSvGms, 'bpSaved': wbpSaved, 'bpFaced': wbpFaced, 'hand': whand}
                    # sum up player stats
                    else:
                        result[row['name']]['count'] += fact
                        result[row['name']]['seed'] += wseed
                        result[row['name']]['ht'] += wht
                        result[row['name']]['age'] += wage
                        result[row['name']]['rank'] += wrank
                        result[row['name']]['rank_pts'] += wrank_pts
                        result[row['name']]['ace'] += wace
                        result[row['name']]['df'] += wdf
                        result[row['name']]['svpt'] += wsvpt
                        result[row['name']]['1stIn'] += w1stIn
                        result[row['name']]['1stWon'] += w1stWon
                        result[row['name']]['2ndWon'] += w2ndWon
                        result[row['name']]['SvGms'] += wSvGms
                        result[row['name']]['bpSaved'] += wbpSaved
                        result[row['name']]['bpFaced'] += wbpFaced

                
        for player in result:
            wfactor = float(result[player]['count'])
            f_out.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (player, result[player]['seed']/wfactor, result[player]['ht']/wfactor, result[player]['age']/wfactor, result[player]['rank']/wfactor, result[player]['rank_pts']/wfactor, result[player]['ace']/wfactor, result[player]['df']/wfactor, result[player]['svpt']/wfactor, result[player]['1stIn']/wfactor, result[player]['1stWon']/wfactor, result[player]['2ndWon']/wfactor, result[player]['SvGms']/wfactor, result[player]['bpSaved']/wfactor, result[player]['bpFaced']/wfactor, result[player]['hand'], wfactor))



if __name__ == "__main__":
    for year in range(2000, 2018):
        print "generating data assuming prediction year of", str(year)
        analyze_weighted(int(year))

