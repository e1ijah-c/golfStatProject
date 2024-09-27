import golfStatisticsCalculator as gs
import pandas as pd
import os
import time

"""
Next Step:
1. Use ChatGPT to generate more data sets
2. Schedule meeting
"""

start_time = time.time()

pdf = pd.read_csv('Players_stats.csv')
data_folder_path = 'PlayerData/'

player_count = 0
roundIDs, playerIDs = [], []
player_round_indexes, par_stats, player_stats, dfs = {}, {}, {}, {}

def CalculateStats():
    gs.UpdateTotalHoles()
    gs.UpdateParIndexes()
    gs.CheckBunkerAttempts()
    gs.CheckChipShots()
    gs.CalculateGIRs()
    gs.CalculateParPlusMinus()
    gs.CalculateFairwaysHit()

def AverageTotals(numerator: int, denominator: int) -> float:
    if numerator == 0 or denominator == 0:
        return 0
    else:
        return round(float(numerator / denominator), 2)

def PercentTotals(numerator: int, denominator: int) -> float:
    if numerator == 0 or denominator == 0:
        return 0
    else:
        return round(float((numerator / denominator) * 100), 2)

def ScoringAverage(key: str) -> float:
    cumulativeScore = 0
    for r in range(len(player_round_indexes[key])):
        cumulativeScore += gs.adf.loc[player_round_indexes[key][r], 'Total_score']
    
    return AverageTotals(cumulativeScore, len(player_round_indexes[key]))

def ParScoringAverage(key: str, par: int) -> float:
    cumulativeParScore = 0
    for r in range(len(player_round_indexes[key])):
        if par == 3:
            cumulativeParScore += gs.adf.loc[player_round_indexes[key][r], 'Total_par_3_score']
        if par == 4:
            cumulativeParScore += gs.adf.loc[player_round_indexes[key][r], 'Total_par_4_score']
        if par == 5:
            cumulativeParScore += gs.adf.loc[player_round_indexes[key][r], 'Total_par_5_score']
    
    return AverageTotals(cumulativeParScore, len(player_round_indexes[key]))

def OverallAverageParPlusMinus(key: str) -> float:
    cumulativePlusMinus = 0
    for r in range(len(player_round_indexes[key])):
        cumulativePlusMinus += gs.adf.loc[player_round_indexes[key][r], 'Total_par_plus_minus']
    
    return AverageTotals(cumulativePlusMinus, len(player_round_indexes[key]))

def AverageParPlusMinus(key: str, par: int) -> float:
    cumulativeParPlusMinus = 0
    for r in range(len(player_round_indexes[key])):
        if par == 3:
            cumulativeParPlusMinus += gs.adf.loc[player_round_indexes[key][r], 'Total_par_3_plus_minus']
        if par == 4:
            cumulativeParPlusMinus += gs.adf.loc[player_round_indexes[key][r], 'Total_par_4_plus_minus']
        if par == 5:
            cumulativeParPlusMinus += gs.adf.loc[player_round_indexes[key][r], 'Total_par_5_plus_minus']
    
    return AverageTotals(cumulativeParPlusMinus, len(player_round_indexes[key]))

def AveragePutts(key: str) -> float:
    cumulativePutts = 0
    cumulativeHoles = 0
    for r in range(len(player_round_indexes[key])):
        cumulativePutts += gs.adf.loc[player_round_indexes[key][r], 'Total_putts']
        cumulativeHoles += gs.adf.loc[player_round_indexes[key][r], 'Holes_played']
    
    return AverageTotals(cumulativePutts, cumulativeHoles)

