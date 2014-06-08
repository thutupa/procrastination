#!/usr/bin/python

import time
import tester

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
            raise SolutionError
    endDataTestTimeMs = getTimeMs()
    return {'setupTime': startDataTestTimeMs - startTimeMs, 'runTime': endDataTestTimeMs - startDataTestTimeMs}

def main(solution):
    print '   size |   build |     run'
    for i in range(2, 6):
        sz = 10 ** i
        stats = measureRunTime(solution, sz, 1000)
        print '% 7d | % 7d | % 7d' % (sz, stats['setupTime'], stats['runTime'])

if __name__ == '__main__':
    import sys
    import imp
    name = sys.argv[1]
    if name[-3:] == '.py': name = name[:-3]

    # The following is mostly copied from python's documentation of imp
    fp, pathname, description = imp.find_module(name)

    try:
        solution = imp.load_module(name, fp, pathname, description)
        main(solution)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()