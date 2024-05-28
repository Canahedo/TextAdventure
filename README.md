# TextAdventure

This is a text adventure game written in Python3\
It accepts player input in the form of a single word command\
Some commands use either one or two words acting as modifiers

Examples:\
LOOK\
CHECK WINDOW\
PLACE BOOK TABLE

Commands and modifiers can be lower or upper case, but will shown in upper case here\
A command cannot be used without all of its modifiers, or accept additional modifiers

A glossary of supported commands follows:

LOOK - Look around, gather information about your general surroundings\
CHECK [THING] - Investigate something specific\
TAKE [THING] - Move an object into your inventory\
USE [THING] [THING] - Use the first object on the second object\
MOVE [THING] [PLACE] - Move an object to a nearby location\
PLACE [THING] [PLACE] - Remove an object from your inventory, and move it to a nearby location\
WALK [LOCATION] - Move the player to a location, accepts cardinal directions or room description\
SPEAK [PERSON] - Talk to someone\
HELP - Brings up this page\
END - Ends the current game, with the option to restart\
QUIT - Exits the game, closing the program