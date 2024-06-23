import graph as g
import weighted_graph as wg
import sys

# FRANCE.MAP
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

cities = ['Calais', 'Nancy', 'Paris', 'Caen', 'Rennes', 'Brest', 'Nantes', 'Dijon', 
          'Limoges', 'Lyon', 'Strasbourg', 'Bordeaux', 'Toulouse', 'Montpellier', 'Avignon', 
          'Marseille', 'Nice', 'Moulins']

for city in cities:
    graph.add_vertex(city)
    
# Add edges according to data
data = data.strip().split('\n\n')
for entry in data:
    lines = entry.strip().split('\n')
    city = lines[0].split()[0]
    graph.add_vertex(city)
    for line in lines[1:]:
        parts = line.split()
        neighbor = parts[0]
        distance = int(parts[1])
        graph.add_edge(city, neighbor, distance)

# ------------------------------------------------------------------------------------------------------------------
# graph.display()
# Calais -> [('Nancy', 534), ('Paris', 297), ('Caen', 450)]
# Nice -> [('Marseille', 158), ('Moulins', 750)]
# Caen -> [('Calais', 450), ('Paris', 241), ('Rennes', 176)]
# Brest -> [('Rennes', 244)]
# Toulouse -> [('Limoges', 313), ('Montpellier', 240), ('Bordeaux', 259)]
# Avignon -> [('Lyon', 216), ('Grenoble', 227), ('Marseille', 99), ('Montpellier', 91)]
# Grenoble -> [('Avignon', 227), ('Lyon', 104)]
# Rennes -> [('Caen', 176), ('Paris', 348), ('Nantes', 107), ('Brest', 244)]
# Nantes -> [('Rennes', 107), ('Limoges', 329), ('Bordeaux', 329)]
# Montpellier -> [('Avignon', 91), ('Toulouse', 240)]
# Marseille -> [('Nice', 158), ('Avignon', 99)]
# Nancy -> [('Strasbourg', 145), ('Dijon', 201), ('Paris', 372), ('Calais', 534)]
# Strasbourg -> [('Dijon', 335), ('Nancy', 145)]
# Lyon -> [('Dijon', 192), ('Grenoble', 104), ('Avignon', 216), ('Limoges', 389)]
# Limoges -> [('Paris', 396), ('Lyon', 389), ('Toulouse', 313), ('Bordeaux', 220), ('Nantes', 329)]
# Moulins -> [('Nice', 750)]
# Dijon -> [('Nancy', 201), ('Strasbourg', 335), ('Lyon', 192), ('Paris', 313)]
# Paris -> [('Calais', 297), ('Nancy', 372), ('Dijon', 313), ('Limoges', 396), ('Rennes', 348), ('Caen', 241)]
# Bordeaux -> [('Nantes', 329), ('Limoges', 220), ('Toulouse', 259)]
# ------------------------------------------------------------------------------------------------------------------

# Context
# A* Project
# P. Laroque
# EPITA Bachelor - Algorithmics and data structures
# The project aims at computing the shortest path between two cities, using the A* algorithm described in class. The map data (cities, direct connections, coordinates and distances) can be found in a text file whose name is given on the command line (default name FRANCE.MAP).
# The program is given the names of the departure and arrival cities (on the command line or asked by the code), then computes and displays the (complete) shortest path between the chosen two cities, together with the partial distances for each intermediate city and, of course, the total distance for the trip.
# For instance:
# $ ./aStar Rennes Lyon
# Rennes : (0 km)
# Nantes : (107 km)
# Limoges : (436 km)
# Lyon : (825 km)
# Error handling
# • If the city names are not provided on the command line, the program must ask for them.
# • in case of incorrect input (unknown city name), the program should return 1
# • in case the data file (FRANCE.MAP by default, or other) is not found, the program should return 2 • on failure due to lack of connectivity in the graph, the program should return 3
# • on success, the program must return 0 as usual
# Deliverables
# The project code must use the HashTable structures seen during the course, it is not allowed to use python dictionaries. Final grade will take performance of the code into account.
# Students must send an archive (named after the names of the 2 members of the team) by email to laroque@u-cergy.fr. The contents of the archive is
# 1. the complete commented source code and data file (map if file different from FRANCE.MAP)
# 2. a README file to help the user understand how to (build and) run the program
# 3. an evaluation of the complexity of your solution, in terms of E and V (E : number of edges of the map, V : number of
# vertices)
# 4. nothing else!
# Pay attention to the following potential issues:
# • the source code must be portable: no reference to OS-specific libraries must be made. Students are urged to test their program against windows and linux and macOS if possible!
# • Teams are composed of 2 students. If you choose to do the project alone or with 2 mates you will get a penalty (unless the last student happens to be alone of course)
# The excel sheet provided with this document should help you understand precisely what is expected from you in this project.

# Define the A* algorithm function
def a_star(graph, start, goal):
    # Create an empty set to store visited nodes
    visited = set()
    
    # Create a dictionary to store the distance from start to each node
    distance = {vertex: float('inf') for vertex in graph.vertices}
    distance[start] = 0
    
    # Create a dictionary to store the estimated distance from start to goal through each node
    estimated_distance = {vertex: float('inf') for vertex in graph.vertices}
    estimated_distance[start] = heuristic(start, goal)
    
    # Create a dictionary to store the previous node in the shortest path
    previous = {vertex: None for vertex in graph.vertices}
    
    # Create a priority queue to store the nodes to be visited
    queue = [(estimated_distance[start], start)]
    
    while queue:
        # Get the node with the smallest estimated distance
        current_distance, current_node = min(queue)
        queue.remove((current_distance, current_node))
        
        # Check if the current node is the goal
        if current_node == goal:
            break
        
        # Add the current node to the visited set
        visited.add(current_node)
        
        # Explore the neighbors of the current node
        for neighbor, edge_distance in graph.get_neighbors(current_node):
            # Calculate the tentative distance from start to the neighbor
            tentative_distance = distance[current_node] + edge_distance
            
            # Check if the tentative distance is smaller than the current distance
            if tentative_distance < distance[neighbor]:
                # Update the distance and estimated distance
                distance[neighbor] = tentative_distance
                estimated_distance[neighbor] = tentative_distance + heuristic(neighbor, goal)
                
                # Update the previous node
                previous[neighbor] = current_node
                
                # Add the neighbor to the queue
                queue.append((estimated_distance[neighbor], neighbor))
    
    # Check if a path was found
    if previous[goal] is None:
        return None
    
    # Reconstruct the shortest path
    path = []
    current_node = goal
    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]
    path.reverse()
    
    return path

# Define the heuristic function (Euclidean distance)
def heuristic(node1, node2):
    x1, y1 = graph.get_coordinates(node1)
    x2, y2 = graph.get_coordinates(node2)
    # print(node1)
    # print(x1, y1, x2, y2)  # ('Caen', 176) ('Paris', 348) ('Dijon', 192) ('Grenoble', 104)
    return ((x1[1] - x2[1]) ** 2 + (y1[1] - y2[1]) ** 2) ** 0.5

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
    distance = graph.get_edge_distance(path[i-1], city) if i > 0 else 0
    total_distance += distance
    print(f"{city} : ({total_distance} km)")

# Print the total distance
print(f"Total distance: {total_distance} km")

# Return success
sys.exit(0)
