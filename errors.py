"""
Unnamed Text Adventure - Errors
Written by Canahedo and WingusInbound
Python3
2024

This file represents custom exception classes used by the game
"""


class CommandNotFound(Exception):
    def __init__(self, command: str):
        self.command = command
        self.message = (
            f'{command} is not a recognized command.',
            '\nEnter "Help" for more info.'
        )
        super().__init__(self.message)


class ObjectNotFound(Exception):
    def __init__(self, obj: str):
        self.object = obj
        self.message = f'" {obj} " was not recognized.'
        super().__init__(self.message)


class NumberOfMods(Exception):
    def __init__(self, command: str, expected: int):
        """
        Raised when a player-entered command is recognized,
        but number of mods doesn't match expected number

        Args:
            command (str): name of player command
            exp_mods (int): expected number of mods of command
        """
        self.command = command
        self.expected = expected
        s = ""
        if expected != 1:
            s = "s"
        self.message = str(command).capitalize()
        self.message.append(f"requires exactly {expected} modifier{s}")
        super().__init__(self.message)


class InvalidTurn(Exception):
    def __init__(self):
        pass
