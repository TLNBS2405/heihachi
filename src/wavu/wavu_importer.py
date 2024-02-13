import os

from heihachi import character
from resources import MOVELIST_BASE_PATH
from wavu import wavu_reader


def import_character(character_meta: dict) -> character.Character:
    name = character_meta["name"]
    portrait = character_meta["portrait"]
    wavu_page = character_meta["wavu_page"]

    move_list = wavu_reader.get_wavu_character_movelist(name)
    cha = character.Character(name, portrait, move_list, wavu_page)
    return cha
