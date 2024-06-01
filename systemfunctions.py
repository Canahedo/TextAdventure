"""
Unnamed Text Adventure - System Functions
Written by Canahedo and WingusInbound
Python3
2024

This file contains the low level functions which are relied on by multiple files
"""

import os  # Used in clear() to erase the board
from gametext import *


# Creates clear() to erase the board
def clear():
    os.system("cls")


###############
### Draw UI ###
###############
# Displays header and formats/displays player inventory
def draw_ui(game):
    clear()
    print(game_title)
    print("You are carrying the following: ")
    # Formats inventory
    if len(game.player_inventory) != 0:
        for item in game.player_inventory:
            print(str(item), end=" ")
            if len(game.player_inventory) != game.player_inventory.index(item) + 1:
                print(", ", end="")
    print("\n\n-------------------------\n")