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
import matplotlib.pyplot as plt
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

def plotFigure(data,stepsize):
    steps = [stepsize*i for i in range(25)]
    plt.plot(steps,data)
    plt.plot((0,stepsize*25),(87.074,87.074))
    plt.axis([0, stepsize*25, min(data), max(data)])
    plt.show()


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
    def __init__(self,name,teams,teamDeltaFactor,numIterations):
        self.name = name
        self.teams = teams
        self.numTeams = len(teams)
        self.gamesPlayed = 0    
        self.teamDeltaFactor = teamDeltaFactor
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
            print(self.name + " Table:")
            print(table.format("Pos ","Pl","W","D","L","GF","GA","GD","Pts"))
            for i in range(len(self.teams)):
                tm = self.teams[i]
                results = tm.results
                goals = tm.goals
                row = (str(i+1),str(self.gamesPlayed),str(results[0]),str(results[1]),str(results[2]),
                       str(goals[0]),str(goals[1]),str(goals[0]-goals[1]),str(tm.points))
                if i == 4 or i == 17: print("-----------------------------")
                print(tm.name,table.format(*row))
        

            
    def playMatch(self,team1,team2):
        Match(team1,team2,self.teamDeltaFactor,False)
    
    def sortTeams(self):
        self.teams = sorted(self.teams,key=lambda x: x.points, reverse = True)
        
    def leagueLoop(self):
        self.avg = 0
        self.dev = 0
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
            
            winner = self.teams[0].points
            winningPoints.append(winner)
            winStreak = max([team.topWinStreak for team in teams])
            unbeatenStreak = max([team.topUnbeatenStreak for team in teams])
            loseStreak = max([team.topLoseStreak for team in teams])
            if self.verbose:
                print("Longest win streak: " + str(winStreak))
                print("Longest unbeaten streak: " + str(unbeatenStreak))
                print("Longest lose streak: " + str(loseStreak))
            
            if winner > mostPoints:
                mostPoints = winner
                
            self.reset()
            
        if not self.verbose:
            #print(winningPoints)
            self.avg = mean(winningPoints)
            self.dev = stddev(winningPoints)
            #print("Avg:",self.avg)
            #print("Std Dev:",self.dev)
            #print("Most points:",mostPoints)
            print("Iteration Complete")
    
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
        self.attack = sum([player.attributes[2] for player in self.players])
        self.defence = sum([player.attributes[0] for player in self.players])
        
    def setGoalProbabilities(self):
        self.goalProbabilities = [player.goalProbability for player in self.players]
        self.totalProbabilities = sum(self.goalProbabilities)
        self.goalProbabilities = [player.goalProbability / self.totalProbabilities for player in self.players]
    
    def reset(self):
        self.points = 0
        self.goals = [0,0]
        self.results = [0,0,0]
        self.goalDifference = 0
        self.topScorer = None
        self.topWinStreak = 0
        self.topUnbeatenStreak = 0
        self.topLoseStreak = 0
        self.unbeatenStreak = 0
        self.winStreak = 0
        self.loseStreak = 0
        self.formLimitUpper = 55
        self.formLimitLower = 30
        
        
        self.setForm()
    
    
    def setName(self,name):
        self.name = name
        
    def setForm(self):
        baseForm = 35
        prevForm = int(round((weightedSum(self.previousFinishes,0.5) / weightedSum([20,20,20,20,20],0.5))))
        previousFinishFactor = 18
        
        self.form = baseForm + previousFinishFactor*prevForm
    
    def setResult(self,index):
        # win
        if index == 0:
            self.winStreak += 1
            self.unbeatenStreak += 1
            if self.winStreak > self.topWinStreak:
                self.topWinStreak = self.winStreak
            if self.unbeatenStreak > self.topUnbeatenStreak:
                self.topUnbeatenStreak = self.unbeatenStreak
                
            self.results[0] += 1
            self.points += 3
            if self.form > self.formLimitLower:
                self.form -= random.randint(1,3)
        # draw
        elif index == 1:
            self.winStreak = 0
            self.unbeatenStreak += 1
            if self.unbeatenStreak > self.topUnbeatenStreak:
                self.topUnbeatenStreak = self.unbeatenStreak
                
            self.results[1] += 1
            self.points += 1
            if self.form < self.formLimitLower: 
                self.form -= random.randint(-2,1)
            elif self.form >= self.formLimitLower and self.form < 50 :
                self.form -= random.randint(-1,2)
            elif self.form >= 50 and self.form < self.formLimitUpper :
                self.form -= random.randint(0,3)
            elif self.form >= self.formLimitUpper:
                self.form -= random.randint(0,3)
        # loss
        elif index == 2:
            self.winStreak = 0
            self.unbeatenStreak = 0
            self.loseStreak += 1
            if self.loseStreak > self.topLoseStreak:
                self.topLoseStreak = self.loseStreak
            self.results[2] += 1
            if self.form < self.formLimitUpper:
                self.form += random.randint(1,3)
        self.changePlayerStats(index)
        self.topScorer = max([player.goals for player in self.players])
        self.attack
        
    def increaseGoals(self,index):
        if(index < len(self.goals)):
            self.goals[index] += 1
            self.goalDifference = self.goals[0] - self.goals[1]
    
    def changePlayerStats(self,index):
        # win
        if index == 0:
            for i in range(3):
                playerIndex = random.randint(0,10)
                statIndex = random.randint(0,2)
                tst = self.players[playerIndex]
                tst.attributes[statIndex] += 1
        # draw
        elif index == 1:
            playerIndex = random.randint(0,10)
            statIndex = random.randint(0,2)
            self.players[playerIndex].attributes[statIndex] += 1
            playerIndex = random.randint(0,10)
            statIndex = random.randint(0,2)
            self.players[playerIndex].attributes[statIndex] -= 1
        # loss
        elif index == 2:
            for i in range(3):
                playerIndex = random.randint(0,10)
                statIndex = random.randint(0,2)
                self.players[playerIndex].attributes[statIndex] -= 1
                
        
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
        #adjustedAttributes = []
        for i in range(len(attributes)):
            attributes[i] = float(attributes[i]) * positionMultipliers[self.position][i]
        return attributes
    
    def setRating(self):
        self.overallRating = sum(self.attributes)     
    
    def scoreGoal(self):
        self.goals += 1
    
        

        
