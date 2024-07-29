import pandas as pd
import random 

CLUBS = ["DRIVER", "3 Wood", "5 Wood", "4 Iron", "5 Iron", "6 Iron", "7 Iron", "8 Iron", "9 Iron", "P Wedge", "G Wedge", "S Wedge", "L Wedge", "Putter"]
CLUB_DISTS = [240, 200, 180, 175, 170, 160, 150, 140, 130, 100, 85, 70, 25, 15]
LIES = ["TEE BOX", "FAIRWAY", "FAIRWAY", "FAIRWAY", "FAIRWAY", "ROUGH", "ROUGH", "ROUGH", "BUNKER", "OTHER/HAZARD", "GREEN"]

PAR_3_MAX = 240
PAR_3_MIN = 100

PAR_4_MAX = 450
PAR_4_MIN = 240

PAR_5_MAX = 580
PAR_5_MIN = 450

PAR_3_PUTTS = [1, 1, 1, 1, 2, 2, 2, 2, 2, 3]
PAR_4_PUTTS = [1, 1, 1, 2, 2, 2, 2, 2, 3, 3]
PAR_5_PUTTS = [1, 1, 2, 2, 2, 2, 2, 3, 3, 3]

PAR_3_STROKES = [1, 1, 2, 2, 2, 2, 2, 2, 2, 3]
PAR_4_STROKES = [2, 2, 2, 3, 3, 3, 3, 3, 4, 4]
PAR_5_STROKES = [2, 3, 3, 4, 4, 4, 4, 4, 5, 5]

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
data.extend([HOLE, PAR, YARDAGE,
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
    
    if PARS[i] == 3:
        yardage = int(random.randint(PAR_3_MIN, PAR_3_MAX))
        #putts = int(random.choice(PAR_3_PUTTS))
        #strokes = int(random.choice(PAR_3_STROKES)) 
    
    if PARS[i] == 4:
        yardage = int(random.randint(PAR_4_MIN, PAR_4_MAX))
        #putts = int(random.choice(PAR_4_PUTTS))
        #strokes = int(random.choice(PAR_4_STROKES)) 

    if PARS[i] == 5:
        yardage = int(random.randint(PAR_5_MIN, PAR_5_MAX))
        #putts = int(random.choice(PAR_5_PUTTS))
        #strokes = int(random.choice(PAR_5_STROKES))

    dist2Go = yardage
    YARDAGE.append(yardage) 
    
    while dist2Go > 20:
        
        if dist2Go > 240:
            randClub = 0
            strokeDist = random.randint(CLUB_DISTS[randClub] - 20, CLUB_DISTS[randClub])
        elif 240 > dist2Go > 200:
            randClub = random.randint(1, 2)
            strokeDist = random.randint(CLUB_DISTS[randClub] - 20, CLUB_DISTS[randClub])
        elif 210 >= dist2Go > 180:
            randClub = int(random.randint(3, 4))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 20, CLUB_DISTS[randClub])
        elif 180 >= dist2Go > 150:
            randClub = int(random.randint(5, 6))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 20, CLUB_DISTS[randClub])
        elif 150 >= dist2Go > 120:
            randClub = int(random.randint(7, 8))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 20, CLUB_DISTS[randClub])
        elif 120 >= dist2Go > 90:
            randClub = int(random.randint(9, 10))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 10, CLUB_DISTS[randClub])
        elif 90 >= dist2Go > 50:
            randClub = int(random.randint(11, 12))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 5, CLUB_DISTS[randClub])
        else:
            randClub = int(random.randint(11, 12))
            strokeDist = random.randint(CLUB_DISTS[randClub] - 5, CLUB_DISTS[randClub])

            if dist2Go - strokeDist < 0:
                strokeDist = 20 - random.randint(5, 15) 

                clubs.append(CLUBS[randClub])
        
                randLie = int(random.randint(1, len(LIES) - 1))
                lies.append(LIES[randLie])
                            
                distances.append(strokeDist)

                dist2Go -=  strokeDist
                strokes += 1

                break

        clubs.append(CLUBS[randClub])

        randLie = int(random.randint(1, len(LIES) - 1))
        lies.append(LIES[randLie])
                      
        distances.append(strokeDist)

        dist2Go -=  strokeDist
        strokes += 1
        
    while dist2Go > 0:

        clubs.append(CLUBS[13])
        lies.append(LIES[10])

        if dist2Go > 15:
            puttDist = random.randint(15, dist2Go)
        elif 15 >= dist2Go > 6:
            puttDist = random.randint(6, dist2Go)
        else:
            puttDist = dist2Go
            distances.append(puttDist)

            dist2Go -= puttDist
            strokes += 1

            break

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

    
    totalStrokes += strokes
    
    print("PAR:", PARS[i],"STROKES:", strokes,"YARDAGE:", yardage)
    
    strokes = 0

    distances.clear()
    clubs.clear()
    lies.clear()

print("TOTAL PAR: 72", "TOTAL STROKES: ", totalStrokes)

df = pd.DataFrame(data)
print(df)

df.to_csv('golf_stats.csv', index=False)



