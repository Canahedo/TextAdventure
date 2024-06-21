"""
Unnamed Text Adventure - Update Locals
Written by Canahedo and WingusInbound
Python3
2024

Updates lists of which object the player is in range of
"""

# ! Legacy code below this point
# ! May be valid, needs verification


def get_locals(self, game):
    self.local_chests.clear()
    self.local_items.clear()
    self.local_rooms.clear()
    for chest in self.location.inventory:
        if chest == "none":
            continue
        if self.location.inventory[chest].visible:
            self.local_chests.append(self.location.inventory[chest])
            for item in self.location.inventory[chest].inventory:
                if item == "none":
                    continue
                prosp_item = self.location.inventory[chest].inventory[item]
                if prosp_item.visible:
                    self.local_items.append(prosp_item)
    for direction in self.location.routes:
        room_name = None
        foo = self.location.routes[direction]
        if foo["door"] == "none":
            room_name = foo["room"]
        else:
            door_obj = game.services.locate_object(foo["door"], game.data)
            door_state = door_obj.state
            if door_state not in ["locked"]:
                room_name = foo["room"]
        if room_name is not None:
            room_obj = game.services.locate_object(room_name, game.data)
            if room_obj.visible:
                self.local_rooms.append(room_obj)
