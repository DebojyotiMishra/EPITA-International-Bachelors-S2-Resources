class AVLTree:
    def __init__(self, root=None, L=None, R=None, level=0):
        if root is None:
            self.clear()
        elif L is None:
            self.root = root
            self.L = AVLTree()
            self.R = AVLTree()
            self.level = 0
        else:
            self.root = root
            self.L = L
            self.R = R
            self.level = level

    def __add__(self, other):
        return AVLTree(self.root, self.L, other)
    
    def clear(self):
        self.root = None
        self.L = self
        self.R = self
        self.level = 0

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
    
    def update_height(self):
        self.level = 1 + max(self.L.height, self.R.height)
        
    def getBalance(self):
        if self.root is None:
            return 0
        return self.L.height() - self.R.height()

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
            return f"<{self.root} (Level: {self.level})>"
        if self.L is None:
            return f"<{self.root} (Level: {self.level}), {self.R}>"
        if self.R is None:
            return f"<{self.root} (Level: {self.level}), {self.L}>"
        return f"<{self.root} (Level: {self.level}), {self.L}, {self.R}>"

    def display(self, depth=0):
        if self.root is None:
            return
        if self.R:
            self.R.display(depth + 1)
        print("  " * 2 * depth + f"{self.root}")
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
                self.L = AVLTree(value)
            else:
                self.L.insert(value)
        if value > self.root:
            if self.R is None:
                self.R = AVLTree(value)
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
            return AVLTree()
        if self.root == value:
            return self.L if self.L else AVLTree()
        if self.root > value:
            return self.L.less_than(value) if self.L else AVLTree()
        if self.root < value:
            return AVLTree(
                self.root,
                self.L,
                self.R.less_than(value) if self.R else AVLTree(),
            )

    def greater_than(self, value):
        if self.root is None:
            return AVLTree()
        if self.root == value:
            return self.R if self.R else AVLTree()
        if self.root < value:
            return self.R.greater_than(value) if self.R else AVLTree()
        return AVLTree(
            self.root,
            self.L.greater_than(value) if self.L else AVLTree(),
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
        
    def rotate_right(self):
        new_root = self.L
        self.L = new_root.R
        new_root.R = self
        self.update_height()
        new_root.update_height()
        return new_root
    
    def rotate_left(self):
        new_root = self.R
        self.R = new_root.L
        new_root.L = self
        self.update_height()
        new_root.update_height()
        return new_root
    
    def rebalance(self):
        self.update_height()
        if self.getBalance() > 1:
            if self.L.getBalance() < 0:
                self.L = self.L.rotate_left()
            return self.rotate_right()
        if self.getBalance() < -1:
            if self.R.getBalance() > 0:
                self.R = self.R.rotate_right()
            return self.rotate_left()
        return self
    
    def next(self):
        self.root = None
        self.level = 0
        
    def set(self, value):
        self.root = value.root
        self.L = value.L
        self.R = value.R
        self.level = value.level
        
    def delete(self, value):
        if self.root is None:
            return
        if value < self.root:
            self.L = self.L.delete(value)
        elif value > self.root:
            self.R = self.R.delete(value)
        else:
            if self.L.root is None:
                return self.R
            if self.R.root is None:
                return self.L
            min = self.R.findmin()
            self.root = min
            self.R = self.R.delete(min)
        return self.rebalance()
        


if __name__ == '__main__':
    import random
    tree = AVLTree()
    
    for i in range(10):
        tree.insert(i)
    
    while tree.root is not None:
        n = random.randint(10)
        print(f"Deleting {n}")
        tree = tree.delete(n)
        tree.display()

