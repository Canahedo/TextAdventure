"""
Unnamed Text Adventure - Objects
Written by Canahedo and WingusInbound
Python3
2024

Stores data about the game and objects within it
"""

from dataclasses import dataclass, field


# * Game Data
# * Lists containing game objects
# *####################
@dataclass
class Game_Data:
    item_list: list[object] = field(default_factory=list)
    chest_list: list[object] = field(default_factory=list)
    room_list: list[object] = field(default_factory=list)
    gate_list: list[object] = field(default_factory=list)


# * Game Objects
# *####################
@dataclass(kw_only=True)
class GameObject:
    name: str  # Name of the object
    type: str  # Type of object
    key: dict  # What items/actions interact with the object
    state: str  # What state the object is in
    visible: bool  # Is the object accessible to the player


# * Placed Objects (Chests & Items)
# *####################
@dataclass(kw_only=True)
class PlacedObj(GameObject):
    checktext_dict: dict
    useable: bool
    checkable: bool


# * Chests
# *####################
@dataclass(kw_only=True)
class Chest(PlacedObj):
    inventory: dict  # Items held in this chest


# * Items
# *####################
@dataclass(kw_only=True)
class Item(PlacedObj):
    takeable: bool


# * Gate
# *####################
@dataclass(kw_only=True)
class Gate(GameObject):
    pass


# * Room
# *####################
@dataclass(kw_only=True)
class Room(GameObject):
    looktext_dict: dict
    routes: dict
    inventory: dict
    local: list[object]
