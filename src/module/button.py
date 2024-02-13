import discord


class DoneButton(discord.ui.View):
    def __init__(self, actioned_channel):
        self.actioned_channel = actioned_channel
        super().__init__()

    @discord.ui.button(label="👍", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        done_message = "{} \nactioned by **{}** with 👍\n".format(
            interaction.message.content, interaction.user.name
        )
        await self.actioned_channel.send(content=done_message)
        await interaction.message.delete()

    @discord.ui.button(label="👎", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        done_message = "{} \nactioned by **{}** with 👎\n".format(
            interaction.message.content, interaction.user.name
        )
        await self.actioned_channel.send(content=done_message)
        await interaction.message.delete()
