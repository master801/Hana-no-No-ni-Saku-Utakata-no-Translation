import sys

if sys.platform == 'linux':
    WINE = 'wine'
    FILE_PATH_SEPARATOR = '/'
    pass
else:
    WINE = ''  # Windows doesn't need wine
    FILE_PATH_SEPARATOR = '\\'
    pass

OUT_PATH = 'pretty'
PATH_SCN = 'SCN'
PATH_SCN_ORIGINAL = PATH_SCN + FILE_PATH_SEPARATOR + 'ORIGINAL'
PATH_SCN_WORKING = PATH_SCN + FILE_PATH_SEPARATOR + 'MODIFIED'
