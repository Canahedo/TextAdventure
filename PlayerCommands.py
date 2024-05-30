"""
Unnamed Text Adventure - PlayerCommands
Written by Canahedo and WingusInbound
Python3
2024

This file contains functions which represent the player commands
args will be a list of 0-2 strings
"""

# Imports
import os.path  # Used to check if a file exists before opening
from UI_Elements import ui
from Inventories import *
from Triggers import *


#####################
###  FILE READER  ###
#####################
# Takes in folder/file name, checks if file exists, and returns text
def file_reader(file_name):
    file_path = "assets/" + str(file_name) + ".md"
    if os.path.isfile(file_path):  # Checks if file exists
        file = open(file_path, "r")
        file_contents = file.read()
        file.close()
        return file_contents
    else:
        return -1


##############
###  LOOK  ###
##############
# Look - Provides general info about surroundings [0 Modifiers]
def look(*args):
    ui()
    print("You are in the", player_stats["room"])
    text = file_reader("look/" + player_stats["room"])  # Loads location description
    if text == -1:
        print("There isn't much to look at right now")  # In case of missing desc
    else:
        print(text)  # Displays location description
    look_triggers()  # Checks for look triggers


###############
###  CHECK  ###
###############
# Check - Provides information about an object [1 Modifier]
def check(*args):
    object = str(args[0][0])
    triggers = check_triggers(object)
    if triggers == 0:
        print("There is nothing more to do here")
    if triggers != 0:
        print(str(object))
        file_path = ("assets/check/" + str(object) + ".md")  # Creates filepath from provided string
        print(file_path)
        if os.path.isfile(file_path):  # Checks if file exists
            file = open(file_path, "r")
            file_contents = file.read()
            ui()
            print(file_contents, "\n")
            file.close()
            if triggers not in [-1, 1]:
                print(triggers)
        else:
            print("I am not sure what you are trying to investigate")
            print("Please try something else\n")


##############
###  TAKE  ###
##############
# Take - Moves an item into player inventory [1 Modifier]
def take(*args):
    player_inventory.append(str(args[0]))
    ui()
    print("You add the", str(args[0]), "to your inventory\n")


#############
###  USE  ###
#############
# Use - Use the first object on the second object [2 modifiers]
def use(*args):
    ui()
    print("You use the", str(args[0]), "on the", str(args[1]), "\n")


##############
###  MOVE  ###
##############
# Move - Move an object to a nearby location [2 modifiers]
def move(*args):
    ui()
    print("You move the", str(args[0]), "to the", str(args[1]), "\n")


###############
###  PLACE  ###
###############
# Place - Remove an object from Inventory, place in nearby location [2 modifiers]
def place(*args):
    ui()
    print("You place the", str(args[0]), "on the", str(args[1]), "\n")


##############
###  WALK  ###
##############
# Walk - Move player to a location. Accepts cardinal directions of room name [1 Modifier]
def walk(*args):
    ui()
    print("You walk to the", str(args[0]))


###############
###  SPEAK  ###
###############
# Speak - Talk to someone [1 Modifier]
def speak(*args):
    ui()
    print("You speak with", str(args[0]), "\n")


##############
###  HELP  ###
##############
# Displays Help
def help(*args):
    ui()
    file = open("assets/help.md", "r")
    file_contents = file.read()
    print(file_contents, "\n")
    file.close()
