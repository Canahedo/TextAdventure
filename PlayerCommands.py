'''
Unnamed Text Adventure - PlayerCommands
Written by Canahedo and WingusInbound
Python3
2024

This file contains functions which execute the player commands
'''

#Imports
import os.path #Used to check if a file exists before opening
from UI_Elements import title_bar, inventory
from Inventories import player_inventory

#Look - Provides general info about surroundings [0 Modifiers]
def look():
    title_bar()
    inventory(player_inventory)
    print('You look around')
    print('There isn\'t anything to see yet\n')

#Check - Provides information about an object [1 Modifier]
def check(object):
    title_bar()
    inventory(player_inventory)
    file_path = 'assets/'+object+'.md' #Creates filepath from provided string
    if os.path.isfile(file_path): #Checks if file exists
        file = open(file_path, 'r') 
        file_contents = file.read()
        print(file_contents,'\n')
        file.close()
    else:
        print('I am not sure what you are trying to investigate')
        print('Please try something else\n')

#Take - Moves an item into player inventory [1 Modifier]
def take(object):
    player_inventory.append(object)
    title_bar()
    inventory(player_inventory)
    print('You add the',object,'to your inventory\n')

#Use - Use the first object on the second object [2 modifiers]
def use(object1,object2):
    title_bar()
    inventory(player_inventory)
    print('You use the',object1,'on the',object2,'\n')

#Move - Move an object to a nearby location [2 modifiers]
def move(object,location):
    title_bar()
    inventory(player_inventory)
    print('You move the',object,'to the',location,'\n')

#Place - Remove an object from Inventory, place in nearby location [2 modifiers]
def place(object,location):
    title_bar()
    inventory(player_inventory)
    print('You place the',object,'on the',location,'\n')

# Walk - Move player to a location. Accepts cardinal directions of room name [1 Modifier]
def walk(location):
    title_bar()
    inventory(player_inventory)
    print('You walk to the',location)

#Speak - Talk to someone [1 Modifier]
def speak(person):
    title_bar()
    inventory(player_inventory)
    print('You speak with',person,'\n')

#Displays Help
def help():
    title_bar()
    inventory(player_inventory)
    file = open('assets/help.md', 'r')
    file_contents = file.read()
    print(file_contents,'\n')
    file.close()