import pytest

from frame_service.json_directory.tests.test_json_directory import json_directory
from framedb import FrameDb, FrameService
from framedb.const import CharacterName, MoveType


@pytest.fixture
def frameDb(json_directory: FrameService) -> FrameDb:
    frameDb = FrameDb()
    frameDb.load(json_directory)
    return frameDb


@pytest.mark.skip(reason="Not implemented")
def test_framedb_export() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_framedb_load() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_framedb_refresh() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_build_autocomplete() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_simplify_input() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_is_command_in_alias() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_is_command_in_alt() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_get_move_by_input() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_get_moves_by_move_name() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_get_moves_by_move_type() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_get_moves_by_move_input() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_get_character_by_name(frameDb: FrameDb) -> None:
    assert frameDb.get_character_by_name("reina") == frameDb.frames[CharacterName.REINA]


def test_get_move_type(frameDb: FrameDb) -> None:
    assert frameDb.get_move_type("heat engagers") == MoveType.HE


@pytest.mark.skip(reason="Not implemented")
def test_search_move() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_all_autocomplete_words_match() -> None:
    "Test that all words in the autocomplete list can be matched to a CharacterName"
    pass
