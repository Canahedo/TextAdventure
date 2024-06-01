"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

This file defines the player
"""

class Player:
    def __init__(self,inventory: list, room: str) -> None:
        self.inventory = inventory
        self.room = room


player = Player([""], "")


def init_player():
    player.inventory = ["letter"]
    player.room = "driveway"