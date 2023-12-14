from src.resources import const
import os, json

base_path = os.path.dirname(__file__)


def get_movelist(character_name: str) -> dict:
    os.path.abspath(os.path.join(base_path, "..", "json_movelist", character_name + ".json"))
    filepath = os.path.abspath(os.path.join(base_path, "..", "json_movelist", character_name + ".json"))
    with open(filepath) as move_file:
        move_file_contents = json.loads(move_file.read())
        return move_file_contents


def _simplify_input(input: str) -> str:
    """Removes bells and whistles from the move_input"""
    input = input.strip().lower()
    input = input.replace("rage", "r.")
    input = input.replace("heat", "h.")

    for old, new in const.REPLACE.items():
        input = input.replace(old, new)

    # cd works, ewgf doesn't, for some reason
    if input[:2].lower() == 'cd' and input[:3].lower() != 'cds':
        input = input.lower().replace('cd', 'fnddf')
    if input[:2].lower() == 'wr':
        input = input.lower().replace('wr', 'fff')
    return input


def get_move(input: str, character_movelist: dict):
    result = [entry for entry in character_movelist if _simplify_input(entry["input"]) == _simplify_input(input)]

    if result:
        result[0]['input'] = result[0]['input'].replace("\\", "")
        return result[0]
    else:
        return {}
