#!/usr/bin/env python3
import os
import subprocess
import shutil
import concurrent.futures

import sys
sys.path.append('..')  # Hacky - For generic_constants

import generic_constants
import constants

EXECUTABLE = f'TOOLS{generic_constants.FP_S}FreeMoteToolkit{generic_constants.FP_S}PsbDecompile.exe'

IN_SCN_DIR = f'ORIGINAL{generic_constants.FP_S}patch2{generic_constants.FP_S}scn'
OUT_SCN_DIR = f'..{generic_constants.FP_S}SCN{generic_constants.FP_S}ORIGINAL'


def process_scn_file(scn_file: str):
    if scn_file.endswith('.txt.scn'):
        print(f'Processing file \"{IN_SCN_DIR}{generic_constants.FP_S}{scn_file}\"...')

        if os.path.exists(OUT_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.json') and \
                os.path.exists(OUT_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.resx.json'):
            print('File has already been processed')
            print('Skipping...\n')
            return

        executable = f'{constants.WINE}{EXECUTABLE}'
        subprocess.call(
            [
                executable,
                IN_SCN_DIR + generic_constants.FP_S + scn_file  # Arguments - No whitespaces allowed
            ],

            stderr=None,
            stdin=None,
            stdout=None
        )
        del executable

        if not os.path.isfile(IN_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.json') or \
                not os.path.isfile(IN_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.resx.json'):
            print('Failed to process file \"{}\"!'.format(scn_file))
            return

        # Move files
        shutil.move(IN_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.json',
                    OUT_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.json'
                    )
        shutil.move(IN_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.resx.json',
                    OUT_SCN_DIR + generic_constants.FP_S + scn_file[:-4] + '.resx.json'
                    )

        print('Done processing\n')
        pass
    return


def process_files():
    scn_files = []
    for i in os.listdir(IN_SCN_DIR):
        if i.endswith('.txt.scn'):
            scn_files.append(i)
            pass
        continue
    del i

    if generic_constants.SHOULD_MULTIPROCESS:
        executor = concurrent.futures.ProcessPoolExecutor()
        pass
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)
        pass

    for scn_file in scn_files:
        executor.submit(
            process_scn_file,
            scn_file
        )
        continue
    del scn_file

    executor.shutdown(wait=True, cancel_futures=False)

    print('Done')
    del executor
    return


def main():
    process_files()
    return


if __name__ == '__main__':
    main()
    pass
