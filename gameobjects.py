"""
Unnamed Text Adventure - Game Objects
Written by Canahedo and WingusInbound
Python3
2024

This file represents all game objects
A game object is either an item or a chest
An item can be moved around by the player or put in their inventory
A chest is a location within a room which can hold items
"""

# import os  # Used in clear() to erase the board
# import time  # Used in sleep() to create a delay
# import json
# from icecream import ic
# from dataclasses import dataclass

# from gametext import *

from systemfunctions import *


#*############
#*### Game ###
#*############
@dataclass(slots=True)
class Game:
    chest_list: list # List of objects representing all chests
    item_list: list # List of objects representing all items
    object_list: list # List of objects combined from chest_list and item_list
    room_list: list # List of objects representing all rooms
    player_inventory: list # List of strings representing the player inventory
    player_location: str # String representing which room the player is in

    # Starts a new game
    def new_game(self):
        
        # Init Player - Sets initial inventory and location
        self.player_inventory.clear()
        self.player_inventory.append("letter")
        self.player_location = "driveway"
        self.room_list = init_game_lists("rooms") # Ties room_list to game object
        self.chest_list = init_game_lists("chests") # Ties chest_list to game object   
        self.item_list = init_game_lists("items") # Ties item_list to game object   
        
        # Init Objects - # Combines chest_list and item_list, ties to game object
        object_list = []
        for chest in self.chest_list: object_list.append(chest)
        for item in self.item_list:object_list.append(item)
        self.object_list = object_list
        return self



#*############
#*### Room ###
#*############
#Room(name)
@dataclass
class Room:
    name: str
    look_text: str
    
#*####################
#*### Game Objects ###
#*####################
#GameObject(name, checkable, key, state, checktext_dict, useable, visible

@dataclass(slots=True)
class GameObject:
    name: str # Name of the object
    checkable: bool # Does the object respond to the check command
    key: dict # What items/actions interact with the object
    state: str # What state the object is in
    checktext_dict: dict # Contains all text which might be used for the check command
    useable: bool # Does the object respond to the use command
    visible: bool # Is the object accessible to the player
   
    


#*##############
#*### Chests ###
#*##############
#Chest(name, checkable, key, state, checktext_dict, trigger_dict, useable, visible, chest_inventory)
class Chest(GameObject):
    def __init__(self, name, checkable, key, state, checktext_dict, trigger_dict, useable, visible, chest_inventory) -> None:
        super().__init__(name, checkable, key, state, checktext_dict, useable, visible)
        self.chest_inventory = chest_inventory # Items held in this chest
        self.trigger_dict = trigger_dict # Contains list of items which react with the object, and the state this reaction puts the object in


#*#############
#*### Items ###
#*#############
#Item(name, checkable, key, state, checktext_dict, useable, visible, takeable)
class Item(GameObject):
    def __init__(self, name, checkable, key, state, checktext_dict, useable, visible, takeable) -> None:
        super().__init__(name, checkable, key, state, checktext_dict, useable, visible)
        self.takeable = takeable # Can the item be put in the player inventory
        
    



#Initializes object and room lists
def init_game_lists(target_list):
    temp_list = []
    with open("assets/"+str(target_list)+".json", "r") as file:
        data = json.load(file)
        for item in data: # Iterates over each object in json, appends to temp_list
            if target_list == "items": temp_list.append(Item(**item))
            if target_list == "chests": temp_list.append(Chest(**item))
            if target_list == "rooms": temp_list.append(Room(**item))       
    return temp_list