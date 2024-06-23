# Binary Search Tree (BST)
# definition: a binary tree in which for each node, all elements in the left subtree are less than the root,
#               and all elements in the right subtree are greater than the root

# Complexity is proportional to the height of the tree

# Balanced BST: height is O(log n)
# Unbalanced BST: height is O(n)

# for perfectly balanced BST:
# if height = h, is proportional to log n
# size = 2^{h+1} - 1, is proportional to 2^h

# for degenerate BST:
# height = n - 1, is proportional to O(n)
# size = n, is proportional to n


class BinarySearchTree:
    def __init__(self, root=None, L=None, R=None):
        self.root = root
        self.L = L
        self.R = R

    def __add__(self, other):
        return BinarySearchTree(self.root, self.L, other)

    def isempty(self):
        return self.root is None

    def contains(self, value):
        if self.root is None:
            return False
        if value == self.root:
            return True
        if value < self.root:
            return self.L.contains(value) if self.L else False
        return self.R.contains(value) if self.R else False
        # Complexity is proportional to the height of the tree = O(h)
        # time complexity is O(log n) for balanced BST
        # time complexity is O(n) for unbalanced BST

    def height(self):
        if self.root is None:
            return -1
        if self.L is None and self.R is None:
            return 1
        if self.L is None:
            return 1 + self.R.height()
        if self.R is None:
            return 1 + self.L.height()
        return 1 + max(self.L.height(), self.R.height())

    def size(self):
        if self.root is None:
            return 0
        if self.L is None and self.R is None:
            return 1
        if self.L is None:
            return 1 + self.R.size()
        if self.R is None:
            return 1 + self.L.size()
        return 1 + self.L.size() + self.R.size()

    def pathlength(self, depth=1):
        if self.root is None:
            return 0
        if self.L is None and self.R is None:
            return depth
        if self.L is None:
            return depth + self.R.pathlength(depth + 1)
        if self.R is None:
            return depth + self.L.pathlength(depth + 1)
        return depth + self.L.pathlength(depth + 1) + self.R.pathlength(depth + 1)

    def breadthfirst(self):
        queue = [self]
        while queue:
            current = queue.pop(0)
            print(current.root)
            if current.L:
                queue.append(current.L)
            if current.R:
                queue.append(current.R)

    def depthfirst(self):
        if self.L:
            self.L.depthfirst()
        print(self.root)
        if self.R:
            self.R.depthfirst()

    def __str__(self):
        if self.root is None:
            return "<>"
        if self.L is None and self.R is None:
            return f"<{self.root}>"
        if self.L is None:
            return f"<{self.root}, {self.R}>"
        if self.R is None:
            return f"<{self.root}, {self.L}>"
        return f"<{self.root}, {self.L}, {self.R}>"

    def display(self, depth=0):
        if self.root is None:
            return
        if self.R:
            self.R.display(depth + 1)
        print("  " * 2 * depth + str(self.root))
        if self.L:
            self.L.display(depth + 1)

    # Leaf Addition
    def insert(self, value):
        if self.root is None:
            self.root = value
            return
        if value == self.root:
            return self
        if value < self.root:
            if self.L is None:
                self.L = BinarySearchTree(value)
            else:
                self.L.insert(value)
        if value > self.root:
            if self.R is None:
                self.R = BinarySearchTree(value)
            else:
                self.R.insert(value)

    def findmin(self):
        if self.L is None:
            return self.root
        return self.L.findmin()

    def findmax(self):
        if self.R is None:
            return self.root
        return self.R.findmax()

    def delete_max_element(self):
        if self.root is None:
            return
        if self.R is None:
            return self.L
        self.R = self.R.delete_max_element()
        return self

    def delete_element(self, value):
        if self.root is None:
            return
        if value < self.root:
            if self.L:
                self.L = self.L.delete_element(value)
        elif value > self.root:
            if self.R:
                self.R = self.R.delete_element(value)
        else:
            if self.L is None:
                return self.R
            if self.R is None:
                return self.L
            min = self.R.findmin()
            self.root = min
            self.R = self.R.delete_element(min)
        return self

    def less_than(self, value):
        if self.root is None:
            return BinarySearchTree()
        if self.root == value:
            return self.L if self.L else BinarySearchTree()
        if self.root > value:
            return self.L.less_than(value) if self.L else BinarySearchTree()
        if self.root < value:
            return BinarySearchTree(
                self.root,
                self.L,
                self.R.less_than(value) if self.R else BinarySearchTree(),
            )

    def greater_than(self, value):
        if self.root is None:
            return BinarySearchTree()
        if self.root == value:
            return self.R if self.R else BinarySearchTree()
        if self.root < value:
            return self.R.greater_than(value) if self.R else BinarySearchTree()
        return BinarySearchTree(
            self.root,
            self.L.greater_than(value) if self.L else BinarySearchTree(),
            self.R,
        )

    def add_new_node(self, value):
        l = self.less_than(value)
        r = self.greater_than(value)
        self.root = value
        self.L = l
        self.R = r
        return self

    def inorder(self):
        if self.root is None:
            return []
        return (
            (self.L.inorder() if self.L else [])
            + [self.root]
            + (self.R.inorder() if self.R else [])
        )
        # time complexity is O(n)
    
    def smallest_that(self, pred):
        if self.root is None:
            return None
        res = self.L.smallest_that(pred) if self.L else None
        if res is not None:
            return res
        if pred(self.root):
            return self.root
        return self.R.smallest_that(pred) if self.R else None
    
    def all_that(self, pred):
        # returns a binary search tree with all elements that satisfy the predicate
        if self.root is None:
            return BinarySearchTree()
        l = self.L.all_that(pred) if self.L else BinarySearchTree()
        r = self.R.all_that(pred) if self.R else BinarySearchTree()
        if pred(self.root):
            return BinarySearchTree(self.root, l, r)
        return l + r

    # Self Balanced trees:
    # Avoid falling back into a linear performance
    # ...
    # Example: AVL trees
    # definition: an AVL tree is a binary search tree in which the height of the two child subtrees of any node differ by at most one.
    # The level of unbalance never exceeds 1
    # BALANCE FACTOR/DEGREE = height of left subtree - height of right subtree
    # balance factor is either -1, 0, or 1
    # height of an AVL tree is O(log n)
    # insertion, deletion, search are O(log n)

    # Balancing a tree when balance degree exceeds 1
    # 1. Left rotation: when balance factors are -2, -1, 0
    # 2. Right rotation: when balance factors are 2, 1, 0
    # 3. Left-Right rotation
    # 4. Right-Left rotation
    # 5. Rebalancing the tree
    
def is_even(n):
    return n % 2 == 0

if __name__ == "__main__":
    tree = BinarySearchTree()
    for e in [4, 2, 8, 5, 7, 1]:
        tree.insert(e)

    print("smallest that", tree.smallest_that(is_even))
    print("all that", tree.all_that(is_even))


# Conclusion:
# 1. Main operations: contains, insert, delete are proportional to the height of the tree
# 2. In the best case, height is proportional to log n, and time complexity is O(log n)
# 3. In the worst case, height is proportional to n, and time complexity is O(n) - like in a deteriorated tree
# 4. In average case, height is proportional to log n, and time complexity is O(log n)
