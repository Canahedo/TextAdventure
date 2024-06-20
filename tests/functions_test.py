"""
Unnamed Text Adventure - Function Test
Written by Canahedo and WingusInbound
Python3
2024

Tests the game loop function by providing dummy inputs
"""

from gamefiles.subfunctions.setupwizard import SetupWizard
from ..gamefiles.functions import Game_Functions
from ..gamefiles.objects import Game_Data
from ..gamefiles.player import Player
from gamefiles.services import Services


# *
# *  Variables
# *####################

debug_line = "################################################################"

success = ["SUCCESS"]

error = [
    "ERROR: No Input Entered",
    "ERROR: Command Not Recognized",
    "ERROR: Incorrect Number Of Mods",
    "ERROR: Object Not Found",
    "ERROR: Object Not Checkable",
    "ERROR: Object Not Takeable",
    "ERROR: Object Not Useable",
    "ERROR: Tried To Take Non-Item Object",
    "ERROR: Tried To Check A Room",
    "ERROR: Chest Not Local",
    "ERROR: Item Not Local",
    "ERROR: Item Not Local And Not In Inv",
    "ERROR: Object Already In Inventory",
    "ERROR: Already In That Room",
    "ERROR: Object Not A Room",
    "ERROR: No Way In" "System Command Canceled",
]


# *
# *  Setup
# *####################
def setup():
    # * Initializes new game for testing
    game = Game_Functions(Game_Data(), Player(), Services())
    SetupWizard(game.data, game.player, game.services)
    return game


# *
# *  Base Test Types
# *####################
def complete(turn_list: list[str]) -> str:
    """
    For a "complete" test, turn list should be formatted as
        a list of strings representing player inputs:
    turn_list = [
        "check rock",
        "take key"
    ]
    This test expects no errors to occurr in the entire turn list,
        and checks that the final test returns "Turn Executed Successfully"
    """
    game = setup()
    for turn in turn_list:
        print(debug_line)
        test_output = game.game_loop(turn)
        print(f"{turn} -> {test_output}")
    if test_output in success:
        return True


def each(turn_list: list[list[str]]) -> str:
    """
    For an "each" test, turn list should be formatted as
        a list of lists, representing player inputs and
        either success or error, depending on expected result:
    turn_list = [
        ["check rock", success],
        ["check foo", error]
    ]
    If any turn returns a result different than expected,
        the test will fail
    """
    game = setup()
    for turn in turn_list:
        print(debug_line)
        test_output = game.game_loop(turn[0])
        print(f"{turn[0]} -> {test_output}")
        if test_output not in turn[1]:
            return False
    return True


# *
# *  Tests
# *####################
def test_complete_just_boot() -> None:
    """
    Tries to launch game
    """
    game = setup()
    print(game)
    loc = game.player.location.name
    assert loc == "driveway"


def test_complete_just_look() -> None:
    """
    Tries to launch game and look
    """
    turn_list = [
        "look",
    ]
    assert complete(turn_list)


def test_complete_open_door() -> None:
    """
    Tries to get key and open door
    """
    turn_list = [
        "look",
        "check rock",
        "take key",
        "walk porch",
        "look",
        "use key door",
    ]
    assert complete(turn_list)


def test_each_open_door() -> None:
    """
    Tries to get key and open door
    """
    turn_list = [
        ["look", success],
        ["check rock", success],
        ["take key", success],
        ["walk porch", success],
        ["look", success],
        ["use key door", success],
    ]
    assert each(turn_list)


def test_each_handled_errors() -> None:
    """
    Checks for possible issues which should be accounted for
    """
    turn_list = [
        [" ", error],
        ["look dog", error],
        ["check door", error],
        [".", error],
    ]
    assert each(turn_list)


def test_each_walk_look() -> None:
    """
    Walks to each room, and tries to look
    """
    room_list = ["porch", "driveway", "porch", "foyer", "kitchen", "foyer"]
    turn_list = [["look", success]]
    for room in room_list:
        turn_list.append([f"walk {room}", success])
        turn_list.append(["look", success])
    assert each(turn_list)
