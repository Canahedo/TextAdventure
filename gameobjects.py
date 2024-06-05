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
    #! Does object_list cause problems when making changes? Which list is being changed?
    #? Does copying the lists to object_list mean they are tied together?
    #? Do changes carry over?
    chest_list: list[str] = field(default_factory=list) # List of objects representing all chests
    item_list: list[str] = field(default_factory=list) # List of objects representing all items
    object_list: list[str] = field(default_factory=list) # List of objects combined from chest_list and item_list
    room_list: list[str] = field(default_factory=list) # List of objects representing all rooms
    player_inventory: list[str] = field(default_factory=list) # List of strings representing the player inventory
    player_location: str = field(default_factory=str) # String representing which room the player is in
    
    # Sets starting values for game lists and player data.
    def new_game(self): 
        """
        Wipes player inventory, and adds starting item(s). Sets initial player location.
        Runs function to set starting lists for items, chests, and rooms.
        Combines item and chest list into object list.        
        """        
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


#*############
#*### Room ###
#*############
#Room(name, look_text)
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
        
    


#*#######################
#*### Init Game Lists ###
#*#######################
#Initializes object and room lists
def init_game_lists(obj_type: str) -> list:
    """
    Initializes a blank list, then reads a json file containing data for either the game's items, chests,
    or rooms (selected by obj_type), and copies that data to the list as objects of the respective type.
    Finally, returns the list of objects.

    Args:
        obj_type (str): Will be either "items", "chests", or "rooms". Set by game.new_game().

    Returns:
        list: List of objects of either Class Item, Chest, or Room, depending on obj_type.
    """    
    list_builder = []
    with open("assets/"+str(obj_type)+".json", "r") as file:
        data = json.load(file)
        for item in data: # Iterates over each object in json, appends to temp_list
            if obj_type == "items": list_builder.append(Item(**item))
            if obj_type == "chests": list_builder.append(Chest(**item))
            if obj_type == "rooms": list_builder.append(Room(**item))       
    return list_builder

