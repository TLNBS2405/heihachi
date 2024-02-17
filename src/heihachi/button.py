import discord


class DoneButton(discord.ui.View):  # TODO: investigate interaction failing sometimes
    def __init__(self, actioned_channel: discord.channel.TextChannel) -> None:
        self.actioned_channel = actioned_channel
        super().__init__()

    @discord.ui.button(label="👍", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction[discord.Client], button: discord.ui.Button[discord.ui.View]) -> None:
        if interaction.message:
            done_message = "{} \nactioned by **{}** with 👍\n".format(interaction.message.content, interaction.user.name)
            await self.actioned_channel.send(content=done_message)
            await interaction.message.delete()
        else:
            pass

    @discord.ui.button(label="👎", style=discord.ButtonStyle.red)
    async def cancel(
        self, interaction: discord.Interaction[discord.Client], button: discord.ui.Button[discord.ui.View]
    ) -> None:
        if interaction.message:
            done_message = "{} \nactioned by **{}** with 👎\n".format(interaction.message.content, interaction.user.name)
            await self.actioned_channel.send(content=done_message)
            await interaction.message.delete()
        else:
            pass
