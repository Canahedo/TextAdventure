"""
Unnamed Text Adventure - Commands
Written by Canahedo and WingusInbound
Python3
2024

This file defines all commands accessible to the player
"""

from icecream import ic


class Command:
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        self.name = name
        self.alias = alias
        self.num_mods = num_mods
        
        
#* Look       
#* Displays text describing the player's surroundings
#*####################
class Look(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)     
        
    def __call__(self, game: object, mod1: None, mod2: None):
        room = game.player.location
        game.player.turn_text.extend(game.text_fetcher("look", room.name, room.looktext_dict[room.state]))
        return (0,"Look")


#* Check
#* Displays text describing a specific object
#*####################       
class Check(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
    
    def __call__(self, game: object, obj, mod2: None):
        if obj == -1:
            return(-1,"Unrecognized object")
        if obj.visible == False:
            return(-1,f"You can't see the "+obj.name)
        if obj.checkable == False:
            return(-1,f"You can't check the "+obj.name)
        game.player.turn_text.extend(game.text_fetcher("check", obj.name, obj.checktext_dict[obj.state])) #Retrieves check text for current state
        if "none" not in obj.key:    
            obj.try_key("check", game)
        return (0,"Check")        

                
#* Take
#* Removes a nearby object from it's chest, adds it to player inventory
#*####################
class Take(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        
    def __call__(self, game: object, obj: object, mod2: None):
        if obj == -1:
            return(-1,"Unrecognized object")
        if obj.name in game.player.inventory:
            return(-1,f"You already have the "+obj.name)
        if obj.visible == False:
            return(-1,f"You can't see the "+obj.name)        
        if obj.takeable == False:
            return(-1,f"You can't take the "+obj.name)
        game.player.inventory.append(obj.name)
        game.player.turn_text.append(f"You take the "+obj.name)
        if "none" not in obj.key:    
            obj.try_key("take", game)
        return (0,"Take")        


#* Walk
#* Moves the player to an adjacent room
#*####################
class Walk(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        
        
    def __call__(self, game: object, room: object, mod2: None):
        if room == -1:
            return(-1,"I don't know where you're trying to go")
        if room == game.player.location:
            return(-1,f"You are already in the "+room.name)
        if room.name in ["north","south","east","west"]:
            goto = gps(game, room)        
        else:
            goto = room
        game.player.location = goto
        game.player.turn_text.append("You walk to the "+goto.name)
        return(0,"Walk")
 
        
#* Speak
#* Displays dialogue text for an NPC. May be removed in the future, undecided.
#*####################
class Speak(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)  
        
    def __call__(self, game: object, targ: object, mod2: None): 
            return(-1,"Speak not implimented")
   
        
#* Use
#* Attempts to use the first item on the second, and checks for triggers  
#*####################  
class Use(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)    
        
    def __call__(self, game: object, obj1: object, obj2: object):
        if obj1 == -1:
            return(-1,"Object 1 unrecognized")
        if obj2 == -1:
            return(-1,"Object 2 unrecognized")
        if "none" not in obj2.key:    
            obj2.try_key(obj1.name, game)
            return(0,"Use")
    
        
#* Place
#* Remove an item from the player inventory and adds it to a chest
#*####################
class Place(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        

    def __call__(self, game: object, obj1: object, obj2: object):
        return(-1,"Place not implimented")


#* GPS
#* Not yet implimented, potential system for directional navigation
#*####################
def gps(game: object, dir: str):
    raise NotImplementedError()
