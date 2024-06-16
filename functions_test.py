# ! This is just to make pytest happy
from functions import Game_Functions
from objects import Game_Data
from player import Player
from services import Services


success_string = "Turn Executed Successfully"

handled_errors = [
    "ERROR: Object Fetch Failed",
    "ERROR: System Command",
    "ERROR: Invalid Turn",
]


def test_look() -> None:
    game = Game_Functions(Services(), Game_Data(), Player())
    game.data.reset(game)
    game.player.reset(game)
    turn_list = [
        "look",
    ]

    for turn in turn_list:
        raw_input = turn
        comm_str, mod_strs = game.input_handler(raw_input)
        test_output = game.game_loop(comm_str, mod_strs)
    assert test_output == "Turn Executed Successfully"


def test_open_door() -> None:
    game = Game_Functions(Services(), Game_Data(), Player())
    game.data.reset(game)
    game.player.reset(game)
    turn_list = [
        "look",
        "check rock",
        "take key",
        "walk porch",
        "use key door",
    ]

    for turn in turn_list:
        raw_input = turn
        comm_str, mod_strs = game.input_handler(raw_input)
        test_output = game.game_loop(comm_str, mod_strs)
        assert test_output == "Turn Executed Successfully"


def test_invalid_turn() -> None:
    game = Game_Functions(Services(), Game_Data(), Player())
    game.data.reset(game)
    game.player.reset(game)
    turn_list = [
        "look dog",
    ]

    for turn in turn_list:
        raw_input = turn
        comm_str, mod_strs = game.input_handler(raw_input)
        test_output = game.game_loop(comm_str, mod_strs)
    assert test_output in handled_errors
