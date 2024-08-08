import pandas as pd

clubColumnsStrings = ['STROKE_1_CLUB', 'STROKE_2_CLUB', 'STROKE_3_CLUB', 'STROKE_4_CLUB', 'STROKE_5_CLUB', 
                      'STROKE_6_CLUB', 'STROKE_7_CLUB', 'STROKE_8_CLUB', 'STROKE_9_CLUB', 'STROKE_10_CLUB']

lieColumnStrings = ['STROKE_1_LIE', 'STROKE_2_LIE', 'STROKE_3_LIE', 'STROKE_4_LIE', 'STROKE_5_LIE', 
                    'STROKE_6_LIE', 'STROKE_7_LIE', 'STROKE_8_LIE', 'STROKE_9_LIE', 'STROKE_10_LIE', ]

scores, putts, strokes, gir, lieOutput = [], [], [], [], []
putt, stroke, fairwayHits, totalGIR = 0, 0, 0, 0

par3locs, par4locs, par5locs = [], [], []
totalPar3Score, totalPar4Score, totalPar5Score = 0, 0, 0
avgPar3Score, avgPar4Score, avgPar5Score = 0, 0, 0

# import the data that is going to get analysed as a csv file
df = pd.read_csv('GolfDataExamples/Handicap10_1.csv')

# get total strokes used (i.e. total score across the 18 holes)
for i in range(len(df['STROKES'])):
    
    # calculate score for each hole
    score = int(df['STROKES'][i] - df['PAR'][i])
    scores.append(score)
    
    # get row index of each hole's par number
    if df['PAR'][i] == 3:
        par3locs.append(i)

        # check if 'green in regulation' (GIR) is achieved
        if df.loc[i, 'STROKE_1_LIE'] == "GREEN":
            gir.append("YES")
        else:
            gir.append("NO")
    
    if df['PAR'][i] == 4:
        par4locs.append(i)

        # check if 'green in regulation' (GIR) is achieved
        for l in range(2):
            lieOutput.append(df.loc[i, lieColumnStrings[l]])

        if "GREEN" in lieOutput:
            gir.append("YES")
        else:
            gir.append("NO")
    
    if df['PAR'][i] == 5:
        par5locs.append(i)
        
        # check if 'green in regulation' (GIR) is achieved
        for l in range(3):
            lieOutput.append(df.loc[i, lieColumnStrings[l]])
        
        if "GREEN" in lieOutput:
            gir.append("YES")
        else:
            gir.append("NO")
        
    lieOutput.clear()
 
    """ 
    calculate number of strokes used for each hole => value is calculated seperately again as a challenge
    value is divided by 2 as each stroke that isn't used will consist of 2 empty cells, one for club and one for lie
    distance is just equal to 0, hence not considered empty
    """
    stroke = 10 - (pd.isnull(df.loc[i, :]).sum()) / 2

    # check how many times putter is used for each hole, and tracks it using putt variable    
    for n in range(len(clubColumnsStrings)):
        if df[clubColumnsStrings[n]][i] == 'Putter':
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

# calculate total individual scores for each par (i.e. either 3, 4 or 5) 
for i in range(len(par3locs)):
    totalPar3Score += df.loc[par3locs[i], 'SCORE']

for i in range(len(par4locs)):
    totalPar4Score += df.loc[par4locs[i], 'SCORE']
    
    # check if fairway is hit from tee off for all par 4 holes
    if df.loc[par4locs[i], 'STROKE_2_LIE'] == "FAIRWAY":
        fairwayHits += 1

for i in range(len(par5locs)):
    totalPar5Score += df.loc[par5locs[i], 'SCORE']

    # check if fairway is hit from tee off for all par 5 holes
    if df.loc[par5locs[i], 'STROKE_2_LIE'] == "FAIRWAY":
        fairwayHits += 1


# turn total individual scores into average by dividing by number of par 3, 4 and 5 holes
# dividing by 4, 10 and 4 as there are typically 4 par 3s, 10 par 4s, and 4 par 5s on an 18 hole course
avgPar3Score = round(totalPar3Score / 4, 2)
avgPar4Score = round(totalPar4Score / 10, 2)
avgPar5Score = round(totalPar5Score / 4, 2)

# gets total number of putts used throughout all 18 holes by summing the 'PUTTS' column
totalPutts = df.loc[: , 'PUTTS'].sum()

for g in range(len(gir)):
    if gir[g] == "YES":
        totalGIR += 1

# print dataframe for reference
print(df)

# print data analysis stats
print("AVG. PAR 3 SCORE:", avgPar3Score)
print("AVG. PAR 4 SCORE:", avgPar4Score)
print("AVG. PAR 5 SCORE:", avgPar5Score)
print("TOTAL PUTTS:", totalPutts, "| AVG. PUTTS:", round(totalPutts / 18, 2))

# fairways hit only applies to par 4 and 5s, hence total is divided by 14 (excludes par 3s)
print("TOTAL FAIRWAYS HIT:", fairwayHits, "| FAIRWAY HIT PERCENTAGE (%):", round((fairwayHits / 14) * 100, 2))
print("TOTAL GREENS IN REGULATION (GIRs):", totalGIR)


