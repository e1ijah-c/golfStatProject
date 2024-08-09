import pandas as pd

distanceColumnStrings = ['STROKE_1_DISTANCE', 'STROKE_2_DISTANCE', 'STROKE_3_DISTANCE', 'STROKE_4_DISTANCE', 'STROKE_5_DISTANCE', 
                         'STROKE_6_DISTANCE', 'STROKE_7_DISTANCE', 'STROKE_8_DISTANCE', 'STROKE_9_DISTANCE', 'STROKE_10_DISTANCE']

clubColumnStrings = ['STROKE_1_CLUB', 'STROKE_2_CLUB', 'STROKE_3_CLUB', 'STROKE_4_CLUB', 'STROKE_5_CLUB', 
                      'STROKE_6_CLUB', 'STROKE_7_CLUB', 'STROKE_8_CLUB', 'STROKE_9_CLUB', 'STROKE_10_CLUB']

lieColumnStrings = ['STROKE_1_LIE', 'STROKE_2_LIE', 'STROKE_3_LIE', 'STROKE_4_LIE', 'STROKE_5_LIE', 
                    'STROKE_6_LIE', 'STROKE_7_LIE', 'STROKE_8_LIE', 'STROKE_9_LIE', 'STROKE_10_LIE', ]

clubs = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]

scores, putts, strokes, gir = [], [], [], []
putt, stroke, totalHoles = 0, 0, 0
par3locs, par4locs, par5locs = [], [], []
clubDists, avgClubDists = {}, {}

# import the data that is going to get analysed as a csv file
df = pd.read_csv('GolfDataExamples/Handicap10_1.csv')

# get total number of holes based on the index length of the dataframe
totalHoles = len(df.index)

def ScoringAverage() -> float:
    roundsPlayed = 1
    totalStrokes = df.loc[:, "STROKES USED"].sum()

    return round((totalStrokes / roundsPlayed), 2)

def CalculateAvgParScore(par: float, locList: list) -> float:
    totalParScore = 0
    
    for i in range(len(locList)):
        totalParScore += df.loc[locList[i], "SCORE"]

    if par == 3 or par == 5:
        return round(totalParScore / 4, 2)
    elif par == 4:
        return round(totalParScore / 10, 2)
    else:
        print("Error: par value is not 3, 4 or 5")

def TotalPutts() -> int:
    # gets total number of putts used throughout all 18 holes by summing the 'PUTTS' column
    return df.loc[: , 'PUTTS'].sum()

def AveragePutts() -> int:
    return round(TotalPutts() / 18, 2)

def TotalFairwaysHit(par3LocList: list, par4LocList: list, par5LocList: list) -> int:
    fairwayHits = 0

    for i in range(len(par3LocList)):
        if df.loc[par3LocList[i], 'STROKE_2_LIE'] == 'FAIRWAY':
            fairwayHits += 1

    for i in range(len(par4LocList)):
        if df.loc[par4LocList[i], 'STROKE_2_LIE'] == "FAIRWAY":
            fairwayHits += 1

    for i in range(len(par5LocList)):
        if df.loc[par5LocList[i], 'STROKE_2_LIE'] == "FAIRWAY":
            fairwayHits += 1
    
    return fairwayHits

def FairwayHitPercentage() -> float:
    global totalHoles
    return round((TotalFairwaysHit(par3locs, par4locs, par5locs) / totalHoles) * 100, 2)

def TotalGIR() -> int:
    totalGIR = 0
    global totalHoles
    global gir

    # counts the total number of GIRs
    for g in range(len(gir)):
        if gir[g] == "YES":
            totalGIR += 1
    
    return totalGIR

def DrivingAccuracyPercentage() -> float:
    global totalHoles
    global clubColumnStrings
    global lieColumnStrings
    driverAttempts = 0
    successfulDriverAttempts = 0
    successfulLies = ["FAIRWAY", "GREEN"]
    driverLocs = {}

    for c in range(len(clubColumnStrings)):
        col = str(clubColumnStrings[c])
        driverLocs[col] = []

    for i in range(totalHoles):
        for c in range(len(clubColumnStrings)):
            if df.loc[i, clubColumnStrings[c]] == "DRIVER":
                driverAttempts += 1
                col = str(clubColumnStrings[c])
                driverLocs[col].append(i)
    
    for c in range(len(clubColumnStrings)):
        key = str(clubColumnStrings[c])
        for r in range(len(driverLocs[key])):
            if df.loc[driverLocs[key][r], lieColumnStrings[c + 1]] in successfulLies:
                successfulDriverAttempts += 1

    #print(successfulDriverAttempts)
    return round((successfulDriverAttempts / driverAttempts) * 100, 2)


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
        
        if int(sum(clubDists[key])) == 0:
            avgClubDists[key] = 0
        else:
            result = round(sum(clubDists[key]) / len(clubDists[key]), 2)
            avgClubDists[key] = result

