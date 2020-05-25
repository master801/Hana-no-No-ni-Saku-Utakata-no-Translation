from models import ModelTextLine, ModelVoice


# noinspection PyComparisonWithNone,PyTypeChecker
def json_import_serialize(obj):
    if 'texts' in obj:
        new_texts = []
        for text in obj['texts']:
            voices = None

            if text[3] != None:
                voices = []
                for voice in text[3]:
                    voices.append(
                        ModelVoice(
                            voice['name'],  # Name
                            voice['pan'],  # Pan
                            voice['type'],  # Type
                            voice['voice']  # Voice
                        )
                    )
                    continue
                pass

            model: ModelTextLine = None
            if len(text) == 9:
                model = ModelTextLine(
                    text[0],  # Character speaking
                    text[1],  # idk 1
                    text[2],  # Text
                    voices,  # Voices
                    text[4],  # idk 2
                    text[5],  # scene data
                    text[6],  # idk 3
                    text[7],  # text idk 1
                    text[8]  # text idk2
                )
                pass
            elif len(text) == 6:
                model = ModelTextLine(
                    text[0],  # Character speaking
                    text[1],  # idk 1
                    text[2],  # Text
                    voices,  # Voices
                    text[4],  # idk 2
                    text[5]  # scene data
                )
                pass

            if model == None or model is None:
                print()
                pass

            new_texts.append(model)
            continue

        obj['texts'] = new_texts
        pass
    return obj


# noinspection PyComparisonWithNone
def json_import_deserialize(obj):
    serialized: map
    if isinstance(obj, ModelTextLine):
        voices = obj.voices
        new_voices = None
        if voices != None:
            new_voices = []
            for voice in voices:
                new_voices.append(
                    json_import_deserialize(voice)
                )
                continue
            pass
        return {
            'character_speaking': obj.character_speaking,
            'idk_1': obj.idk_1,
            'txt': obj.txt,
            'voices': new_voices,
            'idk_2': obj.idk_2,
            # 'scene_data': obj.scene_data,
            'scene_data': None,  # Do not write scene data, this is written back later on
            'idk_3': obj.idk_3,
            'txt_idk_1': obj.txt_idk_1,
            'txt_idk_2': obj.txt_idk_2,
        }
    elif isinstance(obj, ModelVoice):
        return {
            'name': obj.name,
            'pan': obj.pan,
            'type': obj.voice_type,
            'voice': obj.voice
        }
    return obj


# noinspection PyComparisonWithNone
def json_export_serialize(obj):
    if len(obj) == 9:
        # Do not write full 9 if last 3 are invalid
        if obj['idk_3'] == None and obj['txt_idk_1'] == None and obj['txt_idk_2'] == None:
            return [
                obj['character_speaking'],
                obj['idk_1'],
                obj['txt'],
                obj['voices'],
                obj['idk_2'],
                obj['scene_data']
            ]
        else:
            return [
                obj['character_speaking'],
                obj['idk_1'],
                obj['txt'],
                obj['voices'],
                obj['idk_2'],
                obj['scene_data'],
                obj['idk_3'],
                obj['txt_idk_1'],
                obj['txt_idk_2']
            ]
    else:
        print('SOMETHING BROKE?!')
        return obj
