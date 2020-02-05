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
    def __init__(self,name,teams,teamDeltaFactor=3,numIterations=1,verbose=True):
        self.name = name
        self.teams = teams
        self.numIterations = numIterations
        self.teamDeltaFactor = teamDeltaFactor
        self.verbose = verbose
        self.numTeams = len(self.teams)
        self.reset()
        self.leagueLoop()
        

    def reset(self):
        self.schedule = list(permutations([i for i in range(self.numTeams)],2))
        random.shuffle(self.schedule)
        self.schedule = self.splitSchedule(self.schedule)
        self.topScorers = []
        if self.numIterations > 1:
            self.verbose = False
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
    
    def getTopScorers(self):
        players = []
        for i in range(len(self.teams)):
            #players = self.teams[i].players
            for j in range(11):
                players.append(self.teams[i].players[j])
        playersSorted = sorted(players,key=lambda x: x.goals,reverse = True)
        topScorers = playersSorted[1:10]
        return topScorers
    
    def getTable(self):
        # First, sort teams by points
        self.teams = sorted(self.teams,key=lambda x: (x.points,x.goalDifference), reverse = True)
        self.topScorers = self.getTopScorers()
        if self.verbose:
            # Print table
            table = "{0:3}|{1:2}|{2:2}|{3:2}|{4:2}|{5:2}|{6:2}|{7:2}|{8:2}"
            print(f"{self.name.capitalize()} TABLE:")
            print(table.format("Pos ","Pl","W","D","L","GF","GA","GD","Pts"))
            for i in range(len(self.teams)):
                tm = self.teams[i]
                results = tm.results
                goals = tm.goals
                row = (str(i+1),str(self.gamesPlayed),str(results[0]),str(results[1]),str(results[2]),
                       str(goals[0]),str(goals[1]),str(goals[0]-goals[1]),str(tm.points))
                if i == 4 or i == 17: print("-----------------------------")
                print(tm.name,table.format(*row))        
            # Print top scorers
            print("=============================")
            print("TOP SCORERS:")
            for i in range(len(self.topScorers)):
                print(f"{self.topScorers[i].name} - {self.topScorers[i].goals}")
            print("=============================")
        
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
                        Match(self.teams[fixture[0]],self.teams[fixture[1]])
                        self.gamesPlayed += 1
                self.gamesPlayed = week + 1
                #self.getTable()
                #input("Press ENTER to continue")
            
            self.getTable()
            winner = self.teams[0].points
            winningPoints.append(winner)
            winStreak = max([team.topWinStreak for team in self.teams])
            unbeatenStreak = max([team.topUnbeatenStreak for team in self.teams])
            loseStreak = max([team.topLoseStreak for team in self.teams])
            if self.verbose:
                print(f"Longest win streak: {str(winStreak)}")
                print(f"Longest unbeaten streak: {str(unbeatenStreak)}")
                print(f"Longest lose streak: {str(loseStreak)}")
            
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
