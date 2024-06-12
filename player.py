"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

This file contains a class which records info about a player turn
"""

from icecream import ic
from dataclasses import dataclass, field


@dataclass
class Player:
    inventory: list[object] = field(default_factory=list)
    location: object = field(default_factory=object)
    turn_text: list[str] = field(default_factory=list)
        
    def reset(self, game):
        self.inventory.clear()
        self.inventory.append(game.locate_object("letter"))
        self.location = game.locate_object("driveway")
