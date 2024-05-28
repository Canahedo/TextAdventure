
'''
Unnamed Text Adventure
Written by Canahedo
Python3
2024
'''

#Imports
import os #Used in clear() to erase the board
import time #Used in sleep() to create a delay

#Creates clear() to erase the board
clear = lambda: os.system('cls')

#########################
### Primary Variables ###
#########################
player_inventory = ['letter'] #Initializes player inventory, which contains held items


######################
### Game Functions ###
######################

#Displays title bar at top of screen
def title_bar():
    clear()
    print("Untitled Text Adventure","\nCreated by Canahedo, 2024","\nWritten in Python 3")
    print("-------------------------\n")


#Offers to show Help screen at start of first game
def tutorial_prompt():
    title_bar()
    while True:
        time.sleep(.5)
        print("Welcome to my game","\nThank you for playing\n")
        tutorial = input('Enter "T" to view the Tutorial, or "S" to skip\n\n')
        if tutorial in ['Tutorial', 'tutorial', 'TUTORIAL', 't', 'T']:
            title_bar()
            print('Welcome to the Tutorial!')
            print('Enter "Help" while in game to return to this page\n')
            help()
            input('\nPress Enter to Continue\n\n')
            break
        elif tutorial in ['Start', 'start', 'START', 's', 'S']:
            break
        else: 
            clear()
            title_bar()
            print('Sorry, "',tutorial,'" is an invalid response\n')

#Lists objects in player inventory
def inventory(player_inventory):
    player_inventory.sort()
    print('You are carrying the following: ')
    for item in player_inventory:
        print(item, end=' ')
        if player_inventory.index(item) != len(player_inventory)-1:
            print(', ', end='')
    print("\n\n-------------------------")

    
#Game goes here
def game():
    title_bar()
    inventory(player_inventory)
    while True:
        time.sleep(.5)
        player_input = input('\nWhat do you do next?\n\n').lower()
        if player_input in ['help', 'h']:
            help()
        elif player_input in ['end', 'e', 'r', 'restart', 'reboot']:
            return 'end'
        elif player_input in ['quit', 'q', 'qq']:
            return 'quit'
        else:
            print('\nSorry, "',player_input,'" is an invalid response.')


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


########################
### Player Functions ###
########################

#Displays Help
def help():
    title_bar()
    inventory(player_inventory)
    file = open('assets/help.md', 'r')
    help_txt = file.read()
    print(help_txt)
    file.close()
    



#################
### Main Code ###
#################

clear()                         #This is just here because VSCode terminal starts with junk in it
player_interest = True          #Assume player wants to play. If not, why did they run the program?
tutorial_prompt()               #Offers tutorial on first play
while player_interest:          #As long as player wants to play, keep looping the game
    result = game()                      #Runs game
    if result == 'end':
        player_interest = replay()  #Checks if player still wants to keep playing after each game
    elif result == 'quit':
        break