#!/usr/bin/env python3

"""The entry point for the bot."""

import datetime
import logging
import os
import sched
import sys
import threading
import time

from frame_service import Wavu
from framedb import FrameDb
from heihachi import configurator
from heihachi.bot import FrameDataBot, periodic_function

"How often to update the bot's frame data from the external service and write to file."
UPDATE_INTERVAL_SEC = 3600

logger = logging.getLogger(__name__)
logger.setLevel(
    logging.DEBUG
)  # TODO: format logger output to include timestamps, line numbers and file names and print to stdout
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def main() -> None:
    # retrieve config
    try:
        config = configurator.Configurator.from_file(sys.argv[1])  # TODO: potentially use argparse
        assert config is not None
    except FileNotFoundError:
        logger.error(f"Config file not found at {sys.argv[1]}. Exiting...")
        exit(1)

    export_dir_path = os.path.join(os.getcwd(), "json_movelist")

    # initialize bot
    try:
        frame_service = Wavu()
        framedb = FrameDb()
        framedb.load(frame_service)
        hei = FrameDataBot("/", framedb, frame_service, config)

    except Exception as e:
        # time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        logger.error(f"Failed to initialize bot: {e}")
        exit(1)

    # schedule and start the frame refresh thread
    try:
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler_thread = threading.Thread(
            target=periodic_function,
            args=(scheduler, UPDATE_INTERVAL_SEC, framedb.refresh, (frame_service, export_dir_path, "json")),
        )
        scheduler_thread.start()

    except Exception as e:
        logger.error(f"Error in scheduling the frame refresh thread: {e}")

    # start the bot
    try:
        hei.run(config.discord_token)
    except Exception as e:
        logger.error(f"Error in running the bot: {e}")


if __name__ == "__main__":
    main()
