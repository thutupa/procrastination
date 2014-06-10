#!/usr/bin/python

import fixpath
fixpath.FixPath()

import time
import tester
import sys
import printastable

class SolutionException(BaseException):
    def __init__(self, ds, data, nonData):
        self.ds = ds
        self.data = data
        self.nonData = nonData

    def __unicode__(self):
        return '%r' % {'DS': self.ds,
        'Data': self.data,
        'NonData': self.nonData}
    def __str__(self):
        return self.__unicode__()

def getTimeMs():
    return int(time.time() * 1000000)

def measureRunTime(solution, dataSize, testSize):
    testData = tester.generateTestData(dataSize)
    startTimeMs = getTimeMs()
    dataStructure = solution.setupDs(testData)
    startDataTestTimeMs = getTimeMs()
    for i in range(testSize):
        (testCase, expectedResult) = tester.generateTestCase(testData)
        seenResult = solution.runTest(dataStructure, testCase)
        if seenResult != expectedResult:
            print "Program fails at testcase %r (expected: %r, seen: %r)" % (testCase, expectedResult, seenResult)
            print "ABORTING PERFORMANCE ANALYSIS"
            raise SolutionException(dataStructure, testData['data'], testData['nonData'])
    endDataTestTimeMs = getTimeMs()
    return {'setupTime': startDataTestTimeMs - startTimeMs, 'runTime': endDataTestTimeMs - startDataTestTimeMs}

def main(solution):
    header = ['size', 'build', 'run']
    data = []
    for i in range(2, 7):
        sz = 10 ** i
        stats = measureRunTime(solution, sz, 1000)
        data = data + [[sz, stats['setupTime'], stats['runTime']]]
    printastable.printAsTable(header, data)

if __name__ == '__main__':
    import sys
    import imp
    for name in sys.argv[1:]:
        if name[-3:] == '.py': name = name[:-3]

        # The following is mostly copied from python's documentation of imp
        fp, pathname, description = imp.find_module(name)
        
        try:
            solution = imp.load_module(name, fp, pathname, description)
            print name
            main(solution)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
