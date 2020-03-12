# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 17:12:11 2020

@author: Alex

Column indexes:
    3 - Name
    4 - Age
    8 - Nationality
    9 - Club
    14 - Positions
    31 - Pace
    32 - Shooting
    33 - Passing
    34 - Dribbling
    35 - Defending
    36 - Physicality
    37 - GK Diving
    38 - GK Handling
    39 - GK Kicking
    40 - GK Reflexes
    41 - GK Speed
    42 - GK Position
"""

prem = ["Arsenal","Burnley","Manchester United","Manchester City","Wolverhampton Wanderers","Watford",\
 "Tottenham Hotspur","Chelsea","Liverpool","Everton","Brighton & Hove Albion","Leicester City",\
 "Bournemouth","Southampton","Newcastle United","West Ham United","Sheffield United",\
 "Crystal Palace","Aston Villa","Norwich City"]

import csv

def get_team(name):
    players = []
    with open('players_20.csv','r',encoding='utf-8') as stats:
        csv_reader = csv.reader(stats,delimiter=',')
        #print(type(csv_reader[0]))
        for line in csv_reader:
            if(line[9] == name):
                if(line[14] == "GK"):
                    players.append([line[3],line[4],line[8],line[9],line[37],line[38],line[39],line[40],line[41],line[42]])
                else:
                    players.append([line[3],line[4],line[8],line[9],line[31],line[32],line[33],line[34],line[35],line[36]])
    return players
                
def write_team(name,team):
    with open(f'{name}.txt','w+',encoding='utf-8') as players:
        for i in range(len(team)):
            for j in range(len(team[0])-1):
                players.write(team[i][j]+',')
            players.write(team[i][len(team[0])-1])
            players.write('\n')

i=0
for team in prem:
    write_team(f'team{i}',get_team(team))
    i += 1

    