from src.resources import const
import os, json

base_path = os.path.dirname(__file__)


def get_movelist(character_name: str) -> dict:
    os.path.abspath(os.path.join(base_path, "..", "json_movelist", character_name + ".json"))
    filepath = os.path.abspath(os.path.join(base_path, "..", "json_movelist", character_name + ".json"))
    with open(filepath, encoding='utf-8') as move_file:
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

def _correct_move_type(move_type :str) -> str:
    for k in const.MOVE_TYPES.keys():
        if move_type in const.MOVE_TYPES[k]:
            return k

def get_by_move_type(move_type: str, move_list: dict) -> list:
    """Gets a list of moves that match move_type from local_json
    returns a list of move Commands if finds match(es), else empty list"""
    move_type = _correct_move_type(move_type.lower()).lower()
    moves = list(filter(lambda x: (move_type in x["notes"].lower()), move_list))

    if moves:
        result = []
        for move in moves:
            result.append(move['input'])
        return list(set(result))
    else:
        return []
