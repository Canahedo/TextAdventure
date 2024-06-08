"""
Unnamed Text Adventure - Main
Written by Canahedo and WingusInbound
Python3
2024

This is the main file for the program
"""

# import os  # Used in clear() to erase the board
# import time  # Used in sleep() to create a delay
# import json
# from icecream import ic
# from dataclasses import dataclass

# from gametext import *
# from systemfunctions import *t
# from gameobjects import *

from commands import *


#*######################
#*### Locate Command ###
#*######################
def locate_command(game: object, comm: str, player_input: list):
    """
    Iterates over command_list looking for corresponding object.
    Checks that correct number of mods were supplied.
    If no matches, an error message will be returned as a str.
    """
    for obj in command_list: # Compare input to list of accepted commands
        if comm in obj.alias:
            if len(player_input) == obj.num_mods: # Confirms if correct number of mods were entered
                return obj
            # Error if command accepted but wrong number of mods
            num_error = str(obj.name)+" requires exactly "+str(obj.num_mods)+" modifier" # Creates error message
            if obj.num_mods != 1: num_error = num_error + 's' # Adds an 's' to end of error if num_mods == 0 or 2
            return (num_error.capitalize())
    return ("Enter a valid command") # Error if command not recognized           
            

#*#####################
#*### Input Handler ###
#*#####################
def input_handler(game,text):
    """
    Takes in input from game_loop, formats it and checks for null input.
    Compares against system functions and executes them.
    Validates command and if found, returns command and mod objects
    """
    player_input = text.strip().lower().split()  # Turns player input into list of words
    if len(player_input) == 0: # Prevents error if no text entered
        print("Enter a valid command\n") 
        game_loop(game) # Restarts game loop
    comm = player_input.pop(0)
    # Checks for system commands
    if comm in ["quit", "q"]:
        exit() # Close program
    if comm in ["end", "e"]:
        replay(game) # End current game, offer replay
    if comm in ["r", "restart", "reboot"]:
        run(game) # Restart game
    comm_obj = locate_command(game, comm, player_input) #find command object which corresponds with player input
    if not isinstance(comm_obj, Command):
            print(comm_obj)
            game_loop(game) # if command not valid, restart game loop
    while len(player_input) < 2:
        player_input.append("none") # Fills mods slots for commands with < 2 mods so downstream functions get enough args
    return comm_obj, game.locate_object(player_input[0]), game.locate_object(player_input[1])


#*#################
#*### Game Loop ###
#*#################
def game_loop(game):
    """
    Primary game loop. Requests input, runs it through handler, and executes command
    """
    while True:
        time.sleep(.5)
        command, mod1, mod2 = input_handler(game, input("What do you do next?\n"))
        player_turn = command(game, mod1, mod2)
        try:
            print(player_turn[1])
        except:
            pass
        
        
#*###########
#*### Run ###
#*###########
def run(game):
    '''
    Start of new game.
    Resets values for game data and runs game loop
    '''
    game.reset()
    draw_ui(game)
    print(opening_crawl_text)
    while True:
        game_loop(game)
        

#*################
#*### End Game ###
#*################ 
# Basic end game function
# Not currently in use
def end_game():
    print("Congratulations!")
    print("    You Win!    ")
    return replay()


#*##############
#*### Replay ###
#*##############                            
def replay(game):
    """
    Asks the player if they want to play again
    """
    while True:
        time.sleep(0.5)
        response = input("Would you like to play again? y/n\n\n").lower()
        if response in ['y', 'yes']:
            run(game)
        elif response in ['n', 'no']:
            exit()
        else:
            clear()
            print('Sorry, "', response, '" is an invalid response.')


#*############
#*### Main ###
#*############ 
def main():
    """
    Initializes game data and starts game
    """
    clear() # Clears text VSCode terminal starts with
    game = Game_Data() # Initilize game object
    run(game)


if __name__ == "__main__":
    main()


