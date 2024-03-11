import json
import logging
import os

import requests

from framedb import Character, CharacterName, FrameService, Move, Url

logger = logging.getLogger("main")


class JsonDirectory(FrameService):
    def __init__(self, char_meta_dir: str, movelist_dir: str) -> None:
        self.name = f"JSON Directory ({movelist_dir})"
        self.icon = None
        self.movelist_dir = movelist_dir

        try:
            with open(char_meta_dir, "r") as f:
                self.character_meta = json.load(f)
        except Exception as e:
            raise Exception(f"Could not load character meta data from {char_meta_dir}") from e

    def get_frame_data(self, character: CharacterName, session: requests.Session | None = None) -> Character:
        # TODO: duplicated across wavu and json_directory -> refactor
        target_char_meta = None
        for char_meta in self.character_meta:
            if char_meta["name"] == character.value:
                target_char_meta = char_meta
                break
        if target_char_meta is None:
            raise Exception(f"Could not find character meta data for {character.value}")

        name = CharacterName(target_char_meta["name"])
        portrait = target_char_meta["portrait"]
        page = target_char_meta["page"]

        filepath = os.path.abspath(os.path.join(self.movelist_dir, f"{character.value}.json"))
        with open(filepath, encoding="utf-8") as move_file:
            move_file_contents = json.load(move_file)
            movelist = {
                move["id"]: Move(
                    id=move["id"],
                    name=move["name"],
                    input=move["input"],
                    target=move["target"],
                    damage=move["damage"],
                    on_block=move["on_block"],
                    on_hit=move["on_hit"],
                    on_ch=move["on_ch"],
                    startup=move["startup"],
                    recovery=move["recovery"],
                    notes=move["notes"],
                    image=move["image"],
                    video=move["video"],
                    alias=move["alias"],
                )
                for move in move_file_contents
            }
        char = Character(name, portrait, movelist, page)
        return char

    def get_move_url(self, character: Character, move: Move) -> Url | None:
        return None
