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
          

#*#####################
#*### Input Handler ###
#*#####################
# Converts player input into usable form
# Returns (command, [mods]) if input accepted or (-1, error) if not
"""
Takes in unmodified player input str from run_game, removes unneeded
whitespace, sets lower case, and splits words into list of str.
Removes first word and compares that word to system funtions and command_list alias field.
If command validated and the player entered the correct number of modifiers,
return command object and mods list of str.

Will instead return -1 and an error if:
    no input (empty input str)
    command not recognized
    incorrect number of mods for recognized command

Args:
    raw_input (str): Accepts str of raw player input text

Returns:
    tuple[object, list]: On Success: command object, mods list of str
                        On fail: -1, error message str
"""    
def input_handler(raw_input: str): # -> (object, list)    
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
            if len(mods) == command.num_mods:
                while len(mods) < 2:
                    mods.append("") # Fills mods slots for commands with < 2 mods so downstream functions get enough args
                return (command, mods) # * Success Condition, returns command object and list of str mods
            # Error if command accepted but wrong number of mods
            num_error = str(command.name)+" requires exactly "+str(command.num_mods)+" modifier" # Creates error message
            if command.num_mods != 1: num_error = num_error + 's' # Adds an 's' to end of error if num_mods == 0 or 2
            return (-1, num_error.capitalize())
    return (-1,"Enter a valid command") # Error if command not recognized    
        

#*#####################        
#*### locate Object ###        
#*#####################       
"""
Iterates through object_list checking if obj matches a name field.
Also checks obj with last letter removed (in case player pluralized a word).
Return object if found
    else return -1

Args:
    game (object): Game file containing object/room lists, and player data
    obj (str): Name of an item or chest, entered by player as a mod to a command

Returns:
    object: Object representing an item or chest the player is interacting with
            If no object is found, return -1
"""    
def locate_obj(game, obj): # -> object
    ob = obj[:-1]
    for thing in game.object_list:
        if thing.name == obj or thing.name == ob:
            return thing
    return -1
    

#*################        
#*### Run Game ###        
#*################      
# Prompts for input, directs functions
"""
Primary game loop
Requests player input, and runs it through input_handler.
Checks for system commands or returned errors.
Refreshes screen.
Runs player-entered mod strings through locate_obj to retrieve object for relevant item or chest.
Calls relevant command function, passing three objects representing the game, 
and any items or chests the player is interacting with

Args:
    game (Game): Game file containing object/room lists, and player data

Returns:
    bool:  
"""    
def run_game(game):    
    while True:
        time.sleep(.5)
        player_input = input_handler(input("What do you do next?\n")) # Request input, convert to (command, ["mods"])   
        if player_input[0] in ["quit", "end"]:
            return player_input[1] # Ends game, and returns Bool to main, representing if the player wants to play again or not
        if player_input[0] == -1: #Displays returned error and restarts loop
            print(player_input[1])
            continue
        draw_ui(game) # Refresh screen
        #? How to impliment Previous Command for commands which require a screen refresh (ie take)? Disabled for now.
        #print(f"Previous Command:",str(player_input[0].name),str(player_input[1][0]),str(player_input[1][1]))
        player_turn = player_input[0]( # Uses Command object call function to run player command after locating item/chest objects being referenced
            game, # Game object
            locate_obj(game, player_input[1][0]), # Object representing player mod 1
            locate_obj(game, player_input[1][1])  # Object representing player mod 2
            )
        print(player_turn[1])
        #! Currently no way to end game, just keeps looping forever until player quits
        #! Needs to end by returning bool
        

#*################
#*### End Game ###
#*################ 
# Basic end game function
# Result of replay needs to be returned to main
# Not currently in use
def end_game():
    print("Congratulations!")
    print("    You Win!    ")
    return replay()


#*##############
#*### Replay ###
#*##############                            
# Asks the player if they want to play again
# Returns bool responce to wants_to_play in main
def replay() -> bool:
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
              
