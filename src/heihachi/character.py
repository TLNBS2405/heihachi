import json
import logging
from dataclasses import dataclass
from typing import Tuple

logger = logging.getLogger(__name__)


@dataclass
class Move:
    id: str
    name: str = ""
    input: str = ""
    target: str = ""
    damage: str = ""
    on_block: str = ""
    on_hit: str = ""
    on_ch: str = ""
    startup: str = ""
    recovery: str = ""
    notes: str = ""
    gif: str = ""
    alias: Tuple[str, ...] = ()


@dataclass
class Character:
    name: str

    "The URL to the character's portrait image to be used in embeds"
    portrait: str

    move_list: Tuple[Move, ...]

    "The URL of the character's page on wavu.wiki"
    wavu_page: str

    def export_movelist_as_json(self, move_list_path: str) -> None:
        try:
            with open(move_list_path, "w", encoding="utf-8") as outfile:
                json.dump(
                    self.move_list,
                    outfile,
                    sort_keys=True,
                    default=vars,
                    indent=4,
                    ensure_ascii=False,
                )
        except Exception as e:
            logger.error(f"Error writing to file: {e}")
