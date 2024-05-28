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
        print("Welcome to my game","\nThank you for playing\n")
        tutorial = input('Enter "T" to view the Tutorial, or "S" to skip\n\n').strip().lower() #Requests player input, removes leading/trailing whitespace, sets lowercase
        if tutorial in ['tutorial', 't']:
            title_bar()
            print('Welcome to the Tutorial!')
            print('Enter "Help" while in game to return to this page\n')
            help()
            input('\nPress Enter to Continue\n\n')
            break
        elif tutorial in ['start', 's']:
            break
        else: 
            clear()
            title_bar()
            print('Sorry, "',tutorial,'" is an invalid response\n')
   
#Accepts player input, determines which command to run, passes parameters
def game():
    title_bar() #Displays Title Bar
    inventory(player_inventory) #Displays Inventory
    while True:
        time.sleep(.5)
        player_input = input('What do you do next?\n\n').strip().lower() #Requests player input, removes leading/trailing whitespace, sets lowercase
        player_input_list = player_input.split() #Breaks player input into list of words
               
        #Look - Provides general info about surroundings [0 Modifiers]
        if player_input_list[0] in ['look', 'l']: 
            if len(player_input_list) != 1:
                print('The "Look" command cannot be modified\n')
            else:look()
        
        #Check - Provides information about an object [1 Modifier]
        elif player_input_list[0] in ['check', 'c']: 
            if len(player_input_list) != 2:
                print('The "Check" command requires one modifier\n')
            else:check(player_input_list[1])
        
        #Take - Moves an item into player inventory [1 Modifier]
        elif player_input_list[0] in ['take', 't']:
            if len(player_input_list) != 2:
                    print('The "Take" command requires one modifier\n')
            else:take(player_input_list[1])
        
        #Use - Use the first object on the second object [2 modifiers]
        elif player_input_list[0] in ['use', 'u']: 
            if len(player_input_list) != 3:
                    print('The "Use" command requires two modifiers\n')
            else:use(player_input_list[1],player_input_list[2])
            
        #Move - Move an object to a nearby location [2 modifiers]
        elif player_input_list[0] in ['move', 'm']: 
            if len(player_input_list) != 3:
                    print('The "Move" command requires two modifiers\n')
            else:move(player_input_list[1],player_input_list[2])
                
        #Place - Remove an object from Inventory, place in nearby location [2 modifiers]
        elif player_input_list[0] in ['place', 'p']: 
            if len(player_input_list) != 3:
                    print('The "Take" command requires two modifiers\n')
            else:place(player_input_list[1],player_input_list[2])
            
        #Walk - Move player to a location. Accepts cardinal directions of room name [1 Modifier]
        elif player_input_list[0] in ['walk', 'w']: 
            if len(player_input_list) != 2:
                    print('The "Take" command requires one modifier\n')
            else:walk(player_input_list[1])
            
        #Speak - Talk to someone [1 Modifier]
        elif player_input_list[0] in ['speak', 's']: 
            if len(player_input_list) != 2:
                    print('The "Take" command requires one modifier\n')
            else:speak(player_input_list[1])
            
        #Help - Displays Help screen [0 modifiers]
        elif player_input_list[0] in ['help', 'h']:
            if len(player_input_list) != 1:
                print('The "Help" command cannot be modified\n')
            else:help()
    
        #End & Quit [0 Modifiers]
        elif player_input_list[0] in ['end', 'e', 'r', 'restart', 'reboot']:
            if len(player_input_list) != 1:
                print('The "End" command cannot be modified\n')
            else:
                return 'end'
        elif player_input_list[0] in ['quit', 'q', 'qq']:
            if len(player_input_list) != 1:
                print('The "Quit" command cannot be modified\n')
            else:
                return 'quit'
        else:
            print('\nSorry, "',player_input,'" is an invalid response.\n') 


#Asks if player wants to play again
def replay():
    while True:
        time.sleep(.5)
        response = input('\nWould you like to play again? y/n\n\n')
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