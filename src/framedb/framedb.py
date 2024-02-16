import logging
import os
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest
from typing import Dict, List

from .character import Character, Move
from .const import CHARACTER_ALIAS, MOVE_TYPE_ALIAS, REPLACE, CharacterName, MoveType
from .frame_service import FrameService

logger = logging.getLogger(__name__)


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
                    character.export_movelist(os.path.join(export_dir_path, f"{character.name}.{format}"), format=format)
                    logger.info(f"Exported frame data for {character.name} to {export_dir_path}/{character.name}.{format}")

    def load(self, frame_service: FrameService) -> None:
        "Load the frame database using a frame service."

        for character in CharacterName:
            frames = frame_service.get_frame_data(character)
            logger.info(f"Retrieved frame data for {character.value} from {frame_service.name}")
            if frames:
                self.frames[character] = frames
            else:
                logger.warning(f"Could not load frame data for {character}")

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
    def _is_command_in_alias(command: str, move: Move) -> bool:
        for alias in move.alias:
            if FrameDb._simplify_input(command) == FrameDb._simplify_input(alias):
                return True
        return False

    @staticmethod
    def _correct_character_name(char_name_query: str) -> str | None:
        "Check if input in dictionary or in dictionary values"

        if char_name_query in CHARACTER_ALIAS:
            return char_name_query

        for key, value in CHARACTER_ALIAS.items():
            if char_name_query in value:
                return key.value

        return None

    @staticmethod
    def _correct_move_type(move_type_query: str) -> MoveType | None:
        """Given a move type query, correct it to a known move type."""

        move_type_query = move_type_query.lower()
        for move_type, aliases in MOVE_TYPE_ALIAS.items():
            if move_type_query in aliases:
                return move_type

        logger.warning(f"Could not match move type {move_type_query} to a known move type.")
        return None

    def get_move_by_input(self, character: CharacterName, input_query: str) -> Move | None:
        """Given an input move query for a known character, retrieve the move from the database."""

        character_movelist = self.frames[character].movelist.values()
        result = [
            entry
            for entry in character_movelist
            if FrameDb._simplify_input(entry.input) == FrameDb._simplify_input(input_query)
        ]
        if result:
            return result[0]
        else:
            result = list(filter(lambda x: (FrameDb._is_command_in_alias(input_query, x)), character_movelist))
            if result:
                return result[0]
            else:
                return None

    def get_moves_by_move_type(self, character: CharacterName, move_type_query: str) -> List[Move]:
        """
        Gets a list of moves that match a move_type query
        returns a list of Move objects if finds match(es), else empty list
        """

        move_list = self.frames[character].movelist.values()
        move_type = FrameDb._correct_move_type(move_type_query)
        if move_type:
            moves = list(filter(lambda x: (move_type.value in x.notes.lower()), move_list))
        else:
            moves = []

        return moves

    def get_move_by_id(self, character: CharacterName, move_id: str) -> Move | None:
        """Given a move id for a known character, retrieve the move from the database."""

        character_movelist = self.frames[character].movelist
        if move_id not in character_movelist:
            logger.warning(f"Move {move_id} not found for {character}")
            return None
        else:
            return character_movelist[move_id]

    def get_similar_moves(self, character: CharacterName, input_query: str) -> List[Move]:
        """
        Given an input query for a known character, find all moves which are similar to the input query.
        """

        movelist = list(self.frames[character].movelist.values())
        command_list = [entry.input for entry in movelist]
        similar_move_indices = _get_close_matches_indices(
            FrameDb._simplify_input(input_query), list(map(FrameDb._simplify_input, command_list))
        )

        result = [movelist[idx] for idx in similar_move_indices]

        return result

    def get_character_by_name(self, name_query: str) -> Character | None:
        """Given a character name query, return the corresponding character"""

        for character_name, character in self.frames.items():
            if character_name.value == name_query:
                return character
        return None

    def get_move_type(self, move_type_query: str) -> MoveType | None:
        """Given a move type query, return the corresponding move type"""

        for move_type, aliases in MOVE_TYPE_ALIAS.items():
            if move_type_query.lower() in aliases:
                return move_type


def _get_close_matches_indices(word: str, possibilities: List[str], n: int = 5, cutoff: float = 0.7) -> List[int]:
    """
    Use SequenceMatcher to return a list of the indexes of the best
    "good enough" matches.

    word is a sequence for which close matches
    are desired (typically a string).

    possibilities is a list of sequences against which to match word
    (typically a list of strings).

    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.

    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.
    """

    if not n > 0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff and s.ratio() >= cutoff:
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]
