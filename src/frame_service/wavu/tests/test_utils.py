import pytest

import frame_service.wavu.utils as utils
from framedb import CharacterName


def test_get_character_movelist() -> None:
    char_name = CharacterName.AZUCENA
    movelist = utils._get_wavu_character_movelist(char_name)
    assert movelist["Azucena-1"].input == "1"
    assert movelist["Azucena-df+1,4"].id == "Azucena-df+1,4"
    assert movelist["Azucena-df+1,4,1"].input == "df+1,4,1"
    assert movelist["Azucena-df+1,4,1"].startup == "i13~14"
    assert movelist["Azucena-f+4,4~3"].input == "f+4,4~3"
    assert movelist["Azucena-LIB.1,2"].damage == "14,20"
    assert movelist["Azucena-b+4,3,4,3"].damage == "10,10,16,23"
    assert movelist["Azucena-b+4,3,4,3"].startup == "i15~16"
    assert movelist["Azucena-df+1,4,1~2"].input == "df+1,4,1~2"
    assert movelist["Azucena-ws4,1,3"].on_ch == "[+27a](https://wavu.wiki/t/Azucena_combos#Mini-combos 'Mini-combo')"
    assert movelist["Azucena-BT.3"].on_hit == "+4~+5"

    char_name = CharacterName.ASUKA
    movelist = utils._get_wavu_character_movelist(char_name)
    assert movelist["Asuka-Destabilizer.1"].alias == ["f+2+4,1"]
    assert movelist["Asuka-f+1+3"].alias == ["f+2+4"]

    char_name = CharacterName.BRYAN
    movelist = utils._get_wavu_character_movelist(char_name)
    assert movelist["Bryan-4,3,f+4"].on_ch == "[+31a (+21)](https://wavu.wiki/t/Bryan_combos#Staples 'Combo')"

    char_name = CharacterName.JUN
    movelist = utils._get_wavu_character_movelist(char_name)
    move = movelist["Jun-1,2,u_d"]
    assert move.alias == ["1,2,d"]
    assert move.input == "1,2,u"

    char_name = CharacterName.JIN
    movelist = utils._get_wavu_character_movelist(char_name)
    assert movelist["Jin-1,2,3"].name == "Left Right > Axe Kick"


def test_convert_json_move() -> None:
    pass


def test_convert_json_movelist() -> None:
    pass


def test_convert_wavu_movelist() -> None:
    pass


def test_normalize_data() -> None:
    pass


def test_create_aliases() -> None:
    assert utils._create_aliases("f+2+4,1") == ("f+2+4,1", [])
    assert utils._create_aliases("f+1+3_f+2+4") == ("f+1+3", ["f+2+4"])


def test_remove_html_tags() -> None:
    pass


def test_process_links() -> None:
    assert utils._process_links("[[Snake_Edge|Snake Edge]]") == "[Snake Edge](https://wavu.wiki/t/Snake_Edge 'Snake Edge')"
    assert (
        utils._process_links("[[Azucena combos#Mini-combos|+27a]]")
        == "[+27a](https://wavu.wiki/t/Azucena_combos#Mini-combos 'Mini-combo')"
    )
