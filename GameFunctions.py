"""
Unnamed Text Adventure - GameFunctions
Written by Canahedo and WingusInbound
Python3
2024

This file holds internal functions used by the game
"""

# Imports
import os  # Used in clear() to erase the board
import time  # Used in sleep() to create a delay
from UI_Elements import title_bar, ui
from Inventories import *
from Triggers import init_triggers
from PlayerCommands import look, check, take, use, place, speak, help, move, walk


# Creates clear() to erase the board
def clear():
    os.system("cls")


##################
###  TUTORIAL  ###
##################
# Offers to show Help screen at start of first game
def tutorial_prompt():
    init_triggers()
    init_inventories()
    title_bar()
    while True:
        time.sleep(0.5)
        print("Welcome to our game", "\nThank you for playing\n")
        print('Enter "H" to view the Help Screen, or "S" to skip\n')
        print("You can ask for help at any time in-game\n")
        tutorial = (input().strip().lower())  # Requests player input, removes leading/trailing whitespace, sets lowercase
        if tutorial in ["tutorial", "t", "help", "h"]:
            help()
            input("Press Enter to Continue\n\n")
            break
        elif tutorial in ["start", "s", ""]:
            break
        else:
            clear()
            title_bar()
            print('Sorry, "', tutorial, '" is an invalid response\n')


###################
###  INIT GAME  ###
###################
# Displays opening_crawl
def init_game():
    file = open("assets/opening_crawl.md", "r")
    file_contents = file.read()
    print(file_contents, "\n")
    file.close()


#######################
###  INPUT HANDLER  ###
#######################
# Processes player input into useable form, or throws error when input is invalid
def input_handler(raw_input):
    if raw_input == "": # Prevents error if no text entered
        return (-1,"Enter a valid command")
    mods = raw_input.strip().lower().split()  # Turns player input into list of words
    command = mods.pop(0)  # Turns first word into command, leaves rest as mods

    command_parcer = {
        "look": [0, "look", "l"],
        "help": [0, "help", "h"],
        "end": [0, "end", "e", "r", "restart", "reboot"],
        "quit": [0, "quit", "q"],
        "check": [1, "check", "c"],
        "take": [1, "take", "t"],
        "walk": [1, "walk", "w"],
        "speak": [1, "speak", "s"],
        "use": [2, "use", "u"],
        "move": [2, "move", "m"],
        "place": [2, "place", "p"],}

    for item in command_parcer: # Checks command against recognized terms
        n = command_parcer[item][0] # Represents the expected number of mods
        # If command is valid and number of mods correct, return both
        if command in command_parcer[item] and len(mods) == n:
            return (item, mods)
        # If command valid but wrong number of mods, return error
        elif command in command_parcer[item] and len(mods) != n:
            error = '\nThat command requires exactly '+str(n)+' modifier'
            if n != 1: error = error+'s' # Adds an 's' for 0 or 2
            return (-1, error)
    # If command invalid, return error
    return (-1, "\n" + command + " is an unrecognized command")


##############
###  GAME  ###
##############
# Requests player input, determines which command to run, passes parameters to PlayerCommands
def game():
    ui()
    init_game()  # Presents start of game text
    while True:
        time.sleep(0.5)
        # player_input is formatted as (command,[mods])
        player_input = input_handler(input("What do you do next?\n"))  # Requests player input, runs through input_handler
        # If input_handler errors, display error and return to start of loop, requesting new input
        if player_input[0] == -1:
            print(player_input[1])  
        elif player_input[0] in ["end", "quit"]:
            return player_input[0]
        else: 
            globals()[player_input[0]](player_input[1]) # Calls player_input[0] as a function, with player_input[1] as a parameter #! Broken


################
###  REPLAY  ###
################
# Asks if player wants to play again
def replay():
    while True:
        time.sleep(0.5)
        response = input("Would you like to play again? y/n\n\n").lower()
        if response in ['y', 'yes']:
            init_triggers()
            init_inventories()
            return True
        elif response in ['n', 'no']:
            return False
        else:
            clear()
            print('Sorry, "', response, '" is an invalid response.')
