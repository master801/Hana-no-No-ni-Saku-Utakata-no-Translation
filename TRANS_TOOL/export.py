#!/usr/bin/env python3

import argparse
import os
import json
import csv
import concurrent.futures
import hashlib
from typing import List

import sys
sys.path.append('..')  # Hacky - For generic_constants

import generic_constants
import constants
import json_data


def write_pretties_hash(hash_file: str, pretty_fps: List[str], called_from_encoding: bool):
    calculated_hashes = {}
    for pretty_fp in pretty_fps:
        hasher = hashlib.md5()
        with open(pretty_fp, 'rb+') as pretty_fp_io:
            while chunk := pretty_fp_io.read(8192):
                hasher.update(chunk)
                pass
            pretty_fp_io.close()
            pass
        calculated_hashes.update({
            pretty_fp[pretty_fp.rindex(generic_constants.FP_S) + 1:]: hasher.hexdigest().upper()
        })
        continue

    if not os.path.exists(hash_file):
        print(f'Hash file \"{hash_file}\" does not exist!')
        hashes = calculated_hashes
        pass
    else:
        print(f'Hash file \"{hash_file}\" exists')

        read_hashes = {}
        with open(hash_file, 'rt+', encoding='utf-8', newline='') as hash_io:
            reader = csv.reader(hash_io)

            for row in reader:
                if row[0] == 'file':  # Skip first row... no data
                    continue
                read_hashes.update({
                    row[0]: [row[1], row[2]]
                })
                pass

            hash_io.close()
            pass

        modified = False
        for key in read_hashes.keys():
            if key in calculated_hashes:
                read_hash = read_hashes[key]
                if read_hash[0] != calculated_hashes[key] and read_hash[1] != calculated_hashes[key]:
                    read_hash[1] = calculated_hashes[key]
                    modified = True
                    pass
                pass
            continue
            pass
        if modified:
            os.remove(hash_file)  # Delete hash file, since CSVs have been modified
            hashes = read_hashes
            print(f'Hash file \"{hash_file}\" has been modified...')
            print('Deleting to recreate...')
            pass
        else:
            hashes = None
        pass

    if not os.path.exists(hash_file):
        if hashes != None:
            print('Creating...')
            with open(hash_file, 'xt+', encoding='utf-8', newline='') as hash_io:
                writer = csv.writer(hash_io)
                writer.writerow(['file', 'original_hash', 'modified_hash'])
                for hash_key in hashes.keys():
                    writer.writerow([
                        hash_key,
                        hashes[hash_key][0],
                        hashes[hash_key][1]
                    ])
                    continue
                pass
            print(f'Done creating hash file \"{hash_file}\"!\n')
            pass
        else:
            print('No hash to be written...')
            pass
        pass
    return


