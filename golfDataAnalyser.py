import pandas as pd

clubColumnsStrings = ['STROKE_1_CLUB', 'STROKE_2_CLUB', 'STROKE_3_CLUB', 'STROKE_4_CLUB', 'STROKE_5_CLUB', 
                      'STROKE_6_CLUB', 'STROKE_7_CLUB', 'STROKE_8_CLUB', 'STROKE_9_CLUB', 'STROKE_10_CLUB']

scores, putts = [], []
putt = 0

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
    
    if df['PAR'][i] == 4:
        par4locs.append(i)
    
    if df['PAR'][i] == 5:
        par5locs.append(i)
    
    for n in range(len(clubColumnsStrings)):
        # check how many times putter is used for each hole, and tracks it using putt variable
        if df[clubColumnsStrings[n]][i] == 'Putter':
            putt += 1

    putts.append(putt)

    # reset putt variable so next hole starts from 0 again
    putt = 0

# add new columns after data analysis
df['TOTAL SCORE'] = scores
df['TOTAL PUTTS'] = putts

# calculate total individual scores for each par (i.e. either 3, 4 or 5) 
for i in range(len(par3locs)):
    totalPar3Score += df.loc[par3locs[i], 'TOTAL SCORE']

for i in range(len(par4locs)):
    totalPar4Score += df.loc[par4locs[i], 'TOTAL SCORE']

for i in range(len(par5locs)):
    totalPar5Score += df.loc[par5locs[i], 'TOTAL SCORE']

# turn total individual scores into average by dividing by number of par 3, 4 and 5 holes
# dividing by 4, 10 and 4 as there are typically 4 par 3s, 10 par 4s, and 4 par 5s on an 18 hole course
avgPar3Score = totalPar3Score / 4
avgPar4Score = totalPar4Score / 10
avgPar5Score = totalPar5Score / 4

# print dataframe for reference
print(df)

# print data analysis stats
print("AVERAGE PAR 3 SCORE:", avgPar3Score)
print("AVERAGE PAR 4 SCORE:", avgPar4Score)
print("AVERAGE PAR 5 SCORE:", avgPar5Score)
