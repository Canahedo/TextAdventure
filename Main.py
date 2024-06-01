"""
Unnamed Text Adventure - Main
Written by Canahedo and WingusInbound
Python3
2024

This is the main file for the program
"""

from gamefunctions import *

def main():
    wants_to_play = True
    while wants_to_play:
        wants_to_play: bool = run_game()
        
if __name__ == "__main__":
    main()


