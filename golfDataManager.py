import golfStatisticsCalculator as golfstats
import pandas as pd
import time

start_time = time.time()

roundsStatsDF = pd.read_csv('Rounds_stats_per_player.csv')
playerStatsDF = pd.read_csv('Players_stats.csv')

"""
Next Step:
Update the playerStatsDF with the necessary data in this script.
"""

golfstats.UpdateTotalHoles()
golfstats.CalculateGIRs()
golfstats.CalculateScores()
golfstats.CalculateFairwaysHit()

# for i in range(golfstats.PlayerCount()):
#     golfstats.playerID = i + 1
#     golfstats.UpdatePlayerIndexes()
    
#     for r in range(golfstats.RoundCount()):
#         golfstats.roundID = r + 1

#         golfstats.UpdateRoundIndexes()
#         golfstats.UpdateTotalHoles()
#         golfstats.UpdateParIndexes()

#         golfstats.AddRoundData()

pd.set_option("display.max_columns", None)
print(golfstats.roundsStatsDF)
#print(golfstats.df)

print("--- %s seconds ---" % (time.time() - start_time))
