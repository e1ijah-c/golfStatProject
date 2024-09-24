import pandas as pd
import numpy as np
import statistics as st


distanceColumnStrings = ['STROKE_1_DISTANCE', 'STROKE_2_DISTANCE', 'STROKE_3_DISTANCE', 'STROKE_4_DISTANCE', 'STROKE_5_DISTANCE', 
                         'STROKE_6_DISTANCE', 'STROKE_7_DISTANCE', 'STROKE_8_DISTANCE', 'STROKE_9_DISTANCE', 'STROKE_10_DISTANCE']

clubColumnStrings = ['STROKE_1_CLUB', 'STROKE_2_CLUB', 'STROKE_3_CLUB', 'STROKE_4_CLUB', 'STROKE_5_CLUB', 
                      'STROKE_6_CLUB', 'STROKE_7_CLUB', 'STROKE_8_CLUB', 'STROKE_9_CLUB', 'STROKE_10_CLUB']

lieColumnStrings = ['STROKE_1_LIE', 'STROKE_2_LIE', 'STROKE_3_LIE', 'STROKE_4_LIE', 'STROKE_5_LIE', 
                    'STROKE_6_LIE', 'STROKE_7_LIE', 'STROKE_8_LIE', 'STROKE_9_LIE', 'STROKE_10_LIE', ]

clubs = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]

scores, putts, strokes, gir, fairwaysHit = [], [], [], [], []
sandSaves, sandShots, driverAttempts, successfulDriverAttempts, scrambles, birdiesOrBetter, doubleBogeysOrWorse, holesAfterBogey, birdiesAfterBogey, ThreePutts = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
par3indexes, par4indexes, par5indexes = [], [], []
clubDists, avgClubDists = {}, {}

playerID = 0
roundID = 0

round_indexes, player_indexes = [], []
totalHoles = 0

# import the data that is going to get analysed as a csv file

#   df = pd.read_csv('Raw_Data_Example.csv')
df = pd.read_csv('Real_Data_1.csv')

roundsStatsDF = pd.read_csv('Rounds_stats_per_player.csv')

def PlayerCount() -> int:
    return df['PLAYER_ID'].nunique()

def UpdatePlayerIndexes():
    global player_indexes
    player_indexes = []
    
    for i in range(len(df.index)):
        if df.loc[i, 'PLAYER_ID'] == playerID:
            player_indexes.append(i)

def RoundCount() -> int:
    rounds = []
    
    for r in range(len(player_indexes)):
        rounds.append(int(df.loc[r, 'ROUND_ID']))
    
    return len(set(rounds)) 

def UpdateRoundIndexes():
    global round_indexes
    round_indexes = []

    for i in range(len(player_indexes)):
        if df.loc[player_indexes[i], 'ROUND_ID'] == roundID:
            round_indexes.append(player_indexes[i])
    
def UpdateTotalHoles():
    global totalHoles
    #totalHoles = len(round_indexes)
    totalHoles = len(df)


def ScoringAverage() -> float:
    totalStrokes = df.loc[round_indexes[0]:round_indexes[-1], "STROKES USED"].sum()

    return round((totalStrokes / totalHoles), 2)

def CalculateAvgParScore(parIndexList: list) -> float:
    totalParScore = 0
    
    for i in range(len(parIndexList)):
        totalParScore += df.loc[parIndexList[i], "SCORE"]

    return round(totalParScore / len(parIndexList), 2)

def UpdateParIndexes():
    global par3indexes
    global par4indexes
    global par5indexes

    par3indexes, par4indexes, par5indexes = [], [], []

    for i in range(totalHoles):
        if df.loc[round_indexes[i], 'PAR'] == 3:
            par3indexes.append(round_indexes[i])
        elif df.loc[round_indexes[i], 'PAR'] == 3:
            par4indexes.append(round_indexes[i])
        else: 
            par5indexes.append(round_indexes[i])

def TotalPutts() -> int:
    # gets total number of putts used throughout all 18 holes by summing the 'PUTTS' column
    return int(df.loc[round_indexes[0]:round_indexes[-1] , 'PUTTS'].sum())

def AveragePutts() -> int:
    return round(TotalPutts() / totalHoles, 2)

def TotalFairwaysHit() -> int:
    #return playerStatsDF.loc[playerID - 1, 'Total_Fairways_hit']
    totalFairways = 0

    for i in range(totalHoles):
        if df.loc[round_indexes[i], 'STROKE_2_LIE'] == "FAIRWAY":
            totalFairways += 1

    for i in range(len(par3indexes)):
        if df.loc[par3indexes[i], 'STROKE_2_LIE'] == "FAIRWAY":
            totalFairways -= 1
    
    return totalFairways

