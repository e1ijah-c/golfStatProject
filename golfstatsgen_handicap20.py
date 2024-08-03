import pandas as pd
import random 

CLUBS = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]
CLUB_DISTS = [215, 175, 155, 150, 145, 135, 125, 115, 105, 75, 60, 45, 10]
LIES = ["TEE BOX", "FAIRWAY", "FAIRWAY", "FAIRWAY", "FAIRWAY", "ROUGH", "ROUGH", "ROUGH", "BUNKER", "OTHER/HAZARD", "GREEN"]

PAR_3_MAX = 240
PAR_3_MIN = 100

PAR_4_MAX = 450
PAR_4_MIN = 280

PAR_5_MAX = 580
PAR_5_MIN = 450

data = []
distances = []
clubs = []
lies = []

randClub = 0
strokes = 0
totalStrokes = 0

HOLE = ['HOLE', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
        11, 12, 13, 14, 15, 16, 17, 18]

PAR = ['PAR'] 
PARS = [3, 3, 3, 3, 
       4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
       5, 5, 5, 5]

YARDAGE = ['YARDAGE']
STROKES = ['STROKES']

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

# added HOLE and PAR lists to the main data list
data.extend([HOLE, PAR, YARDAGE, STROKES, 
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

# simulate golf game for all 18 holes
for i in range(18):
    
    if PARS[i] == 3:
        yardage = int(random.randint(PAR_3_MIN, PAR_3_MAX))
    if PARS[i] == 4:
        yardage = int(random.randint(PAR_4_MIN, PAR_4_MAX))
    if PARS[i] == 5:
        yardage = int(random.randint(PAR_5_MIN, PAR_5_MAX))

    dist2Go = yardage
    YARDAGE.append(yardage) 
    
    while dist2Go > 15:
        
        if dist2Go > 240 and strokes == 0:
            randClub = 0
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub] + 5)
        elif dist2Go > 200:
            randClub = random.randint(1, 2)
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub] + 5)
        elif 200 >= dist2Go > 180:
            randClub = int(random.randint(3, 4))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub] + 5)
        elif 180 >= dist2Go > 150:
            randClub = int(random.randint(5, 6))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub] + 5)
        elif 150 >= dist2Go > 120:
            randClub = int(random.randint(7, 8))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub] + 5)
        elif 120 >= dist2Go > 90:
            randClub = int(random.randint(9, 10))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub] + 5)
        elif 90 >= dist2Go > 50:
            randClub = int(random.randint(11, 12))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 5, CLUB_DISTS[randClub] + 5)
        else:
            randClub = int(random.randint(11, 12))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 5, CLUB_DISTS[randClub] + 5)

        if dist2Go - strokeDist < 0:
            overShot = dist2Go - strokeDist

            strokeDist -= random.randint( -1 * overShot + 1, -1 * overShot + 10) 

        clubs.append(CLUBS[randClub])

        if strokes == 0:
            randLie = 0
            lies.append(LIES[randLie])
        else:
            randLie = int(random.randint(1, len(LIES) - 1))
            lies.append(LIES[randLie])
                      
        distances.append(strokeDist)

        dist2Go -=  strokeDist
        strokes += 1
        
    while dist2Go > 0:

        clubs.append(CLUBS[13])
        lies.append(LIES[10])

        if dist2Go >= 10:
            puttDist = dist2Go - random.randint(1, 3)
        elif dist2Go > 3:
            puttDist = dist2Go - random.randint(0, 2)
        else:
            puttDist = dist2Go

        distances.append(puttDist)

        dist2Go -= puttDist
        strokes += 1
    
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

    STROKES.append(strokes)

    totalStrokes += strokes
    
    print("PAR:", PARS[i],"STROKES:", strokes,"YARDAGE:", yardage)
    
    strokes = 0

    distances.clear()
    clubs.clear()
    lies.clear()

# format, print and save data into a .csv file
df = pd.DataFrame(data)
print(df)

df.to_csv('golf_stats_handicap20.csv', index=False)

print("TOTAL PAR: 72", "TOTAL STROKES: ", totalStrokes)



