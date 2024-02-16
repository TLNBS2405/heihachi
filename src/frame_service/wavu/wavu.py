import json
import os

import requests

from framedb import Character, CharacterName, FrameService

from . import utils

WAVU_CHARACTER_META_PATH = os.path.join(os.path.dirname(__file__), "static", "character_list.json")
WAVU_LOGO = "https://wavu.wiki/android-chrome-192x192.png"


class Wavu(FrameService):
    def __init__(self, _format: str = "json") -> None:
        self.name = "Wavu Wiki"
        self.icon = WAVU_LOGO
        self._format = _format

        try:
            with open(WAVU_CHARACTER_META_PATH, "r") as f:
                self.character_meta = json.load(f)
        except Exception as e:
            raise Exception(f"Could not load character meta data from {WAVU_CHARACTER_META_PATH}") from e

    def get_frame_data(self, character: CharacterName, session: requests.Session | None = None) -> Character:
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

        assert session is not None
        response = utils._get_wavu_response(session, name, self._format)
        movelist = utils._get_wavu_character_movelist(response, self._format)
        char = Character(name, portrait, movelist, page)
        return char
