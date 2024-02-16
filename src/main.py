#!/usr/bin/env python3

"""The entry point for the bot."""

import datetime
import logging
import os
import sched
import threading
import time

import discord

from frame_service import Wavu
from framedb import FrameDb
from heihachi import configurator
from heihachi.bot import FrameDataBot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # TODO: format logger output to include timestamps, line numbers and file names

try:
    config = configurator.Configurator.from_file(os.path.abspath("config.json"))  # TODO: take as cmdline arg
    assert config is not None
except FileNotFoundError:
    logger.error("Config file not found. Exiting.")
    exit(1)

CHARACTER_LIST_PATH = os.path.abspath(os.path.join("src", "resources", "character_list.json"))
JSON_PATH = os.path.abspath(os.path.join("json_movelist"))

try:
    hei = FrameDataBot(config, intents=discord.Intents.default())
    tree = discord.app_commands.CommandTree(hei)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f"{time_now} \n Error: {e}")

wavu = Wavu()
framedb = FrameDb()
try:
    character_list = util.create_json_movelists(CHARACTER_LIST_PATH)
    scheduler = sched.scheduler(time.time, time.sleep)

    # Repeat importing move list of all character from frame service once an hour
    scheduler_thread = threading.Thread(
        target=util.periodic_function,
        args=(
            scheduler,
            3600,
            framedb.load(wavu),
            CHARACTER_LIST_PATH,
        ),  # TODO: schedule calling framedb.load(frame_service) to rebuild frame data
        # TODO: also schedule saving newly loaded frame data to json based on configurable path
    )
    scheduler_thread.start()
    hei.run(config.discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.error(f"{time_now} \n Error: {e}")
