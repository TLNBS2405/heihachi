"""Embeds for the Heihachi bot."""

from typing import Any, List

import discord

from framedb import Character, CharacterName, FrameDb, FrameService, Move, MoveType

MOVE_NOT_FOUND_TITLE = "Move not found"

SUCCESS_COLOR = discord.Colour.from_rgb(50, 168, 82)
WARNING_COLOR = discord.Colour.from_rgb(253, 218, 13)
ERROR_COLOR = discord.Colour.from_rgb(220, 20, 60)


def get_similar_moves_embed(  # TODO: look into improving the similar moves flow where a user can select the move they want directly
    frame_service: FrameService,
    character: Character,
    similar_moves: List[Move],
) -> discord.Embed:
    """Returns the embed message for similar moves."""

    embed = discord.Embed(
        title=MOVE_NOT_FOUND_TITLE,
        colour=WARNING_COLOR,
        description=f"Similar moves from {character.name.pretty()} -",
    )

    embed.add_field(
        name="Input", value="\n".join([move.input for move in similar_moves]).replace("*", "\\*")
    )  # TODO: replacement should be done when storing in Move object
    embed.set_thumbnail(url=character.portrait)
    embed.set_footer(text=frame_service.name, icon_url=frame_service.icon)
    return embed


def get_move_list_embed(
    frame_service: FrameService, character: Character, moves: List[Move], move_type: MoveType
) -> discord.Embed:
    """Returns the embed message for a list of moves matching a special move type."""

    desc_string = "\n".join(sorted([move.input for move in moves]))  # TODO: add move links or more data?

    embed = discord.Embed(
        title=f"{character.name.pretty()} {move_type.value.lower()}:\n",
        colour=SUCCESS_COLOR,
        description=desc_string,
    )
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

    return embed


def get_frame_data_embed(framedb: FrameDb, frame_service: FrameService, char_query: str, move_query: str) -> discord.Embed:
    """
    Creates an embed for the frame data of a character and move.

    1. Check if the character can be matched to one that exists in the DB. If not, return error embed.
    2. Check if the move query can be matched to a move type. If yes, return all moves matching that move type.
    3. Check if the move query can be matched to a single move. If yes, return the move.
    4. If no match is found, return a list of (possibly empty) similar moves.
    """

    character = framedb.get_character_by_name(char_query)
    if character:
        move_type = framedb.get_move_type(move_query)

        if move_type:
            moves = framedb.get_moves_by_move_type(character.name, move_type.value)
            moves_embed = get_move_list_embed(frame_service, character, moves, move_type)
            embed = moves_embed
        else:
            character_move = framedb.get_move_by_input(character.name, move_query)
            similar_name_moves = framedb.get_moves_by_move_name(character.name, move_query)
            similar_input_moves = framedb.get_moves_by_move_input(character.name, move_query)

            if character_move:
                move_embed = get_move_embed(frame_service, character, character_move)
                embed = move_embed
            elif len(similar_name_moves) == 1:
                move_embed = get_move_embed(frame_service, character, similar_name_moves[0])
                embed = move_embed
            elif len(similar_input_moves) == 1:
                move_embed = get_move_embed(frame_service, character, similar_input_moves[0])
                embed = move_embed
            else:
                similar_moves = similar_name_moves + similar_input_moves
                similar_moves_embed = get_similar_moves_embed(frame_service, character, similar_moves)
                embed = similar_moves_embed
    else:
        embed = get_error_embed(f"Could not locate character {char_query}.")
    return embed
