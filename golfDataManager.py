import golfStatisticsCalculator as gs
import pandas as pd
import os
import time

"""
Next Step:
1. Setup data aggregation across multiple rounds and players => completed
2. Update the playerStatsDF with the necessary data in this script.
3. Use ChatGPT to generate more data sets
"""

start_time = time.time()
pdf = pd.read_csv('Players_stats.csv')
data_folder_path = 'PlayerData/'

player_count = 0
cumulativePutts, avgPutts = 0, 0
playerKeys = []
roundIDs = []
playerIDs = []
player_round_indexes = {}
player_stats = {}
par_stats = {}
dfs = {}

def CalculateStats():
    gs.UpdateTotalHoles()
    gs.UpdateParIndexes()
    gs.CheckBunkerAttempts()
    gs.CheckChipShots()
    gs.CalculateGIRs()
    gs.CalculateParPlusMinus()
    gs.CalculateFairwaysHit()

def AverageTotals(sum_of_parts: int, total_parts: int) -> float:
    return round(float(sum_of_parts / total_parts), 2)

def ScoringAverage(key: str) -> float:
    cumulativeScore = 0
    for r in range(len(player_round_indexes[key])):
        cumulativeScore += gs.adf.loc[player_round_indexes[key][r], 'Total_score']
    
    return AverageTotals(cumulativeScore, len(player_round_indexes[key]))

def OverallAverageParPlusMinus(key: str) -> float:
    cumulativePlusMinus = 0
    for r in range(len(player_round_indexes[key])):
        cumulativePlusMinus += gs.adf.loc[player_round_indexes[key][r], 'Total_par_plus_minus']
    
    return AverageTotals(cumulativePlusMinus, len(player_round_indexes[key]))

def AveragePutts(key: str) -> float:
    cumulativePutts = 0
    cumulativeHoles = 0
    for r in range(len(player_round_indexes[key])):
        cumulativePutts += gs.adf.loc[player_round_indexes[key][r], 'Total_putts']
        cumulativeHoles += gs.adf.loc[player_round_indexes[key][r], 'Holes_played']
    
    return AverageTotals(cumulativePutts, cumulativeHoles)


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
        playerKeys.append(player_folder)

player_count = len(dfs)


# perform stat calculations for each round while assigning the appropriate round and player id
for i in range(player_count):
    for d in range(len(dfs[playerKeys[i]])):
        gs.df = dfs[playerKeys[i]][d]
        CalculateStats()
        gs.AddRoundData()
        roundIDs.append(d+1)
        playerIDs.append(i+1)
        
        gs.UpdateParScoringAverage(3), gs.UpdateParScoringAverage(4), gs.UpdateParScoringAverage(5)
        gs.UpdateAverageParPlusMinus(3), gs.UpdateAverageParPlusMinus(4), gs.UpdateAverageParPlusMinus(5)

        print(gs.df)

    par_stats[playerKeys[i]] = []
    par_stats[playerKeys[i]].extend((AverageTotals(gs.totalPar3Score, gs.totalPar3Holes), AverageTotals(gs.totalPar3PlusMinus, gs.totalPar3Holes), 
                                     AverageTotals(gs.totalPar4Score, gs.totalPar4Holes), AverageTotals(gs.totalPar4PlusMinus, gs.totalPar4Holes), 
                                     AverageTotals(gs.totalPar5Score, gs.totalPar5Holes), AverageTotals(gs.totalPar5PlusMinus, gs.totalPar5Holes)))
    
    gs.totalPar3Score, gs.totalPar3PlusMinus, gs.totalPar3Holes = 0, 0, 0
    gs.totalPar4Score, gs.totalPar4PlusMinus, gs.totalPar4Holes = 0, 0, 0
    gs.totalPar5Score, gs.totalPar5PlusMinus, gs.totalPar5Holes = 0, 0, 0

   

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

    player_stats[key].extend((int(p+1), ScoringAverage(key), OverallAverageParPlusMinus(key), 
                              par_stats[key][0], par_stats[key][1], par_stats[key][2], par_stats[key][3], par_stats[key][4], par_stats[key][5],
                              AveragePutts(key)))


            
#print(player_round_indexes)
print(player_stats)
#print(dfs)
#d.set_option("display.max_columns", None)
print(gs.adf)

print("--- %s seconds ---" % (time.time() - start_time))
