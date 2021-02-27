#!/usr/bin/env python3

import os
import subprocess
import shutil
import argparse
import codecs
import concurrent.futures
import csv

import sys
sys.path.append('..')  # Hacky - For generic_constants

import generic_constants
import constants


EXECUTABLE: str = f'TOOLS{generic_constants.FP_S}FreeMoteToolkit{generic_constants.FP_S}PsBuild.exe'

#if sys.platform == 'linux':
#    EXECUTABLE: str = './' + EXECUTABLE
#    pass

IN_DIR: str = 'WORKING'
IN_PATCH_DIR: str = f'{IN_DIR}{generic_constants.FP_S}patch2'
OUT_DIR: str = 'MODIFIED'
OUT_PATCH_DIR: str = f'{OUT_DIR}{generic_constants.FP_S}patch2'
OUT_XP3: str = f'{OUT_DIR}{generic_constants.FP_S}patch2.xp3'
IN_SCN_DIR: str = f'..{generic_constants.FP_S}SCN'
IN_SCN_MODIFIED_DIR: str = f'{IN_SCN_DIR}{generic_constants.FP_S}MODIFIED'


def copy_files():
    sub_dirs: list = [
        '',
        'main', f'main{generic_constants.FP_S}flowmap',
        'sysscn',
        'image', f'image{generic_constants.FP_S}pop',
        'uipsd'
    ]
    for sub_dir in sub_dirs:
        if sub_dir == '':
            path: str = IN_PATCH_DIR
            pass
        else:
            path: str = f'{IN_PATCH_DIR}{generic_constants.FP_S}{sub_dir}'
            pass

        for dir_file in os.listdir(path):
            fp: str = f'{path}{generic_constants.FP_S}{dir_file}'
            if not os.path.isfile(fp):  # Skip paths that aren't files
                print(f'\"{fp}\" is not a file.\nSkipping...\n')
                continue

            out_fp: str = f'{OUT_PATCH_DIR}{generic_constants.FP_S}{dir_file}'
            if fp.endswith('.txt') or fp.endswith('.ini') or fp.endswith('.tjs') or fp.endswith('.ks'):
                rewrite: bool = False
                try:
                    f = codecs.open(fp, encoding='shift-jis', errors='strict')
                    for line in f:
                        # NOOP
                        # We're just reading lines to see if it's not shift-jis
                        continue
                    f.close()

                    print(f'File \"{fp}\" is a Shift-JIS file!')
                    pass
                except:
                    print(f'File \"{fp}\" is NOT a Shift-JIS file?!')
                    rewrite = True
                    pass

                if rewrite:
                    print('Attempting to rewrite as Shift-JIS...')

                    f = open(fp, mode='r+t', encoding='utf-8', errors='strict')
                    f2 = open(out_fp, mode='xt', encoding='shift-jis', errors='strict')

                    f2.write(f.read())

                    f2.flush()
                    f2.close()
                    f.close()

                    print(f'Wrote rewritten file to \"{out_fp}\"!\n')
                    continue
                pass
            print(f'Copying file \"{fp}\" to \"{OUT_PATCH_DIR}\"...')
            shutil.copy2(fp, out_fp)
            print(f'Copied file \"{fp}\" to \"{OUT_PATCH_DIR}\"!\n')
            pass
        continue
    return


