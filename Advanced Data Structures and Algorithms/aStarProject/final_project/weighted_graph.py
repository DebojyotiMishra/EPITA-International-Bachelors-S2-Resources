from hash_table import HashTable

class WeightedGraph:
    def __init__(self, capacity=100):
        self.ht = HashTable(capacity)

    def add_vertex(self, name):
        self.ht.set(name, [])

    def add_edge(self, from_vertex, to_vertex, distance):
        if not self.ht.get(from_vertex):
            self.ht.set(from_vertex, [])
        if not self.ht.get(to_vertex):
            self.ht.set(to_vertex, [])
        self.ht.get(from_vertex).append((to_vertex, distance))

    def get_neighbors(self, vertex):
        if self.ht.contains(vertex):
            return self.ht.get(vertex)
        else:
            return []
    
    @property
    def vertices(self):
        return list(self.ht.keys())
    
    def get_coordinates(self, node):
        vertex = self.ht.get(node)
        if vertex is not None and len(vertex) >= 2:
            return vertex[0], vertex[1]
        else:
            raise ValueError(f"Node {node} not found in graph or does not have valid coordinates")
    
    def get_edge_distance(self, from_vertex, to_vertex):
        neighbors = self.ht.get(from_vertex)
        for neighbor in neighbors:
            if neighbor[0] == to_vertex:
                return neighbor[1]
        return None
    
    def display(self):
        for key in self.ht.keys():
            print(f"{key} -> {self.ht.get(key)}")