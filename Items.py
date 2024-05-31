"""
Unnamed Text Adventure - Items
Written by Canahedo and WingusInbound
Python3
2024

This file contains the items the player can interact with
"""

def init_items():
    pass    

class Item:
    def __init__(self, name, checkable, takeable, useable, moveable) -> None:
        self.name = name
        self.checkable = checkable
        self.takeable = takeable
        self.useable = useable
        self.moveable = moveable
        


#Item = Item(name, checkable, takeable, useable, moveable)
rock = Item("rock", True, True, False, False)
newspaper = Item("newspaper", True, False, False, False)
key = Item("key", True, True, True, True)
