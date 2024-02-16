import os
from typing import Callable

import pytest

from frame_service.wavu.tests.test_wavu import STATIC_BASE
from heihachi.configurator import Configurator

STATIC_BASE = os.path.join(os.path.dirname(__file__), "static")


@pytest.fixture
def config() -> Configurator:
    return Configurator(
        discord_token="123456789",
        feedback_channel_id=123456789,
        action_channel_id=987654321,
        blacklist=None,
        id_blacklist=None,
    )


def test_from_file() -> None:
    config = Configurator.from_file(os.path.join(STATIC_BASE, "test_config.json"))
    assert config
    assert config.discord_token == "123456789"
    assert config.feedback_channel_id == 123456789
    assert config.action_channel_id == 987654321


def test_to_file(config: Configurator) -> None:
    config.to_file(os.path.join(STATIC_BASE, "test_config_tmp.json"))
    new_config = Configurator.from_file(os.path.join(STATIC_BASE, "test_config_tmp.json"))
    assert new_config
    assert new_config.discord_token == "123456789"
    assert new_config.feedback_channel_id == 123456789
    assert new_config.action_channel_id == 987654321
    os.remove(os.path.join(STATIC_BASE, "test_config_tmp.json"))
