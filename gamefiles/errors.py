"""
Unnamed Text Adventure - Errors
Written by Canahedo and WingusInbound
Python3
2024

This file represents custom exception classes used by the game
"""


class CustomException(Exception):
    def __init__(self, message, return_string):
        self.message = message
        self.return_string = return_string


class BlankInput(CustomException):
    def __init__(self):
        self.return_string = "ERROR: No Input Entered"
        self.message = "Enter a valid command\n"
        super().__init__(self.message, self.return_string)


class CommandNotFound(CustomException):
    def __init__(self, command: str):
        self.command = command
        self.return_string = "ERROR: Command Not Recognized"
        self.message = f"{command} is not a recognized command.\n".capitalize()
        self.message += 'Enter "Help" for more info.\n'
        super().__init__(self.message, self.return_string)


class ObjectNotFound(CustomException):
    def __init__(self, obj: str):
        self.object = obj
        self.return_string = "ERROR: Object Not Found"
        self.message = f'" {obj} " is not a recognized word.\n'
        self.message += "Try something else\n"
        super().__init__(self.message, self.return_string)


class NumberOfMods(CustomException):
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
        self.return_string = "ERROR: Incorrect Number Of Mods"
        s = ""
        if expected != 1:
            s = "s"
        self.message = str(command).capitalize()
        self.message += f" requires exactly {expected} modifier{s}\n"
        super().__init__(self.message, self.return_string)


class InvalidTurn(CustomException):
    def __init__(self, text: list):
        self.message = text[0]
        self.return_string = text[1]
        super().__init__(self.message, self.return_string)
