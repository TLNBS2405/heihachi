#!/usr/bin/env python3

"""The entry point for the bot."""

import logging
import os
import sched
import sys
import threading
import time
from typing import Any, Callable, Tuple

from frame_service import Wavu
from framedb import FrameDb
from heihachi import configurator
from heihachi.bot import FrameDataBot

"How often to update the bot's frame data from the external service and write to file."
UPDATE_INTERVAL_SEC = 3600

logger = logging.getLogger("main")
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s     %(module)s:%(funcName)s:%(lineno)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


def periodic_function(scheduler: sched.scheduler, interval: float, function: Callable, args: Tuple[Any, ...]) -> None:
    "Run a function periodically"

    while True:
        scheduler.enter(interval, 1, function, args)
        scheduler.run()


def main() -> None:
    # retrieve config
    try:
        config = configurator.Configurator.from_file(sys.argv[1])  # TODO: potentially use argparse
        assert config is not None
        logger.info(f"Config file loaded from {sys.argv[1]}")
    except FileNotFoundError:
        logger.error(f"Config file not found at {sys.argv[1]}. Exiting...")
        exit(1)

    export_dir_path = os.path.join(os.getcwd(), "json_movelist")
    _format = "json"

    # initialize bot
    try:
        frame_service = Wavu()
        framedb = FrameDb()
        framedb.refresh(frame_service, export_dir_path, _format)
        logger.info(f"Frame data loaded from service {frame_service.name} and written to {export_dir_path} as {_format}")
        hei = FrameDataBot(framedb, frame_service, config)

    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        exit(1)

    # schedule and start the frame data refresh thread
    try:
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler_thread = threading.Thread(
            target=periodic_function,
            daemon=True,
            args=(scheduler, UPDATE_INTERVAL_SEC, framedb.refresh, (frame_service, export_dir_path, _format)),
        )
        scheduler_thread.start()
        logger.info(f"Frame data refresh thread started with tid: {scheduler_thread.native_id}")

    except Exception as e:
        logger.error(f"Error in scheduling the frame refresh thread: {e}")

    # start the bot
    try:
        logger.info("Starting bot...")
        hei.run(config.discord_token)
    except Exception as e:
        logger.error(f"Error in running the bot: {e}")
    logger.info("Bot stopped")


if __name__ == "__main__":
    main()
