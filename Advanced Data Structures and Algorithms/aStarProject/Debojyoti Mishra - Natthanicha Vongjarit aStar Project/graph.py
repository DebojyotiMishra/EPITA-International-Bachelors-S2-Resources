from hash_table import *

class Graph:
    def __init__(self, directional=False, capacity=100):
        self.directional = directional
        self.ht = HashTable(capacity)
        self.distances = {}  # Dictionary to store distances between vertices

    def __str__(self):
        return f"#Graph<{self.directional}_{self.capacity}>"

    def add_vertex(self, key):
        """
        Add a vertex to the graph.

        Args:
            key: The key of the vertex to be added.
        """
        self.ht.set(key, [])

    def add_edge(self, key1, key2):
        """
        Add an edge between two vertices in the graph.

        Args:
            key1: The key of the first vertex.
            key2: The key of the second vertex.
        """
        if not self.ht.get(key1):
            self.ht.set(key1, [])
        if not self.ht.get(key2):
            self.ht.set(key2, [])
        self.ht.get(key1).append(key2)
        self.ht.get(key2).append(key1)

    def set_distance(self, key1, key2, distance):
        """
        Set the distance between two vertices in the graph.

        Args:
            key1: The key of the first vertex.
            key2: The key of the second vertex.
            distance: The distance between the vertices.
        """
        if self.ht.get(key1) and key2 in self.ht.get(key1):
            self.distances[(key1, key2)] = distance
            self.distances[(key2, key1)] = distance

    def get_edge_distance(self, key1, key2):
        """
        Get the distance between two vertices in the graph.

        Args:
            key1: The key of the first vertex.
            key2: The key of the second vertex.

        Returns:
            The distance between the vertices, or None if no distance is set.
        """
        return self.distances.get((key1, key2))

    def display(self):
        """
        Display the graph by printing each vertex and its adjacent vertices.
        """
        for key in self.ht.keys():
            print(f"{key} -> {self.ht.get(key)}")

    def breadth_first_search(self, start):
        """
        Perform breadth-first search starting from a given vertex.

        Args:
            start: The key of the starting vertex.
        """
        queue = []
        visited = []
        queue.append(start)
        visited.append(start)
        while len(queue) > 0:
            m = queue.pop(0)
            print(m)
            for neighbor in self.ht.get(m):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.append(neighbor)

    def depth_first_search(self, start):
        """
        Perform depth-first search starting from a given vertex.

        Args:
            start: The key of the starting vertex.
        """
        stack = []
        visited = []
        stack.append(start)
        visited.append(start)
        while len(stack) > 0:
            m = stack.pop()
            print(m)
            for neighbor in self.ht.get(m):
                if neighbor not in visited:
                    stack.append(neighbor)
                    visited.append(neighbor)


if __name__ == "__main__":
    g = Graph()

    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("C", "D")
    g.add_edge("C", "B")
    g.display()
