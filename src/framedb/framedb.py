import logging
import os
from typing import Dict, List

import requests
import thefuzz.fuzz
import thefuzz.process
from fast_autocomplete import AutoComplete

from .character import Character, Move
from .const import CHARACTER_ALIAS, MOVE_TYPE_ALIAS, REPLACE, CharacterName, MoveType
from .frame_service import FrameService

MATCH_SCORE_CUTOFF = 95
logger = logging.getLogger("main")

# TODO: refactor the query methods - simplify + handle alts and aliases correctly


class FrameDb:
    """
    An in-memory "database" of frame data for all characters that is used
    to query frame data while the bot is running.
    """

    def __init__(self) -> None:
        self.frames: Dict[CharacterName, Character] = {}

    def export(self, export_dir_path: str, format: str = "json") -> None:
        "Export the frame database in a particular format."

        if not os.path.exists(export_dir_path):
            os.makedirs(export_dir_path)

        match format:
            case "json":
                for character in self.frames.values():
                    character.export_movelist(os.path.join(export_dir_path, f"{character.name.value}.{format}"), format=format)
                    logger.info(
                        f"Exported frame data for {character.name.value} to {export_dir_path}/{character.name.value}.{format}"
                    )

    def load(self, frame_service: FrameService) -> None:
        "Load the frame database using a frame service."

        with requests.session() as session:  # TODO: assumes a frame service will always require a session
            for character in CharacterName:
                frames = frame_service.get_frame_data(character, session)
                logger.info(f"Retrieved frame data for {character.value} from {frame_service.name}")
                if frames:
                    self.frames[character] = frames
                else:
                    logger.warning(f"Could not load frame data for {character}")
        self._build_autocomplete()

    def refresh(self, frame_service: FrameService, export_dir_path: str, format: str = "json") -> None:
        "Refresh the frame database using a frame service."

        logger.info(f"Refreshing frame data from {frame_service.name} and exporting to {export_dir_path}")
        self.load(frame_service)
        self.export(export_dir_path, format=format)

    def _build_autocomplete(self) -> None:
        "Builds the autocomplete list for the characters in the frame database."

        words: Dict[str, Dict[str, str]] = {character.pretty().lower(): {} for character in self.frames.keys()}
        synonyms = {character.pretty().lower(): CHARACTER_ALIAS[character] for character in self.frames.keys()}
        self.autocomplete = AutoComplete(words=words, synonyms=synonyms)

    @staticmethod
    def _simplify_input(input_query: str) -> str:
        """Removes bells and whistles from a move input query"""

        input_query = input_query.strip().lower()
        input_query = input_query.replace("rage", "r.")
        input_query = input_query.replace("heat", "h.")

        for old, new in REPLACE.items():
            input_query = input_query.replace(old, new)

        # cd works, ewgf doesn't, for some reason
        if input_query[:2].lower() == "cd" and input_query[:3].lower() != "cds":
            input_query = input_query.lower().replace("cd", "fnddf")
        if input_query[:2].lower() == "wr":
            input_query = input_query.lower().replace("wr", "fff")
        return input_query

    @staticmethod
    def _is_command_in_alias(move_query: str, move: Move) -> bool:
        "Check if an input move query is in the alias of the given Move"

        for alias in move.alias:
            if thefuzz.fuzz.ratio(move_query, alias) > MATCH_SCORE_CUTOFF:  # an alias is an alternate name for a move
                return True
        return False

    @staticmethod
    def _is_command_in_alt(move_query: str, move: Move) -> bool:
        "Check if an input move query is in the alt of the given Move"

        for alt in move.alt:
            if FrameDb._simplify_input(move_query) == FrameDb._simplify_input(alt):  # an alt is an alternate input for a move
                return True
        return False

    def get_move_by_input(self, character: CharacterName, input_query: str) -> Move | None:
        """Given an input move query for a known character, retrieve the move from the database."""

        character_movelist = self.frames[character].movelist.values()

        # compare input directly
        result = [
            entry
            for entry in character_movelist
            if FrameDb._simplify_input(entry.input) == FrameDb._simplify_input(input_query)
        ]
        if result:
            return result[0]

        # compare alt
        result = list(filter(lambda x: (FrameDb._is_command_in_alt(input_query, x)), character_movelist))
        if result:
            return result[0]

        # compare alias
        result = list(filter(lambda x: (FrameDb._is_command_in_alias(input_query, x)), character_movelist))
        if result:
            return result[0]

        # couldn't match anything :-(
        return None

    def get_moves_by_move_name(self, character: CharacterName, move_name_query: str) -> List[Move]:
        """
        Gets a list of moves that match a move name query, by comparing the move name and its aliases
        returns a list of Move objects if it finds match(es), else empty list
        """

        result: List[Move] = []
        inverted_movelist = {}
        for move in self.frames[character].movelist.values():
            inverted_movelist[move] = [move.name] + list(move.alias)
        for move, choices in inverted_movelist.items():
            match = thefuzz.process.extractOne(move_name_query, choices, score_cutoff=MATCH_SCORE_CUTOFF)
            if match:
                result.append(move)

        return result

    def get_moves_by_move_type(self, character: CharacterName, move_type: MoveType) -> List[Move]:
        """
        Gets a list of moves that match a move_type query by checking for the existence of the move type in the notes
        returns a list of Move objects if it finds match(es), else empty list
        """

        move_list = self.frames[character].movelist.values()
        moves = list(
            filter(lambda x: (move_type.value.lower() in x.notes.lower()), move_list)
        )  # TODO: revisit this logic for throws (and perhaps others)
        return moves

    def get_moves_by_move_input(self, character: CharacterName, input_query: str) -> List[Move]:
        """
        Given an input query for a known character, find all moves whose inputs are similar to the input query.
        """

        results = []
        inverted_movelist = {}
        for key, value in self.frames[character].movelist.items():
            inverted_movelist[value] = [FrameDb._simplify_input(key)] + list(map(FrameDb._simplify_input, value.alt))
        for move, choices in inverted_movelist.items():
            match = thefuzz.process.extractOne(FrameDb._simplify_input(input_query), choices, score_cutoff=MATCH_SCORE_CUTOFF)
            if match:
                results.append(move)

        return results

    def get_character_by_name(self, name_query: str) -> Character | None:
        """Given a character name query, return the corresponding character if a close match is found, else return None"""

        choices_dict = {}
        for character_name, aliases in CHARACTER_ALIAS.items():
            choices_dict[character_name] = aliases
            choices_dict[character_name].append(character_name.value)
        for character_name, choices in choices_dict.items():
            match = thefuzz.process.extractOne(name_query, choices, score_cutoff=MATCH_SCORE_CUTOFF)
            logger.debug(f"Match: {match}")
            if match:
                logger.debug(f"Matched name query {name_query} to character {character_name} with score {match[1]}.")
                return self.frames[character_name]
        logger.debug(f"Could not match character {name_query} to a known character.")
        return None

    def get_move_type(self, move_type_query: str) -> MoveType | None:
        """Given a move type query, return the corresponding move type if a close match is found, else return None"""

        move_type_query = move_type_query.lower()
        choices_dict = {}
        for move_type, aliases in MOVE_TYPE_ALIAS.items():
            choices_dict[move_type] = aliases
            choices_dict[move_type].append(move_type.value)
        for move_type, choices in choices_dict.items():
            match = thefuzz.process.extractOne(move_type_query, choices, score_cutoff=MATCH_SCORE_CUTOFF)
            logger.debug(f"Match: {match}")
            if match:
                logger.debug(f"Matched move type query {move_type_query} to move type {move_type} with score {match[1]}.")
                return move_type
        logger.debug(f"Could not match move type {move_type_query} to a known move type.")
        return None

    def search_move(self, character: Character, move_query: str) -> Move | List[Move]:
        """Given a move query for a character, search for the move

        1. Check if the move query can be matched exactly by input (+ alts).
        2. Check if the move query can be matched by name (+ aliases)
        3. Check if the move query can be matched fuzzily by input (+ alts) or name (+ aliases)
        4. If no match is found, return a list of (possibly empty) similar moves.
        """

        moves: Move | List[Move] = []

        # check for exact input match
        character_move = self.get_move_by_input(character.name, move_query)

        # check for name match
        similar_name_moves = self.get_moves_by_move_name(character.name, move_query)

        # check for fuzzy input match
        similar_input_moves = self.get_moves_by_move_input(character.name, move_query)

        if character_move:
            moves = character_move
        elif len(similar_name_moves) == 1:
            moves = similar_name_moves[0]
        else:
            similar_moves = similar_name_moves + similar_input_moves
            moves = similar_moves

        return moves
