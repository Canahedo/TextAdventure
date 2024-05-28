'''
Unnamed Text Adventure - Main
Written by Canahedo and WingusInbound
Python3
2024

This is the main file for the game
'''

#Imports
from GameFunctions import clear, tutorial_prompt, game, replay

if __name__ == '__main__':
    clear()                         #This is just here because VSCode terminal starts with junk in it
    player_interest = True          #Assume player wants to play. If not, why did they run the program?
    tutorial_prompt()               #Offers tutorial on first play
    while player_interest:          #As long as player wants to play, keep looping the game
        result = game()             #Runs game
        if result == 'end':
            player_interest = replay()  #Checks if player still wants to keep playing after each game
        elif result == 'quit':
            break