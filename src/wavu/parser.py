from typing import List

from mediawiki import MediaWiki
import requests

from src.character import Move, Character
from src.resources import const

wavuwiki = MediaWiki(url=const.WAVU_API_URL)
session = requests.Session()


def get_character_movelist(character_name: str) -> List[Move]:
    params = {
        "action": "cargoquery",
        "tables": "Move",
        "fields": "id,name,input,parent,target,damage,startup, recv, tot, crush, block,hit,ch,notes",
        "join_on": "",
        "group_by": "",
        "where": "id LIKE '" + character_name + "%'",
        "having": "",
        "order_by": "id",
        "offset": "0",
        "limit": "500",
        "format": "json"
    }

    response = session.get(const.WAVU_API_URL, params=params)
    move_list_json = response.json()["cargoquery"]
    move_list = convert_json_movelist(move_list_json)
    return move_list


def get_move(move_id: str, move_list: List[Move]) -> Move:
    result = [move for move in move_list if move.id == move_id]
    return result[0]


def get_all_parent_values_of(field: str, move_id: str, move_list_json: list) -> str:
    complete_input = ""
    if move_id:
        for move in move_list_json:
            if move["title"]["id"] == move_id:
                if move["title"]["parent"]:
                    complete_input += get_all_parent_values_of(field, move["title"]["parent"], move_list_json)
                return complete_input + move["title"][field]
    else:
        return ""


def convert_json_movelist(move_list_json: list) -> List[Move]:
    move_list = []
    for move in move_list_json:
        id = move["title"]["id"]
        name = move["title"]["name"]
        input = get_all_parent_values_of("input", move["title"]["parent"], move_list_json) + move["title"]["input"]
        target = move["title"]["target"]
        damage = get_all_parent_values_of("damage", move["title"]["parent"], move_list_json) + move["title"]["damage"]

        on_block = move["title"]["block"]
        on_hit = move["title"]["hit"]
        on_ch = move["title"]["ch"]
        startup = move["title"]["startup"]
        recovery = move["title"]["recv"]

        notes = move["title"]["notes"]

        move = Move(id, name, input, target, damage, on_block, on_hit, on_ch, startup, recovery, notes, "")
        move_list.append(move)
    return move_list
