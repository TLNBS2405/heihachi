import json
import os

from frame_service import FrameService
from framedb import Character, CharacterName

from . import wavu_reader

WAVU_CHARACTER_META_PATH = os.path.join(os.path.dirname(__file__), "static", "character_list.json")
WAVU_API_URL = "https://wavu.wiki/w/api.php"
WAVU_LOGO = "https://wavu.wiki/android-chrome-192x192.png"


class Wavu(FrameService):
    def __init__(self) -> None:
        self.name = "Wavu Wiki"
        self.icon = WAVU_LOGO

        try:
            with open(WAVU_CHARACTER_META_PATH, "r") as f:
                self.character_meta = json.load(f)
        except Exception as e:
            raise Exception(f"Could not load character meta data from {WAVU_CHARACTER_META_PATH}") from e

    def get_frame_data(self, character: CharacterName) -> Character:
        target_char_meta = None
        for char_meta in self.character_meta:
            if char_meta["name"] == character.value:
                target_char_meta = char_meta
                break
        if target_char_meta is None:
            raise Exception(f"Could not find character meta data for {character.value}")

        name = target_char_meta["name"]
        portrait = target_char_meta["portrait"]
        page = target_char_meta["page"]

        movelist = wavu_reader.get_wavu_character_movelist(name)
        char = Character(name, portrait, movelist, page)
        return char
