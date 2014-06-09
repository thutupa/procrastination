import os
import os.path
import sys
import time
# A magic file that should only be present in the base directory.
MAGIC_NAME = 'this_is_base_dir'

def _discoverBaseDir():
    fname = os.getcwd()
    while fname != '/':
        fdir = os.path.dirname(fname)
        if os.path.exists(os.path.join(fdir, MAGIC_NAME)):
            return fdir
        fname = fdir
    raise Exception("Could not discover base dir")

def FixPath():
    baseDir = _discoverBaseDir()
    sys.path.append(os.path.join(baseDir, 'lib/prettytable'))
    return