def export_pretty_file(pretty_file: str):
    if constants.LEGACY:
        with open(pretty_file, 'rt+', encoding='utf-8') as io_pretty:
            pretty_scene_texts = json.load(io_pretty)
            io_pretty.close()
            pass
        pass
    else:
        pretty_scene_texts = []
        with open(pretty_file, 'rt+', encoding='utf-8', newline='') as io_pretty:
            reader = csv.reader(io_pretty)
            for row in reader:
                pretty_scene_texts.append(row)
                continue
            del row
            io_pretty.close()
            pass
        del reader
        pass
    del io_pretty

    print(f'Read pretty file \"{pretty_file}\"')

    if constants.LEGACY:
        fn: str = pretty_file[len(constants.PRETTY_PATH_CURRENT) + 1:]
        pass
    else:
        fn: str = pretty_file[len(constants.PRETTY_PATH_CURRENT) + 1:-4] + '.json'  # get rid of .csv extension
        pass

    fp: str = f'{constants.PATH_SCN_ORIGINAL}{generic_constants.FP_S}{fn}'
    if not os.path.isfile(fp):
        print(f'SCN JSON file \"{fp}\" does not exist!')
        return

    with open(fp, 'r', encoding='utf-8') as io_scn:
        json_scn = json.load(io_scn)
        io_scn.close()
        print(f'Read SCN JSON file \"{fp}\"\n')
        pass

    for i in range(len(pretty_scene_texts)):
        pretty_scene_text: list = pretty_scene_texts[i]
        if constants.LEGACY:
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
            pass
        else:
            sorted_pretty_scene_texts = {}
            for i1 in range(len(pretty_scene_texts)):
                pretty_scene_text = pretty_scene_texts[i1]
                if i1 == 0:
                    continue
                if int(pretty_scene_text[0]) not in sorted_pretty_scene_texts:
                    sorted_pretty_scene_texts.update(
                        {
                            int(pretty_scene_text[0]): []
                        }
                    )
                    pass
                sorted_pretty_scene_texts[int(pretty_scene_text[0])].append(pretty_scene_text[1:])
                continue
            del pretty_scene_text
            del i1

            for key in sorted_pretty_scene_texts.keys():
                pretty_scene_text = sorted_pretty_scene_texts[key]
                for i1 in range(len(pretty_scene_text)):
                    data = pretty_scene_text[i1]
                    scn_text = json_scn['scenes'][key]['texts'][i1]
                    if len(scn_text) == 9:
                        scn_text[0] = data[1]  # actual char
                        scn_text[1] = data[2]  # hidden char
                        scn_text[2] = data[3]  # txt
                        scn_text[4] = int(data[0])  # idk_1
                        scn_text[7] = data[4]  # txt hira
                        scn_text[8] = data[5]  # txt kata
                        pass
                    elif len(scn_text) == 6:
                        scn_text[0] = data[1]  # actual char
                        scn_text[1] = data[2]  # hidden char
                        scn_text[2] = data[3]  # txt
                        scn_text[4] = int(data[0])  # idk_1
                        pass
                    else:
                        print('Unexpected!')
                        breakpoint()
                        pass
                    continue
                del data
                del scn_text
                del i1
                continue
            del key
            del pretty_scene_text
            pass
        continue

    if not os.path.exists(constants.PATH_SCN_WORKING):
        os.mkdir(constants.PATH_SCN_WORKING)
        pass
    fp = constants.PATH_SCN_WORKING + generic_constants.FP_S + fn
    mode = 't+'
    if os.path.exists(fp):
        mode += 'w'
        pass
    else:
        mode += 'x'
        pass
    with open(fp, mode, encoding='utf-8') as io_scn:
        json.dump(json_scn, io_scn, ensure_ascii=False, indent=2)
        io_scn.close()
        print(f'Wrote modified scn json file \"{fp}\"\n')
        pass
    del fp
    return


def main():
    """
    Exports the modified text lines from pretty directories
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--ENCODING', dest='encoding', required=False, action='store_true')  # If export.py is called from ENCODING.py
    args = arg_parser.parse_args()

    pretty_fps = []
    for (root, subdirs, files) in os.walk(constants.PRETTY_PATH_CURRENT):
        for file in files:
            if (constants.LEGACY and file.endswith('.txt.json')) or (not constants.LEGACY and file.endswith('.txt.csv')):
                pretty_fps.append(f'{root}{generic_constants.FP_S}{file}')
                pass
            continue
        continue

    if len(pretty_fps) > 0:
        if constants.LEGACY:
            print('LEGACY MODE IS ENABLED!')
            print('THIS WILL NO LONGER BE SUPPORTED IN THE FUTURE!!')
            pass

        if generic_constants.SHOULD_MULTIPROCESS:
            executor = concurrent.futures.ProcessPoolExecutor()
            pass
        else:
            executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)
            pass

        for pretty_fp in pretty_fps:
            executor.submit(
                export_pretty_file,
                pretty_fp,
            )
            continue
        del pretty_fp

        executor.shutdown(wait=True, cancel_futures=False)

        write_pretties_hash(constants.PRETTY_PATH_CURRENT_HASH, pretty_fps, args.encoding)

        print('Done')
        del executor
        pass
    else:
        print(f'No pretty files in path \"{constants.PRETTY_PATH_CURRENT}\" were found?!')
        pass
    return


if __name__ == '__main__':
    main()
    pass
