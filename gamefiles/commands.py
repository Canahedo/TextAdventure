"""
Unnamed Text Adventure - Commands
Written by Canahedo and WingusInbound
Python3
2024

This file defines all commands accessible to the player
"""

import sys
from icecream import ic


class Command:
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        self.name = name
        self.alias = alias
        self.num_mods = num_mods


# * Look
# * Displays text describing the player's surroundings
# *####################
class Look(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return True, "success"  # ! Replace with actual logic

    def __call__(self, mods: list[object], game: object):
        room = game.player.location
        txt = room.looktext_dict[room.state]
        looktxt = game.text_fetcher("look", room.name, txt)
        game.player.turn_text.extend(looktxt)


# * Check
# * Displays text describing a specific object
# *####################
class Check(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        obj = mods[0]
        if not all([obj.checkable, obj.visible]):
            return False, f"You don't see a {obj.name}\n"
        if obj.type == "chest":
            if obj not in game.player.local_chests:
                return False, f"You don't see a {obj.name}\n"
        if obj.type == "item":
            if obj not in game.player.local_items:
                if obj not in game.player.inventory:
                    return False, f"You don't see a {obj.name}\n"
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        obj = mods[0]
        chk_target = obj.checktext_dict[obj.state]
        chktxt = game.text_fetcher("check", obj.name, chk_target)
        game.player.turn_text.extend(chktxt)  # Retrieves check text
        if "none" not in obj.key:
            obj.try_key("check", game)


# * Take
# * Removes a nearby object from it's chest, adds it to player inventory
# *####################
class Take(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        obj = mods[0]
        if obj.type != "item":
            return False, f"You can't take the {obj.name}\n"
        if not all([obj.takeable, obj.visible]):
            return False, f"There isn't a {obj.name} you can take\n"
        if obj in game.player.inventory:
            return False, f"You already have the {obj.name}\n"
        if obj.type == "item":
            if obj not in game.player.local_items:
                return False, f"You don't see a {obj.name}\n"
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        obj = mods[0]
        game.player.inventory.append(obj)
        game.player.turn_text.append(f"You take the {obj.name}")
        if "none" not in obj.key:
            obj.try_key("take", game)
        game.player.local_items.remove(obj)
        for chest in game.player.location.inventory:
            if obj.name in game.player.location.inventory[chest].inventory:
                del game.player.location.inventory[chest].inventory[obj.name]


# * Walk
# * Moves the player to an adjacent room
# *####################
class Walk(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        room = mods[0]
        if room == game.player.location:
            return False, f"You are already in the {room.name}\n"
        if room.type != "room":
            error = f"{room.name} is neither a room name, or a direction.\n"
            return False, error.capitalize()
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        room = mods[0]
        if room.name in ["north", "south", "east", "west"]:
            goto = gps(game, room)
        else:
            goto = room
        game.player.location = goto
        game.player.turn_text.append("You walk to the " + goto.name)


# * Speak
# * Displays dialogue text for an NPC. May be removed in the future, undecided.
# *####################
class Speak(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return True, "success"  # ! Replace with actual logic

    def __call__(self, mods: list[object], game: object):
        game.player.turn_text.append("Speak not implimented yet")


# * Use
# * Attempts to use the first item on the second, and checks for triggers
# *####################
class Use(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        for obj in mods:
            if not all([obj.useable, obj.visible]):
                error = f"There isn't a {obj.name} you can use right now\n"
                return False, error
            if obj.type == "chest":
                if obj not in game.player.local_chests:
                    return False, f"There isn't a {obj.name} nearby\n"
            if obj.type == "item":
                if (
                    obj not in game.player.local_items
                    and obj not in game.player.inventory
                ):
                    return False, f"You don't have a {obj.name} to use\n"
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        obj1, obj2 = mods[0], mods[1]
        if "none" not in obj2.key:
            obj2.try_key(obj1.name, game)


# * Place
# * Remove an item from the player inventory and adds it to a chest
# *####################
class Place(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return True, "success"  # ! Replace with actual logic

    def __call__(self, mods: list[object], game: object):
        game.player.turn_text.append("Place not implimented yet")


# * Quit
# * Ends the game and closes the program
# *####################
class Quit(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return game.services.double_check("quit"), "system"

    def __call__(self, mods: list[object], game: object):
        sys.exit()


# * Restart
# * Ends the game and offers replay
# *####################
class Restart(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return game.services.double_check("restart"), "system"

    def __call__(self, mods: list[object], game: object):
        game.replay()


# * Tutorial
# * Displays the help screen
# *####################
class Tutorial(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        with open("gamefiles/assets/text/tutorial.md", "r") as file:
            file_contents = file.read()
        game.player.turn_text.append(file_contents)


# * Inspect Object
# * Displays a game object
# ! DEBUG FEATURE
# *####################
class InspObj(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        ic(mods[0])


# * Inspect Game
# * Displays all game data
# ! DEBUG FEATURE
# *####################
class InspGame(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return True, "success"

    def __call__(self, mods: list[object], game: object):
        ic(game.player)
        ic(game.data)
        pass


# * GPS
# * Not yet implimented, potential system for directional navigation
# *####################
def gps(game: object, dir: str):
    raise NotImplementedError()
