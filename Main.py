"""
Unnamed Text Adventure - Main
Written by Canahedo and WingusInbound
Python3
2024

This is the main file for the program
"""

# import os  # Used in clear() to erase the board
# import time  # Used in sleep() to create a delay
# import json
# from icecream import ic
# from dataclasses import dataclass

# from gametext import *
# from systemfunctions import *t
# from gameobjects import *
# from commands import *

from gamefunctions import *


def main():
    clear() # Clears text VSCode terminal starts with
    wants_to_play = True # If player opts to not play again, wants_to_play is set to False and program closes
    game = Game() # Initilize game object
    while wants_to_play:
        game.new_game() # Set up lists and player data for new game
        draw_ui(game)
        print(opening_crawl_text)
        wants_to_play = run_game(game) # Runs game, returns True if player wants to replay, False if not


if __name__ == "__main__":
    main()


