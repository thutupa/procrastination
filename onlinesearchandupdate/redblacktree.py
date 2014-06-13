import tester

class Node(object):
    def __init__(self, value):
        self.is_red_ = True
        self.value_ = value
        self.left_ = None
        self.right_ = None
        self.parent_ = None

    def value(self): return self.value_
    def print_value(self):
        if self.is_red():
            return '%r *' % self.value_
        else:
            return '%r  ' % self.value_
    def is_red(self): return self.is_red_
    def is_black(self): return not self.is_red()
    def set_black(self, is_black=True): self.is_red_ = not is_black
    def set_red(self, is_red=True): self.is_red_ = is_red
    def left(self): return self.left_
    def set_left(self, node): self.left_ = node
    def right(self): return self.right_
    def set_right(self, node): self.right_ = node
    def parent(self): return self.parent_
    def set_parent(self, parent): self.parent_ = parent
    def grandparent(self):
        assert self.parent() is not None
        return self.parent().parent()

    @staticmethod
    def node_black(node):
        if node:
            return node.is_black()
        else:
            return True
    
    @staticmethod
    def node_red(node):
        return not Node.node_black(node)

    def left_child_black(self):
        return self.node_black(self.left())

    def left_child_red(self):
        return not self.left_child_black()

    def right_child_black(self):
        return self.node_black(self.right())
    
    def right_child_red(self):
        return not self.right_child_black()
        

class RedBlackTree(object):
    def __init__(self):
        self.root_ = None

    def root(self): return self.root_

    def search_value_(self, value):
        parent = None
        current = self.root_
        
        while current is not None:
            if value == current.value():
                break
            elif value > current.value():
                parent = current
                current = current.right()
            else:
                assert value < current.value()
                parent = current
                current = current.left()

        return (parent, current)

    def rotate_and_recolor_(self, node):
        """Rotate about node and it's parent."""
        parent = node.parent()
        assert parent is not None
        if parent.left() == node:
            # A picture helps at this point.
            #     gp?               gp?
            #     |                 |
            #     p                 n1
            #    / \               / \
            #   n   *  --->       *  p1
            #  / \                   / \  
            # *   b?                b1? *
            # n is node; p is parent
            # The '?' implies the node could be None, which is
            # relevant because we need to fix parent pointers.
            n1 = node
            p1 = parent
            b1 = node.right()
            gp = parent.parent()

            # Fix links from and to gp going to lower levels.
            if gp:
                if gp.left() == parent:
                    gp.set_left(n1)
                else:
                    gp.set_right(n1)
            else:
                self.root_ = n1
            n1.set_parent(gp)

            # Fix links from and to n1 going to lower levels.
            n1.set_right(p1)
            p1.set_parent(n1)

            # Fix links from and to p1 going to lower levels
            p1.set_left(b1)
            if b1: b1.set_parent(p1)
        else:
            # A picture helps at this point, too
            #    gp?               gp?
            #    |                 |
            #    p                 n1
            #   / \               / \
            #  *   n  --->       p1  *
            #     / \            / \  
            #    a?  *          *   a1?
            # n is node; p is parent
            # The '?' implies the node could be None, which is
            # relevant because we need to fix parent pointers.
            n1 = node
            p1 = parent
            a1 = node.left()
            gp = parent.parent()

            # Fix links from and to gp going to lower levels.
            if gp:
                if gp.left() == parent:
                    gp.set_left(n1)
                else:
                    gp.set_right(n1)
            else:
                self.root_ = n1
            n1.set_parent(gp)
            
            # Fix links from and to n1 going to lower levels.
            p1.set_parent(n1)
            n1.set_left(p1)

            # Fix links from and to p1 going to lower levels.
            p1.set_right(a1)
            if a1: a1.set_parent(p1)
        n_is_red = node.is_red()
        p_is_red = parent.is_red()
        node.set_red(p_is_red)
        parent.set_red(n_is_red)
        
    def lookup_uncle_(self, gp, p, node):
        assert gp is not None
        if gp.left() == p:
            return gp.right()
        else:
            return gp.left()

    def fix_violation_up_(self, node):
        if node == self.root():
            node.set_black()
            return
        if node.is_red():
            parent = node.parent()
            assert parent is not None
            if parent.is_red():
                grandparent = parent.parent()
                uncle = self.lookup_uncle_(grandparent, parent, node)
                assert grandparent is not None
                if Node.node_red(uncle):
                    # Parent is red, uncle is red. Move the redness upto grandparent
                    # and fix starting at grandparent
                    assert uncle is not None
                    uncle.set_black()
                    parent.set_black()
                    grandparent.set_red()
                    self.fix_violation_up_(grandparent)
                    return
                else:
                    # parent is red, uncle is black (could be None).
                    # Rotate about the parent<->grandparent axis
                    self.rotate_and_recolor_(parent)

                    self.fix_violation_up_(node)
            else:
                # Parent is black
                # Nothing to fix.
                pass
        else:
            # Node is black.
            # Nothing to fix.
            pass
                
    def insert(self, value):
        if not self.root():
            self.root_ = Node(value)
            self.root_.set_black()
            return
        
        (parent, node) = self.search_value_(value)
        # Check the search did not succeed
        if node is not None:
            raise Exception("Value %r already present in the tree" % value)
        
        # Attach the node in the right place
        node = Node(value)
        if value > parent.value():
            parent.set_right(node)
        else:
            parent.set_left(node)
        node.set_parent(parent)
        self.fix_violation_up_(node)

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


if __name__ == '__main__':
    import fixpath
    fixpath.FixPath()
    import binarytreeutil
    rbtree = RedBlackTree()
    print '-----------------------------------'
    for i in range(28):
        rbtree.insert(i)
    binarytreeutil.printTreeBoxModel(rbtree.root())
    print '-----------------------------------'
