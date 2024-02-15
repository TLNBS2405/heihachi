import os

from heihachi import json_movelist_reader

STATIC_BASE = os.path.join(os.path.dirname(__file__), "static")


def test_get_movelist_from_json() -> None:
    result = json_movelist_reader.get_movelist("azucena", STATIC_BASE)
    assert result[0].id == "Azucena-1"
