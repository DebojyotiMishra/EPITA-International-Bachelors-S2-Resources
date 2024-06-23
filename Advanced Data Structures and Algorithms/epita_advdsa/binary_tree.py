class BinaryTree:
    def __init__(self, root=None, L=None, R=None):
        self.root = root
        self.L = L
        self.R = R

    def isempty(self):
        return self.root is None

    def contains(self, value):
        if self.root is None:
            return False
        if self.root == value:
            return True
        if self.L:
            if self.L.contains(value):
                return True
        if self.R:
            if self.R.contains(value):
                return True
        return False
        # Complexity: O(n)

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


if __name__ == "__main__":
    root = BinaryTree(1)
    root.L = BinaryTree(2)
    root.R = BinaryTree(3)
    root.L.L = BinaryTree(4)
    root.L.R = BinaryTree(5)
    root.R.L = BinaryTree(6)
    root.R.R = BinaryTree(7)
    root.L.L.L = BinaryTree(8)
    root.L.L.R = BinaryTree(9)
    root.L.R.L = BinaryTree(10)
    root.L.R.R = BinaryTree(11)
    root.R.L.L = BinaryTree(12)
    root.R.L.R = BinaryTree(13)
    root.R.R.L = BinaryTree(14)
    root.R.R.R = BinaryTree(15)
    print(root.contains(15))
    print(root.contains(16))
    print(root.contains(1))
    print(root.contains(0))
    print(root.contains(2))
    print(root.contains(3))
    print(root.contains(4))
    print(root.contains(5))
    print(root.contains(6))
    print(root.contains(7))
    print(root.contains(8))
    print(root.contains(9))
    print(root.contains(10))
    print(root.contains(11))
    print(root.contains(12))
    print(root.contains(13))
    print(root.contains(14))
    print(root.contains(15))
    print(root.isempty())
    print(root.L.isempty())
    print(root.L.L.isempty())
    print(root.L.L.L.isempty())
    print(root.L.L.R.isempty())
    print(root.L.R.isempty())
    print(root.L.R.L.isempty())
    print(root.L.R.R.isempty())
    print(root.R.isempty())
    print(root.R.L.isempty())
    print(root.R.L.L.isempty())
    print(root.R.L.R.isempty())
    print(root.R.R.isempty())
    print(root.R.R.L.isempty())
    print(root.R.R.R.isempty())
    
    print(root)
