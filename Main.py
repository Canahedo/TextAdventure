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
    clear()
    wants_to_play = True
    while wants_to_play:
        game = Game()
        wants_to_play = new_game(game)
        
if __name__ == "__main__":
    main()


