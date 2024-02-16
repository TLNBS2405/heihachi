import datetime
import logging
import sched

import discord

from framedb.const import CharacterName
from heihachi import Configurator, button, embed
from heihachi.embed import create_frame_data_embed

logger = logging.getLogger(__name__)


class FrameDataBot(discord.Client):
    def __init__(self, config: Configurator, intents: discord.Intents):
        super().__init__(intents=intents)
        self.config = config
        self.synced = False

    async def on_ready(self, tree: discord.app_commands.CommandTree) -> None:
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        logger.info(f"Logged on as {self.user}")

    def is_user_blacklisted(self, user_id: str | int) -> bool:
        "Check if a user is blacklisted"

        if isinstance(user_id, str):
            blacklist = self.config.blacklist
        else:
            blacklist = self.config.id_blacklist

        if blacklist:
            return user_id in blacklist
        else:
            return False

    def is_author_newly_created(self, interaction: discord.Interaction) -> bool:
        "Check if author of an interaction is newly created"

        today = datetime.datetime.strptime(datetime.datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
        age = today - interaction.user.created_at.replace(tzinfo=None)
        return age.days < self.config.new_author_age_limit


# TODO: fix all this
@hei.event
async def on_message(message) -> None:
    if not self.is_user_blacklisted(message.author.id) and message.content and message.author.id != hei.user.id:
        user_command = message.content.split(" ", 1)[1]
        parameters = user_command.strip().split(" ", 1)
        character_name = parameters[0].lower()
        character_move = parameters[1]

        embed = create_frame_data_embed(character_name, character_move)
        await message.channel.send(embed=embed)


@tree.command(name="fd", description="Frame data from a character move")
async def self(interaction: discord.Interaction, character_name: str, move: str) -> None:
    if not (self.is_user_blacklisted(str(interaction.user.id)) or self.is_author_newly_created(interaction)):
        embed = create_frame_data_embed(character_name, move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


def character_command_factory(name: str):
    async def command(interaction: discord.Interaction, move: str) -> None:
        if not (self.is_user_blacklisted(str(interaction.user.id)) or self.is_author_newly_created(interaction)):
            embed = create_frame_data_embed(name, move)
            await interaction.response.send_message(embed=embed, ephemeral=False)

    return command


for character in CharacterName:
    name = character.value
    tree.command(name=name, description=f"Frame data from {name}")(character_command_factory(name))

if self.config.feedback_channel_id:

    @tree.command(name="feedback", description="Send feedback incase of wrong data")
    async def self(interaction: discord.Interaction, message: str) -> None:
        if not (self.is_user_blacklisted(str(interaction.user.id)) or util.is_author_newly_created(interaction)):
            try:
                feedback_message = "Feedback from **{}** with ID **{}** in **{}** \n- {}\n".format(
                    str(interaction.user.name),
                    interaction.user.id,
                    interaction.guild,
                    message,
                )
                try:
                    channel = hei.get_channel(config.feedback_channel_id)
                    actioned_channel = hei.get_channel(config.action_channel_id)
                except Exception as e:
                    logger.error(f"Error getting channel: {e}")
                await channel.send(content=feedback_message, view=button.DoneButton(actioned_channel))
                result = embed.success_embed("Feedback sent")
            except Exception as e:
                result = embed.error_embed(f"Feedback couldn't be sent, caused by: {str(e)}")

            await interaction.response.send_message(embed=result, ephemeral=False)
else:
    logger.warning("Feedback channel ID is not set. Disabling feedback command.")


def periodic_function(scheduler: sched.scheduler, interval: float, function: sched._ActionCallback, character_list_path: str):
    while True:
        scheduler.enter(interval, 1, function, (character_list_path,))
        scheduler.run()