def FairwayHitPercentage() -> float:
    par3s = 0
    for i in range(totalHoles):
        if df.loc[round_indexes[i], 'PAR'] == 3:
            par3s += 1

    holesWithoutPar3s = totalHoles - par3s
    return round((TotalFairwaysHit() / holesWithoutPar3s) * 100, 2)

def TotalGIR() -> int:
    totalGIR = 0
    global gir

    # counts the total number of GIRs
    for i in range(totalHoles):
        if gir[round_indexes[i]] == "YES":
            totalGIR += 1
    
    return totalGIR

def DrivingAccuracyPercentage() -> float:
    global clubColumnStrings
    global lieColumnStrings
    global driverAttempts 
    global successfulDriverAttempts
    successfulLies = ["FAIRWAY", "GREEN"]
    driverLocations = {}
    driverAttempts, successfulDriverAttempts = 0, 0

    # create dictionary to store index for each hole that the driver was used
    for c in range(len(clubColumnStrings)):
        col = str(clubColumnStrings[c])
        driverLocations[col] = []

    # store the index for each hole that a driver was used into their respective lists inside the dictionary & tally up the total times the driver was used
    for i in range(totalHoles):
        for c in range(len(clubColumnStrings)):
            if df.loc[round_indexes[i], clubColumnStrings[c]] == "DRIVER":
                driverAttempts += 1
                col = str(clubColumnStrings[c])
                driverLocations[col].append(round_indexes[i])
    
    # go through each stroke for every hole in which a driver was used 
    # next, check if the corresponding lie is on the fairway or green; counting a successful driver attempt if it was
    for c in range(len(clubColumnStrings)):
        key = str(clubColumnStrings[c])
        for r in range(len(driverLocations[key])):
            if df.loc[driverLocations[key][r], lieColumnStrings[c + 1]] in successfulLies:
                successfulDriverAttempts += 1

    if driverAttempts != 0:
        return round((successfulDriverAttempts / driverAttempts) * 100, 2)
    else:
        return 0

def CalculateAvgClubDists():
    # generate list to store distances hit by each club
    for c in range(len(clubs)):
        club = str(clubs[c])
        clubDists[club] = []

    # store the distances hit by each club into their respective lists inside of the dictionary
    for n in range(len(clubColumnStrings)):
        for r in range(totalHoles):
                if pd.isnull(df.loc[round_indexes[r], clubColumnStrings[n]]) == False:
                    key = str(df.loc[r, clubColumnStrings[n]])
                    clubDists[key].append(int(df.loc[round_indexes[r], distanceColumnStrings[n]]))

    # calculates the average distance of each club and adds it to a seperate dictionary
    for c in range(len(clubs)):
        key = str(clubs[c])
        # begins counting average only if the club is used more than 5 times
        if len(clubDists[key]) < 5:
            if len(clubDists[key]) == 0:
                avgClubDists[key] = "No Data"
            else:
                avgClubDists[key] = round(st.mean(clubDists[key]), 2)
        
        # special case for Wedges where only the 5 longest strokes are averaged
        elif 'Wedge' in key:
            # sort list in descending order
            clubDists[key].sort(reverse=True)
            # get the top 5 longest shots
            top5LWedgeDists = []
            for n in range(5):
                top5LWedgeDists.append(clubDists[key][n])
            # get average of those 5 shots
            avgClubDists[key] = round(st.mean(top5LWedgeDists), 2)
        
        # disregard putting distance
        elif key == 'Putter':
            return 

        else:
            # arrange the distances in descending order (largest to smallest)
            clubDists[key].sort(reverse=True)
            top5ClubDists = []
            distsInRange = []

            # store the 5 longest distances in a seperate list
            for n in range(5):
                top5ClubDists.append(clubDists[key][n])

            # calculate the mean (average) of the top 5 clubs
            avgTop5ClubDists = st.mean(top5ClubDists)

            # calculate error of 5% of the average
            distError = avgTop5ClubDists * 0.05

            # store the number of distance values that fall within 5% of the averaged top 5 longest distances
            for d in range(len(clubDists[key])):
                if avgTop5ClubDists - distError <= clubDists[key][d] <= avgTop5ClubDists + distError:
                    distsInRange.append(clubDists[key][d]) 
            
            # keep final averaged value as the average of the top 5 distances if there are less than 5 distance values that fall within range
            # otherwise final value is taken as the average of the values that are within the acceptable range of error
            if len(distsInRange) < 5:
                avgClubDists[key] = round(avgTop5ClubDists, 2)
            else:
                avgClubDists[key] = round(st.mean(distsInRange), 2)


