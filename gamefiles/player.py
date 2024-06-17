"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

This file contains a class which records info about a player turn
"""

from dataclasses import dataclass, field
from gamefiles.assets.text.misc_gametext import opening_crawl_text
from gamefiles.commands import Look, Check, Take, Walk, Speak, Use, Place
from gamefiles.commands import Quit, Restart, Tutorial, InspObj, InspGame


@dataclass
class Player:
    inventory: list[object] = field(default_factory=list)
    location: object = field(default_factory=object)
    turn_text: list[str] = field(default_factory=list)
    local_rooms: list = field(default_factory=list)
    local_chests: list[object] = field(default_factory=list)
    local_items: list[object] = field(default_factory=list)
    comm_obj: object = field(default_factory=object)
    mod_objs: list[object] = field(default_factory=list)
    command_list: list[object] = (
        Look("look", ["look", "l"], 0),
        Check("check", ["check", "c"], 1),
        Take("take", ["take", "t"], 1),
        Walk("walk", ["walk", "w", "move", "m"], 1),
        Speak("speak", ["speak", "s"], 1),
        Use("use", ["use", "u"], 2),
        Place("place", ["place", "p"], 2),
        Quit("quit", ["quit", "q"], 0),
        Restart("restart", ["restart", "r"], 0),
        Tutorial("help", ["tutorial", "help", "h"], 0),
        InspObj("inspobj", ["inspobj", "i"], 1),  # ! Debug command
        InspGame("inspgame", ["inspgame", "game", "g"], 0),  # ! Debug command
    )

    def reset(self, game):
        self.inventory.clear()
        self.inventory.append(game.services.locate_object("letter", game.data))
        self.location = game.services.locate_object("driveway", game.data)
        self.turn_text = [opening_crawl_text]
        self.get_locals(game)

    def get_locals(self, game):
        self.local_chests.clear()
        self.local_items.clear()
        self.local_rooms.clear()
        for chest in self.location.inventory:
            if chest == "none":
                continue
            if self.location.inventory[chest].visible:
                self.local_chests.append(self.location.inventory[chest])
                for item in self.location.inventory[chest].inventory:
                    if item == "none":
                        continue
                    prosp_item = self.location.inventory[chest].inventory[item]
                    if prosp_item.visible:
                        self.local_items.append(prosp_item)
        for direction in self.location.adjoining:
            room_name = None
            foo = self.location.adjoining[direction]
            if foo["door"] == "none":
                room_name = foo["room"]
            else:
                door_obj = game.services.locate_object(foo["door"], game.data)
                door_state = door_obj.state
                if door_state not in ["locked"]:
                    room_name = foo["room"]
            if room_name is not None:
                room_obj = game.services.locate_object(room_name, game.data)
                if room_obj.visible:
                    self.local_rooms.append(room_obj)
