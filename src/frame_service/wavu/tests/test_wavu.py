import os

import requests

from frame_service import Wavu
from framedb import CharacterName
from framedb.const import NUM_CHARACTERS

STATIC_BASE = os.path.join(os.path.dirname(__file__), "static")


def test_wavu_creation() -> None:
    wavu = Wavu()
    assert wavu.name == "Wavu Wiki"
    assert wavu.icon == "https://wavu.wiki/android-chrome-192x192.png"


def test_get_frame_data() -> None:
    wavu = Wavu()
    with requests.session() as session:
        char = wavu.get_frame_data(CharacterName.AZUCENA, session)
    assert char.name.value.title() == "Azucena"
    assert char.portrait == "https://i.imgur.com/fjMRO7I.png"


def test_all_char_meta() -> None:
    wavu = Wavu()
    assert len(wavu.character_meta) == NUM_CHARACTERS
