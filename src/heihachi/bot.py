import datetime
import logging
import traceback
from typing import List

import discord
import discord.ext.commands

from framedb import FrameDb, FrameService
from heihachi import button, embed
from heihachi.configurator import Configurator
from heihachi.embed import get_frame_data_embed

logger = logging.getLogger("main")


class FrameDataBot(discord.Client):
    def __init__(
        self,
        framedb: FrameDb,
        frame_service: FrameService,
        config: Configurator,
    ) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents)
        self.framedb = framedb
        self.frame_service = frame_service
        self.config = config
        self.synced = False
        self.tree = discord.app_commands.CommandTree(self)

        self._add_bot_commands()
        logger.debug(f"Bot command tree: {[command.name for command in self.tree.get_commands()]}")

    async def on_ready(self) -> None:
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync()
            logger.debug("Bot command tree synced")
            self.synced = True
        if self.config.action_channel_id:
            action_channel = self.get_channel(self.config.action_channel_id)
            assert isinstance(action_channel, discord.channel.TextChannel)
            self.add_view(button.DoneButton(action_channel))
        logger.info(f"Logged on as {self.user}")

    def _is_user_blacklisted(self, user_id: str | int) -> bool:
        "Check if a user is blacklisted"

        blacklist: List[str] | List[int] | None
        if isinstance(user_id, str):
            blacklist = self.config.blacklist
        else:
            blacklist = self.config.id_blacklist

        if blacklist:
            return user_id in blacklist
        else:
            return False

    def _is_author_newly_created(self, interaction: discord.Interaction["FrameDataBot"]) -> bool:
        "Check if author of an interaction is newly created"

        today = datetime.datetime.strptime(datetime.datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
        age = today - interaction.user.created_at.replace(tzinfo=None)
        return age.days < self.config.new_author_age_limit

    async def on_message(self, message: discord.Message) -> None:
        logger.debug(f"Received message from {message.author.name} in {message.guild}: {message.content}")
        if not self._is_user_blacklisted(message.author.id) and self.user and message.author.id != self.user.id:
            if message.content and self.user.mentioned_in(message):
                try:
                    user_command, params = message.content.split(" ", 1)
                    char_name_query, move_query = params.split(" ", 1)

                    embed = get_frame_data_embed(self.framedb, self.frame_service, char_name_query, move_query)
                    await message.channel.send(embed=embed, reference=message)
                except ValueError:
                    logger.debug(f"Message from {message.author.name} in {message.guild} is not a valid command")
            else:
                logger.debug(f"Message from {message.author.name} in {message.guild} does not mention the bot")

    # def _character_command_factory(
    #     self, name: str
    # ) -> Callable[[discord.Interaction["FrameDataBot"], str], Coroutine[Any, Any, None]]:
    #     "A factory function to create /character command functions"

    #     async def _character_command(interaction: discord.Interaction["FrameDataBot"], move: str) -> None:
    #         logger.info(f"Received command from {interaction.user.name} in {interaction.guild}: /{name} {move}")
    #         if not (self._is_user_blacklisted(str(interaction.user.id)) or self._is_author_newly_created(interaction)):
    #             embed = get_frame_data_embed(self.framedb, self.frame_service, name, move)
    #             await interaction.response.send_message(embed=embed, ephemeral=False)

    #     return _character_command

    async def _character_name_autocomplete(
        self, interaction: discord.Interaction["FrameDataBot"], current: str
    ) -> List[discord.app_commands.Choice[str]]:
        """
        Autocomplete function for character names

        Ref.: https://stackoverflow.com/a/75912806/6753162
        """

        current = current.lower()  # autocomplete is case-sensitive
        choices = self.framedb.autocomplete.search(word=current, max_cost=3, size=3)
        return [discord.app_commands.Choice(name=choice[0].title(), value=choice[0]) for choice in choices][
            :25
        ]  # Discord has a max choice number of 25 (https://github.com/Rapptz/discord.py/discussions/9241)
        # TODO: why can't we leverage Discord subcommands/group commands for fd autocompletion? They're essentially
        # the same as the /character commands, no? Less commands to worry about too, just groups everything under
        # /fd

    def _add_bot_commands(self) -> None:
        "Add all frame commands to the bot"

        @self.tree.command(name="fd", description="Frame data from a character move")
        @discord.app_commands.autocomplete(character=self._character_name_autocomplete)
        async def _frame_data_cmd(interaction: discord.Interaction["FrameDataBot"], character: str, move: str) -> None:
            logger.info(f"Received command from {interaction.user.name} in {interaction.guild}: /fd {character} {move}")
            character_name_query = character
            move_query = move
            if not (self._is_user_blacklisted(str(interaction.user.id)) or self._is_author_newly_created(interaction)):
                embed = get_frame_data_embed(self.framedb, self.frame_service, character_name_query, move_query)
                await interaction.response.send_message(embed=embed, ephemeral=False)

        # for character in CharacterName:
        #     char_name = character.value
        #     self.tree.command(name=char_name, description=f"Frame data from {char_name}")(
        #         self._character_command_factory(char_name)
        #     )

        if self.config.feedback_channel_id and self.config.action_channel_id:

            @self.tree.command(name="feedback", description="Send feedback to the authors in case of incorrect data")
            async def _feedback_cmd(interaction: discord.Interaction["FrameDataBot"], message: str) -> None:
                logger.info(f"Received command from {interaction.user.name} in {interaction.guild}: /feedback {message}")
                if not (
                    self._is_user_blacklisted(str(interaction.user.id)) or self._is_author_newly_created(interaction)
                ):  # TODO: possible way to refactor these checks using discord.py library? discord.ext.commands.Bot.check()
                    try:
                        feedback_message = "Feedback from **{}** with ID **{}** in **{}** \n- {}\n".format(
                            str(interaction.user.name),
                            interaction.user.id,
                            interaction.guild,
                            message,
                        )
                        try:
                            assert self.config.feedback_channel_id and self.config.action_channel_id
                            feedback_channel = self.get_channel(self.config.feedback_channel_id)
                            actioned_channel = self.get_channel(self.config.action_channel_id)
                        except Exception as e:
                            logger.error(f"Error getting channel: {e}")
                        assert feedback_channel and actioned_channel
                        assert isinstance(feedback_channel, discord.channel.TextChannel)
                        assert isinstance(actioned_channel, discord.channel.TextChannel)
                        await feedback_channel.send(content=feedback_message, view=button.DoneButton(actioned_channel))
                        result = embed.get_success_embed("Feedback sent")
                    except Exception as e:
                        result = embed.get_error_embed(f"Feedback couldn't be sent, caused by: {traceback.format_exc()}")

                    await interaction.response.send_message(embed=result, ephemeral=False)
        else:
            logger.warning("Feedback or Action channel ID is not set. Disabling feedback command.")

        @self.tree.command(name="help", description="Show help")
        async def _help_command(interaction: discord.Interaction["FrameDataBot"]) -> None:
            logger.info(f"Received command from {interaction.user.name} in {interaction.guild}: /help")
            if not (self._is_user_blacklisted(str(interaction.user.id)) or self._is_author_newly_created(interaction)):
                help_embed = embed.get_help_embed(self.frame_service)
                await interaction.response.send_message(embed=help_embed, ephemeral=True)
