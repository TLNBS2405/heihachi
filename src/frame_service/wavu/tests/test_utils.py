import json
import os
from typing import Any

import pytest

import frame_service.wavu.utils as utils
from frame_service.wavu.tests.test_wavu import STATIC_BASE
from framedb import CharacterName


@pytest.fixture
def wavu_response(request: Any) -> Any:
    with open(os.path.join(STATIC_BASE, f"{request.param.value}.json"), "r") as f:
        return request.param, json.load(f)


@pytest.mark.skip(reason="Not implemented")
def test_get_wavu_response() -> None:
    pass


class TestGetWavuCharacterMovelist:
    @pytest.mark.parametrize("wavu_response", [CharacterName.AZUCENA], indirect=True)
    def test_get_wavu_character_movelist(self, wavu_response: Any) -> None:
        char_name, response = wavu_response
        movelist = utils._get_wavu_character_movelist(response)
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

    @pytest.mark.parametrize("wavu_response", [CharacterName.ASUKA], indirect=True)
    def test_get_wavu_character_movelist_aliases(self, wavu_response: Any) -> None:
        char_name, response = wavu_response
        movelist = utils._get_wavu_character_movelist(response)
        assert movelist["Asuka-Destabilizer.1"].alias == ("f+2+4,1",)
        assert movelist["Asuka-f+1+3"].alias == ("f+2+4",)

    @pytest.mark.parametrize("wavu_response", [CharacterName.BRYAN], indirect=True)
    def test_get_wavu_character_movelist_links(self, wavu_response: Any) -> None:
        char_name, response = wavu_response
        movelist = utils._get_wavu_character_movelist(response)
        assert movelist["Bryan-4,3,f+4"].on_ch == "[+31a (+21)](https://wavu.wiki/t/Bryan_combos#Staples 'Combo')"

    @pytest.mark.parametrize("wavu_response", [CharacterName.JUN], indirect=True)
    def test_get_wavu_character_movelist_aliases_and_links(self, wavu_response: Any) -> None:
        char_name, response = wavu_response
        movelist = utils._get_wavu_character_movelist(response)
        move = movelist["Jun-1,2,u_d"]
        assert move.alias == ("1,2,d",)
        assert move.input == "1,2,u"

    @pytest.mark.parametrize("wavu_response", [CharacterName.JIN], indirect=True)
    def test_get_wavu_character_movelist_html(self, wavu_response: Any) -> None:
        char_name, response = wavu_response
        movelist = utils._get_wavu_character_movelist(response)
        assert movelist["Jin-1,2,3"].name == "Left Right > Axe Kick"


@pytest.mark.skip(reason="Not implemented")
def test_convert_json_move() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_convert_json_movelist() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_convert_wavu_movelist() -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_normalize_data() -> None:
    pass


def test_create_aliases() -> None:
    assert utils._create_aliases("f+2+4,1") == ("f+2+4,1", ())
    assert utils._create_aliases("f+1+3_f+2+4") == ("f+1+3", ("f+2+4",))


@pytest.mark.skip(reason="Not implemented")
def test_remove_html_tags() -> None:
    pass


def test_process_links() -> None:
    assert utils._process_links("[[Snake_Edge|Snake Edge]]") == "[Snake Edge](https://wavu.wiki/t/Snake_Edge 'Snake Edge')"
    assert (
        utils._process_links("[[Azucena combos#Mini-combos|+27a]]")
        == "[+27a](https://wavu.wiki/t/Azucena_combos#Mini-combos 'Mini-combo')"
    )
    assert (
        utils._process_links("[[Devil Jin combos#Mini-combos|+10]]")
        == "[+10](https://wavu.wiki/t/Devil_Jin_combos#Mini-combos 'Mini-combo')"
    )
