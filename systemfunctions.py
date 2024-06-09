"""
Unnamed Text Adventure - System Functions
Written by Canahedo and WingusInbound
Python3
2024

This file contains the low level functions which are relied on by multiple files
"""

import os  # Used in clear() to erase the board
import time  # Used in sleep() to create a delay
import json
from icecream import ic
from dataclasses import dataclass, field

from assets.text.misc_gametext import *


# Creates clear() to erase the board
def clear():
    os.system("cls")


#*###################
#*## DEBUG TOGGLE ###
#*###################
#* Set to False, True, or "verbose"
DEBUG = False
#DEBUG = True
#DEBUG = "verbose"


#*##############
#*## Draw UI ###
#*##############
# Displays header and formats/displays player inventory
def draw_ui(game) -> None:
    """
    Wipes the screen, displays the game_title, and displays
    the player inventory without list formatting
    Disables screen wipe if DEBUG == "verbose"

    Args:
        game (Game): The object containing all game lists and player data
    """    
    if DEBUG:
        print("-------------------------")
        print("-------------------------")
        print("DEBUG MODE")
        print(DEBUG)
    if DEBUG != "verbose": #* DEBUG: Disables screen wipe when DEBUG     
        clear() # Erases screen before redrawing UI, disabled in verbose DEBUG
        print(game_title)
    print("You are carrying the following: ")
    # Formats inventory  
    if len(game.player_inventory) != 0:
        for item in game.player_inventory:
            print(str(item), end=" ")
            if len(game.player_inventory) != game.player_inventory.index(item) + 1:
                print(", ", end="")
    print("\n\n-------------------------\n")
    


