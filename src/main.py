import json, datetime, logging, os
import discord

from src.module import character_importer
from src.dc.connector import Discord_Connector
from src.module import configurator

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

base_path = os.path.dirname(__file__)
config = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))

discord_token = config.read_config()['DISCORD_TOKEN']


def create_all_character_json(character_list_path: str):
    try:
        with open(character_list_path) as file:
            characters = json.load(file)

            for character_meta in characters:
                character = character_importer.import_character(character_meta)
                character.export_movelist_as_json()
    except Exception as e:
        raise Exception("Error when importing character from wavu" + str(e))

try:

    client = Discord_Connector(intents=discord.Intents.default())
    client.run(discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')
