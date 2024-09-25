import golfStatisticsCalculator as gs
import pandas as pd
import time

start_time = time.time()

roundsStatsDF = pd.read_csv('Rounds_stats_per_player.csv')
playerStatsDF = pd.read_csv('Players_stats.csv')

"""
Next Step:
1. Setup data aggregation across multiple rounds and players
2. Update the playerStatsDF with the necessary data in this script.
"""

def CalculateStats():
    gs.UpdateTotalHoles()
    gs.UpdateParIndexes()
    gs.CheckBunkerAttempts()
    gs.CheckChipShots()
    gs.CalculateGIRs()
    gs.CalculateScores()
    gs.CalculateFairwaysHit()
    gs.FillNaNs()

CalculateStats()
gs.AddRoundData()


print(gs.df)
pd.set_option("display.max_columns", None)
print(gs.roundsStatsDF)


print("--- %s seconds ---" % (time.time() - start_time))
