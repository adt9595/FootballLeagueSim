# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 17:12:07 2020
@author: Alex Taylor

Stores league information
name - String, name of league
teams - Array, list of teams
teamDeltaFactor - Float, ...
numIterations - Int, number of iterations to run
"""

import random
import math
from itertools import permutations
from match import Match

### Helper functions ################################

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

#####################################################

class League:
    def __init__(self,name,teams,teamDeltaFactor=0.055,numIterations=1):
        self.name = name
        self.teams = teams
        self.numTeams = len(teams)
        self.gamesPlayed = 0    
        self.teamDeltaFactor = teamDeltaFactor
        self.numIterations = numIterations
        self.schedule = list(permutations([i for i in range(self.numTeams)],2))
        random.shuffle(self.schedule)
        self.schedule = self.splitSchedule(self.schedule)
        if numIterations == 1:
            self.verbose = True
        else:
            self.verbose = False
        self.leagueLoop()
        

    def reset(self):
        self.gamesPlayed = 0
        for team in self.teams:
            team.reset()
    
    # Sorts schedule into unique, week-by-week fixtures
    def splitSchedule(self,fixtures):
        sortedSchedule = []
        numWeeks = (self.numTeams * 2) - 2
        for i in range(numWeeks):
            usedTeams = []
            week = []
            for fixture in self.schedule:
                if (fixture[0] in usedTeams) or (fixture[1] in usedTeams):
                    continue
                else:
                    week.append(fixture)
                    usedTeams.extend([fixture[0],fixture[1]])
                    self.schedule.remove(fixture)
            sortedSchedule.append(week)
        return sortedSchedule
    
    def getTable(self):
        self.sortTeams()
        if self.verbose:
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
        Match(team1,team2)
    
    def sortTeams(self):
        self.teams = sorted(self.teams,key=lambda x: x.points, reverse = True)
        
    def leagueLoop(self):
        self.avg = 0
        self.dev = 0
        mostPoints = 0
        winningPoints = []
        
        for i in range(self.numIterations):
            for week in range(38):
                for fixture in self.schedule[week]:
                    if fixture[0] == fixture[1]:
                        continue
                    else:
                        self.playMatch(self.teams[fixture[0]],self.teams[fixture[1]])
                        self.gamesPlayed += 1
            self.gamesPlayed = 2 * self.numTeams - 2 
            self.getTable()
            
            winner = self.teams[0].points
            winningPoints.append(winner)
            winStreak = max([team.topWinStreak for team in self.teams])
            unbeatenStreak = max([team.topUnbeatenStreak for team in self.teams])
            loseStreak = max([team.topLoseStreak for team in self.teams])
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
