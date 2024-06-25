"""
Unnamed Text Adventure - Triggers
Written by Canahedo and WingusInbound
Python3
2024

This file contains classes which handle
changes that result from the player turn
"""

from icecream import ic


class Triggers:
    def __init__(self, prospect: str, target: object, game: object) -> None:
        self.prosp = prospect
        self.target = target
        self.game = game
        self.player = game.player
        self.data = game.data
        self.services = game.services
        self.checkkeys()

    def checkkeys(self):
        if self.prosp in self.target.key:
            self.triggers(self.target, self.target.key[self.prosp])
            del self.target.key[self.prosp]

    # * Triggers
    # *####################
    def triggers(self, obj: object, trigger: dict) -> None:
        # * trigger (dict): Block of triggers to be executed

        # State
        obj.state = trigger["state"]  # Set state of object

        # Trigger Text
        a, b, c = "triggers", obj.name, trigger["trigger_text"]
        txt = self.services.text_fetcher(a, b, c)
        self.player.turn_text.extend(txt)

        # Attrs
        for attr in trigger["attr_changes"]:
            if attr != "none":
                setattr(obj, attr, trigger["attr_changes"][attr])

        # Ext Triggers
        for prosp in trigger["ext_triggers"]:  # Checks for external triggers
            if prosp != "none" and prosp not in ["player_inv", "reveal"]:
                obj = self.targ_findobj(prosp, self.game)
                if obj is not None:
                    Triggers(trigger["ext_triggers"][prosp], obj, self.game)

            if prosp == "player_inv":
                for line in trigger["ext_triggers"][prosp]:
                    new_item = trigger["ext_triggers"][prosp][line]
                    new_obj = self.targ_findobj(new_item, self.game)
                    if new_obj is not None:
                        if line == "add":
                            self.player.inventory.append(new_obj)
                        if line == "del":
                            self.player.inventory.remove(new_obj)

            if prosp == "reveal":
                for obj in trigger["ext_triggers"]["reveal"]:
                    target = self.targ_findobj(obj, self.game)
                    if target is not None:
                        target.visible = True
                        ic(obj)

    # Handler which acts as an interface between triggers code and findobj
    def targ_findobj(self, prosp, game):
        for lst in [
            game.data.item_list,
            game.data.chest_list,
            game.data.room_list,
            game.data.gate_list,
        ]:
            new_obj = game.services.findobj(prosp, lst)
            return new_obj
