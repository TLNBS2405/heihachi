import json
import logging
from dataclasses import dataclass
from typing import Dict, Tuple

from .const import CharacterName

logger = logging.getLogger("main")

DiscordMd = str  # Discord Markdown
Url = str


@dataclass
class Move:
    id: str
    name: DiscordMd = ""
    input: DiscordMd = ""
    target: DiscordMd = ""
    damage: DiscordMd = ""
    on_block: DiscordMd = ""
    on_hit: DiscordMd = ""
    on_ch: DiscordMd = ""
    startup: DiscordMd = ""
    recovery: DiscordMd = ""
    notes: DiscordMd = ""
    image: Url = ""
    video: Url = ""
    alias: Tuple[DiscordMd, ...] = ()


@dataclass
class Character:
    name: CharacterName

    "The URL to the character's portrait image to be used in embeds"
    portrait: Url

    "A dictionary mapping move IDs to Move objects"
    movelist: Dict[str, Move]

    "The URL of the character's page to link to in embeds"
    page: Url

    def export_movelist(self, movelist_path: str, format: str = "json") -> None:
        "Export a character's movelist to a file."

        match format:
            case "json":
                try:
                    with open(movelist_path, "w", encoding="utf-8") as outfile:
                        json.dump(
                            list(self.movelist.values()),
                            outfile,
                            sort_keys=True,
                            default=vars,
                            indent=4,
                            ensure_ascii=False,
                        )
                except Exception as e:
                    logger.error(f"Error writing to file: {e}")
            case _:
                logger.error(f"Unsupported format: {format}")
                return
