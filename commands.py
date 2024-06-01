"""
Unnamed Text Adventure - Commands
Written by Canahedo and WingusInbound
Python3
2024

This file defines all commands accessible to the player
"""

class Command:
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        self.name = name
        self.alias = alias
        self.num_mods = num_mods   
        self.type = type   
     
        
#Command = Command(name, alias, num_mods)
command_list = [
Command("look", ["look", "l"], 0),
Command("help", ["help", "h"], 0),
Command("end", ["end", "e", "r", "restart", "reboot"], 0),
Command("quit", ["quit", "q"], 0),
Command("check", ["check", "c"], 1),
Command("take", ["take", "t"], 1),
Command("walk", ["walk", "w"], 1),
Command("speak", ["speak", "s"], 1),
Command("use", ["use", "u"], 2),
Command("move", ["move", "m"], 2),
Command("place", ["place", "p"], 2)
]


'''

l - 0 = read player location, display text
h - 0 = display text
e/q - 0 = system command

c - 1 = is in player.room or player.inv?
        is checkable?
        display text
        triggers? > apply changes
        
        
        
t - 1
w - 1
s - 1

u - 2
m - 2
p - 2








'''