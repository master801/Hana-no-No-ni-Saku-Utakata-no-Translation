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
                 actual_character_speaking: str,
                 hidden_character_speaking: str,
                 txt: str,
                 voices: List[ModelVoice],
                 idk_1: int,
                 scene_data: dict,
                 idk_2=None,
                 txt_hira: str = None,
                 txt_kata: str = None
                 ):
        self.actual_character_speaking = actual_character_speaking  # Name of actual character speaking
        self.hidden_character_speaking = hidden_character_speaking  # Name of hidden character speaking
        self.txt = txt  # Text
        self.voices = voices  # Character voices - ModelVoice
        self.idk_1 = idk_1  # Not sure what this is used for, but it's an int
        self.scene_data = scene_data  # The scene's data
        self.idk_2 = idk_2  # No idea
        self.txt_hira = txt_hira
        self.txt_kata = txt_kata
        return

