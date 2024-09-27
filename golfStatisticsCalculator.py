import pandas as pd
import numpy as np
import statistics as st

distanceColumnStrings = ['STROKE_1_DISTANCE', 'STROKE_2_DISTANCE', 'STROKE_3_DISTANCE', 'STROKE_4_DISTANCE', 
                         'STROKE_5_DISTANCE', 'STROKE_6_DISTANCE', 'STROKE_7_DISTANCE', 'STROKE_8_DISTANCE']

clubColumnStrings = ['STROKE_1_CLUB', 'STROKE_2_CLUB', 'STROKE_3_CLUB', 'STROKE_4_CLUB', 
                     'STROKE_5_CLUB', 'STROKE_6_CLUB', 'STROKE_7_CLUB', 'STROKE_8_CLUB']

lieColumnStrings = ['STROKE_1_LIE', 'STROKE_2_LIE', 'STROKE_3_LIE', 'STROKE_4_LIE', 
                    'STROKE_5_LIE', 'STROKE_6_LIE', 'STROKE_7_LIE', 'STROKE_8_LIE']

clubs = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]

scores, putts, strokes, gir, fairwaysHit = [], [], [], [], []
par3indexes, par4indexes, par5indexes = [], [], []
sandSaves, sandShots, driverAttempts, successfulDriverAttempts, scrambles, birdiesOrBetter, doubleBogeysOrWorse, holesAfterBogey, birdiesAfterBogey, ThreePutts = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
clubDists, avgClubDists = {}, {}
totalHoles = 0


df = 'dataframe reference'
adf = pd.read_csv('Rounds_stats_per_player.csv')

def UpdateTotalHoles():
    global totalHoles
    totalHoles = len(df)

def OverallTotalParPlusMinus():
    return df['PAR +/-'].sum()

def UpdateParIndexes():
    global par3indexes
    global par4indexes
    global par5indexes

    par3indexes, par4indexes, par5indexes = [], [], []

    for i in range(totalHoles):
        if df.loc[i, 'PAR'] == 3:
            par3indexes.append(i)
        elif df.loc[i, 'PAR'] == 4:
            par4indexes.append(i)
        else: 
            par5indexes.append(i)

def TotalParScore(par: int) -> int:
    totalParScore = 0
    if par == 3:
        for p in range(len(par3indexes)):
            totalParScore += df.loc[par3indexes[p],'SCORE']
    elif par == 4:
        for p in range(len(par4indexes)):
            totalParScore += df.loc[par4indexes[p],'SCORE']
    elif par == 5:
        for p in range(len(par5indexes)):
            totalParScore += df.loc[par5indexes[p],'SCORE']
    else:
        print('Error: input must be either 3, 4 or 5')
    
    return totalParScore

def TotalParPlusMinus(par: int) -> int:
    totalParPlusMinus = 0
    if par == 3:
        for p in range(len(par3indexes)):
            totalParPlusMinus += df.loc[par3indexes[p],'PAR +/-']
    elif par == 4:
        for p in range(len(par4indexes)):
            totalParPlusMinus += df.loc[par4indexes[p],'PAR +/-']
    elif par == 5:
        for p in range(len(par5indexes)):
            totalParPlusMinus += df.loc[par5indexes[p],'PAR +/-']
    else:
        print('Error: input must be either 3, 4 or 5')
    
    return totalParPlusMinus


def TotalPutts() -> int:
    # gets total number of putts used throughout all 18 holes by summing the 'PUTTS' column
    return df['PUTTS'].sum()

def AveragePutts() -> int:
    return round(TotalPutts() / totalHoles, 2)

def TotalFairwaysHit() -> int:
    return sum(df['FAIRWAY_HIT'] == 'YES')


def FairwayHitPercentage() -> float:
    par3s = 0
    for i in range(totalHoles):
        if df.loc[i, 'PAR'] == 3:
            par3s += 1

    holesWithoutPar3s = totalHoles - par3s
    return round((TotalFairwaysHit() / holesWithoutPar3s) * 100, 2)

def TotalGIR() -> int:
    totalGIR = 0
    global gir

    # counts the total number of GIRs
    for i in range(totalHoles):
        if gir[i] == "YES":
            totalGIR += 1
    
    return totalGIR

def DrivingAccuracyPercentage() -> float:
    global clubColumnStrings
    global lieColumnStrings
    global driverAttempts 
    global successfulDriverAttempts
    successfulLies = ["Fairway", "Green"]
    driverLocations = {}
    driverAttempts, successfulDriverAttempts = 0, 0

    # create dictionary to store index for each hole that the driver was used
    for c in range(len(clubColumnStrings)):
        col = str(clubColumnStrings[c])
        driverLocations[col] = []

    # store the index for each hole that a driver was used into their respective lists inside the dictionary & tally up the total times the driver was used
    for i in range(totalHoles):
        for c in range(len(clubColumnStrings)):
            if df.loc[i, clubColumnStrings[c]] == "Driver":
                driverAttempts += 1
                col = str(clubColumnStrings[c])
                driverLocations[col].append(i)
    
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
                if pd.isnull(df.loc[r, clubColumnStrings[n]]) == False:
                    key = str(df.loc[r, clubColumnStrings[n]])
                    clubDists[key].append(int(df.loc[r, distanceColumnStrings[n]]))

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
        if df.loc[i, "GIR"] == "NO":
            missedGIRLocations.append(i)
    
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
            if df.loc[i, lieColumnStrings[l]] == "Bunker":
                sandShots += 1
                sandShotLocations.append(i)
    
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
        if df.loc[i, "SCORE"] <= -1:
            birdiesOrBetter += 1
    
    return round((birdiesOrBetter / totalHoles) * 100, 2)

