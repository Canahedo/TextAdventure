"""
Unnamed Text Adventure - Lakitu
Written by Canahedo and WingusInbound
Python3
2024

This file contains a class which records all info about a player turn
"""

class Lakitu:
    def __init__(self, command: object, mod1: object, mod2: object, player_location: object, turn_text: list[str]) -> None:
        self.command = command
        self.mod1 = mod1
        self.mod2 = mod2
        self.player_location = player_location
        self.turn_text = turn_text