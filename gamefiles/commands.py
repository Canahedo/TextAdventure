"""
Unnamed Text Adventure - Commands
Written by Canahedo and WingusInbound
Python3
2024

This file defines all commands accessible to the player
"""

from icecream import ic
from gamefiles.errors import InvalidTurn
from gamefiles.triggers import Triggers


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
        pass  # Currently there are no conditions to Look

    def __call__(self, mods: list[object], game: object):
        room = game.player.location

        # Looktext
        txt = room.looktext_dict[room.state]
        looktxt = game.services.text_fetcher("look", room.name, txt)
        game.player.turn_text.extend(looktxt)

        # Look triggers
        if "none" not in room.key:
            Triggers("look", room, game)

        # Add adjoining rooms and gates to local
        for adj in room.routes:
            gate = room.routes[adj]["gate"]
            adj_room = room.routes[adj]["room"]
            if gate != "none":
                if gate.state == "locked":
                    if gate in room.local:
                        continue
                    # ! Disabled adding gates to local lost
                    # room.local.append(gate)
                    # game.player.local_rooms.append(gate)
                    continue

            if adj_room != "none" and adj_room not in room.local:
                room.local.append(adj_room)
                game.player.local_rooms.append(adj_room)

        # Add chests to local
        for che in room.inventory:
            chest = room.inventory[che]
            ic(chest)
            if chest not in ["none", ""]:
                if chest.visible and chest not in room.local:
                    room.local.append(chest)
                    game.player.local_chests.append(chest)
        return "SUCCESS"


