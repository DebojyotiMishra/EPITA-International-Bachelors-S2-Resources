# A* Pathfinding Project

This project is an implementation of the A* pathfinding algorithm. It computes the shortest path between two cities using a weighted graph. The map data (cities, direct connections, coordinates, and distances) are provided in a text file.

## Files

- [`astar.py`](command:_github.copilot.openSymbolInFile?%5B%22astar.py%22%2C%22astar.py%22%5D "astar.py"): The main file that runs the A* algorithm.
- [`graph.py`](command:_github.copilot.openSymbolInFile?%5B%22graph.py%22%2C%22graph.py%22%5D "graph.py"): Contains the `Graph` class which is used to create a graph of the cities.
- [`weighted_graph.py`](command:_github.copilot.openSymbolInFile?%5B%22weighted_graph.py%22%2C%22weighted_graph.py%22%5D "weighted_graph.py"): Contains the `WeightedGraph` class which extends the `Graph` class to add weights to the edges.
- [`hash_table.py`](command:_github.copilot.openSymbolInFile?%5B%22hash_table.py%22%2C%22hash_table.py%22%5D "hash_table.py"): Contains the `HashTable` class which is used to store the graph data.

## Usage

To run the program, use the following command:

```sh
python astar.py [departure city] [arrival city]
```

If the city names are not provided on the command line, the program will ask for them.

## Error Handling

- If the city names are not provided on the command line, the program will ask for them.
- In case of incorrect input (unknown city name), the program will return 1.
- In case the data file (FRANCE.MAP by default, or other) is not found, the program will return 2.
- On failure due to lack of connectivity in the graph, the program will return 3.
- On success, the program will return 0 as usual.

## Example

```sh
python astar.py Rennes Lyon
```

Output:

```
Rennes : (0 km)
Nantes : (107 km)
Limoges : (436 km)
Lyon : (825 km)
```

## Complexity Evaluation

This section provides an analysis of the time and space complexity for the provided implementation of the A* search algorithm and the supporting hash table.

## Hash Table Operations

The hash table is implemented using linear probing. Here are the complexities for its operations:

- **Insertion (`set`)**:
  - Average case: $O(1)$ 
  - Worst case: $O(n)$ (when a resize is needed or many collisions occur)

- **Search (`get`)**:
  - Average case: $O(1)$
  - Worst case: $O(n)$ (in case of many collisions)

- **Deletion (`delete`)**:
  - Average case: $O(1)$
  - Worst case: $O(n)$ (in case of many collisions)

- **Resize (`grow`)**: $O(n)$ (because it rehashes all elements)

## A* Algorithm

The A* algorithm's complexity involves several key components:

1. **Initialization**:
   - Initializing `distance`, `estimated_distance`, `previous`, and `queue` data structures takes $O(V)$, where $V$ is the number of vertices.

2. **Priority Queue Operations**:
   - The `queue` is managed using a list with a `min` operation for extracting the current node, leading to $O(V^2)$ complexity due to finding the minimum element each time.

3. **Main Loop**:
   - Each node is processed once, resulting in $O(V)$ iterations.
   - For each node, all its neighbors are examined. In a dense graph, this is $O(V)$ per node, leading to $O(V^2)$ in total.

4. **Heuristic Function**:
   - The heuristic function is called for each node evaluation, contributing $O(1)$ each time.

### Overall Time Complexity

Combining these factors:

- **Initialization**: $O(V)$
- **Priority Queue Operations**: $O(V^2)$
- **Main Loop**: $O(V^2)$ (if dense)
- **Heuristic Evaluation**: $O(1)$ per call

Thus, the overall time complexity of the A* algorithm with the current implementation is $O(V^2)$.

### Space Complexity

The space complexity is determined by the storage required for the graph and auxiliary data structures:

1. **Graph Storage**:
   - The hash table stores vertices and their edges, leading to $O(V + E)$ space, where $E$ is the number of edges.

2. **Auxiliary Data Structures**:
   - `distance`, `estimated_distance`, `previous`: Each requires $O(V)$ space.
   - `queue`: At most $O(V)$ elements.

Thus, the overall space complexity is $O(V + E)$.

## Summary

- **Time Complexity**: $O(V^2)$ $\rightarrow$ Where $V$ is the number of vertices
- **Space Complexity**: $O(V + E)$ $\rightarrow$ Where $V$ is the number of vertices and $E$ is the number of edges
