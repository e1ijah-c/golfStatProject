import pandas as pd

distanceColumnStrings = ['STROKE_1_DISTANCE', 'STROKE_2_DISTANCE', 'STROKE_3_DISTANCE', 'STROKE_4_DISTANCE', 'STROKE_5_DISTANCE', 
                         'STROKE_6_DISTANCE', 'STROKE_7_DISTANCE', 'STROKE_8_DISTANCE', 'STROKE_9_DISTANCE', 'STROKE_10_DISTANCE']

clubColumnStrings = ['STROKE_1_CLUB', 'STROKE_2_CLUB', 'STROKE_3_CLUB', 'STROKE_4_CLUB', 'STROKE_5_CLUB', 
                      'STROKE_6_CLUB', 'STROKE_7_CLUB', 'STROKE_8_CLUB', 'STROKE_9_CLUB', 'STROKE_10_CLUB']

lieColumnStrings = ['STROKE_1_LIE', 'STROKE_2_LIE', 'STROKE_3_LIE', 'STROKE_4_LIE', 'STROKE_5_LIE', 
                    'STROKE_6_LIE', 'STROKE_7_LIE', 'STROKE_8_LIE', 'STROKE_9_LIE', 'STROKE_10_LIE', ]

clubs = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]

scores, putts, strokes, gir = [], [], [], []
putt, stroke, fairwayHits = 0, 0, 0
par3locs, par4locs, par5locs = [], [], []
clubDists, avgClubDists = {}, {}

# import the data that is going to get analysed as a csv file
df = pd.read_csv('GolfDataExamples/Handicap10_1.csv')

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

def TotalFairwaysHit(par4LocList: list, par5LocList: list) -> int:
    # check if fairway is hit from tee off for all par 4 & 5 holes
    global fairwayHits

    for i in range(len(par4LocList)):
        if df.loc[par4LocList[i], 'STROKE_2_LIE'] == "FAIRWAY":
            fairwayHits += 1

    for i in range(len(par5LocList)):
        if df.loc[par5LocList[i], 'STROKE_2_LIE'] == "FAIRWAY":
            fairwayHits += 1
    
    return fairwayHits

def FairwayHitPercentage() -> float:
    return round((TotalFairwaysHit(par4locs, par5locs) / 14) * 100, 2)

def TotalGIR() -> int:
    totalGIR = 0
    global gir

    # counts the total number of GIRs
    for g in range(len(gir)):
        if gir[g] == "YES":
            totalGIR += 1
    
    return totalGIR

def CalculateAvgClubDists():
    # generate list to store distances hit by each club
    for c in range(len(clubs)):
        club = str(clubs[c])
        clubDists[club] = []

    # store the distances hit by each club into their respective lists inside of the dictionary
    for n in range(len(clubColumnStrings)):
        for r in range(18):
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
print("AVG. PAR 3 SCORE:", CalculateAvgParScore(3, par3locs))
print("AVG. PAR 4 SCORE:", CalculateAvgParScore(4, par4locs))
print("AVG. PAR 5 SCORE:", CalculateAvgParScore(5, par5locs))
print("TOTAL PUTTS: {:<12} AVG. PUTTS: {}".format(TotalPutts(), AveragePutts()))

# fairways hit only applies to par 4 and 5s, hence total is divided by 14 (excludes par 3s)
print("TOTAL FAIRWAYS HIT: {:<5} FAIRWAY HIT PERCENTAGE (%): {}".format(TotalFairwaysHit(par4locs, par5locs), FairwayHitPercentage()))

print("TOTAL GREENS IN REGULATION (GIR):", TotalGIR())
print("")

CalculateAvgClubDists()
# prints out each club and its average distance neatly 
print("CLUB          AVG. DISTANCE")
print("---------------------------")
for club, avgDist in avgClubDists.items():
    print("{:<14}{}".format(club, avgDist))