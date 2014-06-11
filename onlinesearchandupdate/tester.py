import random

SEARCH = 'search'
INSERT = 'insert'
DELETE = 'delete'

def generateTestData(dataSize):
    """an inefficient method to generate sample data."""
    testData = {'data': random.sample(xrange(dataSize * 100), dataSize)}
    dataSet = set(testData['data'])
    nonData = set()
    while len(nonData) < dataSize:
        newElements = set(random.sample(xrange(dataSize * 100), dataSize)) - dataSet - nonData
        required = min(dataSize - len(nonData), len(newElements))
        nonData = nonData | set(random.sample(newElements, required))
    testData['nonData'] = list(nonData)
    assert len(set(testData['data']) & set(testData['nonData'])) == 0
    assert len(testData['data']) == dataSize
    assert len(testData['nonData']) == dataSize
    return testData

def generateTestCase(testData):
    bitOne = random.getrandbits(1)
    bitTwo = random.getrandbits(1)
    if bitOne:
        if bitTwo:
            return ((SEARCH, random.choice(testData['data'])), True)
        else:
            return ((SEARCH, random.choice(testData['nonData'])), False)
    else:
        if bitTwo:
            toInsert = random.choice(testData['nonData'])
            testData['nonData'].remove(toInsert)
            testData['data'] += [toInsert]
            return ((INSERT, toInsert), True)
        else:
            toDelete = random.choice(testData['data'])
            testData['data'].remove(toDelete)
            testData['nonData'] += [toDelete]
            return ((DELETE, toDelete), True)
