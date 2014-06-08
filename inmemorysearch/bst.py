""" An implementation of the binary search tree as the in-memory
    data structure that returns if an element is present."""

class Node(object):
    def __init__(self, v):
        self.value = v
        self.left = None
        self.right = None

    def search(self, x):
        if self.value == x:
            return True
        if self.left is not None and self.value > x:
            return self.left.search(x)
        if self.right is not None and self.value < x:
            return self.right.search(x)
        return False
        

class Bst(object):
    def __init__(self): pass

    @staticmethod
    def build(sortedList):
        l = len(sortedList)
        # Check list is sorted
        for i in range(l - 1):
            assert sortedList[i] <= sortedList[i+1]
        # Recursively build the bst
        bst = Bst()
        bst.root = Bst.buildRecursive(sortedList, 0, l)
        return bst

    @staticmethod
    def buildRecursive(sortedList, start, length):
        rootIndex = start + length / 2
        root = Node(sortedList[rootIndex])
        leftTreeSize = rootIndex - start
        rightTreeSize = start + length - rootIndex - 1
        if leftTreeSize > 0:
            root.left = Bst.buildRecursive(sortedList, start, leftTreeSize)
        if rightTreeSize > 0:
            root.right = Bst.buildRecursive(sortedList, rootIndex+1, rightTreeSize)
        return root

def setupDs(testData):
    return Bst.build(sorted(testData['data']))

def runTest(bst, testCase):
    return bst.root.search(testCase)
