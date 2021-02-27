import os
import json
import csv

import sys
sys.path.append('..')  # Hacky - For generic_constants

import generic_constants
import json_data
import constants


def main():
    """
    Imports the text lines from the scn json file
    """
    fp_txt_json_files = []
    for (root, subdirs, files) in os.walk(constants.PATH_SCN_ORIGINAL):
        for file in files:
            if file.endswith('.txt.json'):
                fp_txt_json_files.append(root + generic_constants.FP_S + file)
                pass
            continue
        continue

    if len(fp_txt_json_files) > 0:
        for txt_json_file in fp_txt_json_files:  # Open and read json files
            with open(txt_json_file, 'r+', encoding='utf8') as fp_json:
                json_file = json.load(
                    fp_json,
                    object_hook=json_data.json_import_serialize
                )
                fp_json.close()
                pass
            print(f'Read SCN JSON file \"{txt_json_file}\"')

            scenes: list = json_file['scenes']

            text_scenes: list = [None] * len(scenes)
            for i in range(len(scenes)):
                scene = scenes[i]
                if 'texts' in scene:
                    text_scenes[i] = scene['texts']
                    pass
                continue
            del scene
            del i

            if len(text_scenes) > 0:
                pretty_fp = f'{constants.PRETTY_PATH_DEFAULT}{generic_constants.FP_S}' + json_file['name']
                if constants.LEGACY:
                    pretty_fp += '.json'
                    pass
                else:
                    pretty_fp += '.csv'
                    pass

                if not os.path.exists(constants.PRETTY_PATH_DEFAULT):
                    os.mkdir(constants.PRETTY_PATH_DEFAULT)
                    pass
                if os.path.exists(pretty_fp):
                    print(f'File \"{pretty_fp}\" already exists! Deleting...')
                    os.remove(pretty_fp)
                    print(f'Deleted file \"{pretty_fp}\"')
                    pass

                if constants.LEGACY:
                    print('LEGACY WILL NO LONGER BE SUPPORTED IN THE FUTURE')
                    with open(pretty_fp, 'x+', encoding='utf-8') as fp_out_json:
                        json.dump(
                            text_scenes,
                            fp_out_json,
                            ensure_ascii=False,
                            indent=2,
                            default=json_data.json_import_deserialize
                        )
                        fp_out_json.close()
                    del fp_out_json
                    pass
                else:
                    with open(pretty_fp, 'xt+', encoding='utf-8', newline='') as fp_out:
                        writer = csv.writer(fp_out, quoting=csv.QUOTE_NONNUMERIC)
                        writer.writerow([
                            'scene',
                            'idk_1',
                            'actual_char',
                            'hidden_char',
                            'text',
                            'text_hira',
                            'text_kata'
                        ])
                        for i in range(len(text_scenes)):
                            text_scene = text_scenes[i]
                            if text_scene == None:
                                continue
                            for text in text_scene:
                                writer.writerow([
                                    i,
                                    text.idk_1,
                                    text.actual_character_speaking,
                                    text.hidden_character_speaking,
                                    text.txt,
                                    text.txt_hira,
                                    text.txt_kata
                                ])
                                continue
                            del text
                            del text_scene
                            continue
                        del i
                        fp_out.flush()
                        fp_out.close()
                        pass
                    pass

                print(f'Wrote pretty file \"{pretty_fp}\"\n')
                pass
            continue
        print('\nDone')
        pass
    else:
        print(f'No scn json files in path \"{constants.PATH_SCN_ORIGINAL}\" were found?!')
        pass
    return


if __name__ == '__main__':
    main()
    pass
