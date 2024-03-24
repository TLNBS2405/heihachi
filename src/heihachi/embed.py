"""Embeds for the Heihachi bot."""

import logging
from typing import Any, List

import discord

from framedb import Character, FrameDb, FrameService, Move

logger = logging.getLogger("main")

MOVE_NOT_FOUND_TITLE = "Move not found"

SUCCESS_COLOR = discord.Colour.from_rgb(50, 168, 82)
WARNING_COLOR = discord.Colour.from_rgb(253, 218, 13)
ERROR_COLOR = discord.Colour.from_rgb(220, 20, 60)
HEIHACHI_COLOR = discord.Colour.from_rgb(149, 251, 255)


def get_similar_moves_embed(  # TODO: look into improving the similar moves flow where a user can select the move they want directly
    frame_service: FrameService,
    character: Character,
    similar_moves: List[Move],
) -> discord.Embed:
    """Returns the embed message for similar moves."""

    embed = discord.Embed(
        title=MOVE_NOT_FOUND_TITLE,
        colour=WARNING_COLOR,
    )

    if len(similar_moves) > 0:
        embed.add_field(name="Similar Moves", value="\n".join([move.input for move in similar_moves]))
    else:
        embed.add_field(name="No similar moves found", value="")
    embed.set_thumbnail(url=character.portrait)
    embed.set_footer(text=frame_service.name, icon_url=frame_service.icon)
    embed.set_author(name=character.name.pretty(), url=character.page)
    return embed


def get_success_movelist_embed(
    frame_service: FrameService, character: Character, moves: List[Move], title: str
) -> discord.Embed:
    """Returns the embed message for a list of moves that was successfully matched.

    For e.g., to a move type
    """

    desc_string = "\n".join(sorted([move.input for move in moves]))

    embed = discord.Embed(
        title=f"{title}\n",
        colour=SUCCESS_COLOR,
        description=desc_string,
    )
    embed.set_thumbnail(url=character.portrait)
    embed.set_footer(text=frame_service.name, icon_url=frame_service.icon)
    embed.set_author(name=character.name.pretty(), url=character.page)
    return embed


def get_error_embed(message: Any | None) -> discord.Embed:
    embed = discord.Embed(title="Error", colour=ERROR_COLOR, description=message)
    return embed


def get_success_embed(message: Any | None) -> discord.Embed:
    embed = discord.Embed(title="Success", colour=SUCCESS_COLOR, description=message)
    return embed


def get_move_embed(frame_service: FrameService, character: Character, move: Move) -> discord.Embed:
    """Returns the embed message for character and move."""

    embed = discord.Embed(
        title=f"**{move.input}**",
        colour=SUCCESS_COLOR,
        description=move.name,
        url=frame_service.get_move_url(character, move),
    )

    embed.set_thumbnail(url=character.portrait)
    embed.set_footer(text=frame_service.name, icon_url=frame_service.icon)
    embed.set_author(name=character.name.pretty(), url=character.page)

    embed.add_field(name="Target", value=move.target)
    embed.add_field(name="Damage", value=move.damage)
    embed.add_field(name="Startup", value=move.startup)

    embed.add_field(name="Block", value=move.on_block)
    embed.add_field(name="Hit", value=move.on_hit)
    embed.add_field(name="CH", value=move.on_ch)

    if move.notes:
        embed.add_field(name="Notes", value=move.notes)

    if move.image:
        embed.set_image(url=move.image)

    if move.video:
        embed.add_field(name="Video", value=f"[Link]({move.video})", inline=False)

    return embed


def get_frame_data_embed(framedb: FrameDb, frame_service: FrameService, char_query: str, move_query: str) -> discord.Embed:
    """
    Creates an embed for the frame data of a character and move.
    """

    character = framedb.get_character_by_name(char_query)
    if character:
        move_type = framedb.get_move_type(move_query)
        if move_type:
            logger.info(f"Identified move query as move type {move_type}. Getting moves...")
            moves_by_move_type = framedb.get_moves_by_move_type(character.name, move_type.value)
            embed = get_success_movelist_embed(frame_service, character, moves_by_move_type, move_type.value)
        else:
            moves = framedb.search_move(character, move_query)

            if isinstance(moves, Move):
                embed = get_move_embed(frame_service, character, moves)
            elif isinstance(moves, list):
                embed = get_similar_moves_embed(frame_service, character, moves)
    else:
        embed = get_error_embed(f"Could not locate character {char_query}.")
    return embed


def get_help_embed(frame_service: FrameService) -> discord.Embed:
    """Returns the help embed message for the bot."""

    embed = discord.Embed(
        title="Heihachi help",
        colour=SUCCESS_COLOR,
        description="Heihachi is a Discord bot that provides frame data for Tekken 8, primarily from Wavu Wiki.",
    )
    embed.set_thumbnail(url=frame_service.icon)
    embed.add_field(
        name="/fd `<character>` `<move>`",
        value="Get frame data for a particular character's move.",
        inline=False,
    )
    embed.add_field(
        name="/feedback `message`",
        value="Send feedback to the bot authors in case of incorrect frame data (or any other reason).",
        inline=False,
    )
    embed.add_field(
        name="/help",
        value="Display this message.",
        inline=False,
    )
    embed.add_field(
        name="Wavu Wiki",
        value="[Homepage](https://wavu.wiki/t/Main_Page) - [Discord](http://discord.gg/86UFj8GEcC) - [Twitter](https://twitter.com/wavuwiki)",
        inline=False,
    )
    embed.add_field(
        name="Contributing",
        value="Heihachi is open source. Follow the project on [GitHub](https://github.com/TLNBS2405/heihachi).",
        inline=False,
    )
    embed.set_footer(text=frame_service.name, icon_url=frame_service.icon)
    return embed
