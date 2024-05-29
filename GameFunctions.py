'''
Unnamed Text Adventure - GameFunctions
Written by Canahedo and WingusInbound
Python3
2024

This file holds internal functions used by the game
'''

#Imports
import os #Used in clear() to erase the board
import time #Used in sleep() to create a delay
from UI_Elements import title_bar, inventory
from Inventories import player_inventory
from PlayerCommands import look, check, take, use, place, speak, help, move, walk

#Creates clear() to erase the board
def clear():
     os.system('cls')

#Offers to show Help screen at start of first game
def tutorial_prompt():
    title_bar()
    while True:
        time.sleep(.5)
        print("Welcome to our game","\nThank you for playing\n")
        print('Enter "H" to view the Help Screen, or "S" to skip\n')
        print('You can ask for help at any time in-game\n')
        tutorial = input().strip().lower() #Requests player input, removes leading/trailing whitespace, sets lowercase
        if tutorial in ['tutorial', 't', 'help', 'h']:
            help()
            input('Press Enter to Continue\n\n')
            break
        elif tutorial in ['start', 's']:
            break
        else: 
            clear()
            title_bar()
            print('Sorry, "',tutorial,'" is an invalid response\n')

def init_game():
    file = open('assets/opening_crawl.md', 'r') 
    file_contents = file.read()
    print(file_contents,'\n')
    file.close()

#Processes player input into useable form, or throws error when input is invalid   
def input_handler(raw_input):
    
    mods = raw_input.strip().lower().split() #Turns player input into list of words
    command = mods.pop(0) #Turns first word into command, leaves rest as mods
    
    #Bundles all the recognized commands by number of mods
    zero_mods = ['look', 'l', 'help', 'h', 'end', 'e', 'quit', 'q']
    one_mod = ['check', 'c', 'take', 't', 'walk', 'w', 'speak', 's']
    two_mods = ['use', 'u', 'move', 'm', 'place', 'p']
    bundle = (zero_mods, one_mod, two_mods)

    #Checks each item in bundle to see if command is present, and if number of mods is correct
    #Returns (command, [mods]) if success
    #Returns (-1, error message) if fail
    for i in range(3):
        if command in bundle[i] and len(mods) == i:
            return (command, mods)
        elif command in bundle[i] and len(mods) != i:
            if i == 1: return (-1, 'That command requires exactly 1 modifier')
            else: return (-1, 'That command requires exactly '+str(i)+' modifiers')
    return (-1, str(command)+' is an unrecognized command')

#Requests player input, determines which command to run, passes parameters to PlayerCommands
def game():
    title_bar() #Displays Title Bar
    inventory(player_inventory) #Displays Inventory
    init_game() #Presents start of game text
    while True:
        time.sleep(.5)
        command = input_handler(input('What do you do next?\n\n')) #Requests player input, sends to input_handler
        if command[0] == -1: print(command[1])                  #If input_handler errors, display error and return to start of loop, requesting new input
        elif command[0] in ['look', 'l']: look()                #Look - Provides general info about surroundings [0 Modifiers]
        elif command[0] in ['check', 'c']: check(command[1])    #Check - Provides information about an object [1 Modifier]
        elif command[0] in ['take', 't']: take(command[1])      #Take - Moves an item into player inventory [1 Modifier]
        elif command[0] in ['use', 'u']: use(command[1])        #Use - Use the first object on the second object [2 modifiers] 
        elif command[0] in ['move', 'm']: move(command[1])      #Move - Move an object to a nearby location [2 modifiers]
        elif command[0] in ['place', 'p']: place(command[1])    #Place - Remove an object from Inventory, place in nearby location [2 modifiers]
        elif command[0] in ['walk', 'w']: walk(command[1])      #Walk - Move player to a location. Accepts cardinal directions of room name [1 Modifier]
        elif command[0] in ['speak', 's']: speak(command[1])    #Speak - Talk to someone [1 Modifier]
        elif command[0] in ['help', 'h']: help()                #Help - Displays Help screen [0 modifiers]
        elif command[0] in ['end', 'e', 'r', 'restart', 'reboot']: 
            title_bar()
            inventory(player_inventory)
            return 'end'
        elif command[0] in ['quit', 'q', 'qq']: return 'quit'

#Asks if player wants to play again
def replay():
    while True:
        time.sleep(.5)
        response = input('Would you like to play again? y/n\n\n')
        if response in ['y', 'Y', 'yes', 'YES', 'Yes']:
            converted_response = True
            break
        elif response in ['n', 'N', 'no', 'NO', 'No']:
            converted_response = False
            break
        else: 
            clear()
            print('Sorry, "',response,'" is an invalid response.')
    clear()
    return converted_response