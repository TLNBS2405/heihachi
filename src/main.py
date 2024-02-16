#!/usr/bin/env python3

"""The entry point for the bot."""

import argparse
import logging
import os
import sched
import threading
import time
from typing import Any, Callable, Tuple

from frame_service import Wavu
from framedb import FrameDb
from heihachi import Configurator
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


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Heihachi bot")
    parser.add_argument("config_file", type=str, help="Path to the config file")
    parser.add_argument(
        "--export_dir",
        type=str,
        default=os.path.join(os.getcwd(), "json_movelist"),
        help="Path to the directory to export frame data to",
    )
    parser.add_argument("--format", type=str, default="json", help="Format to export frame data to")
    return parser


def main() -> None:
    parser = get_argparser()
    args = parser.parse_args()
    config_file_path = args.config_file
    export_dir_path = args.export_dir
    _format = args.format

    # retrieve config
    try:
        config = Configurator.from_file(config_file_path)
        assert config is not None
        logger.info(f"Config file loaded from {config_file_path}")
    except FileNotFoundError:
        logger.error(f"Config file not found at {config_file_path}. Exiting...")
        exit(1)

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
