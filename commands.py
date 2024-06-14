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
        
    def __call__(self, mods: list[object], game: object):
        room = game.player.location
        game.player.turn_text.extend(game.text_fetcher("look", room.name, room.looktext_dict[room.state]))
        game.player.get_local_chests()
        game.player.turn_text.extend(game.you_see_a(game.player.local_chests))


#* Check
#* Displays text describing a specific object
#*####################       
class Check(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
    
    def __call__(self, mods: list[object], game: object):
        obj = mods[0]
        game.player.turn_text.extend(game.text_fetcher("check", obj.name, obj.checktext_dict[obj.state])) #Retrieves check text for current state
        if "none" not in obj.key:    
            obj.try_key("check", game)
        if obj.type == "chest":   
            game.player.get_local_items(obj)
        if len(game.player.local_chests) > 0:
            game.player.turn_text.extend(game.you_see_a(game.player.local_chests))    
        return (0,"Check")        

                
#* Take
#* Removes a nearby object from it's chest, adds it to player inventory
#*####################
class Take(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)
        
    def __call__(self, mods: list[object], game: object):
        obj = mods[0]
        if obj == -1:
            return(-1,"Unrecognized object")
        if obj.name in game.player.inventory:
            return(-1,f"You already have the "+obj.name)
        if obj.visible == False:
            return(-1,f"You can't see the "+obj.name)        
        if obj.takeable == False:
            return(-1,f"You can't take the "+obj.name)
        game.player.inventory.append(obj)
        game.player.turn_text.append(f"You take the "+obj.name)
        if "none" not in obj.key:    
            obj.try_key("take", game)
        return (0,"Take")        


#* Walk
#* Moves the player to an adjacent room
#! BUG: Because all objects are checked, walk can be used on a chest or item
#*####################
class Walk(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)        
        
    def __call__(self, mods: list[object], game: object):
        room = mods[0]
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
        
    def __call__(self, mods: list[object], game: object): 
            game.player.turn_text.append("Speak not implimented yet")
   
        
#* Use
#* Attempts to use the first item on the second, and checks for triggers  
#*####################  
class Use(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)    
        
    def __call__(self, mods: list[object], game: object):
        obj1, obj2 = mods[0], mods[1]
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

    def __call__(self, mods: list[object], game: object):
        game.player.turn_text.append("Place not implimented yet")


#* GPS
#* Not yet implimented, potential system for directional navigation
#*####################
def gps(game: object, dir: str):
    raise NotImplementedError()
