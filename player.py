"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

This file contains a class which records info about a player turn
"""

from icecream import ic
from dataclasses import dataclass, field

from commands import Command, Look, Check, Take, Walk, Speak, Use, Place


@dataclass
class Player:
    inventory: list[object] = field(default_factory=list)
    location: object = field(default_factory=object)
    turn_text: list[str] = field(default_factory=list)
    local_chests: list[object] = field(default_factory=list)
    local_items: list[object] = field(default_factory=list)
    command_list: list[object] = ( # List of objects representing the player commands
        Look("look", ["look", "l"], 0),
        Check("check", ["check", "c"], 1),
        Take("take", ["take", "t"], 1),
        Walk("walk", ["walk", "w", "move", "m"], 1),
        Speak("speak", ["speak", "s"], 1),
        Use("use", ["use", "u"], 2),
        Place("place", ["place", "p"], 2)
        )
        
    def reset(self, game):
        self.inventory.clear()
        self.inventory.append(game.locate_object("letter"))
        self.location = game.locate_object("driveway")

    def get_local_chests(self):
        chest_list = []
        for chest in self.location.inventory:
            chest_list.append(self.location.inventory[chest])   
        self.local_chests = chest_list
        
    def get_local_items(self, obj):
        item_list = []
        for item in obj.inventory:
            item_list.append(obj.inventory[item])   
        self.local_items = item_list
    
    
    def take_turn(self, command, mod1, mod2, game):
        self.turn_text.clear()
        
        if any([mod1,mod2]) == -1:
            print("Unrecognized object")
            
        if isinstance(command, Look):
            command(game, mod1, mod2)
        if isinstance(command, Check):
            if all([
                mod1.checkable,
                mod1.visible                
            ]):
                command(game, mod1, mod2)
                return
        if isinstance(command, Take):
            command(game, mod1, mod2)
        if isinstance(command, Walk):
            command(game, mod1, mod2)
        if isinstance(command, Speak):
            command(game, mod1, mod2)
        if isinstance(command, Use):
            command(game, mod1, mod2)
        if isinstance(command, Place):
            command(game, mod1, mod2)
        