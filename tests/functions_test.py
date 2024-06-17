# ! This is just to make pytest happy
from ..gamefiles.functions import Game_Functions
from ..gamefiles.objects import Game_Data
from ..gamefiles.player import Player
from ..gamefiles.services import Services

# *
# *  Variables
# *####################

debug_line = "################################################################"

success = ["Turn Executed Successfully"]

error = [
    "ERROR: Object Fetch Failed",
    "ERROR: System Command",
    "ERROR: Invalid Turn",
    "ERROR: No Input Entered",
    "ERROR: Incorrect Number Of Mods",
    "ERROR: Object Not Found",
    "ERROR: Command Not Recognized",
    "ERROR: Chest Not Local",
    "ERROR: Item Not Local",
    "ERROR: Object Not Checkable Or Not Visible",
    "ERROR: Object Not Takeable Or Not Visible",
    "ERROR: Object Not Useable Or Not Visible" "ERROR: Object Not Visible",
    "ERROR: Item Not Local And Not In Inv",
    "ERROR: Object Already In Inventory",
    "ERROR: Already In That Room"
    "ERROR: Object Not A Room"
    "ERROR: Tried To Take Non-Item Object",
    "System Command Canceled",
]


# *
# *  Setup
# *####################
def setup():
    # * Initializes new game for testing
    game = Game_Functions(Services(), Game_Data(), Player())
    game.data.reset(game)
    game.player.reset(game)
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
    if test_output == "Turn Executed Successfully":
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
def test_complete_open_door() -> None:
    """
    Tries to get key and open door
    """
    turn_list = [
        "look",
        "check rock",
        "take key",
        "walk porch",
        "use key door",
    ]
    assert complete(turn_list)


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
