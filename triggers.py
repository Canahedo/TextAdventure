"""
Unnamed Text Adventure - Triggers
Written by Canahedo and WingusInbound
Python3
2024

This file tracks and executes various triggers for the game
"""

# Imports
from Inventories import *

##########################
### TRACKING VARIABLES ###
##########################

driveway = {}


####################
### INIT TRIGGERS###
####################player_location
# Initialize starting positions for a new game
def init_triggers():
    driveway.update({"rock": "stacked"})


##############
###  LOOK  ###
##############
def look_triggers():
    if (
        player_stats["room"] == "driveway"
        and driveway["rock"] == "stacked"):
            print("You see a small pile of rocks at the edge of the driveway.\n")


###############
###  CHECK  ###
###############
def check_triggers(object):
    if (
        object == "rock"
        and player_stats["room"] == "driveway"
        and driveway["rock"] == "stacked"
        ):
            driveway.update({"rock": "toppled"})
            player_inventory.append("key")
            return 1
    if (
        object == "rock"
        and player_stats["room"] == "driveway"
        and driveway["rock"] == "toppled"
        ):
            return 0
    else:
        return -1
