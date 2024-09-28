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
    assert char.portrait == "https://wavu.wiki/t/Special:Redirect/file/AzucenaT8.png"


def test_all_char_meta() -> None:
    wavu = Wavu()
    assert len(wavu.character_meta) == NUM_CHARACTERS


def test_crush_states_dotlist() -> None:
    wavu = Wavu()
    with requests.session() as session:
        char = wavu.get_frame_data(CharacterName.ZAFINA, session)
    assert "&lt" not in char.movelist["Zafina-MNT.uf+3"].notes
    assert "div" not in char.movelist["Zafina-MNT.uf+3"].notes


def test_name_dotlist() -> None:
    wavu = Wavu()
    with requests.session() as session:
        char = wavu.get_frame_data(CharacterName.YOSHIMITSU, session)
    assert "div" not in char.movelist["Yoshimitsu-b+1+2"].name


def test_startup_dotlist() -> None:
    wavu = Wavu()
    with requests.session() as session:
        char = wavu.get_frame_data(CharacterName.YOSHIMITSU, session)
    assert "div" not in char.movelist["Yoshimitsu-KIN.f+1"].startup
