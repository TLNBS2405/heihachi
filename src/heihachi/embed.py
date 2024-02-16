from typing import Any, List

import discord

from framedb import Character, CharacterName, FrameDb, FrameService, Move, MoveType

MOVE_NOT_FOUND_TITLE = "Move not found"

SUCCESS_COLOR = discord.Colour.from_rgb(50, 168, 82)
WARNING_COLOR = discord.Colour.from_rgb(253, 218, 13)
ERROR_COLOR = discord.Colour.from_rgb(220, 20, 60)


def get_similar_moves_embed(
    frame_service: FrameService, similar_moves: List[Move], character_name: CharacterName
) -> discord.Embed:
    """Returns the embed message for similar moves."""

    command_list = [f"**{idx + 1}**. {move.input}" for idx, move in enumerate(similar_moves)]

    embed = discord.Embed(
        title=MOVE_NOT_FOUND_TITLE,
        colour=WARNING_COLOR,
        description="Similar moves from {}\n{}".format(character_name.value, "\n".join(command_list)),
    )
    return embed


def get_move_list_embed(
    frame_service: FrameService, character: Character, moves: List[Move], move_type: MoveType
) -> discord.Embed:
    """Returns the embed message for a list of moves matching to a special move type."""

    desc_string = "\n".join(sorted([move.input for move in moves]))

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
        url=f"{character.page}_movelist#{move.id.replace(' ', '_')}",  # TODO: this is specific to Wavu, change it to be more generic
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
    """Creates an embed for the frame data of a character and move."""

    character = framedb.get_character_by_name(char_query)
    if character:
        move_type = framedb.get_move_type(move_query)

        if move_type:
            moves = framedb.get_moves_by_move_type(character.name, move_type.value)
            moves_embed = get_move_list_embed(frame_service, character, moves, move_type)
            embed = moves_embed
        else:
            character_move = framedb.get_move_by_input(character.name, move_query)

            if character_move:
                move_embed = get_move_embed(frame_service, character, character_move)
                embed = move_embed
            else:
                similar_moves = framedb.get_similar_moves(character.name, move_query)
                similar_moves_embed = get_similar_moves_embed(frame_service, similar_moves, character.name)
                embed = similar_moves_embed
    else:
        embed = get_error_embed(f"Could not locate character {char_query}.")
    return embed