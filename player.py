"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

This file contains a class which records info about a player turn
"""

from dataclasses import dataclass, field

from commands import Look, Check, Take, Walk, Speak, Use, Place


@dataclass
class Player:
    inventory: list[object] = field(default_factory=list)
    location: object = field(default_factory=object)
    turn_text: list[str] = field(default_factory=list)
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
    )

    def reset(self, game):
        self.inventory.clear()
        self.inventory.append(game.locate_object("letter"))
        self.location = game.locate_object("driveway")
        self.get_locals()

    def get_locals(self):
        self.local_chests.clear()
        self.local_items.clear()
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
