import discord
from random import randint
from src.module import character

import re

MOVE_NOT_FOUND_TITLE = 'Move not found'


def move_embed(character :character, move :dict):
    """Returns the embed message for character and move"""
    embed = discord.Embed(title=character.name,
                          colour=0x00EAFF,
                          description='**Move: ' + move['input'] + '**')

    embed.set_thumbnail(url=character.portrait[0])
    embed.set_footer(text=move['name'])

    embed.add_field(name='Target', value=move['target'])
    embed.add_field(name='Damage', value=move['damage'])

    embed.add_field(name='Startup', value=move['startup'])

    embed.add_field(name="Block", value=move['on_block'])
    embed.add_field(name='Hit', value=move['on_hit'])
    embed.add_field(name="CH", value=move['on_ch'])
    embed.add_field(name="Notes", value=move['notes'])


    return embed