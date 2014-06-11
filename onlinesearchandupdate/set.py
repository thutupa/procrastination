import tester

def setupDs(testData):
    return set(testData['data'])
def runTest(dataStructure, testCase):
    (mode, data) = testCase
    if mode == tester.SEARCH:
        return data in dataStructure
    elif mode == tester.INSERT:
        if data in dataStructure: return False
        dataStructure.add(data)
    else:
        assert mode == tester.DELETE
        if data not in dataStructure: return False
        dataStructure.remove(data)
    return True

