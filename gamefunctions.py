"""
Unnamed Text Adventure - Game
Written by Canahedo and WingusInbound
Python3
2024

This file contains the primary functions which run the game
"""

# Imports
import time  # Used in sleep() to create a delay
from icecream import ic
from gameobjects import *
from gametext import *
from commands import *
from systemfunctions import *


game = Game([], [], [], [], [], "")

 
#*#####################
#*### Input Handler ###
#*#####################
# Converts player input into usable form
# Returns (command, [mods]) if input accepted or (-1, error) if not
def input_handler(raw_input):
    mods = raw_input.strip().lower().split()  # Turns player input into list of words
    if len(mods) == 0: return (-1,"Enter a valid command") # Prevents error if no text entered
    player_command = mods.pop(0)  # Turns first word into command, leaves rest as mods
    for command in command_list: # Compare input to list of accepted commands
        if player_command in command.alias:
            if len(mods) != command.num_mods: # Error if command accepted but wrong number of mods
                num_error = str(command.name)+" requires exactly "+str(command.num_mods)+" modifier" # Creates error message
                if command.num_mods != 1: num_error = num_error + 's' # Adds an 's' to end of error if num_mods == 0 or 2
                return (-1, num_error.capitalize())
            if len(mods) == 0: mods = [""] # Prevents error when command used with no mods
            return (command.name, mods) # * Success Condition
        
        
#*#################        
#*### Run Game ###        
#*#################      
# Sets up game, prompts for input, directs functions
def run_game():
    game.new_game()
    draw_ui(game)
    print(opening_crawl_text)
    while True:
        time.sleep(1)
        player_input = input_handler(input("What do you do next?\n")) # Request input, convert to (command, ["mods"])
        player_command: str = player_input[0]
        player_mods: list = player_input[1]
        if len(player_mods) == 0:    
            if player_command in ["quit", "q"]: return False
            if player_command in ["end", "e", "restart", "r"]: return replay()
            if player_command == "help": help()
            if player_command == "look": game.look()
        if len(player_mods) == 1:
                for obj in game.object_list:
                    if obj.name == player_mods[0]:
                        if player_command == "check": obj.check(game)
                        if player_command == "take": obj.take(game)
                        if player_command == "walk": game.walk()
                        if player_command == "speak": obj.speak()


#*##############
#*### Replay ###
#*##############                            
# Asks the player if they want to play again
def replay():
    while True:
        time.sleep(0.5)
        response = input("Would you like to play again? y/n\n\n").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            clear()
            print('Sorry, "', response, '" is an invalid response.')            
              
                        
                        
                        
        
        
        
        