# * Check
# * Displays text describing a specific object
# *####################
class Check(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        obj = mods[0]
        if not obj.checkable:
            error = [f"You don't see a {obj.name}\n"]
            error.append("ERROR: Object Not Checkable")
            raise InvalidTurn(error)

        if obj.type == "room":
            str = f"You can't check the {obj.name}\n"
            str += "Try walking there and using Look"
            error = [str]
            error.append("ERROR: Tried To Check A Room")
            raise InvalidTurn(error)

    def __call__(self, mods: list[object], game: object):
        obj = mods[0]

        # Checktext
        chk_target = obj.checktext_dict[obj.state]
        chktxt = game.services.text_fetcher("check", obj.name, chk_target)
        game.player.turn_text.extend(chktxt)  # Retrieves check text

        # Check Triggers
        if "none" not in obj.key:
            Triggers("check", obj, game)

        # Add items to local
        for itm in obj.inventory:
            item = obj.inventory[itm]
            if item != "none":
                if item.visible and item not in game.player.location.local:
                    game.player.location.local.append(item)
                    game.player.local_items.append(item)

        return "SUCCESS"


# * Take
# * Removes a nearby object from it's chest, adds it to player inventory
# *####################
class Take(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        obj = mods[0]
        if obj in game.player.inventory:
            error = [f"You already have the {obj.name}\n"]
            error.append("ERROR: Object Already In Inventory")
            raise InvalidTurn(error)

        if obj.type != "item":
            error = [f"You can't take the {obj.name}\n"]
            error.append("ERROR: Tried To Take Non-Item Object")
            raise InvalidTurn(error)

        if not all([obj.takeable]):
            error = [f"There isn't a {obj.name} you can take\n"]
            error.append("ERROR: Object Not Takeable")
            raise InvalidTurn(error)

    def __call__(self, mods: list[object], game: object):
        obj = mods[0]

        # Add to player inventory
        game.player.inventory.append(obj)
        game.player.turn_text.append(f"You take the {obj.name}")

        # Take Triggers
        if "none" not in obj.key:
            Triggers("take", obj, game)

        # Remove from locals and chest
        game.player.local_items.remove(obj)
        game.player.location.local.remove(obj)
        for chest in game.player.location.inventory:
            if obj.name in game.player.location.inventory[chest].inventory:
                del game.player.location.inventory[chest].inventory[obj.name]
        return "SUCCESS"


# * Walk
# * Moves the player to an adjacent room
# *####################
class Walk(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        room = mods[0]
        if room == game.player.location:
            error = [f"You are already in the {room.name}\n"]
            error.append("ERROR: Already In That Room")
            raise InvalidTurn(error)
        if room.type == "gate" and room.state == "locked":
            error = [f"You can't walk through the {room.name}.\n"]
            error[0].capitalize()
            error.append("ERROR: Gate Locked")
            raise InvalidTurn(error)
        if room.type != "room":
            error = [f"{room.name} is neither a room name, nor a direction.\n"]
            error[0].capitalize()
            error.append("ERROR: Object Not A Room")
            raise InvalidTurn(error)

    def __call__(self, mods: list[object], game: object):
        room = mods[0]
        # Track where player came from
        prev_room = game.player.location

        # Clear player locals
        game.player.local_rooms.clear()
        game.player.local_chests.clear()
        game.player.local_gates.clear()
        game.player.local_items.clear()

        if room.type == "room":
            game.player.location = room
            game.player.turn_text.append("You walk to the " + room.name)

        else:
            for path in game.player.location.routes:
                newroom = game.player.location.routes[path]
                if newroom["cd"] == room.name:
                    self([newroom["room"]], game)

        # Get new locals
        newlocals = game.player.location.local
        if prev_room not in newlocals:
            newlocals.append(prev_room)
        for obj in newlocals:
            if obj.type == "room":
                game.player.local_rooms.append(obj)
            if obj.type == "chest":
                game.player.local_chests.append(obj)
            if obj.type == "gate":
                game.player.local_gates.append(obj)
            if obj.type == "item":
                game.player.local_items.append(obj)
        return "SUCCESS"


# * Speak
# * Displays dialogue text for an NPC. May be removed in the future, undecided.
# *####################
class Speak(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        pass  # ! Speak not implimented yet

    def __call__(self, mods: list[object], game: object):
        game.player.turn_text.append("Speak not implimented yet")
        return "SUCCESS"


# * Use
# * Attempts to use the first item on the second, and checks for triggers
# *####################
class Use(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        for obj in mods:
            if not obj.useable:
                error = [f"There isn't a {obj.name} you can use right now\n"]
                error.append("ERROR: Object Not Useable")
                raise InvalidTurn(error)

    def __call__(self, mods: list[object], game: object):
        obj1, obj2 = mods[0], mods[1]
        if "none" not in obj2.key:
            Triggers(obj1.name, obj2, game)

        return "SUCCESS"


# * Place
# * Remove an item from the player inventory and adds it to a chest
# *####################
class Place(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        pass

    def __call__(self, mods: list[object], game: object):
        game.player.turn_text.append("Place not implimented yet")
        return "SUCCESS"


# * Quit
# * Ends the game and closes the program
# *####################
class Quit(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        if not game.services.double_check("quit"):
            error = ["System Command Canceled"]
            error.append("System Command Canceled")
            raise InvalidTurn(error)

    def __call__(self, mods: list[object], game: object):
        return "GAME OVER"


# * Restart
# * Ends the game and offers replay
# *####################
class Restart(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        if not game.services.double_check("restart"):
            error = ["System Command Canceled"]
            error.append("System Command Canceled")
            raise InvalidTurn(error)

    def __call__(self, mods: list[object], game: object):
        return "RESTART"


# * Tutorial
# * Displays the help screen
# *####################
class Tutorial(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return

    def __call__(self, mods: list[object], game: object):

        with open("gamefiles/assets/text/tutorial.md", "r") as file:
            file_contents = file.read()
        game.player.turn_text.append(file_contents)

        return "SUCCESS"


# * Inspect Object
# * Displays a game object
# ! DEBUG FEATURE
# *####################
class InspObj(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return

    def __call__(self, mods: list[object], game: object):
        ic(mods[0])

        return "SUCCESS"


# * Inspect Game
# * Displays all game data
# ! DEBUG FEATURE
# *####################
class InspGame(Command):
    def __init__(self, name: str, alias: list, num_mods: int) -> None:
        super().__init__(name, alias, num_mods)

    def verify(self, mods: list[object], game: object):
        return

    def __call__(self, mods: list[object], game: object):
        ic(game.player)
        ic(game.data)

        return "SUCCESS"


# * GPS
# * Not yet implimented, potential system for directional navigation
# *####################
def gps(game: object, dir: str):
    raise NotImplementedError()


# * Creates command list for start of game
def build_command_list():
    return (
        Look("look", ["look", "l"], 0),
        Check("check", ["check", "c"], 1),
        Take("take", ["take", "t"], 1),
        Walk("walk", ["walk", "w", "move", "m"], 1),
        Speak("speak", ["speak", "s"], 1),
        Use("use", ["use", "u"], 2),
        Place("place", ["place", "p"], 2),
        Quit("quit", ["quit", "q"], 0),
        Restart("restart", ["restart", "r"], 0),
        Tutorial("help", ["tutorial", "help", "h"], 0),
        InspObj("inspobj", ["inspobj", "i"], 1),  # ! Debug command
        InspGame("inspgame", ["inspgame", "game", "g"], 0),  # ! Debug command
    )
