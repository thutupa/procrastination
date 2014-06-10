def setupDs(testData):
    dataStructure = {}
    for dataPoint in testData['data']:
        dataStructure[dataPoint] = 1
    return dataStructure
def runTest(dataStructure, testCase):
    return testCase in dataStructure
