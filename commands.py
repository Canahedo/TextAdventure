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
        
    def triggers(): #check current status, make relevant changes, display update text 
        pass
        

class Tutorial(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        self.name = name
        self.alias = alias
        self.num_mods = num_mods
        
    def __call__(self, game: None, mod1: None, mod2: None):
        with open("assets/tutorial.md", "r") as file:
            file_contents = file.read()
        print(file_contents, "\n")
        

class Look(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        self.name = name
        self.alias = alias
        self.num_mods = num_mods     
        
    def __call__(self, game: object, mod1: None, mod2: None):
        for room in game.room_list:
            if game.player_location == room.name:
                print(room.look_text)
                break
        
        
class Check(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
    
    def __call__(self, game: None, obj: object, mod2: None):
        if obj == -1:
            print("Unrecognized object")
            return
        print(obj.checktext_dict[obj.state]) # Displays current checktext according to state
        if ("gameobjects.Chest" in str(obj.__class__) # Only considers triggers if obj is a chest
            and "check" in obj.key # Check is a valid key for some chests
            and obj.key["check"] != obj.state): # Prevent unlocking open doors, etc
                obj.state = obj.key["check"] # Change obj state per key
                print(obj.trigger_dict[obj.state]) # Display any text for the trigger per state


class Take(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        
    def __call__(self, game: object, obj: object, mod2: None):
        if obj == -1:
            print("Unrecognized object")
            return
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


class Walk(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        
        
    def __call__(self, game: object, dir: object, mod2: None):
        if dir == -1:
            print("I don't know where you're trying to go")
            return
        if dir.name == game.player_location:
            print(f"You are already in the",dir.name)
            return
        if dir.name in ["north", "n","south", "s","east", "e","west", "w"]:
            goto = gps(game, dir.name)        
        else:
            goto = dir.name
        
        game.player_location = goto
        print(f"You walk to the",goto)
        
        
        pass
            

class Speak(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)  
        
    def __call__(self, game: object, targ: object, mod2: None):
        pass  
            
        
class Use(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)    
        
    def __call__(self, game: object, obj1: object, obj2: object):
        if obj1 == -1 or obj2 == -1:
            print("Unrecognized object")
            return
        
        pass
        
        
class Place(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        

    def __call__(self, game: object, obj1: object, obj2: object):
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
#TODO:  GPS and cardinals as class
#TODO:  visibilty system
#TODO:
#TODO:
#TODO:
#TODO:
'''

            
        
             

