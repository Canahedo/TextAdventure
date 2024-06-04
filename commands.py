"""
Unnamed Text Adventure - Commands
Written by Canahedo and WingusInbound
Python3
2024

This file defines all commands accessible to the player
"""

# import os  # Used in clear() to erase the board
# import time  # Used in sleep() to create a delay
# import json
# from icecream import ic
# from dataclasses import dataclass
# from gametext import *
# from systemfunctions import *

from gameobjects import *

#command.check(obj, game)
#comamnd.take(obj, game)
#comamnd.walk(dir, game)
#comamnd.speak(per, game)
#comamnd.use(obj, che, game)
#comamnd.move(obj, che, game)
#comamnd.place(obj, che, game)

class Command:
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        self.name = name
        self.alias = alias
        self.num_mods = num_mods   
        
    def statebasedactions(): #check current status, make relevant changes, display update text 
        pass
        
class look(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        
            
        
             
        # def help(self, game):
        #     pass
        # def look(self, object, game):
        #     pass
        # def check(self, object, game):
        #     pass
        # def take(self, object, game):
        #     pass
        # def walk(self, object, game):
        #     pass
        # def speak(self, object, game):
        #     pass
        # def use(self, object, game):
        #     pass
        # def move(self, object, game):
        #     pass
        # def place(self, object, game):
        #     pass
        
# Represents the player command "look"
def look(game):
    for room in game.room_list:
        if game.player_location == room.name:
            print(room.look_text)
            break

# Represents the player command "check"
def check(obj): 
        print(obj.checktext_dict[obj.state]) # Displays current checktext according to state
        if ("gameobjects.Chest" in str(obj.__class__) # Only considers triggers if obj is a chest
            and "check" in obj.key # Check is a valid key for some chests
            and obj.key["check"] != obj.state): # Prevent unlocking open doors, etc
                obj.state = obj.key["check"] # Change obj state per key
                print(obj.trigger_dict[obj.state]) # Display any text for the trigger per state

# Represents the player command "take"        
def take(obj,game):
    if obj.name in game.player_inventory:
        print(f"You already have the",obj.name)
        return
    if obj.takeable == False:
        print(f"You can't take the",obj.name)
        return
    game.player_inventory.append(obj.name)
    draw_ui(game)
    print(f"You take the",obj.name)
    return
        


















#Command = Command(name, alias, num_mods)
command_list = [
Command("look", ["look", "l"], 0),
Command("help", ["help", "h"], 0),
Command("end", ["end", "e", "r", "restart", "reboot"], 0),
Command("quit", ["quit", "q"], 0),
Command("check", ["check", "c"], 1),
Command("take", ["take", "t"], 1),
Command("walk", ["walk", "w", "move", "m"], 1),
Command("speak", ["speak", "s"], 1),
Command("use", ["use", "u"], 2),
Command("place", ["place", "p"], 2)
]


'''

l - 0 = read player location, check for changes, display text
h - 0 = display text
e/q - 0 = system command

c - 1 = is visible?
            is in player.room or player.inv?
        is checkable?
        display chktext
        triggers? > apply changes > Display text
        
t - 1 = is visible?
            is in player.room but not player.inv?
        is takeable?
        add to inv
        display take confirm text
        remove from inv
        triggers? > apply changes > Display text
        
w - 1 = already in location?
        if cardinal, adjust cordinates
        if room name, set by name
        display new room text
        triggers       
        
s - 1 = is visible?
            is in room?
        can speak?
        Display text
        triggers
        
u - 2 = (similar to put. likely item on chest, but may be item on item)
        item in inv?
        chest visible / in room?
        valid combo?
        display confirm text
        remove item from inv (sometimes)
        add item to inv (maybe)
        triggers

m - 2 = eliminated
            move as alias of walk?
                
p - 2 = (simliar to use. likely always iteom on chest)
        item in inv?
        chest visible / in room?
        valid combo?
        display confirm text
        remove item from inv
        add item to inv
        triggers


# Shared tasks
    is obj in inv?
    is player in same room as obj?
    is marked as visible?
    











#TODO:  Tracking changes
#TODO:
#TODO:
#TODO:
#TODO:
#TODO:
#TODO:
'''