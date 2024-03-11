import os

import pytest

from frame_service import JsonDirectory
from framedb import CharacterName

STATIC_BASE = os.path.join(os.path.dirname(__file__), "static")


@pytest.fixture
def json_directory() -> JsonDirectory:
    return JsonDirectory(
        char_meta_dir=os.path.join(STATIC_BASE, "character_list.json"),
        movelist_dir=os.path.join(STATIC_BASE, "json_movelist"),
    )


def test_get_movelist_from_json(json_directory: JsonDirectory) -> None:
    char = json_directory.get_frame_data(CharacterName.AZUCENA, None)
    assert char is not None
