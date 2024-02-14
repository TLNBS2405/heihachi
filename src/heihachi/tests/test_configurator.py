import os

import pytest

from heihachi.configurator import Configurator


@pytest.fixture
def config():
    return Configurator(discord_token="123456789", feedback_channel_id=123456789, action_channel_id=987654321)


def test_from_file():
    config = Configurator.from_file("src/tests/static/test_config.json")
    assert config.discord_token == "123456789"
    assert config.feedback_channel_id == 123456789
    assert config.action_channel_id == 987654321


def test_to_file(config):
    config.to_file("src/tests/static/test_config_tmp.json")
    config = Configurator.from_file("src/tests/static/test_config_tmp.json")
    assert config.discord_token == "123456789"
    assert config.feedback_channel_id == 123456789
    assert config.action_channel_id == 987654321
    os.remove("src/tests/static/test_config_tmp.json")
