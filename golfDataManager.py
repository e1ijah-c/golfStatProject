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
    gs.CalculatePlusMinus()
    gs.CalculateFairwaysHit()

def AverageScore(key: str) -> int:
    cumulativeScore = 0
    for r in range(len(player_round_indexes[key])):
        cumulativeScore += gs.adf.loc[player_round_indexes[key][r], 'Total_score']
    
    return round(float(cumulativeScore / len(player_round_indexes[key])), 2)

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
        
        avgPar3Score = gs.AverageParScore(3)
        avgPar4Score = gs.AverageParScore(4)
        avgPar5Score = gs.AverageParScore(5)

        print(gs.df)

    par_stats[playerKeys[i]] = []
    par_stats[playerKeys[i]].extend((avgPar3Score, avgPar4Score, avgPar5Score))
   

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

    player_stats[key].extend((int(p+1), AverageScore(key), par_stats[key][0], par_stats[key][1], par_stats[key][2]))


            
#print(player_round_indexes)
print(player_stats)
#print(dfs)
#d.set_option("display.max_columns", None)
print(gs.adf)

print("--- %s seconds ---" % (time.time() - start_time))
