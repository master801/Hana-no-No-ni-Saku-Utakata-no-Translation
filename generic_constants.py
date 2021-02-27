#!/usr/bin/env python3

import sys

if sys.platform == 'linux':
    WINE = 'wine'
    FP_S = '/'
    pass
elif sys.platform == 'win32':  # Windows
    WINE = ''  # Windows doesn't need wine
    FP_S = '\\'
    pass
else:
    raise RuntimeError('Unsupported platform!')
    pass

SHOULD_MULTIPROCESS = True  # If multiprocessing should be enabled - This is enabled by default
