#!/usr/bin/python

import fixpath
fixpath.FixPath()

import time
import tester
import sys
import printastable
import random

BUILD_HEADER = 'build'
RUN_HEADER = 'run'
TESTGEN_HEADER = 'testgen'
SIZE_HEADER = 'size'


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

class UTimer(object):
    START = -1

    def __init__(self):
        self.reset()

    def reset(self):
        self.series = [getTimeUs()]
        self.eventIndices = {UTimer.START: 0}

    def record(self, event):
        assert event != UTimer.START
        self.series.append(getTimeUs())
        self.eventIndices[event] = len(self.series) - 1

    def interval(self, event1, event2):
        """Get the interval between event1 and event2."""
        return (self.series[self.eventIndices[event2]] -
                self.series[self.eventIndices[event1]])
       
def getTimeUs():
    return int(time.time() * 1000000)

EVENT_TEST_CASE_GEN_FINISHED = random.randint(1000, 100000)
EVENT_TEST_CASE_RUN_FINISHED = EVENT_TEST_CASE_GEN_FINISHED + random.randint(1000, 100000)
EVENT_DATA_GEN_FINISHED = EVENT_TEST_CASE_RUN_FINISHED + random.randint(1000, 100000)

def reportFailure(i, testCase, expectedResult, seenResult, dataStructure, testData):
    print "Program fails at testcase(index %r) %r (expected: %r, seen: %r)" % (
        i, testCase, expectedResult, seenResult)
    print "ABORTING PERFORMANCE ANALYSIS"
    raise SolutionException(dataStructure, testData['data'], testData['nonData'])

def measureRunTime(solution, dataSize, testRuns):
    # Generate data of given size
    testData = tester.generateTestData(dataSize)

    # Ask DS to initialize itself while timing it.
    buildUTimer = UTimer()
    dataStructure = solution.setupDs(testData)
    buildUTimer.record(EVENT_DATA_GEN_FINISHED)

    # Run the test for the specified number of times
    runTimeUs = 0
    testCaseGenerationTimeUs = 0
    testCaseUTimer = UTimer()
    for i in range(testRuns):
        # Reset the test case timer for every loop
        testCaseUTimer.reset()

        # Generate the testcase.
        (testCase, expectedResult) = tester.generateTestCase(testData)

        # Run the test case.
        testCaseUTimer.record(EVENT_TEST_CASE_GEN_FINISHED)
        seenResult = solution.runTest(dataStructure, testCase)
        testCaseUTimer.record(EVENT_TEST_CASE_RUN_FINISHED)

        # Check the results match.
        if seenResult != expectedResult:
            reportFailure(i, testCase, expectedResult, seenResult, dataStructure, testData)

        # Add up the times for reporting
        runTimeUs += testCaseUTimer.interval(EVENT_TEST_CASE_GEN_FINISHED,
                                             EVENT_TEST_CASE_RUN_FINISHED)
        testCaseGenerationTimeUs += testCaseUTimer.interval(UTimer.START,
                                                            EVENT_TEST_CASE_GEN_FINISHED)
    return {BUILD_HEADER: buildUTimer.interval(UTimer.START, EVENT_DATA_GEN_FINISHED),
            RUN_HEADER: runTimeUs,
            TESTGEN_HEADER: testCaseGenerationTimeUs}

def runSolution(solution, minExponent=2, maxExponent=6, numIterations=1000,
                headerList=None):
    if headerList is None:
        headerList = [SIZE_HEADER, BUILD_HEADER, RUN_HEADER, TESTGEN_HEADER]
    data = []
    for i in range(minExponent, maxExponent):
        sz = 10 ** i
        stats = measureRunTime(solution, sz, numIterations)
        data = data + [[sz, stats[BUILD_HEADER], stats[RUN_HEADER],
                        stats[TESTGEN_HEADER]]]
    printastable.printAsTable(headerList, data)

def main():
    import sys
    import imp
    for name in sys.argv[1:]:
        if name[-3:] == '.py': name = name[:-3]

        # The following is mostly copied from python's documentation of imp
        fp, pathname, description = imp.find_module(name)
        
        try:
            solution = imp.load_module(name, fp, pathname, description)
            print name
            runSolution(solution)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
