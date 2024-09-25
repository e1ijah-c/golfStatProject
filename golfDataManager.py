import golfStatisticsCalculator as gs
import pandas as pd
import os
import time

"""
Next Step:
1. Setup data aggregation across multiple rounds and players
2. Update the playerStatsDF with the necessary data in this script.
"""

start_time = time.time()
playerStatsDF = pd.read_csv('Players_stats.csv')

data_folder_path = 'PlayerData/'
player_count = 0
playerKeys = []
roundIDs = []
playerIDs = []
dfs = {}

def CalculateStats():
    gs.UpdateTotalHoles()
    gs.UpdateParIndexes()
    gs.CheckBunkerAttempts()
    gs.CheckChipShots()
    gs.CalculateGIRs()
    gs.CalculateScores()
    gs.CalculateFairwaysHit()

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
#print(playerKeys)

for i in range(player_count):
    for d in range(len(dfs[playerKeys[i]])):
        gs.df = dfs[playerKeys[i]][d]
        CalculateStats()
        gs.AddRoundData()
        roundIDs.append(d+1)
        playerIDs.append(i+1)

gs.roundsStatsDF['Round_id'] = roundIDs
gs.roundsStatsDF['Player_id'] = playerIDs

pd.set_option("display.max_columns", None)
print(gs.roundsStatsDF)


print("--- %s seconds ---" % (time.time() - start_time))