def ScramblingPercentage() -> float:
    girsMissed = totalHoles - TotalGIR()
    missedGIRLocations = []
    global scrambles 

    scrambles = 0

    # get location of all the holes where GIR is missed
    for i in range(totalHoles):
        if df.loc[round_indexes[i], "GIR"] == "NO":
            missedGIRLocations.append(round_indexes[i])
    
    # for each of these holes, check if par or better is met
    for i in range(len(missedGIRLocations)):
        if df.loc[missedGIRLocations[i], "SCORE"] <= 0:
            scrambles += 1
    
    return round((scrambles / girsMissed) * 100, 2)

def SandSavePercentage() -> float:
    global lieColumnStrings
    global sandShots  
    global sandSaves  
    sandShotLocations = []
    sandShots, sandSaves = 0, 0

    # get number of shots from the bunker and their locations in the dataframe
    for i in range(totalHoles):
        for l in range(len(lieColumnStrings)):
            if df.loc[round_indexes[i], lieColumnStrings[l]] == "BUNKER":
                sandShots += 1
                sandShotLocations.append(round_indexes[i])
    
    # remove duplicates in the sandShotLocations list (i.e. holes where bunker was hit more than once)
    # works by creating dictionary which cannot contain duplicates
    sandShotLocations = list(dict.fromkeys(sandShotLocations)) 

    # check for each of these holes where bunker was landed on, that a par or better was achieved
    for i in range(len(sandShotLocations)):
        if df.loc[sandShotLocations[i], "SCORE"] <= 0:
            sandSaves += 1

    if sandShots != 0:
        return round((sandSaves / sandShots) * 100, 2)
    else:
        return 0

def BirdieOrBetterPercentage() -> float:
    global birdiesOrBetter 
    birdiesOrBetter = 0

    for i in range(totalHoles):
        if df.loc[round_indexes[i], "SCORE"] <= -1:
            birdiesOrBetter += 1
    
    return round((birdiesOrBetter / totalHoles) * 100, 2)

def DoubleBogeyOrWorsePercentage() -> float:
    global doubleBogeysOrWorse

    doubleBogeysOrWorse = 0

    for i in range(totalHoles):
        if df.loc[round_indexes[i], 'SCORE'] >= 2:
            doubleBogeysOrWorse += 1
    
    return round((doubleBogeysOrWorse / totalHoles) * 100, 2)

def TotalPenalties() -> int:
    global lieColumnStrings 
    penalties = 0

    for i in range(totalHoles):
        for l in range(len(lieColumnStrings)):
            if df.loc[round_indexes[i], lieColumnStrings[l]] == 'OTHER/HAZARD':
                penalties += 1

    return penalties

def ProximityToHole() -> float:
    global lieColumnStrings
    global distanceColumnStrings
    duplicates = []
    holeProximities = []
    greenDict = {}

    # create dictionary to store each stroke's lie column and the index of their greens
    for l in range(len(lieColumnStrings)):
        lie = str(lieColumnStrings[l])
        greenDict[lie] = []
    
    # append the index of ALL green lies to its corresponding stroke in the dictionary 
    for i in range(totalHoles):
        for l in range(len(lieColumnStrings)):
            if df.loc[round_indexes[i], lieColumnStrings[l]] == "GREEN":
                key = str(lieColumnStrings[l])
                greenDict[key].append(round_indexes[i])
    
    # find all the duplicates and append them to a seperate list (i.e. duplicate meaning green is hit more than once per hole)
    for l in range(len(lieColumnStrings)):
        key = str(lieColumnStrings[l])
        for i in range(totalHoles):
            if i in greenDict[key]:
                duplicates.append(i)
    
    # remove the duplicates from the list
    duplicates = list(dict.fromkeys(duplicates))

    # remove the duplicates from the dictionary, leaving only the first instance of each green (i.e. keep the earliest stroke at which green was hit)
    for d in range(len(duplicates)):
        count = 0
        for l in range(len(lieColumnStrings)):
            key = str(lieColumnStrings[l])
            if duplicates[d] in greenDict[key]:
                if count == 0:
                    count += 1
                else:
                    greenDict[key].remove(duplicates[d])
    
    # get the sum of the distances of all the strokes before the green was hit, and subtract from the total yardage to get proximity to hole
    for l in range(len(lieColumnStrings)):        
        key = str(lieColumnStrings[l])
        for g in range(len(greenDict[key])):
            dists = []
            for a in range(l + 1):
                if a >= 1:
                    dist = int(df.loc[greenDict[key][g], distanceColumnStrings[l - a]])
                    dists.append(dist)
            holeYardage = df.loc[greenDict[key][g], "YARDAGE"]
            proximity = int(holeYardage - sum(dists))
            holeProximities.append(proximity)
            dists.clear()         

    return round(sum(holeProximities) / totalHoles, 2)

