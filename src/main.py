import json, datetime, logging, os, discord

from src.module import character_importer
from src.module import configurator
from src.module import json_movelist_reader

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

base_path = os.path.dirname(__file__)
config = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))

discord_token = config.read_config()['DISCORD_TOKEN']


class heihachi(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=645011181739835397))
            self.synced = True
        print('Logged on as', self.user)


try:
    client = heihachi(intents=discord.Intents.default())
    tree = discord.app_commands.CommandTree(client)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')


@tree.command(name="fd", description="Frame data from a character move", guild=discord.Object("645011181739835397"))
async def self(interaction: discord.Interaction, character_name: str, move: str):
    character_name = character_name.lower()
    move_list = json_movelist_reader.get_movelist_from_json(character_name)
    result = json_movelist_reader.get_move(move, move_list)
    await interaction.response.send_message(content=result, ephemeral=False)


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
    client.run(discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')
