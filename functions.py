"""
Unnamed Text Adventure - Functions
Written by Canahedo and WingusInbound
Python3
2024

This file contains all primary functions for the game
"""

from icecream import ic
import os  # Used in clear() to erase the board
import time  # Used in sleep() to create a delay
import json

from commands import Command
from assets.text.misc_gametext import *


# Creates clear() to erase the board
def clear():
    os.system("cls")


#*###################
#*## DEBUG TOGGLE ###
#*###################
#* Set to False, True, or "verbose"
DEBUG = False
#DEBUG = True
#DEBUG = "verbose"


class Game_Functions():
    def __init__(self, game_data: object, player: object):
        self.data = game_data
        self.player = player

    
    #* Run
    #* Start of new game. Resets values for game and player data and runs game loop
    #*####################
    def run(self) -> None:
        self.data.reset(self)
        self.player.reset(self)
        self.draw_ui()
        print(opening_crawl_text)
        while True:
            self.game_loop()
          
            
    #* Draw UI
    #* Wipes screen, and displays title bar and player inventory
    #*####################
    def draw_ui(self) -> None:   
        if DEBUG:
            print("-------------------------")
            print("-------------------------")
            print("DEBUG MODE")
            print(DEBUG)
        if DEBUG != "verbose": #* DEBUG: Disables screen wipe when DEBUG     
            clear() # Erases screen before redrawing UI, disabled in verbose DEBUG
            print(game_title)
        print("You are carrying the following: ")
        # Formats inventory  
        if len(self.player.inventory) != 0:
            for item in self.player.inventory:
                print(str(item.name), end=" ")
                if len(self.player.inventory) != self.player.inventory.index(item) + 1:
                    print(", ", end="")
        print("\n\n-------------------------\n")
        
    
    #* Game Loop
    #* Requests input, runs it through handler, executes command, and displays text
    #*####################
    def game_loop(self) -> None:
        while True:
            
            time.sleep(.5)
            command, mod1, mod2, mod_strs = self.input_handler(input("\nWhat do you do next?\n")) # Request input
            try:
                self.player.take_turn(command, mod1, mod2, self)
            # except Exception as e:
            #     print(e)    
            # else:    
                self.draw_ui()
                print(f"PREV COMMAND:",command.name, end="")
                for mod in mod_strs:
                    if mod != "none":
                        print(f"",mod, end="")
                print("\n")
                for line in self.player.turn_text:
                    print(line)                
            finally:
                pass
            
 
    #* Input Handler
    #* Cleans player input, checks for and runs system commands, and locates/returns objects for commands and mods
    #* Returns command object, mod objects (if found, returns -1 if not), and player_input list
    #*####################
    def input_handler(self, raw_input): # -> object, object, object, list
        #* raw_input (str): Raw player input
        
        player_input = raw_input.strip().lower().split()  # Turns player input into list of words
        if len(player_input) == 0: # Restarts game loop if no text entered
            print("Enter a valid command\n") 
            self.game_loop() 
        comm = player_input.pop(0)
        
        #! Remove this eventually, here for testing
        if comm == "x": #if x entered as a command, display object for mod1
            ic(self.locate_object(player_input[0]))
            self.game_loop()
        if comm == "g": #if g entered as a command, display whole game object
            ic(self.data)
            ic(self.player)
            self.game_loop()    
        
        # Checks for system commands
        if comm in ["quit", "q"] and self.double_check("quit and close the program? y/n"):
                exit() # Close program
        if comm in ["end", "e"] and self.double_check("end the current game? y/n"):
                self.replay() # End current game, offer replay
        if comm in ["r", "restart", "reboot"] and self.double_check("restart the game? y/n"):
                self.run() # Restart game
        if comm in ["h", "help", "tutorial"]: # Displays help screen
            self.draw_ui()
            with open("assets/text/tutorial.md", "r") as file:
                file_contents = file.read()
            print(file_contents, "\n")
            self.game_loop()   
        comm_obj = self.locate_command(comm, player_input) # Find command object
        if not isinstance(comm_obj, Command):# If command not valid, restart game loop
                print(comm_obj)
                self.game_loop() 
        while len(player_input) < 2: # Fills mods slots for commands with < 2 mods so downstream functions get enough args
            player_input.append("none") 
        mod1_obj = self.locate_object(player_input[0])
        mod2_obj = self.locate_object(player_input[1])        
        return comm_obj, mod1_obj, mod2_obj, player_input
    
    
    #* Locate Object
    #* Finds item, chest, or room objects called on by player or triggers
    #* Returns object, or -1 if no object found
    #*####################
    def locate_object(self, obj: str): # -> object
        #* obj (str): Name of object or room to be located    
    
        ob = obj[:-1] # Also tests without last letter, in case of pluralization
        for i in self.data.object_list:
            if i.name == obj or i.name == ob:
                return i
        for room in self.data.room_list:
            if room.name == obj:
                return room
        return -1


    #* Locate Command
    #* Finds command object, and verifies number of mods
    #* Returns object, or error string
    #*####################
    def locate_command(self, comm: str, player_input: list): # -> object
        #* comm (str): Name of command to be located
        #* player_input (list[str]): List of player-entered mods
        
        for obj in self.player.command_list: # Compare input to list of accepted commands
            if comm in obj.alias:
                if len(player_input) == obj.num_mods: # Confirms if correct number of mods were entered
                    return obj
                # Error if command accepted but wrong number of mods
                num_error = str(obj.name)+" requires exactly "+str(obj.num_mods)+" modifier" # Creates error message
                if obj.num_mods != 1: num_error = num_error + 's' # Adds an 's' to end of error if num_mods == 0 or 2
                return (num_error.capitalize())
        return ("Enter a valid command") # Error if command not recognized  
    
    
    #* Text Fetcher
    #* Searches json files for text to display to the player, and returns that text.
    #*####################
    def text_fetcher(self, file_name: str, name: str, index: str) -> list:
        #* file_name (str): Chooses which json file to search
        #* name (str): Name of object to be found
        #* index (str): Which line of text to use
   
        text = []
        with open("assets/text/"+str(file_name)+".json", "r") as file:
            data = json.load(file)
            for item in data:
                if name == item["name"]:
                    text = item[index]
                    break
        return text
    
   
    #* You see a...
    #* Accepts either local chest or item list, and tells the player what they see
    #*#################### 
    def you_see_a(self, local_list: list[object]) -> list[str]:
        counter = 0
        uca = "Nearby, you see "
        ic(local_list)
        for obj in local_list:
            ic(local_list)
            if obj.name[0] in ["a","e","i","o","u"]:
                uca += "an "    
            else:
                uca += "a "
            uca += obj.name
            counter += 1
            if counter < len(local_list):
                uca +=", "
            if counter == len(local_list) - 1:
                uca += "and "
            if counter == len(local_list):
                uca += "\n"
        return [uca]
                

    #* End Game
    #* Displays end of game text and triggers replay()
    #! Not currently in use
    #*####################
    def end_game(self) -> None:
        print("Congratulations!")
        print("    You Win!    ")
        return self.replay()


    #* Replay
    #* Asks the player if they want to play again                           
    #*####################
    def replay(self) -> None:
        while True:
            time.sleep(0.5)
            response = input("\nWould you like to play again? y/n\n").lower()
            if response in ['y', 'yes']:
                self.run()
            elif response in ['n', 'no']:
                exit()
            else:
                print('Sorry, "', response, '" is an invalid response.')
                

    #* Double Check
    #* Confirms system commands before running (quit, end, restart)                           
    #*####################
    def double_check(self, string: str) -> bool:
        while True:
            time.sleep(0.5)
            response = input(f"\nAre you sure you want to "+string+"\n").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                self.game_loop()
            else:
                print('Sorry, "', response, '" is an invalid response.')
                