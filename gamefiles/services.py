"""
Unnamed Text Adventure - Services
Written by Canahedo and WingusInbound
Python3
2024

This file contains various subfunctions of the game
"""

import os
import time
from gamefiles.commands import Command
from gamefiles.assets.text.misc_gametext import game_title


class Services:
    def __init__(self):
        pass

    def draw_ui(self, player):

        # Erase screen, print title
        os.system("clear||cls")
        print(game_title)

        # Previous Command
        if isinstance(player.comm_obj, Command):
            print(f"\nPREVIOUS COMMAND: {player.comm_obj.name}", end="")
            for obj in player.mod_objs:
                print(f" {obj.name}", end="")
            print("\n")
            print("-------------------------")

        # Turn text
        for line in player.turn_text:
            print(line)
        print("-------------------------\n")

        # Player
        print(f"You are in the {player.location.name}\n")
        if len(player.local_rooms) > 0:
            print("From here, you can get to:")
            self.print_list(player.local_rooms)
        if len(player.inventory) > 0:
            print("You are carrying:")
            self.print_list(player.inventory)
        local_objs = player.local_chests
        local_objs.extend(player.local_items)
        if len(local_objs) > 0:
            print("Nearby, you can see:")
            self.print_list(local_objs)

    def print_list(self, object_list: list[str]):
        if len(object_list) > 0 and object_list != [None]:
            string = ""
            counter = 0
            for obj in object_list:
                if obj.name[0] in ["a", "e", "i", "o", "u"]:
                    string += "an "
                else:
                    string += "a "
                if counter == 0:
                    string.capitalize()
                string += obj.name
                counter += 1
                if counter < len(object_list):
                    string += ", "
                if counter == len(object_list) - 1:
                    string += "and "
            print(f"{string}\n")

    def double_check(self, string: str) -> bool:
        while True:
            time.sleep(0.5)
            response = input(f"\nAre you sure you want to {string}\n").lower()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print('Sorry, "', response, '" is an invalid response.')
