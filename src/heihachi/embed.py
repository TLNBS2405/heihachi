from typing import List

import discord

from framedb.character import Character, Move
from framedb.const import CharacterName, MoveType

MOVE_NOT_FOUND_TITLE = "Move not found"

SUCCESS_COLOR = discord.Colour.from_rgb(50, 168, 82)
WARNING_COLOR = discord.Colour.from_rgb(253, 218, 13)
ERROR_COLOR = discord.Colour.from_rgb(220, 20, 60)


def similar_moves_embed(similar_moves: List[Move], character_name: CharacterName) -> discord.Embed:
    """Returns the embed message for similar moves."""

    command_list = [f"**{idx + 1}**. {move.input}" for idx, move in enumerate(similar_moves)]

    embed = discord.Embed(
        title=MOVE_NOT_FOUND_TITLE,
        colour=WARNING_COLOR,
        description="Similar moves from {}\n{}".format(character_name.value, "\n".join(command_list)),
    )
    return embed


def move_list_embed(character: Character, moves: List[Move], move_type: MoveType) -> discord.Embed:
    """Returns the embed message for a list of moves matching to a special move type."""

    desc_string = "\n".join(sorted([move.input for move in moves]))

    embed = discord.Embed(
        title=f"{character.name} {move_type.value.lower()}:\n",
        colour=SUCCESS_COLOR,
        description=desc_string,
    )
    return embed


def error_embed(message) -> discord.Embed:
    embed = discord.Embed(title="Error", colour=ERROR_COLOR, description=message)
    return embed


def success_embed(message) -> discord.Embed:
    embed = discord.Embed(title="Success", colour=SUCCESS_COLOR, description=message)
    return embed


def move_embed(character: Character, move: Move) -> discord.Embed:
    """Returns the embed message for character and move."""

    embed = discord.Embed(
        title=f"**{move.input}**",
        colour=SUCCESS_COLOR,
        description=move.name,
        url=f"{character.page}_movelist#{move.id}",
    )

    embed.set_thumbnail(url=character.portrait)
    embed.set_footer(text="Wavu Wiki", icon_url=WAVU_LOGO)
    embed.set_author(name=character.name.value.title(), url=character.page)

    embed.add_field(name="Target", value=move.target)
    embed.add_field(name="Damage", value=move.damage)
    embed.add_field(name="Startup", value=move.startup)

    embed.add_field(name="Block", value=move.on_block)
    embed.add_field(name="Hit", value=move.on_hit)
    embed.add_field(name="CH", value=move.on_ch)
    if move.notes:
        embed.add_field(name="Notes", value=move.notes)

    return embed
