import pytest

from frame_service.json_directory.tests.test_json_directory import json_directory
from framedb import FrameDb, FrameService
from framedb.const import CharacterName, FrameSituation, MoveType


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


def test_sanitize_frame_data(frameDb: FrameDb) -> None:
    assert frameDb._sanitize_frame_data("i59~61") == 59
    assert frameDb._sanitize_frame_data(",i13,14,15") == 13
    assert frameDb._sanitize_frame_data("i13~14,i25 i35 i39 i42") == 13
    assert frameDb._sanitize_frame_data("-5") == -5
    assert frameDb._sanitize_frame_data("+5") == 5
    assert frameDb._sanitize_frame_data("+5~10") == 5
    assert frameDb._sanitize_frame_data("i16") == 16
    assert frameDb._sanitize_frame_data("i5~8") == 5
    assert frameDb._sanitize_frame_data("-5~-10") == -5
    assert frameDb._sanitize_frame_data("+67a (+51)") == 67
    assert frameDb._sanitize_frame_data("invalid data") is None
    assert frameDb._sanitize_frame_data("") is None


def test_get_move_by_frame_on_block(frameDb: FrameDb) -> None:
    # == Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "==", -5, FrameSituation.BLOCK)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-BT.4",
        "Raven-BT.f+2",
        "Raven-BT.f+3",
        "Raven-d+1",
        "Raven-FC.1",
        "Raven-H.BT.4,F",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # > Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, ">", 5, FrameSituation.BLOCK)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = ["Raven-(Back to wall).b,b,UB", "Raven-b+1", "Raven-H.f,f,F+3,4", "Raven-H.2+3"]
    assert set(move_ids) == set(expected_move_ids)

    # >= Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, ">=", 5, FrameSituation.BLOCK)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-H.1+2,F",
        "Raven-H.f+1+2,F",
        "Raven-H.SZN.2,F",
        "Raven-H.ws3+4,F",
        "Raven-(Back to wall).b,b,UB",
        "Raven-b+1",
        "Raven-H.f,f,F+3,4",
        "Raven-H.2+3",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # < Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<", -25, FrameSituation.BLOCK)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = ["Raven-3~4,F", "Raven-b+2,2,1+2", "Raven-BT.3,4,4,F", "Raven-BT.d+3", "Raven-BT.f+3+4,F"]
    assert set(move_ids) == set(expected_move_ids)

    # <= Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<=", -25, FrameSituation.BLOCK)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-3~4,F",
        "Raven-b+2,2,1+2",
        "Raven-BT.3,4,4,F",
        "Raven-BT.d+3",
        "Raven-BT.f+3+4,F",
        "Raven-uf+3+4,3+4",
        "Raven-b+4,B+4~3,3+4",
    ]
    assert set(move_ids) == set(expected_move_ids)


def test_get_move_by_frame_on_hit(frameDb: FrameDb) -> None:
    # == Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "==", 12, FrameSituation.HIT)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-b+2,2,3",
        "Raven-df+3",
        "Raven-SZN.1~F",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # > Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, ">", 45, FrameSituation.HIT)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-H.ws3+4,F",
        "Raven-ws3,2",
        "Raven-H.f,f,F+3,4",
        "Raven-H.ws3,2",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # >= Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, ">=", 44, FrameSituation.HIT)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-H.1+2,F",
        "Raven-BT.4",
        "Raven-H.ws3+4,F",
        "Raven-ws3,2",
        "Raven-H.f,f,F+3,4",
        "Raven-H.ws3,2",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # < Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<", -5, FrameSituation.HIT)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = ["Raven-FC.3", "Raven-3~4,F", "Raven-UB,b,3+4", "Raven-BT.f+3+4,F", "Raven-b+1+3,P"]
    assert set(move_ids) == set(expected_move_ids)

    # <= Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<=", -5, FrameSituation.HIT)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-FC.3",
        "Raven-3~4,F",
        "Raven-UB,b,3+4",
        "Raven-BT.f+3+4,F",
        "Raven-b+1+3,P",
        "Raven-FC.df+3+4",
        "Raven-H.FC.df+3+4",
    ]
    assert set(move_ids) == set(expected_move_ids)


def test_get_move_by_frame_startup(frameDb: FrameDb) -> None:
    # == Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "==", 11, FrameSituation.STARTUP)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-d+2",
        "Raven-df+1+4",
        "Raven-FC.2",
        "Raven-ws4",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # > Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, ">", 26, FrameSituation.STARTUP)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-b+3",
        "Raven-u+3",
        "Raven-u+3,3",
        "Raven-u+3,3,3",
        "Raven-b+1+2",
        "Raven-db+3",
        "Raven-uf+3",
        "Raven-(Back to wall).b,b,UB",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # >= Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, ">=", 26, FrameSituation.STARTUP)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-H.f,f,F+3,4",
        "Raven-f,f,F+3",
        "Raven-b+3",
        "Raven-u+3",
        "Raven-u+3,3",
        "Raven-u+3,3,3",
        "Raven-b+1+2",
        "Raven-db+3",
        "Raven-uf+3",
        "Raven-(Back to wall).b,b,UB",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # < Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<", 10, FrameSituation.STARTUP)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-BT.1",
        "Raven-BT.1,4",
    ]
    assert set(move_ids) == set(expected_move_ids)

    # <= Case
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<=", 10, FrameSituation.STARTUP)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids = [
        "Raven-1",
        "Raven-1,2",
        "Raven-1,2,3+4",
        "Raven-1,2,4",
        "Raven-2",
        "Raven-2,3",
        "Raven-2,4",
        "Raven-BT.1",
        "Raven-BT.1,4",
        "Raven-BT.2",
        "Raven-BT.2,1",
        "Raven-BT.2,1~F",
        "Raven-BT.2,2",
        "Raven-BT.2,2,1",
        "Raven-BT.2,2,3+4",
        "Raven-BT.3",
        "Raven-BT.3,4",
        "Raven-BT.3,4,3",
        "Raven-BT.3,4,4",
        "Raven-BT.3,4,4,F",
        "Raven-BT.d+1",
        "Raven-d+1",
        "Raven-FC.1",
        "Raven-H.BT.2,2,1",
    ]

    assert set(move_ids) == set(expected_move_ids)


def test_get_move_by_frame_no_results(frameDb: FrameDb) -> None:
    returned_moves = frameDb.get_move_by_frame(CharacterName.RAVEN, "<", 1, FrameSituation.STARTUP)
    move_ids = list(map(lambda move: move.id, returned_moves))
    expected_move_ids: list[str] = []
    assert set(move_ids) == set(expected_move_ids)
