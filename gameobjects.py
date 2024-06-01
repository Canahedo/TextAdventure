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


############
### Game ###
############

class Game:
    def __init__(self, chest_list, item_list, object_list, room_list, player_inventory, player_location):
        self.chest_list = chest_list # Contains a list of objects representing all chests
        self.item_list = item_list # Contains a list of objects representing all items
        self.object_list = object_list # Contains a list of objects combined from chest_list and item_list
        self.room_list = room_list # Contains a list of objects representing all rooms
        self.player_inventory = player_inventory # Contains a list representing the player inventory
        self.player_location = player_location # Contains a string representing which room the player is in
        
    @classmethod # No idea, I copied it from the internet. Is it even being used?
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)  

    #init_player - Sets initial inventory and location
    def init_player(self):
        self.player_inventory = ["letter"]
        self.player_location = "driveway"
    
    # init_chests - Initializes list of chest objects
    def init_chests(self):
        chest_list = [] # Creates empty list
        with open("assets/chests.json", "r") as file:
            data = json.load(file)
            for chest in data: # Iterates over each object in json, appends to chest_list
                chest_list.append(Chest(**chest))
            for chest in chest_list: # For an unknown reason, state and key import inside a tuple. This extracts them.
                chest.state = chest.state[0]
                chest.key = chest.key[0]
        self.chest_list = chest_list # Ties chest_list to game object

    # init_items - Initializes list of item objects
    def init_items(self):
        item_list = [] # Creates empty list
        with open("assets/items.json", "r") as file:
            data = json.load(file)
            for item in data: # Iterates over each object in json, appends to item_list
                item_list.append(Item(**item))
            for item in item_list: # For an unknown reason, state and key import inside a tuple. This extracts them.
                item.state = item.state[0]
                item.key = item.key[0]            
        self.item_list = item_list # Ties item_list to game object
    
    def init_objects(self): # Runs modules to init chests and items, combines chest_list and item_list, ties to game object
        self.init_chests()
        self.init_items()
        object_list = []
        object_list = self.chest_list
        for item in self.item_list:
            object_list.append(item)
        self.object_list = object_list
        

####################
### Game Objects ###
####################
#GameObject(name, checkable, key, state, checktext_dict, useable, moveable
class GameObject:
    def __init__(self, name, checkable, key, state, checktext_dict, useable, moveable):
        self.name = name # Name of the object
        self.checkable = checkable # Does the object respond to the check command
        self.key = key, # What items/actions interact with the object
        self.state = state, # What state the object is in
        self.checktext_dict = checktext_dict # Contains all text which might be used for the check command
        self.useable = useable # Does the object respond to the use command
        self.moveable = moveable # Does the object respond to the move command
    
    def check(self): # Represents the player command "check"
        print(self.checktext_dict[self.state]) # Displays current checktext per current state
        if ("gameobjects.Chest" in str(self.__class__) # Only considers triggers if object is a chest
            and "check" in self.key # For some object, the check command triggers as if it were a key
            and self.key["check"] != self.state):    
                self.state = self.key["check"] # Change object state per key
                print(self.trigger_dict[self.state]) # Display any text for the trigger per state
      
        
##############
### Chests ###
##############
#Chest(name, checkable, key, state, checktext_dict, trigger_dict, useable, moveable, chest_inventory)
class Chest(GameObject):
    def __init__(self, name, checkable, key, state, checktext_dict, trigger_dict, useable, moveable, chest_inventory) -> None:
        super().__init__(name, checkable, key, state, checktext_dict, useable, moveable)
        self.chest_inventory = chest_inventory # Items held in theis chest
        self.trigger_dict = trigger_dict # Contains list of items which react with the object, and the state this reaction puts the object in


#############
### Items ###
#############
#Item(name, checkable, key, state, checktext_dict, useable, moveable, takeable)
class Item(GameObject):
    def __init__(self, name, checkable, key, state, checktext_dict, useable, moveable, takeable) -> None:
        super().__init__(name, checkable, key, state, checktext_dict, useable, moveable)
        self.takeable = takeable # Can the item be put in the player inventory
        




