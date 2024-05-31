"""
Unnamed Text Adventure - Game
Written by Canahedo and WingusInbound
Python3
2024

This file contains the primary functions which run the game
"""

# Imports
import os  # Used in clear() to erase the board
import time  # Used in sleep() to create a delay
from player import *
from items import *
from chests import *
from rooms import *
from text import *
from commands import *

# Creates clear() to erase the board
def clear():
    os.system("cls")

title = """
Untitled Text Adventure
Created by Canahedo and WingusInbound, 2024
Written in Python 3
-------------------------
"""


######################
### Initialization ###
######################
# Sets starting locations/stats
def bootup():
    init_player()
    init_items()
    init_rooms()
    init_chests()
    

###############
### Draw UI ###
###############
# Displays header and formats/displays player inventory
def draw_ui():
    clear()
    print(title)
    print("You are carrying the following: ")
    # Formats inventory
    if len(player.inventory) is not 0:
        for item in player.inventory:
            print(str(item), end=" ")
            if len(player.inventory) != player.inventory.index(item) + 1:
                print(", ", end="")
    print("\n\n-------------------------\n")
    

#####################
### Input Handler ###
#####################
# Converts player input into usable form
# Returns (command, [mods]) if input accepter or (-1, error) if not
def player_input(raw_input):
    mods = raw_input.strip().lower().split()  # Turns player input into list of words
    if len(mods) == 0: # Prevents error if no text entered
        return (-1,"Enter a valid command")
    player_command = mods.pop(0)  # Turns first word into command, leaves rest as mods
    for command in command_list: # Compare input to list of accepted commands
        if player_command in command.alias:
            if len(mods) != command.num_mods: # Error if command accepted but wrong number of mods
                num_error = str(command.name)+" requires exactly "+str(command.num_mods)+" modifier"
                if command.num_mods != 1: num_error = num_error+'s' # Adds an 's' for 0 or 2
                return (-1, num_error.capitalize())
            return (command.name, mods) # * Success Condition
        
        
#################        
### Game Loop ###        
#################      
# Sets up game, prompts for input, directs functions
def game():
    bootup()
    draw_ui()
    print(opening_crawl_text)
    while True:
        time.sleep(1)
        player_command = player_input(input("What do you do next?\n"))
        print(player_command)  # ('speak', ['d'])      
        
    
    
    