def ScramblingPercentage() -> float:
    global totalHoles
    girsMissed = totalHoles - TotalGIR()
    missedGIRLocs = []
    scrambles = 0

    # get location of all the holes where GIR is missed
    for i in range(totalHoles):
        if df.loc[i, "GIR"] == "NO":
            missedGIRLocs.append(i)
    
    # for each of these holes, check if par or better is met
    for i in range(len(missedGIRLocs)):
        if df.loc[missedGIRLocs[i], "SCORE"] <= 0:
            scrambles += 1
    
    return round((scrambles / girsMissed) * 100, 2)

def SandSavePercentage() -> float:
    global totalHoles
    global lieColumnStrings
    sandShots = 0
    sandShotLocs = []
    sandSaves = 0

    # get number of shots from the bunker and their locations in the dataframe
    for i in range(totalHoles):
        for l in range(len(lieColumnStrings)):
            if df.loc[i, lieColumnStrings[l]] == "BUNKER":
                sandShots += 1
                sandShotLocs.append(i)
    
    # remove duplicates in the sandShotLocs list (i.e. holes where bunker was hit more than once)
    # works by creating dictionary which cannot contain duplicates
    sandShotLocs = list(dict.fromkeys(sandShotLocs)) 

    # check for each of these holes where bunker was landed on, that a par or better was achieved
    for i in range(len(sandShotLocs)):
        if df.loc[sandShotLocs[i], "SCORE"] <= 0:
            sandSaves += 1

    return round((sandSaves / sandShots) * 100, 2)

def BirdieOrBetterPercentage() -> float:
    global totalHoles
    birdiesOrBetter = 0

    for i in range(totalHoles):
        if df.loc[i, "SCORE"] <= -1:
            birdiesOrBetter += 1
    
    return round((birdiesOrBetter / totalHoles) * 100, 2)


def GenerateNewColumns():
    global putt
    lieOutput = []    
    
    for i in range(len(df['STROKES'])):        
        # calculate score for each hole
        score = int(df['STROKES'][i] - df['PAR'][i])
        scores.append(score)
        
        # get row index of each hole's par number
        if df['PAR'][i] == 3:
            par3locs.append(i)
            if df.loc[i, 'STROKE_1_LIE'] == "GREEN":
                gir.append("YES")
            else:
                gir.append("NO")

        if df['PAR'][i] == 4:
            par4locs.append(i)
            
            for l in range(2):
                lieOutput.append(df.loc[i, lieColumnStrings[l]])
            if "GREEN" in lieOutput:
                gir.append("YES")
            else:
                gir.append("NO")

        if df['PAR'][i] == 5:
            par5locs.append(i)   
            for l in range(3):
                lieOutput.append(df.loc[i, lieColumnStrings[l]])
            if "GREEN" in lieOutput:
                gir.append("YES")
            else:
                gir.append("NO")   
        
        lieOutput.clear()
  
        stroke = 10 - (pd.isnull(df.loc[i, :]).sum()) / 2

        # check how many times putter is used for each hole, and tracks it using putt variable    
        for n in range(len(clubColumnStrings)):
            if df[clubColumnStrings[n]][i] == 'Putter':
                putt += 1
            
        putts.append(putt)
        strokes.append(stroke)
        # reset putt and stroke variable so next hole starts from 0 again
        putt = 0
        stroke = 0

    # add new columns after data analysis
    df['SCORE'] = scores
    df['STROKES USED'] = strokes
    df['PUTTS'] = putts
    df['GIR'] = gir


GenerateNewColumns()
# print dataframe for reference
print(df)
print("")

# print data analysis stats
print("STATISTICS ________________________________________________")
print("")
print("SCORING AVERAGE: {}".format(ScoringAverage()))
print("AVG. PAR 3 SCORE: {}".format(CalculateAvgParScore(3, par3locs)))
print("AVG. PAR 4 SCORE: {}".format(CalculateAvgParScore(4, par4locs)))
print("AVG. PAR 5 SCORE: {}".format(CalculateAvgParScore(5, par5locs)))
print("BIRDIES OR BETTER PERCENTAGE (%): {}".format(BirdieOrBetterPercentage()))
print("TOTAL PUTTS: {:<12} AVG. PUTTS PER ROUND: {}".format(TotalPutts(), AveragePutts()))

# fairways hit only applies to par 4 and 5s, hence total is divided by 14 (excludes par 3s)
print("TOTAL FAIRWAYS HIT: {:<5} FAIRWAY HIT PERCENTAGE (%): {}".format(TotalFairwaysHit(par3locs, par4locs, par5locs), FairwayHitPercentage()))

print("DRIVING ACCURACY PERCENTAGE (%): {}".format(DrivingAccuracyPercentage()))
print("TOTAL GREENS IN REGULATION (GIR): {}".format(TotalGIR()))
print("SCRAMBLING PERCENTAGE(%): {}".format(ScramblingPercentage()))
print("SAND SAVE PERCENTAGE (%): {}".format(SandSavePercentage()))
print("")

CalculateAvgClubDists()
# prints out each club and its average distance neatly 
print("CLUB          AVG. DISTANCE")
print("---------------------------")
for club, avgDist in avgClubDists.items():
    print("{:<14}{}".format(club, avgDist))