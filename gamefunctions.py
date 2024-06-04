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

# #*########################
# #*##  Tutorial Prompt  ###
# #*########################
# #Offers to show Help screen at start of first game
# def tutorial_prompt(game):
#     print("Welcome to our game", "\nThank you for playing\n")
#     print('Enter "H" to view the Help Screen, or "S" to skip\n')
#     print("You can ask for help at any time once you are in the game\n")
#     while True:
#         time.sleep(0.5)
#         tutorial = (input().strip().lower())  # Requests player input, removes leading/trailing whitespace, sets lowercase
#         if tutorial in ["tutorial", "t", "help", "h"]:
#             tutorial(game)
#             input("Press Enter to Continue\n\n")
#             break
#         elif tutorial in ["start", "s", ""]:
#             break
#         else:
#             print(f'Sorry, "',{tutorial},'" is an invalid response\n')
#     draw_ui(game)
            

#*#####################
#*### Input Handler ###
#*#####################
# Converts player input into usable form
# Returns (command, [mods]) if input accepted or (-1, error) if not
def input_handler(raw_input): # -> (str, list)
    mods = raw_input.strip().lower().split()  # Turns player input into list of words
    if len(mods) == 0:
        return (-1,"Enter a valid command") # Prevents error if no text entered
    player_command = mods.pop(0)  # Turns first word into command, leaves rest as mods
    if player_command in ["quit", "q"]:
        return ("quit", False)
    if player_command in ["end", "e", "r", "restart", "reboot"]:
        return ("end",replay())
    for command in command_list: # Compare input to list of accepted commands
        if player_command in command.alias:
            if len(mods) != command.num_mods: # Error if command accepted but wrong number of mods
                num_error = str(command.name)+" requires exactly "+str(command.num_mods)+" modifier" # Creates error message
                if command.num_mods != 1: num_error = num_error + 's' # Adds an 's' to end of error if num_mods == 0 or 2
                return (-1, num_error.capitalize())
            #if len(mods) == 0: mods = [""] # Prevents error when command used correctly with no mods
            while len(mods) < 2:
                mods.append("")
            return (command, mods) # * Success Condition
    return (-1,"Enter a valid command") # Error if command not recognized    
        

#*#####################        
#*### locate Object ###        
#*#####################       
# Given game and a string, finds Game Object with name == string
def locate_obj(game, obj):
    ob = obj[:-1]
    for item in game.object_list:
        if item.name == obj or item.name == ob:
            return item
    return -1
    

#*################        
#*### New Game ###        
#*################ 
# Sets up game
def new_game(game):
    game.new_game() # Resets game to starting state
    draw_ui(game)
    #if not DEBUG:
        #tutorial_prompt(game)
    print(opening_crawl_text)
    return run_game(game)



#*################        
#*### Run Game ###        
#*################      
# Prompts for input, directs functions
def run_game(game):
    while True:
        time.sleep(.5)
        player_input = input_handler(input("What do you do next?\n")) # Request input, convert to (command, ["mods"])   
        if player_input in ["quit", "end"]:
            return player_input[1]
        if player_input[0] == -1: #Displays error and restarts loop
            print(player_input[1])
            continue
        draw_ui(game)
        command = player_input[0]
        mod1 = locate_obj(game, player_input[1][0])
        mod2 = locate_obj(game, player_input[1][1])
        print(f"Previous Command:",str(player_input[0].name),str(player_input[1][0]),str(player_input[1][1]))
        # Runs player command after locating objects being referenced
        command(game, mod1, mod2)
                        

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
              
