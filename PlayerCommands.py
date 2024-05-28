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
from UI_Elements import title_bar, inventory
from Inventories import player_inventory

#Look - Provides general info about surroundings [0 Modifiers]
def look():
    title_bar()
    inventory(player_inventory)
    print('You look around')
    print('There isn\'t anything to see yet\n')

#Check - Provides information about an object [1 Modifier]
def check(mods):
    title_bar()
    inventory(player_inventory)
    file_path = 'assets/'+str(str(mods[0]))+'.md' #Creates filepath from provided string
    if os.path.isfile(file_path): #Checks if file exists
        file = open(file_path, 'r') 
        file_contents = file.read()
        print(file_contents,'\n')
        file.close()
    else:
        print('I am not sure what you are trying to investigate')
        print('Please try something else\n')

#Take - Moves an item into player inventory [1 Modifier]
def take(mods):
    player_inventory.append(str(mods[0]))
    title_bar()
    inventory(player_inventory)
    print('You add the',str(mods[0]),'to your inventory\n')

#Use - Use the first object on the second object [2 modifiers]
def use(mods):
    title_bar()
    inventory(player_inventory)
    print('You use the',str(mods[0]),'on the',str(mods[1]),'\n')

#Move - Move an object to a nearby location [2 modifiers]
def move(mods):
    title_bar()
    inventory(player_inventory)
    print('You move the',str(mods[0]),'to the',str(mods[1]),'\n')

#Place - Remove an object from Inventory, place in nearby location [2 modifiers]
def place(mods):
    title_bar()
    inventory(player_inventory)
    print('You place the',str(mods[0]),'on the',str(mods[1]),'\n')

# Walk - Move player to a location. Accepts cardinal directions of room name [1 Modifier]
def walk(mods):
    title_bar()
    inventory(player_inventory)
    print('You walk to the',str(mods[0]))

#Speak - Talk to someone [1 Modifier]
def speak(mods):
    title_bar()
    inventory(player_inventory)
    print('You speak with',str(mods[0]),'\n')

#Displays Help
def help():
    title_bar()
    inventory(player_inventory)
    file = open('assets/help.md', 'r')
    file_contents = file.read()
    print(file_contents,'\n')
    file.close()