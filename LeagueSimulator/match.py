# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 17:16:20 2020
@author: Alex Taylor

Handles match logic
team1 - Team, home team
team2 - Team, away team
verbose - Boolean, ...
teamDeltaFactor - Float, ...

TO DO:
    Yellow/Red cards
    Substitutions
"""   

import numpy as np
import random
import time

class Match:
    
    def __init__(self,team1,team2,verbose=False,teamDeltaFactor = 2.5):
        self.teams = [team1,team2]
        self.verbose = verbose
        self.goals = [0,0]
        self.minuteCounter = 0
        self.teamDeltaFactor = teamDeltaFactor
        # Calculate probability of scoring a goal based on form and team + player stats
        self.goalChance = [int(round(self.teams[0].form - self.teamDeltaFactor*(self.teams[0].attack / self.teams[1].defence) + random.randint(-2,2) - 2)),\
                           int(round(self.teams[1].form - self.teamDeltaFactor*(self.teams[1].attack / self.teams[0].defence) + random.randint(-2,2)))]
        # Attempt to break from lose streaks
        for i in range(2):
            if self.teams[i].loseStreak > 5:
                self.goalChance[i] -= 1
            self.goalChance[i] = max(self.goalChance[i],2)
        self.yellowChance = random.randint(40,80)
        self.redChance = random.randint(1,5)
        self.cards=[[0]*11,[0]*11]
        self.suspendedPlayers = [[],[]]
        self.matchLoop()
    
    def scoreGoal(self,teamIndex):
        self.goals[teamIndex] += 1
        self.teams[0].increaseGoals(teamIndex)
        self.teams[1].increaseGoals(1 - teamIndex)
        playerIndex = np.random.choice(range(11),1,self.teams[teamIndex].goalProbabilities)[0]
        while self.cards[teamIndex][playerIndex] > 1:
            playerIndex = random.randint(1,10)
        self.teams[teamIndex].players[playerIndex].scoreGoal()
        if self.verbose:
            print(f"GOAL! {self.team[teamIndex].name} {self.teams[teamIndex].players[playerIndex].name}")
        if self.verbose:
            print("")
            time.sleep(1.5)
    
    def giveCard(self,teamIndex):
        playerIndex = random.randint(0,10)
        while playerIndex in self.suspendedPlayers[teamIndex]:
            playerIndex = random.randint(0,10)
        self.cards[teamIndex][playerIndex] += 1
        if self.cards[teamIndex][playerIndex] > 1:
            self.suspendedPlayers[teamIndex].append(playerIndex)
            if self.verbose:
                print(f"RED CARD! {self.teams[teamIndex].name} {self.teams[teamIndex].players[playerIndex].name}")
            self.goalChance[teamIndex] += 3
            self.goalChance[1-teamIndex] -= 3
            self.goalChance[1-teamIndex] = max(self.goalChance[1-teamIndex],2)
        else:
            if self.verbose:
                print(f"YELLOW CARD! {self.teams[teamIndex].name} {self.teams[teamIndex].players[playerIndex].name}")
        if self.verbose:
            print("")
            time.sleep(1.5)
    
    def matchLoop(self):
        while self.minuteCounter <= 90:
            # Check for goal scored
            if random.randint(0,1) == 0:
                if random.randint(0,self.goalChance[0]) == 0:
                    self.scoreGoal(0)
            else:
                if random.randint(0,self.goalChance[1]) == 0:
                    self.scoreGoal(1)
            # Check for card
            if random.randint(0,self.yellowChance) == 0:
                self.giveCard(random.randint(0,1))
            # Update ticker
            if self.verbose:    
                print(str(self.minuteCounter) + ': ' + self.teams[0].name + " " 
                      + str(self.goals[0]) + ' - '  + str(self.goals[1]) + " " + self.teams[1].name)
                time.sleep(0.08)
            self.minuteCounter += 1
        if self.goals[0] > self.goals[1]:
            self.teams[0].setResult(0)
            self.teams[1].setResult(2)
        elif self.goals[0] < self.goals[1]:
            self.teams[0].setResult(2)
            self.teams[1].setResult(0)
        else:
            self.teams[0].setResult(1)
            self.teams[1].setResult(1)