MILLI_SECOND = 1e-3
import math
def setupDs(testCase): return {'size': len(testCase)}
def runTest(dataStructure, testCase):
    import time
    time.sleep(MILLI_SECOND * math.log(dataStructure['size'], 16))
    return False
