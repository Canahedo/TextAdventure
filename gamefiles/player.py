"""
Unnamed Text Adventure - Player
Written by Canahedo and WingusInbound
Python3
2024

Stores data about the player and the turn
"""

from dataclasses import dataclass, field


@dataclass
class Player:
    inventory: list[object] = field(default_factory=list)
    location: object = field(default_factory=object)
    turn_text: list[str] = field(default_factory=list)
    local_rooms: list[object] = field(default_factory=list)
    local_gates: list[object] = field(default_factory=list)
    local_dirs: list[str] = field(default_factory=list)
    local_items: list[object] = field(default_factory=list)
    comm_obj: object = field(default_factory=object)
    mod_objs: list[object] = field(default_factory=list)
    command_list: list[object] = field(default_factory=list)
