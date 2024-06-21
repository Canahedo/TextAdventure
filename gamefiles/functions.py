"""
Unnamed Text Adventure - Functions
Written by Canahedo and WingusInbound
Python3
2024

Contains the primary functions for the game
"""

import time  # Used in sleep() to create a delay
from gamefiles.subfunctions.setupwizard import SetupWizard

from gamefiles.errors import CustomException, ModNotFound
from gamefiles.errors import CommandNotFound, NumberOfMods, BlankInput


class Game_Functions:
    def __init__(self, game_data: object, player: object, services: object):
        self.data = game_data
        self.player = player
        self.services = services

    # * Run
    # * Start of new game.
    # * Resets values for data and player and runs game loop
    # *####################
    def run(self) -> None:
        SetupWizard(self.data, self.player, self.services)
        self.services.draw_ui(self.player)
        status = "New Game"
        while status != "GAME OVER":
            time.sleep(0.5)
            player_input = input("What do you do next?\n")
            status = self.game_loop(player_input)

            if "WIN" in status:
                print("   Congratulations!   ")
                print("       You Win!       \n")
                input("Press Enter To Continue")
                status = self.replay()

            if "RESTART" in status:
                self.run()
                status = "GAME OVER"

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
            comm_obj, mod_objs = self.player.comm_obj, self.player.mod_objs

            # Verifies turn can be completed
            comm_obj.verify(mod_objs, self)

        except CustomException as e:
            print(f"\nInvalid Input: {raw_input}")
            print(f"{e.message}")
            return e.return_string

        else:
            # Execute Turn
            self.player.turn_text.clear()
            turn_result = comm_obj(mod_objs, self)  # Calls command object
            self.services.draw_ui(self.player)

            # "GAME OVER", "WIN", "RESTART" will trigger different outcomes
            # Any other return will start another turn
            return turn_result

    # * Input Handler
    # * Formats raw player input and returns (string, list[str])
    # *####################
    def input_handler(self, raw_input: str) -> tuple[str, list[str]]:
        player_input = raw_input.strip().lower().split()
        if len(player_input) == 0:  # Error if no text entered
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
        local_lists = [
            self.player.local_rooms,
            self.player.local_chests,
            self.player.local_items,
            self.player.inventory,
        ]
        for mod in mod_strs:

            for lst in local_lists:
                obj = self.services.findobj(mod, lst)
                if obj is not None:
                    break
            if obj is None:
                raise ModNotFound(mod)
            mod_list.append(obj)
        self.player.mod_objs = mod_list

    # * Win Con
    # * Checks state of game each turn to see if player has won
    # *####################
    def win_con(self):
        # ! Replace with actual functionality
        # ! Returns true if player meets win con
        return False

    # * End Game
    # * Announces end of game, offers replay
    # *####################
    def end_game(self) -> None:
        print("Congratulations!")
        print("    You Win!    ")
        return self.replay()

    # * Replay
    # * Asks player if they want to play again
    # *####################
    def replay(self) -> None:
        while True:
            time.sleep(0.5)
            response = input("\nWould you like to play again? y/n\n").lower()
            if response in ["y", "yes"]:
                return "RESTART"
            elif response in ["n", "no"]:
                return "GAME OVER"
            else:
                print('Sorry, "', response, '" is an invalid response.')
