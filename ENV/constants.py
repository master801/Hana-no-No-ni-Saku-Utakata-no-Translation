#!/usr/bin/env python3

import sys

if sys.platform == 'linux':  # Linux
    WINE = 'wine'
    FP_S = '/'
    PYTHON: str = 'python3'  # Ensure we use Python 3
    pass
elif sys.platform == 'win32':  # Windows
    WINE = ''  # Windows doesn't need wine
    PYTHON: str = 'python'  # Windows doesn't have a python3 executable...
    FP_S = '\\'
    pass
