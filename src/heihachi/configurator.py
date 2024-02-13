import json
import logging
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class Configurator:
    """
    Class to handle the configuration of the bot
    """

    discord_token: str
    feedback_channel_id: int | None
    action_channel_id: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "DISCORD_TOKEN": self.discord_token,
            "FEEDBACK_CHANNEL_ID": self.feedback_channel_id,
            "ACTION_CHANNEL_ID": self.action_channel_id,
        }

    @staticmethod
    def from_file(config_path: str) -> Optional["Configurator"]:
        """
        Load the configuration from a file
        """

        try:
            with open(config_path) as config_json:
                config_data = json.load(config_json)
                logger.debug(config_data)

            return Configurator(
                discord_token=config_data["DISCORD_TOKEN"],
                feedback_channel_id=config_data.get("FEEDBACK_CHANNEL_ID", None),
                action_channel_id=config_data.get("ACTION_CHANNEL_ID", None),
            )
        except FileNotFoundError:
            logger.error(f"Config file not found at {config_path}")
            return None

    def to_file(self, config_path: str) -> None:
        """
        Write the configuration to a file
        """

        try:
            with open(config_path, "w") as outfile:
                json.dump(self, outfile, cls=ConfiguratorEncoder, indent=4)
        except Exception as e:
            logger.error(f"Error writing to file: {e}")


class ConfiguratorEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for the Configurator class
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, Configurator):
            return o.to_dict()
        return super().default(o)
