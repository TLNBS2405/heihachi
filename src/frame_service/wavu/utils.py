import html
import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

from framedb.character import Move
from framedb.const import CharacterName

WAVU_API_URL = "https://wavu.wiki/w/api.php"

"""Available fields for the Move table in the Wavu DB"""
FIELDS = [
    "id",
    "name",
    "input",
    "parent",
    "target",
    "damage",
    "startup",
    "recv",
    "tot",
    "crush",
    "block",
    "hit",
    "ch",
    "notes",
    # "alias",
    # "image",
    # "video",
    "_pageNamespace=ns",
]


@dataclass
class WavuMove(Move):
    parent: str = ""


def _get_wavu_character_movelist(character_name: CharacterName, format: str = "json") -> Dict[str, Move]:
    """
    Get the movelist for a character from the Wavu API
    """

    params = {
        "action": "cargoquery",
        "tables": "Move",
        "fields": ",".join(FIELDS),
        "where": f"id LIKE '{character_name.value.title()}%'",
        "having": "",
        "order_by": "id",
        "limit": "500",  # TODO: could probably limit this further?
        "format": format,
    }

    with requests.session() as session:
        response = session.get(WAVU_API_URL, params=params)  # TODO: use MediaWiki library to handle
    content = json.loads(response.content)
    movelist_raw = content["cargoquery"]
    match format:
        case "json":
            movelist = _convert_wavu_movelist(_convert_json_movelist(movelist_raw))
        case _:
            raise NotImplementedError(f"Format {format} not implemented")
    return movelist


def _convert_json_move(move_json: Any) -> WavuMove:
    """
    Convert a JSON response object into a WavuMove object
    Process each field to ensure it is in the correct format
    """

    id = _normalize_data(move_json["id"])
    parent = _normalize_data(move_json["parent"])

    name = html.unescape(_normalize_data(_process_links(move_json["name"])))

    input = _normalize_data(move_json["input"])
    if "_" in input:
        input, alias = _create_aliases(input)
    else:
        alias = []

    target = _normalize_data(move_json["target"])

    damage = _normalize_data(move_json["damage"])

    on_block = _remove_html_tags(_normalize_data(move_json["block"]))

    on_hit = _remove_html_tags(_normalize_data(_process_links(move_json["hit"])))

    on_ch = _remove_html_tags(_normalize_data(_process_links(move_json["ch"])))
    if not on_ch or on_ch == "":
        on_ch = on_hit

    startup = _normalize_data(move_json["startup"])

    recovery = _normalize_data(move_json["recv"])

    notes = _remove_html_tags(_process_links(move_json["notes"]))

    move = WavuMove(
        id,
        name,
        input,
        target,
        damage,
        on_block,
        on_hit,
        on_ch,
        startup,
        recovery,
        notes,
        "",  # image
        "",  # video
        tuple(alias),
        parent,
    )
    return move


def _convert_json_movelist(movelist_json: List[Any]) -> List[WavuMove]:
    """
    Convert a list of JSON response objects into a list of WavuMove objects
    Process each field to ensure it is in the correct format
    """

    movelist = [move["title"] for move in movelist_json]  # Wavu response nests moves under 'title' field
    movelist = [move for move in movelist if move["ns"] == "0"]  # TODO: not sure why we need this
    movelist = [_convert_json_move(move) for move in movelist]
    return movelist


def _convert_wavu_movelist(movelist: List[WavuMove]) -> Dict[str, Move]:
    """
    Convert a list of WavuMove objects into a dictionary of Move objects

    Retrieve parent values for the input, target, and damage fields and assign them.
    """

    wavu_movelist = {move.id: move for move in movelist}
    seen = {move.id: False for move in movelist}

    for move in movelist:
        stack = []  # "function call stack"
        curr_move = move
        while curr_move.parent and not seen[curr_move.id]:
            stack.append(curr_move.id)
            seen[curr_move.id] = True
            curr_move = wavu_movelist[curr_move.parent]

        parent_input = curr_move.input
        parent_target = curr_move.target
        parent_damage = curr_move.damage
        seen[curr_move.id] = True

        while stack:
            curr_id = stack.pop()
            curr_move = wavu_movelist[curr_id]

            curr_move.input = parent_input + curr_move.input
            curr_move.target = parent_target + curr_move.target
            curr_move.damage = parent_damage + curr_move.damage
            seen[curr_move.id] = True

            parent_input = curr_move.input
            parent_target = curr_move.target
            parent_damage = curr_move.damage

    return {move.id: move for move in movelist}


def _empty_value_if_none(value: str | None) -> str:
    return value if value else ""


def _normalize_data(data: str | None) -> str:
    if data:
        # remove non-ascii stuff
        return re.sub(r"[^\x00-\x7F]+", "", data)
    else:
        return ""


def _create_aliases(input: str) -> Tuple[str, List[str]]:
    """
    Create move aliases from the input string

    E.g., "f+1+3_f+2+4" -> ["f+2+4", "f+1+3"]
    """

    parts = input.split("_")
    input = parts[0]
    aliases = parts[1:]
    result = []
    for entry in aliases:  # TODO: this can probably be done better
        num_characters = len(entry)
        x = len(input) - num_characters
        if x < 0:
            x = 0
        original_input = input[0:x]
        alias = original_input + entry
        if len(alias) > len(input):
            input = input + entry[len(input) :]

        result.append(alias)
    return input, result


def _remove_html_tags(data: str) -> str:
    "Process HTML content in JSON response to remove tags and unescape characters"

    result = html.unescape(_normalize_data(data))
    result = BeautifulSoup(result, features="lxml").get_text()
    result = result.replace("* \n", "* ")
    result = re.sub(r"(\n)+", "\n", result)
    result = result.replace("'''", "")
    result = result.replace("**", " *")  # hack/fix for nested Plainlists
    return result


link_replace_pattern = re.compile(r"\[\[(?P<page>[^#]+)(#(?P<section>[^|]+))?\|(?P<data>[^|]+)\]\]")
WAVU_PAGE_STEM = "https://wavu.wiki/t/"


def _process_links(data: str | None) -> str:
    def _replace_link(matchobj):
        page, section, data = (
            matchobj.group("page"),
            matchobj.group("section"),
            matchobj.group("data"),
        )
        if section:
            match section:
                case "Staples":
                    hover_text = "Combo"
                case "Mini-combos":
                    hover_text = "Mini-combo"
                case _:
                    hover_text = page.replace("_", " ").title()
            replacement = f"[{data}]({WAVU_PAGE_STEM}{page.replace(' ', '_')}#{section} '{hover_text}')"
        else:
            hover_text = page.replace("_", " ").title()
            replacement = f"[{data}]({WAVU_PAGE_STEM}{page.replace(' ', '_')} '{hover_text}')"
        return replacement

    return link_replace_pattern.sub(_replace_link, _empty_value_if_none(data))
