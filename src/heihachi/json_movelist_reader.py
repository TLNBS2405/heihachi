import json
import logging
import os
from typing import Tuple

from framedb.character import Move

logger = logging.getLogger(__name__)


def get_movelist(character_name: str, json_folder_path: str) -> Tuple[Move, ...]:
    filepath = os.path.abspath(os.path.join(json_folder_path, character_name + ".json"))
    with open(filepath, encoding="utf-8") as move_file:
        move_file_contents = json.loads(move_file.read())
        movelist = tuple(Move(**move) for move in move_file_contents)
        return movelist
