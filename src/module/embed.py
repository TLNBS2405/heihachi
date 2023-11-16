import discord
from random import randint
import re

MOVE_NOT_FOUND_TITLE = 'Move not found'


def move_embed(character, move):
    """Returns the embed message for character and move"""
    embed = discord.Embed(title=character['proper_name'],
                          colour=0x00EAFF,
                          url=character['online_webpage'],
                          description='**Move: ' + move['Command'] + '**')
    embed.set_thumbnail(url=character['portrait'])

    block = "Block"
    counterhit = "Counter hit"

    if 'Throw' in move['Tags']:
        block = "On Break"
        counterhit = "Break Type"

    embed.add_field(name='Property', value=move['Hit level'])
    embed.add_field(name='Damage', value=move['Damage'])

    result = re.match('^\d', move['Start up frame'])

    if result:
        embed.add_field(name='Startup', value='i' + move['Start up frame'])
    else:
        embed.add_field(name='Startup', value=move['Start up frame'])

    embed.add_field(name=block, value=move['Block frame'])
    embed.add_field(name='Hit', value=move['Hit frame'])
    embed.add_field(name=counterhit, value=move['Counter hit frame'])

    if 'Recovery' in move:
        embed.add_field(name='On whiff', value=move['Recovery'])
    if 'Notes' in move and move['Notes'] and not move['Notes'] == "-":
        embed.add_field(name='Notes', value=move['Notes'])
    if 'Gif' in move and move['Gif'] and not move['Gif'] == "-":
        embed.add_field(name='Gif', value=move['Gif'], inline=False)
    if 'Tags' in move and move['Tags'] and not move['Tags'] == "-":
        embed.add_field(name='Tags', value=move['Tags'], inline=False)

    random_value = randint(0, 2)
    if random_value == 2:
        embed.add_field(name='Dev Note',
                        value='**IMPORTANT** \n The bot for T7 will shutdown on the 25th Jan 2024',
                        inline=False)

    return embed


def move_list_embed(character, move_list, move_type):
    """Returns the embed message for a list of moves matching to a special move type"""
    desc_string = ''
    move_list.sort()
    for move in move_list:
        desc_string += move + '\n'

    embed = discord.Embed(title=character['proper_name'] + ' ' + move_type.lower() + ':',
                          colour=0x00EAFF,
                          description=desc_string)
    return embed


def error_embed(err):
    embed = discord.Embed(title='Error',
                          colour=0xFF4500,
                          description=err)
    return embed


def success_embed(message):
    embed = discord.Embed(title='Success',
                          colour=0x3ddb2c,
                          description=message)
    return embed


def similar_moves_embed(similar_moves, character_name):
    for i in range(len(similar_moves)):
        similar_moves[i] = f'**{i + 1}**. {similar_moves[i]}'

    embed = discord.Embed(title=MOVE_NOT_FOUND_TITLE, colour=0xfcba03,
                          description='Similar moves from {}\n{}'
                          .format(character_name, '\n'.join(similar_moves)))
    return embed


def help_embed():
    text = "**Slash command** \n" \
           "/fd <character> <move>\t\t\t- get frame data of a move from a character \n" \
           "/last-updates\t\t\t- get the messages of some latest updates\n" \
           "/feedback <message>\t\t\t- send message including sender name to the devs \n\n" \
           "**Direct Ping** \n " \
           "@discordbot <character> <move>\t\t\t- get frame data of a move from a character \n\n"
    embed = discord.Embed(title='Commands', description=text, colour=0x37ba25)
    embed.set_author(name='Author: Tib#1303')

    return embed


def thank_embed():
    text = "\n\n" \
           "Much thanks and love especially to T7Chicken Team, Ruxx, BKNR, Vesper, Maxwell and Evil. \n\n" \
           "This project won't be possible without you guys <3"
    embed = discord.Embed(title='Commands', description=text, colour=0x37ba25)
    embed.set_author(name='Author: Tib')
    return embed
