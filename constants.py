import sys

if sys.platform == 'linux':
    WINE = 'wine'
    FILE_PATH_SEPARATOR = '/'
    pass
else:
    WINE = ''  # Windows doesn't need wine
    FILE_PATH_SEPARATOR = '\\'
    pass

PRETTY_LANGUAGE_DEFAULT = 'jpn'
PRETTY_LANGUAGE_CURRENT = 'eng'
PRETTY_PATH = 'pretty'
PRETTY_PATH_DEFAULT = PRETTY_PATH + '_' + PRETTY_LANGUAGE_DEFAULT
PRETTY_PATH_CURRENT = PRETTY_PATH + '_' + PRETTY_LANGUAGE_CURRENT

PATH_SCN = 'SCN'
PATH_SCN_ORIGINAL = PATH_SCN + FILE_PATH_SEPARATOR + 'ORIGINAL'
PATH_SCN_WORKING = PATH_SCN + FILE_PATH_SEPARATOR + 'MODIFIED'
