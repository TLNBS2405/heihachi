from typing import Tuple
import os
import json
from json import JSONEncoder
from dataclasses import dataclass


@dataclass
class Move:
    id: str
    name: str = ""
    input: str = ""
    target: str = ""
    damage: str = ""
    on_block: str = ""
    on_hit: str = ""
    on_ch: str = ""
    startup: str = ""
    recovery: str = ""
    notes: str = ""
    gif: str = ""
    alias: Tuple[str] = ()


class MoveEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


@dataclass
class Character:
    name: str
    portrait: str
    move_list: Tuple[Move]
    move_list_path: str
    wavu_page: str

    def export_movelist_as_json(self):
        self.__create_move_list_file()
        with open(self.move_list_path, "w", encoding="utf-8") as outfile:
            json.dump(
                self.move_list,
                outfile,
                sort_keys=True,
                indent=4,
                cls=MoveEncoder,
                ensure_ascii=False,
            )

    def __create_move_list_file(self):
        if not os.path.exists(self.move_list_path):
            with open(self.move_list_path, "w"):
                pass


class ClassEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
