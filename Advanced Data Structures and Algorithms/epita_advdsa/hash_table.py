# ---------- Hash Table using Linear Probing ----------
# Description: This program implements a hash table using linear probing.

# structure: List of (key, value) pairs
# Number of pairs: n
# Capacity of the hash table: m (length of the list)

DELETED = object()


class HashTable:
    DELETED = DELETED

    def __init__(self, capacity=10):
        self.size = 0
        self.capacity = capacity
        self.table = [None] * capacity
        self.deleted = 0
        self.max_load_factor = 0.5
        self.keys_list = []
        self.values_list = []

    def __str__(self):
        return f"HashTable<{self.capacity}, {self.size}, {self.table}>"

    def load_factor(self):
        return (self.size + self.deleted) / self.capacity

    def keys(self):
        return [pair[0] for pair in self.table if pair is not None]

    def values(self):
        return [pair[1] for pair in self.table if pair is not None]

    def get(self, key):
        index = hash(key) % self.capacity
        while True:
            if self.table[index] is None:
                return None
            if self.table[index] is DELETED or self.table[index][0] != key:
                index = (index + 1) % self.capacity
            if self.table[index] is not None and self.table[index][0] == key:
                return self.table[index][1]

    def set(self, key, value):
        if self.load_factor() > self.max_load_factor:
            self.grow()

        index = hash(key) % self.capacity
        while True:
            if self.table[index] is None or self.table[index] is DELETED:
                self.table[index] = (key, value)
                self.size += 1
                self.keys_list.append(key)
                self.values_list.append(value)
                return
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                self.values_list[self.keys_list.index(key)] = value
                return
            index = (index + 1) % self.capacity

    def delete(self, key):
        index = hash(key) % self.capacity
        while True:
            if self.table[index] is None:
                return
            if self.table[index] is DELETED or self.table[index][0] != key:
                index = (index + 1) % self.capacity
            if self.table[index][0] == key:
                self.table[index] = DELETED
                self.size -= 1
                self.deleted += 1
                return
            if self.table[index][0] == key:
                self.table[index] = DELETED
                self.size -= 1
                self.deleted += 1
                key_index = self.keys_list.index(key)
                del self.keys_list[key_index]
                del self.values_list[key_index]
                return

    def grow(self, factor=2):
        old_capacity = self.capacity
        self.capacity *= factor
        old_table = self.table
        self.table = [None] * self.capacity

        for pair in old_table:
            if pair is not None and pair is not DELETED:
                key, value = pair
                index = hash(key) % self.capacity
                while self.table[index] is not None and self.table[index] is not DELETED:
                    index = (index + 1) % self.capacity
                self.table[index] = (key, value)

    def display(self):
        elements = [str(self.table[i]) for i in range(self.capacity) if self.table[i] and self.table[i] is not DELETED]
        print(f"HashTable[{', '.join(elements)}]")


if __name__ == "__main__":
    ht = HashTable(10000)

    for i in range(100):
        ht.set(i, i)
    
    ht.display()
