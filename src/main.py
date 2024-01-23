import datetime, logging, os, discord, sched, time, sys
import threading

from src.module import configurator
from src.module import json_movelist_reader
from src.module import embed
from src.module import util

sys.path.insert(0, (os.path.dirname(os.path.dirname(__file__))))

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

base_path = os.path.dirname(__file__)
CONFIG_PATH = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
CHARACTER_LIST_PATH = os.path.abspath(os.path.join(base_path, "resources", "character_list.json"))
JSON_PATH = os.path.abspath(os.path.join(base_path, "json_movelist"))

discord_token = CONFIG_PATH.read_config()['DISCORD_TOKEN']
feedback_channel_id = CONFIG_PATH.read_config()['FEEDBACK_CHANNEL_ID']

character_list = []


class Heihachi(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print('Logged on as', self.user)


try:
    hei = Heihachi(intents=discord.Intents.default())
    tree = discord.app_commands.CommandTree(hei)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')


def create_frame_data_embed(name: str, move: str) -> discord.Embed:
    character_name = util.correct_character_name(name.lower())
    if character_name:
        character = util.get_character_by_name(character_name, character_list)
        move_list = json_movelist_reader.get_movelist(character_name,JSON_PATH)
        move_type = util.get_move_type(move)

        if move_type:
            moves = json_movelist_reader.get_by_move_type(move_type, move_list)
            moves_embed = embed.move_list_embed(character, moves, move_type)
            return moves_embed
        else:
            character_move = json_movelist_reader.get_move(move, move_list)

            if character_move:
                move_embed = embed.move_embed(character, character_move)
                return move_embed
            else:
                similar_moves = json_movelist_reader.get_similar_moves(move, move_list)
                similar_moves_embed = embed.similar_moves_embed(similar_moves, character_name)
                return similar_moves_embed
    else:
        error_embed = embed.error_embed(f'Character {name} does not exist.')
        return error_embed


@hei.event
async def on_message(message):
    if not util.is_user_blacklisted(message.author.id) and message.content and message.author.id != hei.user.id:
        user_command = message.content.split(' ', 1)[1]
        parameters = user_command.strip().split(' ', 1)
        character_name = parameters[0].lower()
        character_move = parameters[1]

        embed = create_frame_data_embed(character_name, character_move)
        await message.channel.send(embed=embed)


@tree.command(name="fd", description="Frame data from a character move")
async def self(interaction: discord.Interaction, character_name: str, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed(character_name, move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="feedback", description="Send feedback incase of wrong data")
async def self(interaction: discord.Interaction, message: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        try:
            feedback_message = "Feedback from **{}** with ID **{}** in **{}** \n- {}\n".format(
                str(interaction.user.name), interaction.user.id,
                interaction.guild, message)
            channel = hei.get_channel(feedback_channel_id)
            await channel.send(content=feedback_message)
            result = embed.success_embed("Feedback sent")
        except Exception as e:
            result = embed.error_embed("Feedback couldn't be sent caused by: " + e)

        await interaction.response.send_message(embed=result, ephemeral=True)


try:
    character_list = util.create_json_movelists(CHARACTER_LIST_PATH)
    scheduler = sched.scheduler(time.time, time.sleep)

    # Repeat importing move list of all character from wavu.wiki once an hour
    scheduler_thread = threading.Thread(target=util.periodic_function,
                                        args=(scheduler, 3600, util.create_json_movelists, CHARACTER_LIST_PATH))
    scheduler_thread.start()

    hei.run(discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')