class Match:
    """
    Handles match logic
    team1 - Team, home team
    team2 - Team, away team
    """
    def __init__(self,team1,team2,teamDeltaFactor,verbose):
        self.team1 = team1
        self.team2 = team2
        self.verbose = verbose
        self.goals = [0,0]
        self.minuteCounter = 0
        self.teamDeltaFactor = teamDeltaFactor
        self.goalChance1 = int(round(self.team1.form - self.teamDeltaFactor*(team1.attack - team2.defence)))
        self.goalChance2 = int(round(self.team2.form - self.teamDeltaFactor*(team2.attack - team1.defence)))
        if self.verbose:
            print(self.team1.goalProbabilities)
        self.matchLoop()
    
    def scoreGoal(self,index):
        self.goals[index] += 1
        self.team1.increaseGoals(index)
        self.team2.increaseGoals(1 - index)
        if index == 0:
            playerIndex = np.random.choice(list(range(11)),1,self.team1.goalProbabilities)[0]
            self.team1.players[playerIndex].scoreGoal()
            if self.verbose:
                print("GOAL! " + self.team1.name + "" + self.team1.players[playerIndex].name)
        elif index == 1:
            playerIndex = np.random.choice(list(range(11)),1,self.team2.goalProbabilities)[0]
            self.team2.players[playerIndex].scoreGoal()
            if self.verbose:
                print("GOAL! " + self.team2.name + "" + self.team2.players[playerIndex].name)
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
                print(str(self.minuteCounter) + ': ' + self.team1.name + " " 
                      + str(self.goals[0]) + ' - '  + str(self.goals[1]) + " " + self.team2.name)
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
    "RM": [0.5,1.4,1.2],
    "LM": [0.5,1.4,1.2],
    "RW" : [0.3,1.2,1.5],
    "LW" : [0.3,1.2,1.5],
    "CAM" : [0.3,1.4,1.3],
    "ST" : [0.3,1.0,1.7]
}

teams = []
averages = []
stepsize = 0.004

# Populate league
for i in range(20):
    teams.append(Team('teamdata/team{0}.txt'.format(i)))

# Run multiple leagues with varying team rating parameters
for i in range(25):
    prem = League('Premier League',teams,0.0 + (stepsize * i),numIterations=100)
    averages.append(prem.avg)
plotFigure(averages,stepsize)
    
#testgame = Match(teams[0],teams[1],verbose=True)


"""
REAL STATS:
    Champion points avg: 87.074
    Champion points dev: 6.063
"""
