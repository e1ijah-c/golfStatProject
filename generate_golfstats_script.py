import pandas as pd
import random 

CLUBS = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]
CLUB_DISTS = [280, 240, 220, 200, 190, 180, 160, 150, 140, 130, 115, 105, 90, 20]
LIES = ["TEE BOX", "FAIRWAY", "ROUGH", "BUNKER", "GREEN", "OTHER/HAZARD"]

data = []
distances = []
clubs = []
lies = []


HOLE = ['HOLE', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
        11, 12, 13, 14, 15, 16, 17, 18]

PAR = ['PAR'] 
PARS = [3, 3, 3, 3, 
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
       5, 5, 5, 5]

STROKE_1_DISTANCE = ['STROKE_1_DISTANCE']
STROKE_1_CLUB = ['STROKE_1_CLUB']
STROKE_1_LIE = ['STROKE_1_LIE']

STROKE_2_DISTANCE = ['STROKE_2_DISTANCE']
STROKE_2_CLUB = ['STROKE_2_CLUB']
STROKE_2_LIE = ['STROKE_2_LIE']

STROKE_3_DISTANCE = ['STROKE_3_DISTANCE']
STROKE_3_CLUB = ['STROKE_3_CLUB']
STROKE_3_LIE = ['STROKE_3_LIE']

STROKE_4_DISTANCE = ['STROKE_4_DISTANCE']
STROKE_4_CLUB = ['STROKE_4_CLUB']
STROKE_4_LIE = ['STROKE_4_LIE']

STROKE_5_DISTANCE = ['STROKE_5_DISTANCE']
STROKE_5_CLUB = ['STROKE_5_CLUB']
STROKE_5_LIE = ['STROKE_5_LIE']

STROKE_6_DISTANCE = ['STROKE_6_DISTANCE']
STROKE_6_CLUB = ['STROKE_6_CLUB']
STROKE_6_LIE = ['STROKE_6_LIE']

STROKE_7_DISTANCE = ['STROKE_7_DISTANCE']
STROKE_7_CLUB = ['STROKE_7_CLUB']
STROKE_7_LIE = ['STROKE_7_LIE']

STROKE_8_DISTANCE = ['STROKE_8_DISTANCE']
STROKE_8_CLUB = ['STROKE_8_CLUB']
STROKE_8_LIE = ['STROKE_8_LIE']

STROKE_9_DISTANCE = ['STROKE_9_DISTANCE']
STROKE_9_CLUB = ['STROKE_9_CLUB']
STROKE_9_LIE = ['STROKE_9_LIE']

STROKE_10_DISTANCE = ['STROKE_10_DISTANCE']
STROKE_10_CLUB = ['STROKE_10_CLUB']
STROKE_10_LIE = ['STROKE_10_LIE']

# shuffle par order for each hole
random.shuffle(PARS)

# Add pars to par list
for i in range(len(PARS)):
    PAR.append(PARS[i])

# apped HOLE and PAR lists to the main data list
data.extend([HOLE, PAR, 
             STROKE_1_DISTANCE, STROKE_1_CLUB, STROKE_1_LIE, 
             STROKE_2_DISTANCE, STROKE_2_CLUB, STROKE_2_LIE,
             STROKE_3_DISTANCE, STROKE_3_CLUB, STROKE_3_LIE,
             STROKE_4_DISTANCE, STROKE_4_CLUB, STROKE_4_LIE,
             STROKE_5_DISTANCE, STROKE_5_CLUB, STROKE_5_LIE,
             STROKE_6_DISTANCE, STROKE_6_CLUB, STROKE_6_LIE,
             STROKE_7_DISTANCE, STROKE_7_CLUB, STROKE_7_LIE,
             STROKE_8_DISTANCE, STROKE_8_CLUB, STROKE_8_LIE,
             STROKE_9_DISTANCE, STROKE_9_CLUB, STROKE_9_LIE,
             STROKE_10_DISTANCE, STROKE_10_CLUB, STROKE_10_LIE])

for i in range(18):
    strokes = random.randint(PARS[i] - 1, PARS[i] + 2)

    #print("Hole DISTANCES:")
    
    for s in range(strokes):
        
        if s == 0:
            randClub = random.randint(0, 2)

            clubs.append(CLUBS[randClub])
            lies.append(LIES[0])
            distances.append(random.randint(CLUB_DISTS[randClub] - 40, CLUB_DISTS[randClub] + 40))

        
        if s > 0 and s < strokes - 1:
            randClub = random.randint(3, len(CLUBS) - 2)

            clubs.append(CLUBS[randClub])
            lies.append(random.choice(LIES))
            distances.append(random.randint(CLUB_DISTS[randClub] - 40, CLUB_DISTS[randClub] + 40))

        if s == strokes - 1:
            clubs.append(CLUBS[13])
            lies.append(LIES[4])
            distances.append(random.randint(CLUB_DISTS[13] - 20, CLUB_DISTS[13] + 20))
    
    fillZeroesAmount = 10 - len(distances)

    for f in range(fillZeroesAmount):
        distances.append(0)
        clubs.append("N/A")
        lies.append("N/A") 
    
    for d in range(len(distances)):
        if d == 0:
            STROKE_1_DISTANCE.append(distances[0])
            STROKE_1_CLUB.append(clubs[0])
            STROKE_1_LIE.append(lies[0])
            
        if d == 1:
            STROKE_2_DISTANCE.append(distances[1])
            STROKE_2_CLUB.append(clubs[1])
            STROKE_2_LIE.append(lies[1])
        
        if d == 2:
            STROKE_3_DISTANCE.append(distances[2])
            STROKE_3_CLUB.append(clubs[2])
            STROKE_3_LIE.append(lies[2])

        if d == 3:
            STROKE_4_DISTANCE.append(distances[3])
            STROKE_4_CLUB.append(clubs[3])
            STROKE_4_LIE.append(lies[3])
        
        if d == 4:
            STROKE_5_DISTANCE.append(distances[4])
            STROKE_5_CLUB.append(clubs[4])
            STROKE_5_LIE.append(lies[4])
        
        if d == 5:
            STROKE_6_DISTANCE.append(distances[5])
            STROKE_6_CLUB.append(clubs[5])
            STROKE_6_LIE.append(lies[5])
        
        if d == 6:
            STROKE_7_DISTANCE.append(distances[6])
            STROKE_7_CLUB.append(clubs[6])
            STROKE_7_LIE.append(lies[6])
        
        if d == 7:
            STROKE_8_DISTANCE.append(distances[7])
            STROKE_8_CLUB.append(clubs[7])
            STROKE_8_LIE.append(lies[7])

        if d == 8:
            STROKE_9_DISTANCE.append(distances[8])
            STROKE_9_CLUB.append(clubs[8])
            STROKE_9_LIE.append(lies[8])

        if d == 9:
            STROKE_10_DISTANCE.append(distances[9])
            STROKE_10_CLUB.append(clubs[9])
            STROKE_10_LIE.append(lies[9])

    distances.clear()
    clubs.clear()
    lies.clear()

df = pd.DataFrame(data)
print(df)

df.to_csv('golf_stats.csv', index=False)



