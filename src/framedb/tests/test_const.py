from framedb.const import CHARACTER_ALIAS, MOVE_TYPE_ALIAS, NUM_CHARACTERS, SORT_ORDER, CharacterName, MoveType


def test_all_characters_exist() -> None:
    assert len(CharacterName) == NUM_CHARACTERS
    assert len(CHARACTER_ALIAS) == NUM_CHARACTERS


def test_aliases_for_all_chars() -> None:
    for char in CharacterName:
        assert char in CHARACTER_ALIAS


def test_all_move_types_exist() -> None:
    assert len(MoveType) == len(MOVE_TYPE_ALIAS)
    assert len(SORT_ORDER) == len(MOVE_TYPE_ALIAS)
