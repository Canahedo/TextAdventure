"""
Unnamed Text Adventure - Game
Written by Canahedo and WingusInbound
Python3
2024

This file contains the primary functions which run the game
"""

# import os  # Used in clear() to erase the board
# import time  # Used in sleep() to create a delay
# import json
# from icecream import ic
# from dataclasses import dataclass

# from gametext import *
# from systemfunctions import *
# from gameobjects import *

from commands import *


game = Game([], [], [], [], [], "")


#*########################
#*##  Tutorial Prompt  ###
#*########################
#Offers to show Help screen at start of first game
def tutorial_prompt():
    print("Welcome to our game", "\nThank you for playing\n")
    print('Enter "H" to view the Help Screen, or "S" to skip\n')
    print("You can ask for help at any time once you are in the game\n")
    while True:
        time.sleep(0.5)
        tutorial = (input().strip().lower())  # Requests player input, removes leading/trailing whitespace, sets lowercase
        if tutorial in ["tutorial", "t", "help", "h"]:
            help()
            input("Press Enter to Continue\n\n")
            break
        elif tutorial in ["start", "s", ""]:
            break
        else:
            print(f'Sorry, "',{tutorial},'" is an invalid response\n')
    draw_ui(game)
            

#*############
#*### Help ###
#*############
# Represents the tutorial screen, which is also used when the player enters the help command
def help(*args):
    draw_ui(game)
    with open("assets/help.md", "r") as file:
        file_contents = file.read()
    print(file_contents, "\n")


#*#####################
#*### Input Handler ###
#*#####################
# Converts player input into usable form
# Returns (command, [mods]) if input accepted or (-1, error) if not
def input_handler(raw_input): # -> (str, list)
    if DEBUG: 
        ic()
        ic(raw_input)
    mods = raw_input.strip().lower().split()  # Turns player input into list of words
    if len(mods) == 0: return (-1,"Enter a valid command") # Prevents error if no text entered
    player_command = mods.pop(0)  # Turns first word into command, leaves rest as mods
    for command in command_list: # Compare input to list of accepted commands
        if player_command in command.alias:
            if len(mods) != command.num_mods: # Error if command accepted but wrong number of mods
                num_error = str(command.name)+" requires exactly "+str(command.num_mods)+" modifier" # Creates error message
                if command.num_mods != 1: num_error = num_error + 's' # Adds an 's' to end of error if num_mods == 0 or 2
                return (-1, num_error.capitalize())
            if len(mods) == 0: mods = [""] # Prevents error when command used correctly with no mods
            if DEBUG: 
                ic()
                ic(command.name, mods)
            return (command.name, mods) # * Success Condition
    if DEBUG: ic(player_command, mods)
    return (-1,"Enter a valid command") # Error if command not recognized    
        
        
#*################        
#*### Run Game ###        
#*################      
# Sets up game, prompts for input, directs functions
def run_game():
    game.new_game()
    draw_ui(game)
    if not DEBUG:
        tutorial_prompt()
    print(opening_crawl_text)
    while True:
        time.sleep(.5)
        player_input = input_handler(input("What do you do next?\n")) # Request input, convert to (command, ["mods"])   
        if DEBUG: 
            ic()
            ic(player_input)
        if player_input[0] == -1: #Displays error and restarts loop
            print(player_input[1])
            continue
        player_command: str = player_input[0]
        player_mod1: str = player_input[1][0]
        player_mod2: str = "" # Ensures second mod will be emptied on later loops
        if len(player_input[1]) == 2:
            player_mod2: str = player_input[1][1]
        draw_ui(game) 
        if player_mod1 == "":    
            if player_command == "quit": return False
            if player_command == "end": return replay()
            if player_command == "help": help()
            if player_command == "look": look(game)
            continue
        if player_mod2 == "":
            for obj in game.object_list:
                if obj.name == player_mod1:
                    if player_command == "check": check(obj)
                    if player_command == "take": take(obj, game)
                    if player_command == "walk": obj.walk(game)
                    if player_command == "speak": obj.speak(game)
        if player_mod2 != "":
            for obj in game.object_list:
                if (obj.name == player_mod2
                    and player_mod1 in obj.key):
                        if player_command == "use": obj.use(game, obj.key)
                        if player_command == "move": obj.move(game, obj.key)
                        if player_command == "place": obj.place(game, obj.key)
                        

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
              
