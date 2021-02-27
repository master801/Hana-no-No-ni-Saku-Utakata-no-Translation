#!/usr/bin/env python3

import sys
sys.path.append('../..')  # Hacky - For generic_constants

import generic_constants

LEGACY = False  # JSON Legacy mode

PRETTY_LANGUAGE_DEFAULT = 'jpn'
PRETTY_LANGUAGE_CURRENT = 'eng'

if LEGACY:
    PRETTY_LANGUAGE_DEFAULT += '_legacy'
    PRETTY_LANGUAGE_CURRENT += '_legacy'
    pass
else:
    PRETTY_LANGUAGE_DEFAULT += '_new'
    PRETTY_LANGUAGE_CURRENT += '_new'
    pass

PRETTY_PATH = f'..{generic_constants.FP_S}pretty'
PRETTY_PATH_DEFAULT = f'{PRETTY_PATH}_{PRETTY_LANGUAGE_DEFAULT}'
PRETTY_PATH_CURRENT = f'{PRETTY_PATH}_{PRETTY_LANGUAGE_CURRENT}'
PRETTY_PATH_CURRENT_HASH = f'{PRETTY_PATH_CURRENT}{generic_constants.FP_S}hashes.csv'

PATH_SCN = f'..{generic_constants.FP_S}SCN'
PATH_SCN_ORIGINAL = f'{PATH_SCN}{generic_constants.FP_S}ORIGINAL'
PATH_SCN_WORKING = f'{PATH_SCN}{generic_constants.FP_S}MODIFIED'
