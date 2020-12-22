import os
import json

import constants
import json_data


# noinspection PyComparisonWithNone
def main():
    """
    Exports the modified text lines from `out` into the patch folder
    """
    fp_txt_json_files = []
    for (root, subdirs, files) in os.walk(constants.PRETTY_PATH_CURRENT):
        for file in files:
            if file.endswith('.txt.json'):
                fp_txt_json_files.append(root + constants.FILE_PATH_SEPARATOR + file)
                pass
            continue
        continue

    if len(fp_txt_json_files) > 0:
        for txt_json_file in fp_txt_json_files:  # The modified JSON files in 'output'
            with open(txt_json_file, 'r', encoding='utf-8') as io_json:
                pretty_scene_texts = json.load(io_json)
                io_json.close()
                print(f'Read pretty file \"{txt_json_file}\"')
                pass

            file_name: str = txt_json_file[len(constants.PRETTY_PATH_CURRENT)+1:]
            path: str = constants.PATH_SCN_ORIGINAL + constants.FILE_PATH_SEPARATOR + file_name
            if not os.path.isfile(path):
                print(f'Original file \"{path}\" does not exist!')
                continue
            with open(path, 'r', encoding='utf-8') as io_scn:
                json_scn = json.load(io_scn)
                io_scn.close()
                print(f'Read scn json file \"{path}\"')
                pass

            for i in range(len(pretty_scene_texts)):
                pretty_scene_text: list = pretty_scene_texts[i]
                if pretty_scene_text != None:
                    scene_texts: list = json_scn['scenes'][i]['texts']
                    if len(pretty_scene_text) != len(scene_texts):
                        print('SOMETHING UNEXPECTED HAPPENED!')
                        continue

                    for i1 in range(len(pretty_scene_text)):
                        pretty_scene_line = json_data.json_export_serialize(pretty_scene_text[i1])
                        pretty_scene_line[5] = scene_texts[i1][5]
                        json_scn['scenes'][i]['texts'][i1] = pretty_scene_line
                        continue
                    pass
                continue

            if not os.path.exists(constants.PATH_SCN_WORKING):
                os.mkdir(constants.PATH_SCN_WORKING)
                pass
            path = constants.PATH_SCN_WORKING + constants.FILE_PATH_SEPARATOR + file_name
            with open(path, '+w', encoding='utf-8') as io_scn:
                json.dump(json_scn, io_scn, ensure_ascii=False, indent=2)
                io_scn.close()
                print(f'Wrote modified scn json file \"{path}\"\n')
                pass
            continue
        print('Done')
        pass
    else:
        print(f'No pretty files in path \"{constants.PRETTY_PATH_CURRENT}\" were found?!')
        pass
    return


if __name__ == '__main__':
    main()
    pass
