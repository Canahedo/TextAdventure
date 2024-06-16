"""
Unnamed Text Adventure - Functions
Written by Canahedo and WingusInbound
Python3
2024

This file contains all primary functions for the game
"""

import sys
import time  # Used in sleep() to create a delay
import json
from gamefiles.errors import CommandNotFound, NumberOfMods


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
        running = "Start Game"
        while running != "End Game":
            raw_input = input("What do you do next?\n")
            comm_str, mod_strs = self.input_handler(raw_input)
            running = self.game_loop(comm_str, mod_strs)
        self.end_game()

    # * Input Handler
    # * Requests player input
    # * Formats input an attatches to player object
    # *####################
    def input_handler(self, raw_input):
        time.sleep(0.5)
        player_input = raw_input.strip().lower().split()
        if len(player_input) == 0:  # Restarts game loop if no text entered
            print("Enter a valid command\n")
            self.game_loop()
        comm_str = player_input.pop(0)
        return comm_str, player_input

    # * Game Loop
    # * Represents a single turn
    # * Takes cleaned input, finds object,
    # *     verifies turn, and runs player command
    # *####################
    def game_loop(self, comm_str: str, mod_strs: list[str]) -> str:

        if not self.fetch_objects_for_turn(comm_str, mod_strs):
            return "ERROR: Object Fetch Failed"
        comm_obj, mod_list = self.player.comm_obj, self.player.mod_objs

        # * Confirms that player turn can be executed
        valid_turn, message = comm_obj.verify(mod_list, self)

        if not valid_turn:
            if message == "system":
                print("")
                return "ERROR: System Command"

            print(f"\nInvalid turn: {comm_obj.name}", end="")
            for mod in mod_list:
                print(f" {mod.name}", end="")
            print(f"\n{message}")
            return "ERROR: Invalid Turn"

        # * Processes turn and redraws screen
        self.player.turn_text.clear()
        comm_obj(mod_list, self)  # Calls command object
        self.player.get_locals()

        self.services.draw_ui(self.player)
        return "Turn Executed Successfully"

    # * Fetch Objects For Turn
    # * Attempts to retrieve objects for command and relevant mods
    # *####################
    def fetch_objects_for_turn(self, comm_str, player_input) -> bool:
        mod_list = []
        for mod in player_input:
            mod_obj = self.locate_object(mod)
            if mod_obj is None:
                print(f'"{mod}" is not a not recognized term')
                print("Try something else")
            else:
                mod_list.append(mod_obj)
        if len(mod_list) != len(player_input):
            return False
        else:
            try:
                comm_obj = self.locate_command(comm_str, len(mod_list))
            except CommandNotFound as e:
                print(e.message)
                return False
            except NumberOfMods as e:
                print(e.message)
                return False
            self.player.comm_obj = comm_obj
            self.player.mod_objs = mod_list
            return True

    # * Locate Object
    # * Finds and returns item, chest, or room objects
    # *####################
    def locate_object(self, obj: str) -> object:
        # * obj (str): Name of object or room to be located

        ob = obj[:-1]  # Also tests without last letter
        for i in self.data.room_list:
            if i.name == obj:
                return i
        for i in self.data.object_list:
            if i.name == obj or i.name == ob:
                return i

    # * Locate Command
    # * Finds command object, and verifies number of mods
    # * Returns object, or error string
    # *####################
    def locate_command(self, comm_str: str, num_of_mods: int) -> object:
        # * comm (str): Name of command to be located
        # * player_input (list[str]): List of player-entered mods

        for obj in self.player.command_list:
            if comm_str in obj.alias:
                # Confirms if correct number of mods were entered
                if num_of_mods == obj.num_mods:
                    return obj
                # Error if command accepted but wrong number of mods
                raise NumberOfMods(obj.name, obj.num_mods)
        raise CommandNotFound(comm_str)

    # * Text Fetcher
    # * Searches json files for text to display, and returns that text.
    # *####################
    def text_fetcher(self, file: str, name: str, index: str) -> list:
        # * file_name (str): Chooses which json file to search
        # * name (str): Name of object to be found
        # * index (str): Which line of text to use

        text = []
        with open("gamefiles/assets/text/" + str(file) + ".json", "r") as f:
            data = json.load(f)
            for item in data:
                if name == item["name"]:
                    text = item[index]
                    break
        return text

    # * End Game
    # * Displays end of game text and triggers replay()
    # *####################
    def end_game(self) -> None:
        print("Congratulations!")
        print("    You Win!    ")
        return self.replay()

    # * Replay
    # * Asks the player if they want to play again
    # *####################
    def replay(self) -> None:
        while True:
            time.sleep(0.5)
            response = input("\nWould you like to play again? y/n\n").lower()
            if response in ["y", "yes"]:
                self.run()
            elif response in ["n", "no"]:
                sys.exit()
            else:
                print('Sorry, "', response, '" is an invalid response.')
