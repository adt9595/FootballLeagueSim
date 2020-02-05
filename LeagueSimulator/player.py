# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 17:20:51 2020
@author: Alex Taylor

Stores player information
name - String, name of player
position - String, position of player
attributes - Array, list of attributes 
            (defending,passing,shooting) / (stopping, reactions, kicking)
"""    
import random

class Player:
    def __init__(self,name,position,attributes):
        self.name = name
        self.position = position
        self.attributes = self.formatAttributes(attributes)
        
        # Goalkeepers can score too!
        if self.position == "GK":
            self.goalProbability = 0.000001
        else:
            self.goalProbability = self.attributes[2] * positionMultipliers[self.position][2]
            
        self.reset()
    
    def reset(self):
        self.goals = 0
        self.overallRating = sum(self.attributes)     
        self.isSuspended = False
    
    def formatAttributes(self,attributes):
        attributes = attributes.split(' ')
        #adjustedAttributes = []
        for i in range(len(attributes)):
            attributes[i] = float(attributes[i]) * positionMultipliers[self.position][i]
        return attributes
    
    def scoreGoal(self):
        self.goals += 1
        self.goalProbability *= random.uniform(1.01, 1.04)
        
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