def DoubleBogeyOrWorsePercentage() -> float:
    global doubleBogeysOrWorse

    doubleBogeysOrWorse = 0

    for i in range(totalHoles):
        if df.loc[i, 'PAR +/-'] >= 2:
            doubleBogeysOrWorse += 1
    
    return round((doubleBogeysOrWorse / totalHoles) * 100, 2)

def TotalPenalties() -> int:
    return df['PENALTIES'].sum()

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
            if df.loc[i, lieColumnStrings[l]] == "Green":
                key = str(lieColumnStrings[l])
                greenDict[key].append(i)
    
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
    
    putts = list(df['PUTTS'])
    for i in range(totalHoles):
        if putts[i] >= 3:
            ThreePutts += 1
    
    return round((ThreePutts / totalHoles) * 100, 2)

def BounceBackPercentage() -> float:
    global holesAfterBogey
    global birdiesAfterBogey
    
    holesAfterBogey = 0
    birdiesAfterBogey = 0

    for i in range(totalHoles):
        if df.loc[i, 'PAR +/-'] >= 1 and i < totalHoles - 1:
            if df.loc[i+1, 'PAR +/-'] <= -1:
                birdiesAfterBogey += 1
    
    for i in range(totalHoles):
        if df.loc[i, 'PAR +/-'] >= 1:
            holesAfterBogey += 1
    
    if df.loc[totalHoles - 1, 'PAR +/-'] >= 1:
        holesAfterBogey -= 1
    
    if holesAfterBogey != 0:
        return round((birdiesAfterBogey / holesAfterBogey) * 100, 2)
    else:
        return 0

def TotalChipShots():
    return df['CHIP_SHOTS'].sum()

def TotalBunkerAttempts():
    return df['BUNKER_ATTEMPTS'].sum()

def CheckChipShots():
    for i in range(totalHoles):
        chipShots = 0
        if pd.isnull(df.loc[i, 'CHIP_SHOTS']) == True:
            for c in range(len(clubColumnStrings)):
                if pd.isnull(df.loc[i, clubColumnStrings[c]]) == True:
                    break
                elif "Wedge" in df.loc[i, clubColumnStrings[c]] and df.loc[i, distanceColumnStrings[c]] <= 40:
                    chipShots += 1
            df.loc[i, 'CHIP_SHOTS'] = chipShots

def CheckBunkerAttempts():
    for i in range(totalHoles):
        bunkerAttempts = 0
        if pd.isnull(df.loc[i, 'BUNKER_ATTEMPTS']) == True:
            for l in range(len(lieColumnStrings)):
                if df.loc[i, lieColumnStrings[l]] == "Bunker":
                    bunkerAttempts += 1
            df.loc[i, 'BUNKER_ATTEMPTS'] = bunkerAttempts


def CalculateGIRs():
    global gir
    for i in range(totalHoles):
        if pd.isnull(df.loc[i, 'GIR']) == True:
            if df.loc[i, 'SCORE'] - df.loc[i, 'PUTTS'] <= df.loc[i, 'PAR'] - 2:
                gir.append('YES')
            else:
                gir.append('NO')

    df['GIR'] = gir

def CalculateParPlusMinus():
    strokes = list(df['SCORE'])
    pars = list(df['PAR'])

    for i in range(totalHoles):
        plus_minus = strokes[i] - pars[i]
        scores.append(plus_minus)

    df['PAR +/-'] = scores 

def CalculateFairwaysHit():
    lieCheck = list(df['STROKE_1_LIE'])
    pars = list(df['PAR'])

    for i in range(totalHoles):
        if lieCheck[i] == 'Fairway' and pars[i] != 3:
            fairwaysHit.append('YES')
        else:
            fairwaysHit.append('NO')

    df['FAIRWAY_HIT'] = fairwaysHit

def AddRoundData():
    global gir
    global scores
    global fairwaysHit
    roundStats = []
    totalScore = df["SCORE"].sum()
    fairwaysWithoutPar3Holes = int(totalHoles - len(par3indexes))
    holesWithGIRMissed = int(totalHoles - TotalGIR())

    SandSavePercentage()
    DrivingAccuracyPercentage()
    ScramblingPercentage()
    BirdieOrBetterPercentage()
    DoubleBogeyOrWorsePercentage()
    BounceBackPercentage()

    # add each round's data into a single list
    roundStats.extend((0, 0, 
                       totalHoles, totalScore, OverallTotalParPlusMinus(), 
                       TotalParScore(3), TotalParPlusMinus(3), 
                       TotalParScore(4), TotalParPlusMinus(4), 
                       TotalParScore(5), TotalParPlusMinus(5), 
                       TotalPutts(), TotalGIR(), 
                       sandSaves, TotalBunkerAttempts(), SandSavePercentage(), 
                       TotalPenalties(), 
                       TotalFairwaysHit(), fairwaysWithoutPar3Holes, FairwayHitPercentage(), 
                       successfulDriverAttempts, driverAttempts, DrivingAccuracyPercentage(), 
                       scrambles, holesWithGIRMissed, ScramblingPercentage(), 
                       birdiesOrBetter, BirdieOrBetterPercentage(), 
                       doubleBogeysOrWorse, DoubleBogeyOrWorsePercentage(), 
                       birdiesAfterBogey, holesAfterBogey, BounceBackPercentage(),
                       ThreePutts, ThreePutAvoidance(), 
                       ProximityToHole(),
                       TotalChipShots()))

    # add new row indicating round ID, player ID, and the corresponsding stats
    adf.loc[len(adf)] = roundStats

    gir.clear()
    scores.clear()
    fairwaysHit.clear()



