import weighted_graph as wg
import sys

# Data from FRANCE.MAP
data = """
Calais        -200    1200
Nancy         534
Paris         297
Caen          450

Caen          -600    730
Calais        450
Paris         241
Rennes        176

Brest         -1400   560
Rennes        244

Rennes        -910    480
Caen          176
Paris         348
Nantes        107
Brest         244

Paris         -190    640
Calais        297
Nancy         372
Dijon         313
Limoges       396
Rennes        348
Caen          241

Nancy         510     600
Strasbourg    145
Dijon         201
Paris         372
Calais        534

Strasbourg    800     600
Dijon         335
Nancy         145

Nantes        -910    220
Rennes        107
Limoges       329
Bordeaux      329

Dijon         315     220
Nancy         201
Strasbourg    335
Lyon          192
Paris         313

Limoges       -380    -190
Paris         396
Lyon          389
Toulouse      313
Bordeaux      220
Nantes        329

Lyon          290     -215
Dijon         192
Grenoble      104
Avignon       216
Limoges       389

Grenoble      470     -370
Avignon       227
Lyon          104

Bordeaux      -740    -470
Nantes        329
Limoges       220
Toulouse      259

Toulouse      -350    -830
Limoges       313
Montpellier   240
Bordeaux      259

Montpellier   120     -830
Avignon       91
Toulouse      240

Avignon       310     -730
Lyon          216
Grenoble      227
Marseille     99
Montpellier   91

Marseille     430     -910
Nice          158
Avignon       99

Nice          810     -790
Marseille     158
Moulins       750

Moulins       0       0
Nice          750
"""

# Make a weighted graph of the map
graph = wg.WeightedGraph()

cities = [
    "Calais",
    "Nancy",
    "Paris",
    "Caen",
    "Rennes",
    "Brest",
    "Nantes",
    "Dijon",
    "Limoges",
    "Lyon",
    "Strasbourg",
    "Bordeaux",
    "Toulouse",
    "Montpellier",
    "Avignon",
    "Marseille",
    "Nice",
    "Moulins",
    "Grenoble",
]

# Add the cities as vertices
for city in cities:
    graph.add_vertex(city)

# Add the distances as edges between the cities (bidirectional) and the coordinates of the cities
data = data.strip().split("\n\n")
# Parsing and adding vertices and edges from the data
for entry in data:
    lines = entry.strip().split("\n")
    parts = lines[0].split()
    city = parts[0]
    x = int(parts[1])
    y = int(parts[2])
    graph.add_vertex(city, x, y)

    for line in lines[1:]:
        parts = line.split()
        neighbor = parts[0]
        distance = int(parts[1])
        graph.add_edge(city, neighbor, distance)

# ------------------------------------------------------------------------------------------------------------------
# The graph looks like this:
# Dijon -> (315, 220, [('Nancy', 201), ('Strasbourg', 335), ('Lyon', 192), ('Paris', 313)])
# Nice -> (810, -790, [('Marseille', 158), ('Moulins', 750)])
# Grenoble -> (470, -370, [('Avignon', 227), ('Lyon', 104)])
# Calais -> (-200, 1200, [('Nancy', 534), ('Paris', 297), ('Caen', 450)])
# Bordeaux -> (-740, -470, [('Nantes', 329), ('Limoges', 220), ('Toulouse', 259)])
# Limoges -> (-380, -190, [('Paris', 396), ('Lyon', 389), ('Toulouse', 313), ('Bordeaux', 220), ('Nantes', 329)])
# Toulouse -> (-350, -830, [('Limoges', 313), ('Montpellier', 240), ('Bordeaux', 259)])
# Montpellier -> (120, -830, [('Avignon', 91), ('Toulouse', 240)])
# Strasbourg -> (800, 600, [('Dijon', 335), ('Nancy', 145)])
# Nancy -> (510, 600, [('Strasbourg', 145), ('Dijon', 201), ('Paris', 372), ('Calais', 534)])
# Paris -> (-190, 640, [('Calais', 297), ('Nancy', 372), ('Dijon', 313), ('Limoges', 396), ('Rennes', 348), ('Caen', 241)])
# Avignon -> (310, -730, [('Lyon', 216), ('Grenoble', 227), ('Marseille', 99), ('Montpellier', 91)])
# Lyon -> (290, -215, [('Dijon', 192), ('Grenoble', 104), ('Avignon', 216), ('Limoges', 389)])
# Caen -> (-600, 730, [('Calais', 450), ('Paris', 241), ('Rennes', 176)])
# Rennes -> (-910, 480, [('Caen', 176), ('Paris', 348), ('Nantes', 107), ('Brest', 244)])
# Moulins -> (0, 0, [('Nice', 750)])
# Nantes -> (-910, 220, [('Rennes', 107), ('Limoges', 329), ('Bordeaux', 329)])
# Brest -> (-1400, 560, [('Rennes', 244)])
# Marseille -> (430, -910, [('Nice', 158), ('Avignon', 99)])
# ------------------------------------------------------------------------------------------------------------------


# Define the A* algorithm function
def a_star(graph, start, goal):
    visited = set()
    distance = {vertex: float("inf") for vertex in graph.vertices}
    distance[start] = 0

    estimated_distance = {vertex: float("inf") for vertex in graph.vertices}
    estimated_distance[start] = heuristic(start, goal)

    previous = {vertex: None for vertex in graph.vertices}
    queue = [(estimated_distance[start], start)]

    while queue:
        current_distance, current_node = min(queue)
        queue.remove((current_distance, current_node))

        if current_node == goal:
            break

        visited.add(current_node)

        for neighbor, edge_distance in graph.get_neighbors(current_node):
            tentative_distance = distance[current_node] + edge_distance
            if tentative_distance < distance[neighbor]:
                distance[neighbor] = tentative_distance
                estimated_distance[neighbor] = tentative_distance + heuristic(
                    neighbor, goal
                )
                previous[neighbor] = current_node
                queue.append((estimated_distance[neighbor], neighbor))

    if previous[goal] is None:
        return None

    path = []
    current_node = goal
    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]
    path.reverse()

    return path


def heuristic(node1, node2):
    x1, y1 = graph.get_coordinates(node1)
    x2, y2 = graph.get_coordinates(node2)
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# Check if the city names are provided as command line arguments
if len(sys.argv) == 3:
    start_city = sys.argv[1]
    goal_city = sys.argv[2]
else:
    # Ask for the city names
    start_city = input("Enter the name of the start city: ")
    goal_city = input("Enter the name of the goal city: ")

# Check if the start and goal cities are valid
if start_city not in graph.vertices or goal_city not in graph.vertices:
    print("Error: Unknown city name")
    sys.exit(1)

# Run the A* algorithm
path = a_star(graph, start_city, goal_city)

# Check if a path was found
if path is None:
    print("No path found")
    sys.exit(3)

# Print the shortest path
total_distance = 0
for i in range(len(path)):
    city = path[i]
    distance = graph.get_edge_distance(path[i - 1], city) if i > 0 else 0
    total_distance += distance
    print(f"{city} : ({total_distance} km)")

# Print the total distance
print(f"Total distance: {total_distance} km")

# Return success
sys.exit(0)
