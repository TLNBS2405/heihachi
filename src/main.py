import json

from src.module import character_importer

def create_all_character_json(character_list_path: str):
    with open(character_list_path) as file:
        characters = json.load(file)

        for character_meta in characters:
            character = character_importer.import_character(character_meta)
            character.export_movelist_as_json()


create_all_character_json("resources/character_list.json")