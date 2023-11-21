import discord
from discord import app_commands


class Discord_Connector(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def on_ready(self):
        print('Logged on as', self.user)
