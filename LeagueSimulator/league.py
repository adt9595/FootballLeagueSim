# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 17:12:07 2020
@author: Alex Taylor

Stores league information
name - String, name of league
teams - Array, list of teams
teamDeltaFactor - Float, regularization parameter for individual player stats
numIterations - Int, number of league iterations to run
verbose - Boolean, whether or not to print table
"""

import random
import math
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
    def __init__(self,name,teams,teamDeltaFactor,numIterations=1,verbose=True):
        self.generateRoundRobin()
        self.name = name
        self.teams = teams
        self.numIterations = numIterations
        self.teamDeltaFactor = teamDeltaFactor
        self.verbose = verbose
        self.numTeams = len(self.teams)
        self.reset()
        self.leagueLoop()
        

    def reset(self):
        self.schedule = self.generateRoundRobin()
        self.topScorers = []
        if self.numIterations > 1:
            self.verbose = False
        self.gamesPlayed = 0
        for team in self.teams:
            team.reset()

    # Populate schedule using a randomly shuffled double round-robin algorithm
    def generateRoundRobin(self):
        sortedSchedule = []
        # First pass
        matches = [[1,2,3,4,5,6,7,8,9,10],[20,19,18,17,16,15,14,13,12,11]]
        sortedSchedule.append(list(zip(matches[0],matches[1])))
        for i in range(2*len(matches[0])-2):
            currentMatches = [x[:] for x in matches]
            matches[0][1] = currentMatches[1][0]
            for j in range(1,9):
                matches[0][j+1] = currentMatches[0][j]
            matches[1][9] = currentMatches[0][9]
            for j in range(1,10):
                matches[1][j-1] = currentMatches[1][j]
            sortedSchedule.append(list(zip(matches[0],matches[1])))
        # Second pass
        matches = [[20,19,18,17,16,15,14,13,12,11],[1,2,3,4,5,6,7,8,9,10]]
        sortedSchedule.append(list(zip(matches[0],matches[1])))
        for i in range(2*len(matches[0])-2):
            currentMatches = [x[:] for x in matches]
            matches[0][0] = currentMatches[1][1]
            for j in range(0,9):
                matches[0][j+1] = currentMatches[0][j]
            matches[1][9] = currentMatches[0][9]
            for j in range(2,10):
                matches[1][j-1] = currentMatches[1][j]
            sortedSchedule.append(list(zip(matches[0],matches[1])))
        random.shuffle(sortedSchedule)
        return sortedSchedule
    
    def getTopScorers(self):
        players = []
        for i in range(len(self.teams)):
            for j in range(11):
                players.append(self.teams[i].players[j])
        playersSorted = sorted(players,key=lambda x: x.goals,reverse = True)
        topScorers = playersSorted[1:10]
        return topScorers
    
    def getTable(self):
        # Sort teams by points
        self.teams = sorted(self.teams,key=lambda x: (x.points,x.goalDifference), reverse = True)
        self.topScorers = self.getTopScorers()
        if self.verbose:
            # Print table
            table = "{0:3}|{1:2}|{2:2}|{3:2}|{4:2}|{5:2}|{6:2}|{7:2}|{8:2}"
            print(f"{self.name.upper()} TABLE:")
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
                        Match(self.teams[fixture[0]-1],self.teams[fixture[1]-1],teamDeltaFactor = self.teamDeltaFactor)
                self.gamesPlayed = week + 1
            self.getTable()
            winner = self.teams[0].points
            winningPoints.append(winner)
            
            # Update streaks
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
            self.avg = mean(winningPoints)
            self.dev = stddev(winningPoints)
            #print("Avg:",self.avg)
            #print("Std Dev:",self.dev)
            #print("Most points:",mostPoints)
            print("Iteration Complete")

