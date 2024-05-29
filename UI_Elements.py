'''
Unnamed Text Adventure - Main
Written by Canahedo and WingusInbound
Python3
2024

This file defines the UI elements such as the title bar and the player inventory display
'''

#Imports
import os #Used in clear() to erase the board
from Inventories import player_inventory

#Creates clear() to erase the board
clear = lambda: os.system('cls')
#def clear():
#     os.system('cls')

#Displays title bar at top of screen
def title_bar():
    clear()
    print("Untitled Text Adventure","\nCreated by Canahedo and WingusInbound, 2024","\nWritten in Python 3")
    print("-------------------------\n")

#Lists objects in player inventory
def inventory(player_inventory):
    player_inventory.sort()
    print('You are carrying the following: ')
    for item in player_inventory: #Prints inventory without list formatting
        print(item, end=' ') #Prevents new lines
        if player_inventory.index(item) != len(player_inventory)-1: #Prints a comma after every item but the last
            print(', ', end='')
    print("\n\n-------------------------\n")