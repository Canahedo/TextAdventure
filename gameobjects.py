"""
Unnamed Text Adventure - Game Objects
Written by Canahedo and WingusInbound
Python3
2024

This file all game objects
A game object is either an item or a chest
An item can be moved around by the player or put in their inventory
A chest is a location within a room which can hold items
"""

import json
from dataclasses import dataclass
from icecream import ic
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
    player_inventory: list # List representing the player inventory
    player_location: str # String representing which room the player is in
        
    # Starts a new game
    def new_game(self):
        self.init_player()
        self.init_objects()
        self.init_rooms()
        return self
    
    #init_player - Sets initial inventory and location
    def init_player(self):
        self.player_inventory.clear()
        self.player_inventory.append("letter")
        self.player_location = "driveway"
    
    # init_chests - Initializes list of chest objects
    def init_chests(self):
        chest_list = [] # Creates empty list
        with open("assets/chests.json", "r") as file:
            chest_data = json.load(file)
            for chest in chest_data: # Iterates over each object in json, appends to chest_list
                chest_list.append(Chest(**chest))
        self.chest_list = chest_list # Ties chest_list to game object

    # init_items - Initializes list of item objects
    def init_items(self):
        item_list = [] # Creates empty list
        with open("assets/items.json", "r") as file:
            item_data = json.load(file)
            for item in item_data: # Iterates over each object in json, appends to item_list
                item_list.append(Item(**item))       
        self.item_list = item_list # Ties item_list to game object
    
    def init_objects(self): # Runs modules to init chests and items, combines chest_list and item_list, ties to game object
        self.init_chests()
        self.init_items()
        object_list = []
        for chest in self.chest_list: object_list.append(chest)
        for item in self.item_list:object_list.append(item)
        self.object_list = object_list
        
    def init_rooms(self):
        room_list = [] # Creates empty list
        with open("assets/rooms.json", "r") as file:
            room_data = json.load(file)
            for room in room_data: # Iterates over each object in json, appends to room_list
                room_list.append(Room(**room))       
        self.room_list = room_list # Ties room_list to game object
        
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
#GameObject(name, checkable, key, state, checktext_dict, useable, moveable

@dataclass(slots=True)
class GameObject:
    name: str # Name of the object
    checkable: bool # Does the object respond to the check command
    key: dict # What items/actions interact with the object
    state: str # What state the object is in
    checktext_dict: dict # Contains all text which might be used for the check command
    useable: bool # Does the object respond to the use command
    moveable: bool # Does the object respond to the move command
   
    def check(self, game): # Represents the player command "check"
        draw_ui(game)
        print(self.checktext_dict[self.state]) # Displays current checktext according to state
        if ("gameobjects.Chest" in str(self.__class__) # Only considers triggers if object is a chest
            and "check" in self.key # Check is a valid key for some chests
            and self.key["check"] != self.state): # Prevent unlocking open doors, etc
                self.state = self.key["check"] # Change object state per key
                print(self.trigger_dict[self.state]) # Display any text for the trigger per state


#*##############
#*### Chests ###
#*##############
#Chest(name, checkable, key, state, checktext_dict, trigger_dict, useable, moveable, chest_inventory)
class Chest(GameObject):
    def __init__(self, name, checkable, key, state, checktext_dict, trigger_dict, useable, moveable, chest_inventory) -> None:
        super().__init__(name, checkable, key, state, checktext_dict, useable, moveable)
        self.chest_inventory = chest_inventory # Items held in theis chest
        self.trigger_dict = trigger_dict # Contains list of items which react with the object, and the state this reaction puts the object in


#*#############
#*### Items ###
#*#############
#Item(name, checkable, key, state, checktext_dict, useable, moveable, takeable)
class Item(GameObject):
    def __init__(self, name, checkable, key, state, checktext_dict, useable, moveable, takeable) -> None:
        super().__init__(name, checkable, key, state, checktext_dict, useable, moveable)
        self.takeable = takeable # Can the item be put in the player inventory
        
    def take(self,game):
        game.player_inventory.append(self.name)
        draw_ui(game)
        print(f"You take the",self.name)
        
        