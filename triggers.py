'''
Unnamed Text Adventure - Triggers
Written by Canahedo and WingusInbound
Python3
2024

This file tracks and executes various triggers for the game
'''

#Imports
from Inventories import *

##########################
### TRACKING VARIABLES ###
##########################

driveway = {'rock': 'stacked'}





##############
###  LOOK  ###
##############
def look_triggers():
    if player_location == 'driveway' and driveway['rock'] == 'stacked':
        print('You see a small pile of rocks at the edge of the driveway.\n')


###############
###  CHECK  ###
###############
def check_triggers(object):
    if object == 'rock' and player_stats['room'] == 'driveway' and driveway['rock'] == 'stacked':
        driveway.update({'rock': 'toppled'})
        return 'You knock over the rocks and find a key.\nHow long has it been here?'
    if object == 'rock' and player_stats['room'] == 'driveway' and driveway['rock'] == 'toppled':
        return 0