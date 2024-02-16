import abc

import requests

from framedb import Character, CharacterName, Url


class FrameService(abc.ABC):
    """
    Retrieve frame data for characters from an external (or internal) source.
    """

    name: str
    icon: Url | None = None

    @abc.abstractmethod
    def get_frame_data(
        self, character: CharacterName, session: requests.Session | None = None
    ) -> Character | None:  # TODO: is this the right argument order?
        pass
