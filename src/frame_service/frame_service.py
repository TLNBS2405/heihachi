import abc

from framedb import Character, CharacterName


class FrameService(abc.ABC):
    """
    Retrieve frame data for characters from an external (or internal) source.
    """

    @abc.abstractmethod
    def get_frame_data(self, character: CharacterName) -> Character | None:
        pass
