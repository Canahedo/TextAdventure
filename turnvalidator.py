"""
Unnamed Text Adventure - Turn Validator
Written by Canahedo and WingusInbound
Python3
2024

This file represents a class which confirms if a player turn can be executed
"""

from icecream import ic

class TurnValidator():
    def __init__(self, command, mods, data, player):
        self.command = command
        self.mods = mods
        self.data = data
        self.player = player
        self.result = True    #! Currently bypassed, should default to false