import json

from src.module import character_importer

def initiate_characters(character_list_path: str):
    with open(character_list_path) as file:
        characters = json.load(file)

        for character_meta in characters:
            character = character_importer.import_character(character_meta)
            character.export_movelist_as_json()


initiate_characters("resources/character_list.json")