def ThreePutAvoidance() -> float:
    global ThreePutts
    ThreePutts = 0

    for i in range(totalHoles):
        putts = df.loc[i, :].value_counts()["Putter"]
        if putts >= 3:
            ThreePutts += 1
    
    return round((ThreePutts / totalHoles) * 100, 2)

def BounceBackPercentage() -> float:
    global holesAfterBogey
    global birdiesAfterBogey
    
    holesAfterBogey = 0
    birdiesAfterBogey = 0

    for i in range(totalHoles):
        if df.loc[round_indexes[i], 'SCORE'] >= 1 and i < totalHoles - 1:
            if df.loc[i+1, 'SCORE'] <= -1:
                birdiesAfterBogey += 1
    
    for i in range(totalHoles):
        if df.loc[round_indexes[i], 'SCORE'] >= 1:
            holesAfterBogey += 1
    
    if df.loc[totalHoles - 1, 'SCORE'] >= 1:
        holesAfterBogey -= 1
    
    if holesAfterBogey != 0:
        return round((birdiesAfterBogey / holesAfterBogey) * 100, 2)
    else:
        return 0

def CalculateGIRs():

    for i in range(totalHoles):
        if pd.isnull(df.loc[i, 'GIR']) == True:
            if df.loc[i, 'STROKES'] - df.loc[i, 'PUTTS'] <= df.loc[i, 'PAR'] - 2:
                gir.append('YES')
            else:
                gir.append('NO')

    df['GIR'] = gir

def CalculateScores():

    strokes = list(df['STROKES'])
    pars = list(df['PAR'])

    for i in range(totalHoles):
        score = strokes[i] - pars[i]
        scores.append(score)

    df['SCORE'] = scores 

def CalculateFairwaysHit():

    lieCheck = list(df['STROKE_2_LIE'])
    pars = list(df['PAR'])

    for i in range(totalHoles):
        if lieCheck[i] == 'Fairway' and pars[i] != 3:
            fairwaysHit.append('YES')
        else:
            fairwaysHit.append('NO')

    df['FAIRWAY_HIT'] = fairwaysHit


def AddRoundData():
    roundStats = []
    totalStrokes = int(df.loc[round_indexes[0]:round_indexes[-1], "SCORE"].sum())
    fairwaysWithoutPar3Holes = int(totalHoles - len(par3indexes))
    holesWithGIRMissed = int(totalHoles - TotalGIR())

    SandSavePercentage()
    DrivingAccuracyPercentage()
    ScramblingPercentage()
    BirdieOrBetterPercentage()
    DoubleBogeyOrWorsePercentage()
    BounceBackPercentage()

    # add each round's data into a single list
    roundStats.extend((roundID, playerID, 
                       totalHoles, totalStrokes, TotalPutts(), TotalGIR(), 
                       sandSaves, sandShots, SandSavePercentage(), 
                       TotalPenalties(), 
                       TotalFairwaysHit(), fairwaysWithoutPar3Holes, FairwayHitPercentage(), 
                       successfulDriverAttempts, driverAttempts, DrivingAccuracyPercentage(), 
                       scrambles, holesWithGIRMissed, ScramblingPercentage(), 
                       birdiesOrBetter, BirdieOrBetterPercentage(), 
                       doubleBogeysOrWorse, DoubleBogeyOrWorsePercentage(), 
                       birdiesAfterBogey, holesAfterBogey, BounceBackPercentage(),
                       ThreePutts, ThreePutAvoidance(), 
                       ProximityToHole()))

    # add new row indicating round ID, player ID, and the corresponsding stats
    roundsStatsDF.loc[len(roundsStatsDF)] = roundStats


UpdateTotalHoles()
CalculateGIRs()
CalculateScores()
CalculateFairwaysHit()
print(df)
