import os
import subprocess
import sys
import shutil

if sys.platform == 'linux':  # Linux
    WINE = 'wine'
    FP_S = '/'
    pass
elif sys.platform == 'win32':  # Windows
    WINE = ''  # Windows doesn't need wine
    FP_S = '\\'
    pass

EXECUTABLE = f'TOOLS{FP_S}FreeMoteToolkit{FP_S}PsbDecompile.exe'

IN_SCN_DIR = f'ORIGINAL{FP_S}patch2{FP_S}scn'
OUT_SCN_DIR = f'..{FP_S}SCN{FPS_S}ORIGINAL'

def main():
    process_files()
    return

def process_files():
    for scn_file in scn_files:
        if scn_file.endswith('.txt.scn'):
            print(f'Processing file \"{IN_SCN_DIR}{FP_S}{scn_file}\"...')

            if os.path.isfile(OUT_SCN_DIR + FP_S + scn_file[:-4] + '.json') and os.path.isfile(OUT_SCN_DIR + FP_S + scn_file[:-4] + '.resx.json'):
                print('File has already been processed')
                print('Skipping...\n')
                continue

            execut = WINE + EXECUTABLE
            subprocess.call(
                [
                    execut,
                    IN_SCN_DIR + FP_S + scn_file # Arguments - No whitespaces allowed
                ],
    
                stderr=None,
                stdin=None,
                stdout=None
            )

            if not os.path.isfile(IN_SCN_DIR + FP_S + scn_file[:-4] + '.json') or not os.path.isfile(IN_SCN_DIR + FP_S + scn_file[:-4] + '.resx.json'):
                print('Failed to process file \"{}\"!'.format(scn_file))
                continue

            # Move files
            shutil.move(IN_SCN_DIR + FP_S + scn_file[:-4] + '.json', OUT_SCN_DIR + FP_S + scn_file[:-4] + '.json')
            shutil.move(IN_SCN_DIR + FP_S + scn_file[:-4] + '.resx.json', OUT_SCN_DIR + FP_S + scn_file[:-4] + '.resx.json')

            print('Done processing\n')
            pass
        continue
    return

if __name__ == '__main__':
    main()
    pass
