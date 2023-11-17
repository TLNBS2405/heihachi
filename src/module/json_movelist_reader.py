from src.resources import const
from src.module import character_importer,character
import os, json
base_path = os.path.dirname(__file__)


def _correct_character_name(alias: str):
    # check if input in dictionary or in dictionary values
    if alias in const.CHARACTER_ALIAS:
        return alias

    for key, value in const.CHARACTER_ALIAS.items():
        if alias in value:
            return key

    return None

def get_movelist_from_json(character_name :str) -> dict:

    character_name = _correct_character_name(character_name)
    os.path.abspath(os.path.join(base_path, "..", "json_movelist", character_name+".json"))
    filepath = os.path.abspath(os.path.join(base_path, "..", "json_movelist", character_name+".json"))

    with open(filepath) as move_file:
        move_file_contents = json.loads(move_file.read())
        return move_file_contents


def _simplify_input(input :str) -> str:
    """Removes bells and whistles from the move_input"""
    short_input = input.strip().lower()
    short_input = short_input.replace("in rage", "")

    for old, new in const.REPLACE.items():
        short_input = short_input.replace(old, new)

    # cd works, ewgf doesn't, for some reason
    if short_input[:2].lower() == 'cd' and short_input[:3].lower() != 'cds':
        short_input = short_input.lower().replace('cd', 'fnddf')
    if short_input[:2].lower() == 'wr':
        short_input = short_input.lower().replace('wr', 'fff')
    return short_input