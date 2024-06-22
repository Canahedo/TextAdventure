"""
Unnamed Text Adventure - SetupGame
Written by Canahedo and WingusInbound
Python3
2024

Initializes player and data objects and delivers to game via main
"""

import json
from gamefiles.objects import Item, Chest, Room, Gate
from gamefiles.commands import build_command_list
from gamefiles.assets.text.misc_gametext import opening_crawl_text


# *
# * Setup Wizard
# *####################
class SetupWizard:
    def __init__(self, data, player, services):
        self.data = data
        self.player = player
        self.serv = services
        self.build_lists()
        for room in self.data.room_list:
            self.adjoin_rooms(room)
            self.place_objects(room)
        self.player_setup()

    def build_lists(self):
        self.data.item_list = ItemList("items").load()
        self.data.chest_list = ChestList("chests").load()
        self.data.room_list = RoomList("rooms").load()
        self.data.gate_list = GateList("gates").load()

    def adjoin_rooms(self, room: object):
        for direction in room.routes:
            adj = room.routes[direction]

            # Connect rooms
            foo = self.serv.findobj(adj["room"], self.data.room_list)
            room.routes[direction]["room"] = foo

            # Setup gates
            if adj["gate"] != "none":
                foo = self.serv.findobj(adj["gate"], self.data.gate_list)
                room.routes[direction]["gate"] = foo

    def place_objects(self, room: object):

        # Place Chests
        if room.inventory == "none":
            return
        for chest in room.inventory:
            chest_obj = self.serv.findobj(chest, self.data.chest_list)
            if chest_obj is not None:
                room.inventory[chest] = chest_obj

                # Place Items
                if chest_obj.inventory == "none":
                    continue
                for item in chest_obj.inventory:
                    item_obj = self.serv.findobj(item, self.data.item_list)
                    chest_obj.inventory[item] = item_obj

    def player_setup(self):
        self.player.inventory.clear()
        letter = self.serv.findobj("letter", self.data.item_list)
        driveway = self.serv.findobj("driveway", self.data.room_list)
        self.player.inventory.append(letter)
        self.player.location = driveway
        self.player.turn_text = [opening_crawl_text]
        self.player.command_list = build_command_list()


# *
# * List Builder
# *####################
class ListBuilder:
    def __init__(self, obj_type: str):
        self.obj_type = obj_type
        self.obj_list = []

    def load(self):
        with open(f"gamefiles/assets/{str(self.obj_type)}.json", "r") as file:
            file_contents = json.load(file)
        for obj in file_contents:
            self(obj)
        return self.obj_list


class ItemList(ListBuilder):
    def __call__(self, obj):
        self.obj_list.append(Item(**obj))


class ChestList(ListBuilder):
    def __call__(self, obj):
        self.obj_list.append(Chest(**obj))


class RoomList(ListBuilder):
    def __call__(self, obj):
        self.obj_list.append(Room(**obj))


class GateList(ListBuilder):
    def __call__(self, obj):
        self.obj_list.append(Gate(**obj))
