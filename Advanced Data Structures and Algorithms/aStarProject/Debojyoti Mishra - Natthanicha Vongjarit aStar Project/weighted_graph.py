from hash_table import HashTable

class WeightedGraph:
    def __init__(self, capacity=100):
        """
        Initializes a weighted graph with a hash table as the underlying data structure.

        Args:
        - capacity: The initial capacity of the hash table (default: 100)
        """
        self.ht = HashTable(capacity)

    def add_vertex(self, name, x=None, y=None):
        """
        Adds a vertex to the graph with the given name and optional coordinates.

        Args:
        - name: The name of the vertex
        - x: The x-coordinate of the vertex (optional)
        - y: The y-coordinate of the vertex (optional)
        """
        self.ht.set(name, (x, y, []))

    def add_edge(self, from_vertex, to_vertex, distance):
        """
        Adds an edge between two vertices with the given distance.

        Args:
        - from_vertex: The name of the vertex the edge starts from
        - to_vertex: The name of the vertex the edge points to
        - distance: The distance between the two vertices
        """
        from_vertex_data = self.ht.get(from_vertex)
        if from_vertex_data is None:
            raise ValueError(f"Vertex {from_vertex} does not exist.")
        from_vertex_data[2].append((to_vertex, distance))
        self.ht.set(from_vertex, from_vertex_data)

        to_vertex_data = self.ht.get(to_vertex)
        if to_vertex_data is None:
            self.ht.set(to_vertex, (None, None, []))

    def get_neighbors(self, vertex):
        """
        Returns a list of neighboring vertices and their distances from the given vertex.

        Args:
        - vertex: The name of the vertex

        Returns:
        - A list of tuples, where each tuple contains the name of a neighboring vertex and its distance from the given vertex
        """
        vertex_data = self.ht.get(vertex)
        if vertex_data is None:
            return []
        return vertex_data[2]

    @property
    def vertices(self):
        """
        Returns a list of all vertices in the graph.

        Returns:
        - A list of vertex names
        """
        return list(self.ht.keys())

    def get_coordinates(self, node):
        """
        Returns the coordinates (x, y) of the given node.

        Args:
        - node: The name of the node

        Returns:
        - The coordinates (x, y) of the node

        Raises:
        - ValueError if the node is not found in the graph or does not have valid coordinates
        """
        vertex = self.ht.get(node)
        if (
            vertex is not None
            and len(vertex) >= 3
            and vertex[0] is not None
            and vertex[1] is not None
        ):
            return vertex[0], vertex[1]
        else:
            raise ValueError(
                f"Node {node} not found in graph or does not have valid coordinates"
            )

    def get_edge_distance(self, from_vertex, to_vertex):
        """
        Returns the distance between two vertices connected by an edge.

        Args:
        - from_vertex: The name of the vertex the edge starts from
        - to_vertex: The name of the vertex the edge points to

        Returns:
        - The distance between the two vertices, or None if there is no edge between them
        """
        neighbors = self.get_neighbors(from_vertex)
        for neighbor, distance in neighbors:
            if neighbor == to_vertex:
                return distance
        return None

    def display(self):
        """
        Displays the graph by printing each vertex and its outgoing edges.
        """
        for key in self.ht.keys():
            print(f"{key} -> {self.ht.get(key)[2]}")
