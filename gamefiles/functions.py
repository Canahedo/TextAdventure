"""
Unnamed Text Adventure - Functions
Written by Canahedo and WingusInbound
Python3
2024

This file contains all primary functions for the game
"""

import time  # Used in sleep() to create a delay
from gamefiles.errors import CustomException, ObjectNotFound
from gamefiles.errors import CommandNotFound, NumberOfMods, BlankInput


class Game_Functions:
    def __init__(self, services: object, game_data: object, player: object):
        self.services = services
        self.data = game_data
        self.player = player

    # * Run
    # * Start of new game.
    # * Resets values for game and player data and runs game loop
    # *####################
    def run(self) -> None:
        self.data.reset(self)
        self.player.reset(self)
        self.services.draw_ui(self.player)
        running = "New Game"
        while running != "Game Over":
            time.sleep(0.5)
            player_input = input("What do you do next?\n")
            running = self.game_loop(player_input)
        self.services.end_game(self)

    # * Game Loop
    # * Represents a single turn
    # * Takes raw input, finds objects,
    # *     verifies turn, and runs player command
    # *####################
    def game_loop(self, raw_input: str) -> str:
        try:
            # Format player input
            comm_str, mod_strs = self.input_handler(raw_input)

            # Store objects in game.player
            self.locate_command(comm_str, len(mod_strs))
            self.locate_mods(mod_strs)
            comm_obj, mod_list = self.player.comm_obj, self.player.mod_objs

            # Verifies turn can be completed
            comm_obj.verify(mod_list, self)

        except CustomException as e:
            print(f"\nInvalid Input: {raw_input}")
            print(f"{e.message}")
            return e.return_string

        else:
            # Execute Turn
            self.player.turn_text.clear()
            comm_obj(mod_list, self)  # Calls command object
            self.player.get_locals(self)
            self.services.draw_ui(self.player)
            return "Turn Executed Successfully"

    # * Input Handler
    # * Formats raw player input and returns string, list[str]
    # *####################
    def input_handler(self, raw_input: str) -> tuple[str, str]:
        player_input = raw_input.strip().lower().split()
        if len(player_input) == 0:  # Restarts game loop if no text entered
            raise BlankInput
        comm_str = player_input.pop(0)
        return comm_str, player_input

    # * Locate Command
    # * Finds command object, and verifies number of mods
    # *####################
    def locate_command(self, comm_str: str, num_of_mods: int) -> None:
        # * comm_str (str): Name of command to be located
        # * num_of_mods (int): Number of mods entered by player
        for obj in self.player.command_list:
            if comm_str in obj.alias:
                # Confirms if correct number of mods were entered
                if num_of_mods == obj.num_mods:
                    self.player.comm_obj = obj
                    return
                # Error if command accepted but wrong number of mods
                raise NumberOfMods(obj.name, obj.num_mods)
        raise CommandNotFound(comm_str)

    # * Locate Mods
    # * Retrieves objects related to player mods
    # *####################
    def locate_mods(self, mod_strs) -> None:
        mod_list = []
        for mod in mod_strs:
            mod_obj = self.services.locate_object(mod, self.data)
            if mod_obj is not None:
                mod_list.append(mod_obj)
            else:
                raise ObjectNotFound(mod)
        self.player.mod_objs = mod_list
