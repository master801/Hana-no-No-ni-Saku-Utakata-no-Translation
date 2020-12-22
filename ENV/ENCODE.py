import os
import subprocess
import sys
import shutil
import argparse

import codecs

if sys.platform == 'linux':  # Linux
    WINE = 'wine '
    PYTHON = 'python3'  # Ensure we use Python 3
    FILE_PATH_SEPARATOR = '\\'
    pass
elif sys.platform == 'win32':  # Windows
    WINE = ''  # Windows doesn't need wine
    PYTHON = 'python'
    FILE_PATH_SEPARATOR = '/'
    pass

EXECUTABLE = f'TOOLS{FILE_PATH_SEPARATOR}FreeMoteToolkit{FILE_PATH_SEPARATOR}PsBuild.exe'

IN_DIR: str = 'WORKING'
IN_PATCH_DIR: str = f'{IN_DIR}{FILE_PATH_SEPARATOR}patch2'
IN_DIRS: list = ['image', 'uipsd']
OUT_DIR: str = 'MODIFIED'
OUT_PATCH_DIR: str = f'{OUT_DIR}{FILE_PATH_SEPARATOR}patch2'
OUT_XP3: str = f'{OUT_DIR}{FILE_PATH_SEPARATOR}patch2.xp3'
IN_SCN_DIR: str = f'..{FILE_PATH_SEPARATOR}SCN'


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--compile', dest='compile', required=False, action='store_true')
    arg_parser.add_argument('--process_scn', dest='process_scn', required=False, action='store_true')
    args = arg_parser.parse_args()

    make_environment(args.compile)
    if args.compile:
        export()
        pass
    copy_export()

    if args.process_scn:
        process_scn_files()
        pass
    copy_files()

    print('Done!')
    return


def make_environment(compile: bool):
    # Set up MODIFIED/patch2 folder
    if compile:
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
            fp = f'{OUT_PATCH_DIR}/{dir_file}'
            if os.path.isfile(fp) and not dir_file.endswith('.txt.scn'):
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


def export():
    # Dirty hacks...
    os.chdir('../TRANS_TOOL')
    subprocess.call(f'{PYTHON} export.py', shell=True)
    os.chdir('../ENV')
    return


def copy_export():
    for in_dir in IN_DIRS:
        dir_fp: str = f'{IN_PATCH_DIR}/{in_dir}'
        for in_dir_file in os.listdir(dir_fp):
            shutil.copy2(f'{dir_fp}/{in_dir_file}', OUT_PATCH_DIR)
            continue
        continue
    return


def copy_files():
    subdirs = ['', 'main', 'main/flowmap', 'sysscn']
    for subdir in subdirs:
        if subdir == '':
            path = IN_PATCH_DIR
            pass
        else:
            path = f'{IN_PATCH_DIR}{FILE_PATH_SEPARATOR}{subdir}'
            pass

        for dir_file in os.listdir(path):
            file_path = f'{path}{FILE_PATH_SEPARATOR}{dir_file}'
            if not os.path.isfile(file_path):  # Skip paths that aren't files
                print(f'\"{file_path}\" is not a file.\nSkipping...\n')
                continue

            rewrite = False
            try:
                f = codecs.open(file_path, encoding='shift-jis', errors='strict')
                for line in f:
                    # NOOP
                    # We're just reading lines to see if it's not shift-jis
                    continue
                f.close()

                print(f'File \"{file_path}\" is a Shift-JIS file!')
                pass
            except:
                print(f'File \"{file_path}\" is NOT a Shift-JIS file?!')
                rewrite = True
                pass

            out_fp = f'{OUT_PATCH_DIR}{FILE_PATH_SEPARATOR}{dir_file}'
            if rewrite:
                print('Attempting to rewrite as Shift-JIS...')

                f = open(file_path, mode='r+t', encoding='utf-8', errors='strict')
                f2 = open(out_fp, mode='xt', encoding='shift-jis', errors='strict')

                f2.write(f.read())

                f2.flush()
                f2.close()
                f.close()

                print(f'Wrote rewritten file to \"{out_fp}\"!\n')
                pass
            else:
                shutil.copy2(file_path, out_fp)
                print(f'Copied file \"{file_path}\" to \"{OUT_PATCH_DIR}\"!\n')
                pass
            continue
        continue
    return


def process_scn_files():
    # Process scn files
    in_dir_scn = f'{IN_SCN_DIR}{FILE_PATH_SEPARATOR}MODIFIED'
    for dir_file in os.listdir(in_dir_scn):
        fp = f'{in_dir_scn}{FILE_PATH_SEPARATOR}{dir_file}'
        if dir_file.endswith('.json') and not dir_file.endswith('.resx.json'):
            print(f'Processing file \"{fp}\"...')

            execut = WINE + EXECUTABLE
            subprocess.call(
                [
                    execut,
                    f'{in_dir_scn}{FILE_PATH_SEPARATOR}{dir_file}' # Arguments - No whitespaces allowed
                ],
    
                stderr=None,
                stdin=None,
                stdout=None
            )

            # Remove .json and .resx.json in MODIFIED/patch2, then move .scn to MODIFIED/patch2
            scn_in_path = dir_file[:-5] + '.pure.scn'
            if os.path.isfile(scn_in_path):
                fp_json = f'{OUT_PATCH_DIR}{FILE_PATH_SEPARATOR}{dir_file}'
                fp_json_resx = f'{OUT_PATCH_DIR}{FILE_PATH_SEPARATOR}' + dir_file[:-5] + '.resx.json'
                if os.path.isfile(fp_json):
                    os.remove(OUT_PATCH_DIR + FILE_PATH_SEPARATOR + dir_file)  # .json
                    pass
                if os.path.isfile(fp_json):
                    os.remove(OUT_PATCH_DIR + FILE_PATH_SEPARATOR + fp_json_resx)  # .resx.json
                    pass

                shutil.move(scn_in_path, OUT_PATCH_DIR + FILE_PATH_SEPARATOR + dir_file[:-5] + '.scn')
                pass
            else:
                print('!!ERROR!!')
                print('!!Failed to compile scn file!!')
                print(f'ERRORING SCN FILE: \"{in_dir_scn}{FILE_PATH_SEPARATOR}{dir_file}\" \"{scn_in_path}\"')
                pass
            pass
        continue
    return


if __name__ == '__main__':
    main()
    pass
