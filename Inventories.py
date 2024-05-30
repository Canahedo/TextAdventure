"""
Unnamed Text Adventure - Inventories
Written by Canahedo and WingusInbound
Python3
2024

This file contains the inventories and location of the player
as well as various NPCs and containers
"""

player_inventory = []
player_stats = {"room": "None"}

rooms_full_list = ["driveway", "porch"]


def init_inventories():
    player_stats.update({"room": "driveway"})
    player_inventory.clear()
    player_inventory.append("letter")
