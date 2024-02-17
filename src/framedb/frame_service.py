import abc

import requests

from framedb import Character, CharacterName, Move, Url


class FrameService(abc.ABC):
    """
    Retrieve frame data for characters from an external (or internal) source.
    """

    name: str
    icon: Url | None = None

    @abc.abstractmethod
    def get_frame_data(
        self, character: CharacterName, session: requests.Session | None = None
    ) -> Character | None:  # TODO: is there a better argument order?
        """
        Get the frame data for a character from the service
        """
        pass

    @abc.abstractmethod
    def get_move_url(self, character: Character, move: Move) -> Url | None:
        """
        Get the URL for a move in the character's movelist to be used in the embed
        """
        pass