def process_scn_file(in_dir: str, in_scn: str):
    executable = generic_constants.WINE + EXECUTABLE
    subprocess.run(
        [
            executable,
            f'{in_dir}{generic_constants.FP_S}{in_scn}'  # Arguments - No whitespaces allowed
        ],

        stderr=None,
        stdin=None,
        stdout=None
    )

    # Remove .json and .resx.json in MODIFIED/patch2 if exists
    # Then move .scn to MODIFIED/patch2
    scn_in_path = in_scn[:-5] + '.pure.scn'
    if os.path.isfile(scn_in_path):
        fp_json = f'{OUT_PATCH_DIR}{generic_constants.FP_S}{in_scn}'
        fp_json_resx = f'{OUT_PATCH_DIR}{generic_constants.FP_S}' + in_scn[:-5] + '.resx.json'
        if os.path.isfile(fp_json):
            os.remove(f'{OUT_PATCH_DIR}{generic_constants.FP_S}{in_scn}')  # .json
            pass
        if os.path.isfile(fp_json_resx):
            os.remove(f'{OUT_PATCH_DIR}{generic_constants.FP_S}{fp_json_resx}')  # .resx.json
            pass

        shutil.move(scn_in_path, OUT_PATCH_DIR + generic_constants.FP_S + in_scn[:-5] + '.scn')
        pass
    else:
        print('!!ERROR!!')
        print('!!Failed to compile scn file!!')
        print(f'INVALID SCN FILE: \"{IN_SCN_MODIFIED_DIR}{generic_constants.FP_S}{in_scn}\" \"{scn_in_path}\"')
        breakpoint()
        pass
    return


def process_scn_files():
    # Process scn files
    if generic_constants.SHOULD_MULTIPROCESS:
        executor = concurrent.futures.ProcessPoolExecutor()
        pass
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)
        pass

    for dir_file in os.listdir(IN_SCN_MODIFIED_DIR):
        if dir_file.endswith('.json') and not dir_file.endswith('.resx.json'):
            print(f'Processing file \"{IN_SCN_MODIFIED_DIR}{generic_constants.FP_S}{dir_file}\"...')
            executor.submit(
                process_scn_file,
                IN_SCN_MODIFIED_DIR,
                dir_file
            )
        continue
    del dir_file

    executor.shutdown(wait=True, cancel_futures=False)

    print('Done processing scn files')

    del executor
    return


def export():
    # Dirty hacks...
    os.chdir(f'..{generic_constants.FP_S}TRANS_TOOL')
    subprocess.call(
        f'{constants.PYTHON} export.py --ENCODING',
        shell=True
    )
    os.chdir(f'..{generic_constants.FP_S}ENV')
    return


def make_environment(_compile: bool):
    # Set up MODIFIED/patch2 folder
    if _compile:
        if os.path.isdir(OUT_PATCH_DIR):
            print(f'Directory \"{OUT_PATCH_DIR}\" already exists\nRemoving...')
            shutil.rmtree(OUT_PATCH_DIR)
            print('Done Removing!\n')
            pass
        pass

    if not os.path.isdir(OUT_PATCH_DIR):
        print(f'Directory \"{OUT_PATCH_DIR}\" doesn\'t exist.\nCreating...')
        os.mkdir(OUT_PATCH_DIR)  # Make new dir
        print(f'Done Creating!\n')
        pass

    files = os.listdir(OUT_PATCH_DIR)
    if len(files) > 0:
        for dir_file in files:
            fp = f'{OUT_PATCH_DIR}{generic_constants.FP_S}{dir_file}'
            if os.path.exists(fp) and os.path.isfile(fp) and not dir_file.endswith('.txt.scn'):
                os.remove(fp)
                print(f'Removed file \"{fp}\"...')
                pass
            continue
        pass
    pass

    if os.path.exists(OUT_XP3):  # Delete patch xp3
        print(f'File \"{OUT_XP3}\" already exists.\nRemoving...')
        os.remove(OUT_XP3)
        print('Done Removing!\n')
        pass
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--compile', dest='compile', required=False, action='store_true')
    arg_parser.add_argument('--process_scn', dest='process_scn', required=False, action='store_true')
    arg_parser.add_argument('--no_export', dest='no_export', required=False, action='store_false')
    args = arg_parser.parse_args()

    make_environment(args.compile)
    if args.compile and args.no_export:
        export()
        pass

    if args.process_scn:
        process_scn_files()
        pass
    copy_files()

    print('Done!')
    return


if __name__ == '__main__':
    main()
    pass
