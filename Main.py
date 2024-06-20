"""
Unnamed Text Adventure - Main
Written by Canahedo and WingusInbound
Python3
2024

This is the main file for the program,
which initializes the game object and runs the game
"""

from gamefiles.functions import Game_Functions
from gamefiles.objects import Game_Data
from gamefiles.player import Player
from gamefiles.services import Services


# * Main
# * Initializes game object, and game/player data, then starts a new game
# *####################
def main():
    game = Game_Functions(Game_Data(), Player(), Services())
    game.run()


if __name__ == "__main__":
    main()
