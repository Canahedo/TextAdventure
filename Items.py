"""
Unnamed Text Adventure - Items
Written by Canahedo and WingusInbound
Python3
2024

This file contains the items the player can interact with
"""

class Item:
    def __init__(self, name, checkable, takeable, useable, moveable) -> None:
        self.name = name
        self.checkable = checkable
        self.takeable = takeable
        self.useable = useable
        self.moveable = moveable
        


class Command:
    def __init__(self, name, alias: list, num_mods, type) -> None:
        self.name = name
        self.alias = alias
        self.num_mods = num_mods   
        self.type = type    
    
    



#Command = Command(name, alias, num_mods)
look = Command("look", ["look", "l"], 0)
help = Command("help", ["help", "h"], 0)
end = Command("end", ["end", "e", "r", "restart", "reboot"], 0)
quit = Command("quit", ["quit", "q"], 0)
check = Command("check", ["check", "c"], 1)
take = Command("take", ["take", "t"], 1)
walk = Command("walk", ["walk", "w"], 1)
speak = Command("speak", ["speak", "s"], 1)
use = Command("use", ["use", "u"], 2)
move = Command("move", ["move", "m"], 2)
place = Command("place", ["place", "p"], 2)




#Item = Item(name, checkable, takeable, useable, moveable)
rock = Item("rock", True, True, False, False)
newspaper = Item("newspaper", True, False, False, False)
key = Item("key", True, True, True, True)
