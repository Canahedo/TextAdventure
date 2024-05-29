'''
Unnamed Text Adventure - PlayerCommands
Written by Canahedo and WingusInbound
Python3
2024

This file contains functions which represent the player commands
If a command accepts modifiers, the funtion will require a list argument of 1 or 2 items
'''

#Imports
import os.path #Used to check if a file exists before opening
from UI_Elements import ui
from Inventories import *
from Triggers import *

#####################
###  FILE READER  ###
#####################
#Takes in folder/file name, checks if file exists, and returns text
def file_reader(file_name):
    file_path = 'assets/'+str(file_name)+'.md'
    if os.path.isfile(file_path): #Checks if file exists
        file = open(file_path, 'r') 
        file_contents = file.read()
        file.close()
        return file_contents
    else: return -1

##############
###  LOOK  ###
##############
#Look - Provides general info about surroundings [0 Modifiers]
def look():
    ui(player_inventory)
    print('You are in the',player_location)
    text = file_reader('look/'+player_location) #Loads location description
    if text == -1: print('There isn\'t much to look at right now') #In case of missing desc
    else: print(text) #Displays location description
    look_triggers(player_location) #Checks for look triggers


###############
###  CHECK  ###
###############
#Check - Provides information about an object [1 Modifier]
def check(mods):
    object = str(mods[0])
    ui(player_inventory)
    file_path = 'assets/check/'+object+'.md' #Creates filepath from provided string
    if os.path.isfile(file_path): #Checks if file exists
        file = open(file_path, 'r') 
        file_contents = file.read()
        print(file_contents,'\n')
        file.close()
    else:
        print('I am not sure what you are trying to investigate')
        print('Please try something else\n')
    check_triggers(object)

##############
###  TAKE  ###
##############
#Take - Moves an item into player inventory [1 Modifier]
def take(mods):
    player_inventory.append(str(mods[0]))
    ui(player_inventory)
    print('You add the',str(mods[0]),'to your inventory\n')

#############
###  USE  ###
#############
#Use - Use the first object on the second object [2 modifiers]
def use(mods):
    ui(player_inventory)
    print('You use the',str(mods[0]),'on the',str(mods[1]),'\n')

##############
###  MOVE  ###
##############
#Move - Move an object to a nearby location [2 modifiers]
def move(mods):
    ui(player_inventory)
    print('You move the',str(mods[0]),'to the',str(mods[1]),'\n')

###############
###  PLACE  ###
###############
#Place - Remove an object from Inventory, place in nearby location [2 modifiers]
def place(mods):
    ui(player_inventory)
    print('You place the',str(mods[0]),'on the',str(mods[1]),'\n')

##############
###  WALK  ###
##############
# Walk - Move player to a location. Accepts cardinal directions of room name [1 Modifier]
def walk(mods):
    ui(player_inventory)
    print('You walk to the',str(mods[0]))

###############
###  SPEAK  ###
###############
#Speak - Talk to someone [1 Modifier]
def speak(mods):
    ui(player_inventory)
    print('You speak with',str(mods[0]),'\n')

##############
###  HELP  ###
##############
#Displays Help
def help():
    ui(player_inventory)
    file = open('assets/help.md', 'r')
    file_contents = file.read()
    print(file_contents,'\n')
    file.close()