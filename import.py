import os
import json

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
                fp_txt_json_files.append(root + constants.FILE_PATH_SEPARATOR + file)
                pass
            continue
        continue

    if len(fp_txt_json_files) > 0:
        json_obj_list = []
        for txt_json_file in fp_txt_json_files:  # Open and read json files
            with open(txt_json_file, 'r+', encoding='utf8') as fp_json:
                json_file = json.load(
                    fp_json,
                    object_hook=json_data.json_import_serialize
                )
                json_obj_list.append(json_file)
                fp_json.close()

                print('Read SCN Json file \"{}\"'.format(txt_json_file))
                pass
            continue

        for json_obj in json_obj_list:
            scenes: list = json_obj['scenes']
            pretty_file_path = '{}{}{}.json'.format(constants.PRETTY_PATH_DEFAULT, constants.FILE_PATH_SEPARATOR, json_obj['name'])

            # noinspection PyTypeChecker
            text_scenes: list = [None] * len(scenes)
            for i in range(len(scenes)):
                scene = scenes[i]
                if 'texts' in scene:
                    text_scenes[i] = scene['texts']
                    pass
                continue

            # noinspection PyComparisonWithNone
            if text_scenes != None:
                if not os.path.exists(constants.PRETTY_PATH_DEFAULT):
                    os.mkdir(constants.PRETTY_PATH_DEFAULT)
                    pass

                if os.path.exists(pretty_file_path):
                    os.remove(pretty_file_path)
                    pass
                with open(pretty_file_path, 'x+', encoding='utf-8') as fp_out_json:
                    json.dump(
                        text_scenes,
                        fp_out_json,
                        ensure_ascii=False,
                        indent=2,
                        default=json_data.json_import_deserialize
                    )
                    fp_out_json.close()

                    print('Wrote pretty file \"{}\"\n'.format(pretty_file_path))
                    pass
                pass
            continue
        print('Done')
        pass
    else:
        print('No scn json files in path \"{}\" were found?!'.format(constants.PATH_SCN_ORIGINAL))
        pass
    return


if __name__ == '__main__':
    main()
    pass
