"""
Unnamed Text Adventure - Objects
Written by Canahedo and WingusInbound
Python3
2024

This file represents the game data, including lists
of all items, chests, and rooms
"""

from dataclasses import dataclass, field
import json


# * Game Data
# * Lists containing game objects
# *####################
@dataclass
class Game_Data:
    object_list: list[str] = field(default_factory=list)
    room_list: list[str] = field(default_factory=list)
    door_list: list[str] = field(default_factory=list)

    # * Reset
    # * Sets starting values for new game
    # *####################
    def reset(self, game) -> None:
        object_list = []
        for item in self.list_builder("items", game.services):
            object_list.append(item)
        self.object_list = object_list
        for chest in self.list_builder("chests", game.services):
            object_list.append(chest)
        self.object_list = object_list
        self.room_list = self.list_builder("rooms", game.services)
        self.door_list = self.list_builder("doors", game.services)

    # * List Builder
    # * Accesses json file and returns list of objects
    # *####################
    def list_builder(self, obj_type: str, services: object) -> list:
        # * obj_type (str): Will be either "items", "chests", or "rooms"
        list_builder = []
        with open("gamefiles/assets/" + str(obj_type) + ".json", "r") as file:
            file_contents = json.load(file)
        if obj_type == "items":
            for item in file_contents:
                list_builder.append(Item(**item))
            return list_builder
        if obj_type == "doors":
            for item in file_contents:
                list_builder.append(Door(**item))
            return list_builder
        for item in file_contents:
            if obj_type == "chests":
                list_builder.append(Chest(**item))
            if obj_type == "rooms":
                list_builder.append(Room(**item))
            outer_obj = list_builder[-1]  # Reference last object created
            for name in outer_obj.inventory:
                if name is not None and name != "none":
                    inner_obj = services.locate_object(name, self)
                    outer_obj.inventory[name] = inner_obj
        return list_builder


# * Game Objects
# *####################
@dataclass(kw_only=True)
class GameObject:
    name: str  # Name of the object
    type: str  # Type of object (chest or item)
    checkable: bool  # Does the object respond to the check command
    key: dict  # What items/actions interact with the object
    state: str  # What state the object is in
    checktext_dict: dict  # Contains all text used for the check command
    useable: bool  # Does the object respond to the use command
    visible: bool  # Is the object accessible to the player

    # * Try Key
    # *####################
    def try_key(self, prosp_key: str, game: object) -> None:
        if prosp_key in self.key:
            self.triggers(self.key[prosp_key], game)
            del self.key[prosp_key]  # Removes key from list after triggering

    # * Triggers
    # *####################
    def triggers(self, trigger: dict, game: object) -> None:
        # * trigger (dict): Block of triggers to be executed

        # State
        self.state = trigger["state"]  # Set state of object

        # Trigger Text
        a, b, c = "triggers", self.name, trigger["trigger_text"]
        txt = game.services.text_fetcher(a, b, c)
        game.player.turn_text.extend(txt)

        # Attrs
        for attr in trigger["attr_changes"]:
            setattr(self, attr, trigger["attr_changes"][attr])

        # Ext Triggers
        for prosp in trigger["ext_triggers"]:  # Checks for external triggers
            if prosp != "none" and prosp != "player_inv" and prosp != "reveal":
                obj = game.services.locate_object(prosp, game.data)
                obj.try_key(trigger["ext_triggers"][prosp], game)
            if prosp == "player_inv":
                for line in trigger["ext_triggers"][prosp]:
                    new_item = trigger["ext_triggers"][prosp][line]
                    new_obj = game.services.locate_object(new_item, game.data)
                    if line == "add":
                        game.player.inventory.append(new_obj)
                    if line == "del":
                        game.player.inventory.remove(new_obj)
            if prosp == "reveal":
                for obj in trigger["ext_triggers"]["reveal"]:
                    target = game.services.locate_object(obj, game.data)
                    if target is not None:
                        target.visible = True


# * Chests
# *####################
@dataclass(kw_only=True)
class Chest(GameObject):
    inventory: dict  # Items held in this chest


# * Items
# *####################
@dataclass(kw_only=True)
class Item(GameObject):
    takeable: bool


# * Door
# *####################
@dataclass(kw_only=True)
class Door(GameObject):
    checkable: bool = False
    useable: bool = False
    checktext_dict: dict = field(default_factory=dict)


# * Room
# *####################
@dataclass(kw_only=True)
class Room(GameObject):
    useable: bool = False
    checkable: bool = False
    checktext_dict: dict = field(default_factory=dict)
    looktext_dict: dict
    adjoining: dict
    inventory: dict
