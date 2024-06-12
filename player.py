"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

This file contains a class which records info about a player turn
"""

from icecream import ic
from dataclasses import dataclass, field

@dataclass(slots=True)
class Player:
    inventory: list[str] = field(default_factory=list)
    location: str = field(default_factory=str)
    turn_text: list[str] = field(default_factory=list)
        
    def reset(self):
        self.inventory.clear()
        self.inventory.append("letter")
        self.location = "driveway"
