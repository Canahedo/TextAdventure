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
from turnvalidator import TurnValidator
from errors import CommandNotFound, ObjectNotFound, NumberOfMods, InvalidTurn
from assets.text.misc_gametext import *


# Creates clear() to erase the board
def clear():
    os.system("cls")


#*###################
#*## DEBUG TOGGLE ###
#*###################
#*
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
        if not DEBUG:
            clear() # Erases screen before redrawing UI, disabled in verbose DEBUG
        print(game_title)
        print("You are carrying the following: ")
        # Formats inventory  
        if len(self.player.inventory) != 0 and self.player.inventory != [None]:
            for item in self.player.inventory:
                print(str(item.name), end=" ")
                if len(self.player.inventory) != self.player.inventory.index(item) + 1:
                    print(", ", end="")
        print("\n\n-------------------------\n")
        
    
    #* Game Loop
    #* Primary loop of the game
    #* Requests input, retrieves objects, executes command, and displays text
    #*####################
    def game_loop(self) -> None:
        while True:
            
            #* Takes in player input
            time.sleep(.5)
            player_input = input("\nWhat do you do next?\n").strip().lower().split()  # Turns player input into list of words
            if len(player_input) == 0: # Restarts game loop if no text entered
                print("Enter a valid command\n")
                continue
            comm_str = player_input.pop(0)
            self.system_commands(comm_str) # Checks for and runs quit, end, restart, and help
                    
            #! Remove this eventually, here for testing
            if comm_str == "x": #if x entered as a command, display object for mod1
                ic(self.locate_object(player_input[0]))
                continue
            if comm_str == "g": #if g entered as a command, display whole game object
                ic(self.data)
                ic(self.player)
                continue
                
            #* Attempts to retrieve objects for command and relevant mods
            mod_list = []
            for mod in player_input:
                mod_obj = self.locate_object(mod)
                if mod_obj == None:
                    print(f"\"{mod}\" is not a not recognized term\nTry something else")
                else:    
                    mod_list.append(mod_obj)    
            if len(mod_list) == len(player_input):    
                try:
                    comm_obj = self.locate_command(comm_str, len(mod_list))
                except CommandNotFound as e:
                    print(e.message)
                    continue
                except NumberOfMods as e:
                    print(e.message)
                    continue                
            else:
                continue
            
            #* Confirms that player turn can be executed
            #! Temporarily bypassed
            if not TurnValidator(comm_obj, mod_list, self.data, self.player).result:
                raise InvalidTurn    
                continue
            
            #* Processes turn and redraws screen
            self.player.turn_text.clear()
            comm_obj(mod_list, self) # Uses callable trait of objects in command_list
            self.draw_ui()
            print(f"PREV COMMAND:",comm_obj.name, end="")
            for mod in mod_list:
                print(f"",mod.name, end="")
            print("\n")
            for line in self.player.turn_text:
                print(line)                
                     
    
    #* System Commands
    #* Looks for and runs game "system commands" ie quit, end, restart, and help
    #*####################
    def system_commands(self, command:str) -> None:
        if command in ["quit", "q"] and self.double_check("quit and close the program? y/n"):
                exit() # Close program
        if command in ["end", "e"] and self.double_check("end the current game? y/n"):
                self.replay() # End current game, offer replay
        if command in ["r", "restart", "reboot"] and self.double_check("restart the game? y/n"):
                self.run() # Restart game
        if command in ["h", "help", "tutorial"]: # Displays help screen
            self.draw_ui()
            with open("assets/text/tutorial.md", "r") as file:
                file_contents = file.read()
            print(file_contents, "\n")
            self.game_loop()

 
    #* Locate Object
    #* Finds and returns item, chest, or room objects called on by player or triggers
    #*####################
    def locate_object(self, obj: str) -> object:
        #* obj (str): Name of object or room to be located    

        ob = obj[:-1] # Also tests without last letter, in case of pluralization
        for i in self.data.object_list:
            if i.name == obj or i.name == ob:
                return i
        for i in self.data.room_list:
            if i.name == obj:
                return i        

    #* Locate Command
    #* Finds command object, and verifies number of mods
    #* Returns object, or error string
    #*####################
    def locate_command(self, comm_str: str, num_of_mods: int) -> object: 
        #* comm (str): Name of command to be located
        #* player_input (list[str]): List of player-entered mods
        
        for obj in self.player.command_list: # Compare input to list of accepted commands
            if comm_str in obj.alias:
                if num_of_mods == obj.num_mods: # Confirms if correct number of mods were entered
                    return obj
                raise NumberOfMods(obj.name,obj.num_mods)# Error if command accepted but wrong number of mods
        raise CommandNotFound(comm_str)  
     
    
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
                