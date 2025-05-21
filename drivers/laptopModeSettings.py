dirPath: str = "./mSD"
from os import path, mkdir
if not path.isdir(dirPath):
    mkdir(dirPath)

import time
time.monotonic = lambda: time.time()