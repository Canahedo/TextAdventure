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
# from assets.text.misc_gametext import *
# from systemfunctions import *

from gameobjects import *

class Command:
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        self.name = name
        self.alias = alias
        self.num_mods = num_mods
        
    def triggers(): #check current status, make relevant changes, display update text 
        pass
        

class Tutorial(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        self.name = name
        self.alias = alias
        self.num_mods = num_mods
        
    def __call__(self, game: None, mod1: None, mod2: None):
        with open("assets/text/tutorial.md", "r") as file:
            file_contents = file.read()
        print(file_contents, "\n")
        

class Look(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        self.name = name
        self.alias = alias
        self.num_mods = num_mods     
        
    def __call__(self, game: object, mod1: None, mod2: None):
        draw_ui(game)
        for room in game.room_list:
            if game.player_location == room.name:
                text_fetcher("look", room.name, room.looktext_dict[room.state])

        
class Check(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
    
    def __call__(self, game: None, obj: object, mod2: None):
        if obj == -1:
            return(-1,"Unrecognized object")
        if obj.visible == False:
            return(-1,f"You can't see the "+obj.name)
        draw_ui(game)
        text_fetcher("check", obj.name, obj.checktext_dict[obj.state]) #Retrieves and prints check text for current "state"
        if "none" not in obj.key:    
            obj.try_key("check", game)

        
                

class Take(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        
    def __call__(self, game: object, obj: object, mod2: None):
        if obj == -1:
            return(-1,"Unrecognized object")
        if obj.name in game.player_inventory:
            return(-1,f"You already have the "+obj.name)
        if obj.visible == False:
            return(-1,f"You can't see the "+obj.name)        
        if obj.takeable == False:
            return(-1,f"You can't take the "+obj.name)
        game.player_inventory.append(obj.name)
        draw_ui(game)
        return(0,f"You take the "+obj.name)
       


class Walk(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        
        
    def __call__(self, game: object, dir: object, mod2: None):
        if dir == -1:
            return(-1,"I don't know where you're trying to go")
        if dir.name == game.player_location:
            return(-1,f"You are already in the "+dir.name)
        draw_ui(game)
        if dir.name in ["north", "n","south", "s","east", "e","west", "w"]:
            goto = gps(game, dir.name)        
        else:
            goto = dir.name
        
        game.player_location = goto
        return(0,f"You walk to the "+goto)
        
            

class Speak(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)  
        
    def __call__(self, game: object, targ: object, mod2: None):
        pass  
            
        
class Use(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)    
        
    def __call__(self, game: object, obj1: object, obj2: object):
        if obj1 == -1:
            return(-1,"Object 1 unrecognized")
        if obj2 == -1:
            return(-1,"Object 2 unrecognized")
        draw_ui(game)
        if "none" not in obj2.key:    
             obj2.try_key(obj1.name, game)
        
        



class Place(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        

    def __call__(self, game: object, obj1: object, obj2: object):
        draw_ui(game)
        pass


def gps(game: object, dir: str):
    raise NotImplementedError()














# Initializes instances of each command class in command_list
#Command = Command("name", [alias], num_mods)
command_list = [
Tutorial("help", ["help", "h", "tutorial"], 0),
Look("look", ["look", "l"], 0),
Check("check", ["check", "c"], 1),
Take("take", ["take", "t"], 1),
Walk("walk", ["walk", "w", "move", "m"], 1),
Speak("speak", ["speak", "s"], 1),
Use("use", ["use", "u"], 2),
Place("place", ["place", "p"], 2)
]













'''

l - 0 = read player location, check for changes, display text
h - 0 = display text
e/q - 0 = system command

c - 1 = is visible?
            is in player.room or player.inv?
        is checkable?
        display checktext
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
#TODO:  GPS and cardinals as class
#TODO:  visibilty system
#TODO:
#TODO:
#TODO:
#TODO:
'''

            
        
             

