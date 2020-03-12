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

#import pygame
import math
import matplotlib.pyplot as plt
from league import League
from team import Team
from match import Match


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

def plotFigure(data,stepsize,epochs):
    steps = [stepsize*i for i in range(epochs)]
    plt.plot(steps,data)
    plt.plot((0,stepsize*epochs),(87.074,87.074))
    plt.axis([0, stepsize*epochs, min(data), max(data)])
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
        

teams = []
averages = []
stepsize = 0.2
epochs = 15

# Populate league   
for i in range(20):
    teams.append(Team('teamdata/team{0}.txt'.format(i)))
    

# Run multiple leagues with varying team rating parameters
#for i in range(epochs):
#    prem = League('Premier League',teams,numIterations=20,teamDeltaFactor=stepsize*i,verbose=False)
##    prem = League('Premier League',teams,teamDeltaFactor=0.0 + (stepsize * i),numIterations=1)
#    averages.append(prem.avg)
#plotFigure(averages,stepsize,epochs)
prem = League('Premier League',teams,teamDeltaFactor=3.0,verbose=True)
#Match(teams[10],teams[19],verbose=True)


"""
Stats for premier league 92/93 -> 18/19:
    Champion points avg: 87.074
    Champion points dev: 6.063
"""
