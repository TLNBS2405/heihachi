import os

from heihachi import character
from wavu import wavu_reader
from resources import MOVELIST_BASE_PATH


def import_character(character_meta: dict) -> character.Character:
    name = character_meta["name"]
    portrait = character_meta["portrait"]
    wavu_page = character_meta["wavu_page"]

    move_list = wavu_reader.get_wavu_character_movelist(name)
    move_list_path = os.path.abspath(os.path.join(MOVELIST_BASE_PATH, name + ".json"))
    cha = character.Character(name, portrait, move_list, move_list_path, wavu_page)
    return cha
