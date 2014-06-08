MICRO_SECOND = 1e-6
def setupDs(testCase): return {'size': len(testCase)}
def runTest(dataStructure, testCase):
    import time
    time.sleep(MICRO_SECOND * dataStructure['size'])
    return False
