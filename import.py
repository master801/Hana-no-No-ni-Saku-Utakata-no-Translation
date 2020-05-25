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
            name: str = json_obj['name']
            scenes: list = json_obj['scenes']

            out_path = '{}{}{}.json'.format(constants.OUT_PATH, constants.FILE_PATH_SEPARATOR, name)
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
                if not os.path.exists(constants.OUT_PATH):
                    os.mkdir(constants.OUT_PATH)
                    pass

                if os.path.exists(out_path):
                    os.remove(out_path)
                    pass
                with open(out_path, 'x+', encoding='utf-8') as fp_out_json:
                    json.dump(
                        text_scenes,
                        fp_out_json,
                        ensure_ascii=False,
                        indent=2,
                        default=json_data.json_import_deserialize
                    )
                    fp_out_json.close()

                    print('Wrote pretty file \"{}\"\n'.format(out_path))
                    pass
                pass
            continue
        print('Done')
        pass
    return


if __name__ == '__main__':
    main()
    pass
