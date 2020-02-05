# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 17:18:35 2020
@author: Alex Taylor

Stores team information
name - String, name of team
players - Array, list of players
"""

import random
from player import Player

### Helper functions ################################

def fileLen(fname):
    with open(fname) as f:
        for x, y in enumerate(f):
            pass
    return x + 1

def weightedSum(x,factor):
    total = 0
    for i in range(1,len(x)):
        total += x[i-1] * (factor/i)
    return total

#####################################################

class Team:

    def __init__(self,path=None):
        self.name = None
        self.players = []
        self.substitutes = []
        self.previousFinishes = []
        if(path):
            self.loadData(path)
        else:
            self.createData()
            print("Players: ")
            for i in range(11):
                print(self.players[i].name)
        self.initialAttack = sum([player.attributes[2] for player in self.players])
        self.initialDefence = sum([player.attributes[0] for player in self.players])
        self.reset()  
        self.setForm()
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
        
        self.topScorer = None
        self.topWinStreak = 0
        self.topUnbeatenStreak = 0
        self.topLoseStreak = 0
        self.unbeatenStreak = 0
        self.winStreak = 0
        self.loseStreak = 0
        
        self.baseForm = 22
        self.formLimitUpper = self.baseForm + 25
        self.formLimitLower = self.baseForm - 4
        
        self.attack = self.initialAttack
        self.defence = self.initialDefence

    
    
    def setName(self,name):
        self.name = name
        
    def setForm(self):
        prevForm = int(round((weightedSum(self.previousFinishes,0.5) / weightedSum([20,20,20,20,20],0.5))))
        previousFinishFactor = 25
        
        self.form = self.baseForm + (previousFinishFactor * prevForm)
    
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
            if self.form > self.formLimitLower and self.form < (self.formLimitLower + self.formLimitUpper)//2 :
                self.form += random.randint(-2,-1)
            elif self.form >= (self.formLimitLower + self.formLimitUpper)//2 and self.form < self.formLimitUpper :
                self.form += random.randint(-3,-1)
            elif self.form >= self.formLimitUpper:
                self.form += random.randint(-4,-2)
            
            
        # draw
        elif index == 1:
            self.winStreak = 0
            self.unbeatenStreak += 1
            if self.unbeatenStreak > self.topUnbeatenStreak:
                self.topUnbeatenStreak = self.unbeatenStreak
                
            self.results[1] += 1
            self.points += 1
            if self.form < self.formLimitLower: 
                self.form += random.randint(1,2)
            elif self.form >= self.formLimitLower and self.form < (self.formLimitLower + self.formLimitUpper)//2 :
                self.form += random.randint(-1,1)
            elif self.form >= (self.formLimitLower + self.formLimitUpper)//2 and self.form <= self.formLimitUpper :
                self.form += random.randint(-2,0)
            elif self.form > self.formLimitUpper:
                self.form += random.randint(-2,-1)
        # loss
        elif index == 2:
            self.winStreak = 0
            self.unbeatenStreak = 0
            self.loseStreak += 1
            if self.loseStreak > self.topLoseStreak:
                self.topLoseStreak = self.loseStreak
            self.results[2] += 1
            if self.form <= self.formLimitLower: 
                self.form += random.randint(2,3)
            elif self.form > self.formLimitLower and self.form < (self.formLimitLower + self.formLimitUpper)//2 :
                self.form += random.randint(1,3)
            elif self.form >= (self.formLimitLower + self.formLimitUpper)/2 and self.form < self.formLimitUpper :
                self.form += random.randint(1,2)


                
        self.changePlayerStats(index)
        self.topScorer = max([player.goals for player in self.players])
        self.attack = sum([player.attributes[2] for player in self.players])
        self.defence = sum([player.attributes[0] for player in self.players])
        self.setGoalProbabilities()
        
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
        with open(path,'r') as teamData:
            self.setName(teamData.readline())
            tempData = teamData.readline().split(",")
            self.previousFinishes = [int(x) for x in tempData]
            
            for i in range(1,12):
                tempData = teamData.readline()
                tempData = tempData.split(",")
                
                playerName = tempData[0]
                playerPosition = tempData[1]
                playerAttributes = tempData[2].replace('\n','')
                
                self.players.append(Player(playerName,playerPosition,playerAttributes))
        
    def createData(self):
        self.setName(input("Enter team name: ") + "\n")
        self.previousFinishes = [10,10,10,10,10]
        self.setForm()
        numForenames = fileLen('FirstNames.txt')
        numSurnames = fileLen('LastNames.txt')
        for i in range(1,12):
            with open('FirstNames.txt','r') as forenames, \
             open('LastNames.txt','r') as surnames:
                # Generate player name & position
                forenameIndex = random.randint(0,numForenames)
                surnameIndex = random.randint(0,numSurnames)
                for j in range(0,forenameIndex):
                    forename = forenames.readline()
                for j in range(0,surnameIndex):
                    surname = surnames.readline()
                f = list(forename)
                s = list(surname)
                f[0] = forename[0].capitalize()
                s[0] = surname[0].capitalize()
                forename = "".join(f)
                surname = "".join(s)
                #playerName = f + [" "] + s
                playerName = forename + " " + surname
                playerPosition = standardPositions[i]
            
            # Generate player attributes
            tempAttributes = []
            multipliers = positionMultipliers[playerPosition]
            for j in range(3):
                if multipliers[j] > 1.0:
                    stat = 30 + (multipliers[j] - 0.1)*random.randint(28,43)
                    tempAttributes.append(stat)
                elif multipliers[j] < 1.0:
                    stat = 30 + (multipliers[j] + 0.1)*random.randint(28,43)
                    tempAttributes.append(stat)
                else:
                    stat = 30 + multipliers[j]*random.randint(28,43)
                    tempAttributes.append(stat)
            playerAttributes = str(tempAttributes[0]) + " " + str(tempAttributes[1]) + " " + str(tempAttributes[2])
            
            self.players.append(Player(playerName,playerPosition,playerAttributes))
                
# Attribute multipliers based on position
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

# Position enumeration for team generation
standardPositions = {
    1: "GK",
    2: "RB",
    3: "CB",
    4: "CB",
    5: "LB",
    6: "RM",
    7: "CM",
    8: "CM",
    9: "LM",
    10: "ST",
    11: "ST"
}
