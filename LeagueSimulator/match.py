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
    
    def __init__(self,team1,team2,verbose=False,teamDeltaFactor = 3):
        self.team1 = team1
        self.team2 = team2
        self.verbose = verbose
        self.goals = [0,0]
        self.minuteCounter = 0
        self.teamDeltaFactor = teamDeltaFactor
        
        self.goalChance1 = int(round(self.team1.form - self.teamDeltaFactor*(team1.attack / team2.defence) + random.randint(-2,2) - 2)) #) 
        self.goalChance2 = int(round(self.team2.form - self.teamDeltaFactor*(team2.attack / team1.defence) + random.randint(-2,2)))#- self.teamDeltaFactor*(team2.attack - team1.defence))) 
        if self.team1.loseStreak > 5:
            self.goalChance1 -= 1
        if self.team2.loseStreak > 5:
            self.goalChance2 -= 1
        
        self.yellowChance = random.randint(30,80)
        self.redChance = random.randint(1,5)
        self.cards1 = [0] * 11
        self.cards2 = [0] * 11
        self.matchLoop()
    
    def scoreGoal(self,index):
        self.goals[index] += 1
        self.team1.increaseGoals(index)
        self.team2.increaseGoals(1 - index)
        if index == 0:
            playerIndex = np.random.choice(range(11),1,self.team1.goalProbabilities)[0]
            while self.cards1[playerIndex] > 1:
                playerIndex = np.random.choice(range(11),1,self.team1.goalProbabilities)[0]
            self.team1.players[playerIndex].scoreGoal()
            if self.verbose:
                print(f"GOAL! {self.team1.name} {self.team1.players[playerIndex].name}")
        elif index == 1:
            playerIndex = np.random.choice(range(11),1,p=self.team2.goalProbabilities)[0]
            while self.cards2[playerIndex] > 1:
                playerIndex = np.random.choice(range(11),1,p=self.team2.goalProbabilities)[0]
            self.team2.players[playerIndex].scoreGoal()
            if self.verbose:
                print(f"GOAL! {self.team2.name} {self.team2.players[playerIndex].name}")
        if self.verbose:
            print("")
            time.sleep(1.5)
    
    def giveCard(self,teamIndex):
        playerIndex = random.randint(0,10)
        if teamIndex == 0:
            self.cards1[playerIndex] += 1
            if self.cards1[playerIndex] > 1:
                if self.verbose:
                    print(f"RED CARD! {self.team1.name} {self.team1.players[playerIndex].name}")
                self.goalChance1 += 6
                self.goalChance2 -= 6
            else:
                if self.verbose:
                    print(f"YELLOW CARD! {self.team1.name} {self.team1.players[playerIndex].name}")
        else:
            self.cards2[playerIndex] += 1
            if self.cards2[playerIndex] > 1:
                if self.verbose:
                    print(f"RED CARD! {self.team2.name} {self.team2.players[playerIndex].name}")
                self.goalChance2 += 6
                self.goalChance1 -= 6
            else:
                if self.verbose:
                    print(f"YELLOW CARD! {self.team2.name} {self.team2.players[playerIndex].name}")
        if self.verbose:
            print("")
            time.sleep(1.5)
    
    def matchLoop(self):
        while self.minuteCounter <= 90:
            # Check for goal scored
            if random.randint(0,1) == 0:
                if random.randint(0,self.goalChance1) == 0:
                    self.scoreGoal(0)
            else:
                if random.randint(0,self.goalChance2) == 0:
                    self.scoreGoal(1)
            # Check for card
            if random.randint(0,self.yellowChance) == 0:
                self.giveCard(random.randint(0,1))
            # Update ticker
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