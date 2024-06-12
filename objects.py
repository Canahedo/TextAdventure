"""
Unnamed Text Adventure - Objects
Written by Canahedo and WingusInbound
Python3
2024

This file represents the game data, including lists of all items, chests, and rooms
"""

from icecream import ic
from dataclasses import dataclass, field
import json

from commands import Look, Check, Take, Walk, Speak, Use, Place


#* Game Data
#* Holds lists of objects representing objects (items/chests), rooms, and commands
#*####################
@dataclass
class Game_Data:
    object_list: list[str] = field(default_factory=list) # List of objects representing all items and chests
    room_list: list[str] = field(default_factory=list) # List of objects representing all rooms
    command_list: list[object] = ( # List of objects representing the player commands
        Look("look", ["look", "l"], 0),
        Check("check", ["check", "c"], 1),
        Take("take", ["take", "t"], 1),
        Walk("walk", ["walk", "w", "move", "m"], 1),
        Speak("speak", ["speak", "s"], 1),
        Use("use", ["use", "u"], 2),
        Place("place", ["place", "p"], 2)
        ) 
    
    
    #* Reset
    #* Sets starting values for new game
    #* self.object list is set twice because chest list needs to see item list while initializing 
    #*####################
    def reset(self, game) -> None:      
        object_list = []
        for item in self.list_builder("items", game) :object_list.append(item)
        self.object_list = object_list
        for chest in self.list_builder("chests", game): object_list.append(chest)
        self.object_list = object_list
        self.room_list = self.list_builder("rooms", game)     
    
    
    #* List Builder
    #* Accesses json file and returns list of objects
    #* Chest and Room lists are configured to have the appropriate objects in their inventory
    #*####################
    def list_builder(self, obj_type: str, game: object) -> list:
        #* obj_type (str): Will be either "items", "chests"
   
        list_builder = []
        with open("assets/"+str(obj_type)+".json", "r") as file:
            data = json.load(file)
        if obj_type == "items":
            for item in data: list_builder.append(Item(**item)) # Create an Item in list_builder for each json object
            return list_builder
        for item in data:
            if obj_type == "chests":
                list_builder.append(Chest(**item)) # Create a Chest in list_builder for each json object
            if obj_type == "rooms":
                list_builder.append(Room(**item)) # Create a Room in list_builder for each json object
            outer_obj = list_builder[-1] # Reference last object created
            for name in outer_obj.inventory: # Iterate throught "Inventory" dict for each chest/item listed in object inventory
                inner_obj = game.locate_object(name) # Fetch all relevant objects
                if inner_obj != -1:
                    outer_obj.inventory[name] = inner_obj # If object found, add to dict
        return list_builder   


#* Room
#*####################
@dataclass
class Room:
    name: str
    state: str
    looktext_dict: dict
    inventory: dict
    

#* Game Objects
#*####################
@dataclass(kw_only=True)
class GameObject:
    name: str # Name of the object
    checkable: bool # Does the object respond to the check command
    key: dict # What items/actions interact with the object
    state: str # What state the object is in
    checktext_dict: dict # Contains all text which might be used for the check command
    useable: bool # Does the object respond to the use command
    visible: bool # Is the object accessible to the player
    
    
    #* Try Key
    #* Takes in a prospective key and if that key is valid for the object, passes the trigger block into triggers function
    #*####################
    def try_key(self, prosp_key: str, game: object) -> None:
        #* prosp_key (str): Name of an object/action to be checked against list of keys
        
        if prosp_key in self.key:
            self.triggers(self.key[prosp_key],game)
            del self.key[prosp_key] # Removes key from list after triggering
            
   
    #* Triggers
    #* Parses trigger block and executes changes, running prospect ext triggers through try_key
    #*####################
    def triggers(self, trigger: dict, game: object) -> None:
        #* trigger (dict): Block of triggers to be executed
        
        self.state = trigger["state"] # Set state of object
        game.player.turn_text.extend(game.text_fetcher("triggers", self.name, trigger["trigger_text"])) # Display any text for this trigger
        for attr in trigger["attr_changes"]: # update object attributes ie visible, takeable
            setattr(self, attr, trigger["attr_changes"][attr]) 
        for prosp in trigger["ext_triggers"]: # Checks for external triggers
            if prosp != "none" and prosp != "player_inv": 
                obj = game.locate_object(prosp)
                obj.try_key(trigger["ext_triggers"][prosp], game) # Runs prospect ext triggers through try_key
            if prosp == "player_inv": # Modifies player inv when called for by an ext trigger
                for line in trigger["ext_triggers"][prosp]:
                    if line == 'add':
                        game.player.inventory.append(trigger["ext_triggers"][prosp][line])
                    if line == 'del':
                        game.player.inventory.remove(trigger["ext_triggers"][prosp][line])
    
                
#* Chests
#*####################
@dataclass(kw_only=True)
class Chest(GameObject):
    inventory: dict # Items held in this chest
        

#* Items
#*####################
@dataclass(kw_only=True)
class Item(GameObject):
    takeable: bool
        