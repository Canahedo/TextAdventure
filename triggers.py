'''
Unnamed Text Adventure - Triggers
Written by Canahedo and WingusInbound
Python3
2024

This file tracks and executes various triggers for the game
'''

##########################
### TRACKING VARIABLES ###
##########################

driveway = {'rocks': 'stacked'}





##############
###  LOOK  ###
##############
def look_triggers(player_location):
    if player_location == 'driveway' and driveway.get('rocks') == 'stacked':
        print('You see a small pile of rocks at the edge of the driveway.\n')

###############
###  CHECK  ###
###############
def check_triggers():
    ...

    
