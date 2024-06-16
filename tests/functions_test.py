# ! This is just to make pytest happy
from ..gamefiles.functions import Game_Functions
from ..gamefiles.objects import Game_Data
from ..gamefiles.player import Player
from ..gamefiles.services import Services


success = ["Turn Executed Successfully"]

error = [
    "ERROR: Object Fetch Failed",
    "ERROR: System Command",
    "ERROR: Invalid Turn",
]


def complete(turn_list: list[str]) -> str:
    """
    For a "complete" test, turn list should be formatted as
        a list of strings representing player inputs:
    turn_list = [
        "turn1",
        "turn2
    ]
    This test expects no errors to occurr in the entire turn list,:
        and checks that the final test returns "Turn Executed Successfully"
    """
    game = Game_Functions(Services(), Game_Data(), Player())
    game.data.reset(game)
    game.player.reset(game)
    for turn in turn_list:
        print("##############################################################")
        comm_str, mod_strs = game.input_handler(turn)
        test_output = game.game_loop(comm_str, mod_strs)
        print(f"{turn} -> {test_output}")
    if test_output in success:
        return True


def each(turn_list: list[list[str]]) -> str:
    """
    For an "each" test, turn list should be formatted as
        a list of lists, representing player inputs and
        either success or error, depending on expected result:
    turn_list = [
        ["turn1", success],
        ["turn2", error]
    ]
    If any turn returns a result different than expected,
        the test will fail
    """
    game = Game_Functions(Services(), Game_Data(), Player())
    game.data.reset(game)
    game.player.reset(game)
    for turn in turn_list:
        print("##############################################################")
        comm_str, mod_strs = game.input_handler(turn[0])
        test_output = game.game_loop(comm_str, mod_strs)
        print(f"{turn[0]} -> {test_output}")
        if test_output not in turn[1]:
            return False
    return True


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
    turn_list = [
        ["look dog", error],
        ["check door", error],
    ]
    assert each(turn_list)
