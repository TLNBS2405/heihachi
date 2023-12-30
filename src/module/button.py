import discord


class DoneButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
