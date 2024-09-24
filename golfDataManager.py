import golfStatisticsCalculator as gs
import pandas as pd
import time

start_time = time.time()

roundsStatsDF = pd.read_csv('Rounds_stats_per_player.csv')
playerStatsDF = pd.read_csv('Players_stats.csv')

"""
Next Step:
Update the playerStatsDF with the necessary data in this script.
"""

def CalculateStats():
    gs.UpdateTotalHoles()
    gs.UpdateParIndexes()
    gs.CalculateGIRs()
    gs.CalculateScores()
    gs.CalculateFairwaysHit()

CalculateStats()
gs.AddRoundData()

# for i in range(gs.PlayerCount()):
#     gs.playerID = i + 1
#     gs.UpdatePlayerIndexes()
    
#     for r in range(gs.RoundCount()):
#         gs.roundID = r + 1

#         gs.UpdateRoundIndexes()
#         gs.UpdateTotalHoles()
#         gs.UpdateParIndexes()

#         gs.AddRoundData()
print(gs.df)

pd.set_option("display.max_columns", None)
print(gs.roundsStatsDF)


print("--- %s seconds ---" % (time.time() - start_time))
