import json, datetime, logging, os, discord, sched, time
from typing import List

from src.module import character_importer
from src.module import configurator
from src.module import json_movelist_reader
from src.module import embed
from src.module import util
from src.module import character


from threading import Thread


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

base_path = os.path.dirname(__file__)
config = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
character_list_path = "resources/character_list.json"
discord_token = config.read_config()['DISCORD_TOKEN']

character_list = []

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
    character_name = util.correct_character_name(character_name.lower())
    character = util.get_character_by_name(character_name, character_list)

    move_list = json_movelist_reader.get_movelist_from_json(character_name)

    character_move = json_movelist_reader.get_move(move, move_list)
    move_embed = embed.move_embed(character, character_move)
    await interaction.response.send_message(embed=move_embed, ephemeral=False)

def create_all_character_json(character_list_path: str) -> List[character.Character]:
    with open(character_list_path) as file:
        characters = json.load(file)
        character_list = []

        for character_meta in characters:
            character = character_importer.import_character(character_meta)
            character.export_movelist_as_json()
            character_list.append(character)

    return character_list


def schedule_create_all_characters(character_list_path: str, scheduler):
    try:
        create_all_character_json(character_list_path)
        scheduler.enter(3600,1,create_all_character_json, (character_list_path,scheduler,))

    except Exception as e:
        raise Exception("Error when importing character from wavu" + str(e))


try:
    ## Repeat creating character json once an hour
    character_list = create_all_character_json(character_list_path)
    print("Character jsons are successfully created")
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(3600,1,schedule_create_all_characters, (character_list_path,scheduler,))
    Thread(target=scheduler.run).start()

    client.run(discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')
