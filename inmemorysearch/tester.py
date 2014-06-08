import random

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
    if random.getrandbits(1):
        return (random.choice(testData['data']), True)
    else:
        return (random.choice(testData['nonData']), False)
