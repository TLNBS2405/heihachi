from typing import List

from src.resources import const
from src.module import character

import discord, datetime, json

from src.wavu import wavu_importer


def correct_character_name(alias: str):
    # check if input in dictionary or in dictionary values
    if alias in const.CHARACTER_ALIAS:
        return alias

    for key, value in const.CHARACTER_ALIAS.items():
        if alias in value:
            return key

    return None

def get_character_by_name(name :str, character_list :[]) -> character.Character:
    for character in character_list:
        if character.name == name:
            return character

def get_move_type(original_move: str):
    for k in const.MOVE_TYPES.keys():
        if original_move in const.MOVE_TYPES[k]:
            return k

def is_user_blacklisted(user_id):
    if user_id in const.ID_BLACKLIST:
        return True
    else:
        return False


def is_author_newly_created(interaction: discord.Interaction):
    today = datetime.datetime.strptime(datetime.datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
    age = today - interaction.user.created_at.replace(tzinfo=None)
    if age.days < 120:
        return True
    return False


def create_json_movelists(character_list_path: str) -> List[character.Character]:
    with open(character_list_path) as file:
        all_characters = json.load(file)
        cha_list = []

        for character_meta in all_characters:
            cha = wavu_importer.import_character(character_meta)
            cha.export_movelist_as_json()
            cha_list.append(cha)

    return cha_list


def schedule_create_json_movelists(character_list_path: str, scheduler):
    try:
        create_json_movelists(character_list_path)
        scheduler.enter(3600, 1, create_json_movelists, (character_list_path, scheduler,))

    except Exception as e:
        raise Exception("Error when importing character from wavu" + str(e))


