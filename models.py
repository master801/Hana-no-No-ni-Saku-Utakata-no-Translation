from dataclasses import dataclass
from typing import List


@dataclass
class ModelVoice:

    def __init__(self, name: str, pan: int, voice_type: int, voice: str):
        self.name = name
        self.pan = pan
        self.voice_type = voice_type
        self.voice = voice
        return


@dataclass
class ModelTextLine:

    def __init__(self,
                 character_speaking: str,
                 idk_1,
                 txt: str,
                 voices: List[ModelVoice],
                 idk_2: int,
                 scene_data: dict,
                 idk_3=None,
                 txt_idk_1: str = None,
                 txt_idk_2: str = None
                 ):
        self.character_speaking = character_speaking  # Character that is currently speaking
        self.idk_1 = idk_1  # No idea
        self.txt = txt  # Text
        self.voices = voices  # Character voices - ModelVoice
        self.idk_2 = idk_2  # Not sure what this is used for, but it's an int
        self.scene_data = scene_data  # The scene's data
        self.idk_3 = idk_3  # No idea
        self.txt_idk_1 = txt_idk_1  # Some kind of second version of the text (Same?)
        self.txt_idk_2 = txt_idk_2  # Some kind of third version of the text (Same?)
        return

