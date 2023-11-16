from typing import List
import os, json
from json import JSONEncoder


class Move:
    def __init__(self, id: str, name: str, input: str, target: str, damage: str, on_block: str, on_hit: str, on_ch: str,
                 startup: str, recovery: str, notes: str, gif: str):
        self.id = id
        self.name = name
        self.input = input
        self.target = target
        self.damage = damage
        self.on_block = on_block
        self.on_hit = on_hit
        self.on_ch = on_ch
        self.startup = startup
        self.recovery = recovery
        self.notes = notes
        self.gif = gif

class MoveEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Character:
    def __init__(self, name: str, wavu_page: str, portrait: str, move_list: List[Move], move_list_path: str):
        self.name = name
        self.wavu_page = wavu_page,
        self.portrait = portrait,
        self.move_list = move_list
        self.move_list_path = move_list_path

    def export_movelist_as_json(self):
        self.create_move_list_file()
        with open(self.move_list_path, "w") as outfile:
            json.dump(self.move_list, outfile, sort_keys=True, indent=4, cls=MoveEncoder)

    def create_move_list_file(self):
        if not os.path.exists(self.move_list_path):
            with open(self.move_list_path, "w"): pass


class ClassEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__