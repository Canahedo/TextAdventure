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



####################
### Game Objects ###
####################

class GameObject:
    def __init__(self, name, checkable, checktext_dict, useable, moveable):
        self.name = name
        self.checkable = checkable
        self.checktext_dict = checktext_dict
        self.useable = useable
        self.moveable = moveable
    
    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)     
    
    def check(self):
        print("Checking...")
        print(len(self.checktext_dict))
        print(self.checktext_dict['unchecked'])
        
        
##############
### Chests ###
##############
#Chest(name, chest_inventory, checkable, checktext_dict, useable, moveable)
class Chest(GameObject):
    def __init__(self, name, chest_inventory, checkable, checktext_dict, useable, moveable) -> None:
        super().__init__(name, checkable, checktext_dict, useable, moveable)
        self.chest_inventory = chest_inventory

# init_chests       
chest_list = []
def init_chests():
    with open("assets/chests.json", "r") as file:
        data = json.load(file)
        for chest in data:
            chest_list.append(Chest(**chest))



#############
### Items ###
#############
#Item(name, checkable, checktext, takeable, useable, moveable)
class Item(GameObject):
    def __init__(self, name, checkable, checktext, takeable, useable, moveable) -> None:
        super().__init__(name, checkable, checktext, useable, moveable)
        self.takeable = takeable
        
# init_items    
item_list = []
def init_items():
    with open("assets/items.json", "r") as file:
        data = json.load(file)
        for item in data:
            item_list.append(Item(**item))


# Create object_list
object_list = chest_list
for item in item_list:
    object_list.append(item)