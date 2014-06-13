#!/usr/bin/python

def printInBox_(node, boxWidth=0):
    """ boxWidth, if supplied is the *inside width* of the box.
        A one-cell overhead is added for edges."""
    try:
        value = node.print_value()
    except:
        value = node.value()
    valueAsString = '%r' % value
    # Add a space padding on left and right.
    minBoxWidth = len(valueAsString) + 2
    if boxWidth > 0:
        assert minBoxWidth >= boxWidth
    else:
        boxWidth = minBoxWidth
    
    rightPadding = ' ' * ((boxWidth - len(valueAsString)) / 2)
    assert len(rightPadding) >= 1
    leftPadding = ' ' * (boxWidth - len(rightPadding) - len(valueAsString))
    assert len(leftPadding) >= 1

    valueLine = '|' + leftPadding + valueAsString + rightPadding + '|'
    topLine = '+' + '-' * boxWidth + '+'
    bottomLine = topLine

    # Sanity check
    assert len(topLine) == boxWidth + 2
    assert len(valueLine) == boxWidth + 2
    assert len(bottomLine) == boxWidth + 2
    return [topLine, valueLine, bottomLine]

def computeHeightWidth_(tree):
    if tree:
        height = len(tree)
        width = len(tree[0])
    else:
        height = 0
        width = 0
    return (height, width)
    
INTER_CHILD_PADDING = 2

def getLineOfWidthFromArray_(tree, index, expectedWidth, padLeft):
    if len(tree) <= index:
        return ' ' * expectedWidth
    else:
        line = tree[index]
        assert len(line) <= expectedWidth
        if len(line) < expectedWidth:
            padding = ' ' * (expectedWidth - len(line))
            if padLeft:
                line = padding + line
            else:
                line = line + padding
        return line

def printTreeBoxModel(root):
    print '\n'.join(treeInBox_(root))

def treeInBox_(root):
    if not root: return []

    rootTree = printInBox_(root)
    leftTree = treeInBox_(root.left())
    rightTree = treeInBox_(root.right())

    # There are three rectangles. The height of the final rectangle
    # is simple -- it's just the root.height + max(left.height, right.height)
    # The width is a little more complex. We want to print all of the left tree
    # On the left of the center of rootTree and similarly with right. Also, we
    # want a padding, let's call it INTER_CHILD_PADDING (say 2) which separates left
    # and right trees. Let half-wdith of root, rhw = (root.width - INTER_CHILD_PADDING)/2
    # Then width = max(rhw, left.wdith) + INTER_CHILD_PADDING + max(rhw, right.width)
    # It's easy to see that this should atleast be root.width.

    (rootHeight, rootWidth) = computeHeightWidth_(rootTree)
    (leftHeight, leftWidth) = computeHeightWidth_(leftTree)
    (rightHeight, rightWidth) = computeHeightWidth_(rightTree)

    rootHalfWidth = (rootWidth - INTER_CHILD_PADDING)/2
    treeWidth = INTER_CHILD_PADDING + max(rootHalfWidth, leftWidth) + max(rootHalfWidth, rightWidth)
    treeHeight = rootHeight + max(leftHeight, rightHeight)

    tree = []
    # Compute left padding of root. From the left tree, there is an overlap of rhw in the root.
    rootLeftPadding = max(0, leftWidth - rootHalfWidth)
    rootRightPadding = treeWidth - rootLeftPadding - rootWidth

    for line in rootTree:
        tree.append(' ' * rootLeftPadding + line + ' ' * rootRightPadding)
    
    # Next add the children.
    for i in range(treeHeight - rootHeight):
        leftLine = getLineOfWidthFromArray_(leftTree, i, rootLeftPadding + rootHalfWidth, True)
        rightLine = getLineOfWidthFromArray_(rightTree, i, treeWidth - len(leftLine) - INTER_CHILD_PADDING, False)
        tree.append(leftLine + '|' * INTER_CHILD_PADDING + rightLine)

    return tree

if __name__ == '__main__':
    class TestNode(object):
        def __init__(self, value):
            self.value_ = value
            self.left_ = None
            self.right_ = None

        def set_left(self, left):
            self.left_ = left
        
        def set_right(self, right):
            self.right_ = right

        def value(self): return self.value_
        def left(self): return self.left_
        def right(self): return self.right_

    testRoot = TestNode(500)
    testRoot.set_left(TestNode(500))
    testRoot.set_right(TestNode(500))
    testRoot.right().set_right(TestNode(500))
    testRoot.right().right().set_right(TestNode(500))
    testRoot.left().set_left(TestNode(500000))
    testRoot.left().set_right(TestNode(50000))

    print '\n'.join(treeInBox_(testRoot))
