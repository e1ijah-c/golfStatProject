import golfStatisticsCalculator as golfstats
import pandas as pd
import time

start_time = time.time()

rounds = 10
players = 4

roundsStatsDF = pd.read_csv('Rounds_stats_per_player.csv')
playerStatsDF = pd.read_csv('Players_stats.csv')

golfstats.GenerateColumnData()
golfstats.MakeNewColumns()

print("Players:", golfstats.PlayerCount())

for i in range(golfstats.PlayerCount()):
    golfstats.playerID = i + 1
    golfstats.UpdatePlayerIndexes()
    
    for r in range(golfstats.RoundCount()):
        golfstats.roundID = r + 1

        golfstats.UpdateRoundIndexes()
        golfstats.UpdateTotalHoles()
        golfstats.UpdateParIndexes()

        golfstats.AddRoundData()

pd.set_option("display.max_columns", None)
print(golfstats.roundsStatsDF)

print("--- %s seconds ---" % (time.time() - start_time))
