import datetime, logging, os, discord, sched, time, sys
import threading

from src.module import configurator
from src.module import json_movelist_reader
from src.module import embed
from src.module import util
from src.module import button

sys.path.insert(0, (os.path.dirname(os.path.dirname(__file__))))

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

base_path = os.path.dirname(__file__)
CONFIG_PATH = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
CHARACTER_LIST_PATH = os.path.abspath(os.path.join(base_path, "resources", "character_list.json"))
JSON_PATH = os.path.abspath(os.path.join(base_path, "json_movelist"))

discord_token = CONFIG_PATH.read_config()['DISCORD_TOKEN']
feedback_channel_id = CONFIG_PATH.read_config()['FEEDBACK_CHANNEL_ID']
actioned_channel_id = CONFIG_PATH.read_config()['ACTION_CHANNEL_ID']
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
        move_list = json_movelist_reader.get_movelist(character_name, JSON_PATH)
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


@tree.command(name="alisa", description="Frame data from alisa")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("alisa", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="asuka", description="Frame data from asuka")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("asuka", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="azucena", description="Frame data from azucena")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("azucena", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="bryan", description="Frame data from bryan")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("bryan", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="claudio", description="Frame data from claudio")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("claudio", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="devil_jin", description="Frame data from devil_jin")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("devil_jin", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="dragunov", description="Frame data from dragunov")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("dragunov", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="feng", description="Frame data from feng")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("feng", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="hwoarang", description="Frame data from hwoarang")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("hwoarang", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="jack-8", description="Frame data from jack-8")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("jack-8", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="jin", description="Frame data from jin")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("jin", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="jun", description="Frame data from jun")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("jun", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="kazuya", description="Frame data from kazuya")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("kazuya", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="king", description="Frame data from king")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("king", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="kuma", description="Frame data from kuma")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("kuma", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="lars", description="Frame data from lars")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("lars", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="law", description="Frame data from law")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("law", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="lee", description="Frame data from lee")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("lee", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="leo", description="Frame data from leo")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("leo", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="leroy", description="Frame data from leroy")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("leroy", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="lili", description="Frame data from lili")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("lili", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="nina", description="Frame data from nina")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("nina", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="panda", description="Frame data from panda")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("panda", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="paul", description="Frame data from paul")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("paul", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="raven", description="Frame data from raven")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("raven", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="reina", description="Frame data from reina")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("reina", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="shaheen", description="Frame data from shaheen")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("shaheen", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="steve", description="Frame data from steve")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("steve", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="victor", description="Frame data from victor")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("victor", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="xiaoyu", description="Frame data from xiaoyu")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("xiaoyu", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="yoshimitsu", description="Frame data from yoshimitsu")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("yoshimitsu", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="zafina", description="Frame data from zafina")
async def self(interaction: discord.Interaction, move: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        embed = create_frame_data_embed("zafina", move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


@tree.command(name="feedback", description="Send feedback incase of wrong data")
async def self(interaction: discord.Interaction, message: str):
    if not (util.is_user_blacklisted(interaction.user.id) or util.is_author_newly_created(interaction)):
        try:
            feedback_message = "Feedback from **{}** with ID **{}** in **{}** \n- {}\n".format(
                str(interaction.user.name), interaction.user.id,
                interaction.guild, message)
            channel = hei.get_channel(feedback_channel_id)
            actioned_channel = hei.get_channel(actioned_channel_id)
            await channel.send(content=feedback_message, view=button.DoneButton(actioned_channel))
            result = embed.success_embed("Feedback sent")
        except Exception as e:
            result = embed.error_embed("Feedback couldn't be sent caused by: " + e)

        await interaction.response.send_message(embed=result, ephemeral=False)


try:
    character_list = util.create_json_movelists(CHARACTER_LIST_PATH)
    scheduler = sched.scheduler(time.time, time.sleep)

    # Repeat importing move list of all character from wavu.wiki once an hour
    scheduler_thread = threading.Thread(target=util.periodic_function,
                                        args=(scheduler, 3600, util.create_json_movelists, CHARACTER_LIST_PATH))
    scheduler_thread.start()
    hei.run(discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')