def CalculateAggregatedStat(key: str, numerator_column_name: str, denominator_column_name: str, denominator_is_total_holes: bool, stat_is_percentage: bool) -> float:
    cumulative_numerator = 0
    cumulative_denominator = 0
    cumulative_holes = 0

    if denominator_is_total_holes == False:
        for r in range(len(player_round_indexes[key])):
            cumulative_numerator += gs.adf.loc[player_round_indexes[key][r], numerator_column_name]
            cumulative_denominator += gs.adf.loc[player_round_indexes[key][r], denominator_column_name]
    
        return PercentTotals(cumulative_numerator, cumulative_denominator)
    else:
        for r in range(len(player_round_indexes[key])):
            cumulative_numerator += gs.adf.loc[player_round_indexes[key][r], numerator_column_name]
            cumulative_holes += gs.adf.loc[player_round_indexes[key][r], 'Holes_played']

        if stat_is_percentage == True:
            return PercentTotals(cumulative_numerator, cumulative_holes)
        else:
            return AverageTotals(cumulative_numerator, cumulative_holes)

def AverageProximityToHole(key: str) -> float:
    cumulative_proximity = 0
    cumulative_holes = 0

    for r in range(len(player_round_indexes[key])):
            cumulative_proximity += sum(gs.holeProximities)
            cumulative_holes += gs.adf.loc[player_round_indexes[key][r], 'Holes_played']
    
    print(gs.holeProximities)
    #gs.holeProximities.clear()
    return AverageTotals(cumulative_proximity, cumulative_holes)
    

# get player count by checking number of folders within the main 'PlayerData' folder (one folder per player)
for player_folder in os.listdir(data_folder_path):
    player_folder_path = os.path.join(data_folder_path, player_folder)
    if os.path.isdir(player_folder_path):
        player_dfs = []
        # Loop through each file in the player subfolder
        for file in os.listdir(player_folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(player_folder_path, file)
                df = pd.read_csv(file_path)
                player_dfs.append(df)
        dfs[player_folder] = player_dfs

player_count = len(dfs)

# perform stat calculations for each round while assigning the appropriate round and player id
for i in range(player_count):
    key = "Player_" + str(i+1)
    for d in range(len(dfs[key])):
        gs.df = dfs[key][d]
        CalculateStats()
        gs.AddRoundData()
        roundIDs.append(d+1)
        playerIDs.append(i+1)

gs.adf['Round_id'] = roundIDs
gs.adf['Player_id'] = playerIDs

# fill dictionary with lists to store indexes of each player's rounds
for p in range(player_count):
    key = "Player_" + str(p+1)
    player_round_indexes[key] = []
    player_stats[key] = []
    for i in range(len(gs.adf.index)):
        if gs.adf.loc[i, 'Player_id'] == p+1:
            player_round_indexes[key].append(i)

    rounds_played = len(player_round_indexes[key])

    player_stats[key].extend((p+1, rounds_played, ScoringAverage(key), OverallAverageParPlusMinus(key), 
                             ParScoringAverage(key, 3), AverageParPlusMinus(key, 3), 
                             ParScoringAverage(key, 4), AverageParPlusMinus(key, 4),
                             ParScoringAverage(key, 5), AverageParPlusMinus(key, 5),
                             CalculateAggregatedStat(key, 'Total_putts', '', True, False),
                             CalculateAggregatedStat(key, 'Total_bunker_saves', 'Total_bunker_save_attempts', False, True),
                             CalculateAggregatedStat(key, 'Total_fairways_hit', 'Total_fairways_attempts', False, True),
                             CalculateAggregatedStat(key, 'Total_drivers_hit', 'Total_drivers_attempted', False, True),
                             CalculateAggregatedStat(key, 'Total_scrambles', 'Total_scrambles_attempted', False, True),
                             CalculateAggregatedStat(key, 'Total_birdies_or_better', '', True, True),
                             CalculateAggregatedStat(key, 'Total_double_bogey_or_worse', '', True, True),
                             CalculateAggregatedStat(key, 'Total_bounce_backs', 'Total_bounce_back_attempts', False, True),
                             CalculateAggregatedStat(key, 'Total_three_putts', '', True, True), 
                             CalculateAggregatedStat(key, 'Total_distance_to_hole_from_approach_shots', '', True, False),
                             CalculateAggregatedStat(key, 'Total_chip_shots', '', True, False)))

    pdf.loc[len(pdf)] = player_stats[key]
            
#pd.set_option("display.max_columns", None)
print(gs.adf)
print(pdf)

print("--- %s seconds ---" % (time.time() - start_time))
