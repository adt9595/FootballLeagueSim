# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 19:41:59 2019
League Simulator
    - Loads team data from text files
    - Simulates matches minute-by-minute 
    - A goal may be scored each minute, with probability based on previous finishes and recent form
    - Leagues can be run through multiple of these matches


@author: Alex
"""
import numpy as np
import pygame
import math
import sys
import random
import time
from itertools import permutations

#pygame.init()
#pygame.font.init()
#gameFont = pygame.font.SysFont('Arial', 22)
#titleFont = pygame.font.Font('freesansbold.ttf',72)
#endFont = pygame.font.Font('freesansbold.ttf',60)
#clock = pygame.time.Clock()
#screen_size = 480
#grey = (184,184,184)
#black = (0,0,0)
#background = (255,255,174)
#tagColour =  (255, 238, 71)


### Helper functions ################################

def weightedSum(x,factor):
    total = 0
    for i in range(1,len(x)):
        total += x[i-1] * (factor/i)
    return total
        
def mean(x):
    avg = 0
    for i in range(len(x)):
        avg = avg + x[i]
    avg = avg / len(x)
    return avg

def stddev(x):
    ans = 0
    avg = mean(x)
    for i in range(len(x)):
        ans = ans + (x[i] - avg)*(x[i] - avg)
    ans = ans / (len(x) - 1)
    return math.sqrt(ans)

def listProduct(x,y):
    return sum(i[0]*i[1] for i in zip(x,y))

#####################################################

#class Game:
#    def __init__(self):
#        screen = pygame.display.set_mode((screen_size, screen_size))
#        running = True
#        while(running):
#            self.draw(screen)
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    running = False
#                    pygame.display.quit()
#                    pygame.quit()
#                    sys.exit(0)
#                  
#    def draw(self,screen):
#        screen.fill(background)
#        title = titleFont.render('FOOTY',False,black)
#        screen.blit(title,(screen_size/2 - 150,screen_size/2 - 50))
#        pygame.display.update()
        

class League:
    """
    Stores league information
    name - String, name of league
    teams - Array, list of teams
    numIterations - Int, number of iterations to run
    """
    def __init__(self,name,teams,numIterations):
        self.name = name
        self.teams = teams
        self.numTeams = len(teams)
        self.gamesPlayed = 0    
        self.schedule = list(permutations([i for i in range(self.numTeams)],2))
        self.numIterations = numIterations
        if numIterations == 1:
            self.verbose = True
        else:
            self.verbose = False
        self.leagueLoop()
        

    def reset(self):
        self.gamesPlayed = 0
        for team in self.teams:
            team.reset()
        
    def getTable(self):
        self.sortTeams()
        if(self.verbose):
            table = "{0:3}|{1:2}|{2:2}|{3:2}|{4:2}|{5:2}|{6:2}|{7:2}|{8:2}"
            print("League Table:")
            print(table.format("Pos ","Pl","W","D","L","GF","GA","GD","Pts"))
            for i in range(len(self.teams)):
                tm = self.teams[i]
                results = tm.getResults()
                goals = tm.getGoals()
                row = (str(i+1),str(self.gamesPlayed),str(results[0]),str(results[1]),str(results[2]),
                       str(goals[0]),str(goals[1]),str(goals[0]-goals[1]),str(tm.getPoints()))
                if i == 4 or i == 17: print("-----------------------------")
                print(tm.getName(),table.format(*row))
        

            
    def playMatch(self,team1,team2):
        Match(team1,team2,False)
        #self.getTable()
    
    def sortTeams(self):
        self.teams = sorted(self.teams,key=lambda x: x.getPoints(), reverse = True)
        
    def leagueLoop(self):
        avg = 0
        dev = 0
        mostPoints = 0
        winningPoints = []
        
        # Run numIterations times
        for i in range(self.numIterations):
            for fixture in self.schedule:
                if fixture[0] == fixture[1]:
                    continue
                else:
                    self.playMatch(self.teams[fixture[0]],self.teams[fixture[1]])
                    self.gamesPlayed += 1
            self.gamesPlayed = 2 * self.numTeams - 2 
            self.getTable()
            winner = self.teams[0].getPoints()
            winningPoints.append(winner)
            if winner > mostPoints:
                mostPoints = winner
            self.reset()
        if not self.verbose:
            print(winningPoints)
            avg = mean(winningPoints)
            dev = stddev(winningPoints)
            print("Avg:",avg)
            print("Std Dev:",dev)
            print("Most points:",mostPoints)
    
class Team:
    """
    Stores team information
    name - String, name of team
    players - Array, list of players
    """
    def __init__(self,path):
        self.name = None
        self.players = []
        self.previousFinishes = []
        
        self.reset()
        self.loadData(path)
        self.setGoalProbabilities()
        
    def setGoalProbabilities(self):
        self.goalProbabilities = [player.goalProbability for player in self.players]
        self.totalProbabilities = sum(self.goalProbabilities)
        self.goalProbabilities = [player.goalProbability / self.totalProbabilities for player in self.players]
    
    def reset(self):
        self.points = 0
        self.goals = [0,0]
        self.results = [0,0,0]
        self.goalDifference = 0
        self.setForm()
    
    def getName(self):
        return self.name
    
    def getForm(self):
        return self.form
    
    def getGoals(self):
        return self.goals
    
    def getPlayers(self):
        return self.players
    
    def getPoints(self):
        return self.points
    
    def getResults(self):
        return self.results
    
    def setName(self,name):
        self.name = name
        
    def setForm(self):
        self.form = 30 + int(round((weightedSum(self.previousFinishes,0.5) / weightedSum([20,20,20,20,20],0.5))*70))
    
    def setResult(self,index):
        if index == 0:
            self.results[0] += 1
            self.points += 3
            if self.form > 35:
                self.form -= random.randint(1,4)
        elif index == 1:
            self.results[1] += 1
            self.points += 1
            if self.form < 35: 
                self.form -= random.randint(-2,1)
            elif self.form >= 35 and self.form < 50 :
                self.form -= random.randint(-1,2)
            elif self.form >= 50 and self.form < 65 :
                self.form -= random.randint(0,4)
            elif self.form >= 65:
                self.form -= random.randint(0,3)
        elif index == 2:
            self.results[2] += 1
            if self.form < 65:
                self.form += random.randint(1,4)
    
    def increaseGoals(self,index):
        if(index < len(self.goals)):
            self.goals[index] += 1
            self.goalDifference = self.goals[0] - self.goals[1]
    
    def loadData(self,path):
        # Data format:
        # TeamName
        # Form
        # Player1
        # ...
        # Player11
        teamData = open(path,'r')
        
        self.setName(teamData.readline())
        tempData = teamData.readline().split(",")
        self.previousFinishes = [int(x) for x in tempData]
        self.setForm()
        
        for i in range(1,12):
            tempData = teamData.readline()
            tempData = tempData.split(",")
            
            playerName = tempData[0]
            playerPosition = tempData[1]
            playerAttributes = tempData[2].replace('\n','')
            
            self.players.append(Player(playerName,playerPosition,playerAttributes))
        teamData.close()
                 
    
class Player:
    """
    Stores player information
    name - String, name of player
    position - String, position of player
    attributes - Array, list of attributes 
                (defending,passing,shooting) / (stopping, reactions, kicking)
    """
    def __init__(self,name,position,attributes):
        self.name = name
        self.position = position
        self.attributes = self.formatAttributes(attributes)

        if self.position == "GK":
            self.goalProbability = 0.0000001
        else:
            self.goalProbability = self.attributes[2] * positionMultipliers[self.position][2]
        self.overallRating = 0
        self.reset()
    
    def reset(self):
        self.goals = 0
        self.setRating()
    
    def formatAttributes(self,attributes):
        attributes = attributes.split(' ')
        for i in range(len(attributes)):
            attributes[i] = int(attributes[i])
        return attributes
    
    def setRating(self):
        multiplier = positionMultipliers[self.position] 
        self.overallRating = listProduct(multiplier,self.attributes)        
    
    def scoreGoal(self):
        self.goals += 1
    
    def getName(self):
        return self.name
    
    def getPosition(self):
        return self.position
        

        
class Match:
    """
    Handles match logic
    team1 - Team, home team
    team2 - Team, away team
    """
    def __init__(self,team1,team2,verbose):
        self.team1 = team1
        self.team2 = team2
        self.verbose = verbose
        self.goals = [0,0]
        self.minuteCounter = 0
        self.goalChance1 = self.team1.getForm()
        self.goalChance2 = self.team2.getForm()
        if self.verbose:
            print(self.team1.goalProbabilities)
        self.matchLoop()
    
    def scoreGoal(self,index):
        self.goals[index] += 1
        self.team1.increaseGoals(index)
        self.team2.increaseGoals(1 - index)
        if index == 0:
            playerIndex = np.random.choice(list(range(11)),1,self.team1.goalProbabilities)[0]
            if self.verbose:
                print("GOAL! " + self.team1.getName() + "" + self.team1.players[playerIndex].getName())
        elif index == 1:
            playerIndex = np.random.choice(list(range(11)),1,self.team2.goalProbabilities)[0]
            if self.verbose:
                print("GOAL! " + self.team2.getName() + "" + self.team2.players[playerIndex].getName())
        if self.verbose:
            print("")
            time.sleep(1.5)
                
        
        
    
    def matchLoop(self):
        while self.minuteCounter <= 90:
            
            if random.randint(0,self.goalChance1) == 0:
                self.scoreGoal(0)
            if random.randint(0,self.goalChance2) == 1:
                self.scoreGoal(1)
            if self.verbose:    
                print(str(self.minuteCounter) + ': ' + self.team1.getName() + " " 
                      + str(self.goals[0]) + ' - '  + str(self.goals[1]) + " " + self.team2.getName())
                time.sleep(0.08)
            self.minuteCounter += 1
        
        if self.goals[0] > self.goals[1]:
            self.team1.setResult(0)
            self.team2.setResult(2)
        elif self.goals[0] < self.goals[1]:
            self.team1.setResult(2)
            self.team2.setResult(0)
        else:
            self.team1.setResult(1)
            self.team2.setResult(1)
            
positionMultipliers = {
    "GK": [1.0,1.0,1.0],
    "RB": [1.3,1.2,0.5],
    "LB": [1.3,1.2,0.5],
    "CB": [1.7,1.0,0.3],
    "CDM": [1.4,1.1,0.6],
    "CM": [0.6,1.7,0.7],
    "RM": [0.5,1.3,1.2],
    "LM": [0.5,1.3,1.2],
    "RW" : [0.3,1.2,1.5],
    "LW" : [0.3,1.2,1.5],
    "CAM" : [0.3,1.4,1.3],
    "ST" : [0.3,1.0,1.7]
}

teams = []
for i in range(20):
    teams.append(Team('teamdata/team{0}.txt'.format(i)))

prem = League('Premier League',teams,numIterations=40)
#testgame = Match(teams[0],teams[1],verbose=True)

"""
REAL STATS:
    Champion points avg: 87.074
    Champion points dev: 6.063
"""
