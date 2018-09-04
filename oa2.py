from search import *
from math import *
from heapq import *
from itertools import *


class RoutingGraph(Graph):
    def __init__(self, map_str):
        self.obstacles = []
        self.starting_list = []
        self.fuel = []
        self.goal_nodes = []  # only ever one goal node
        self.map = []

        self.locations = dict()
        self.edge_list = []
        self.read_map_str(map_str)

    def read_map_str(self, map_str):
        for row in map_str.split("\n"):
            row = row.strip(" ")
            if len(row) > 0:
                self.map.append(list(row))

        i = 0
        while i < len(self.map):
            j = 0
            while j < len(self.map[i]):
                entity = self.map[i][j]
                if entity == "X" or entity == "-" or entity == "+" or entity == "|":  # Obstacle/boundary nodes
                    self.obstacles.append((i, j))
                elif entity == "F":  # Fuel Node
                    self.fuel.append((i, j))
                elif entity == "G":  # Goal Node
                    self.goal_nodes.append((i, j))

                # Starting Nodes
                elif entity == "S":
                    self.starting_list.append((i, j, inf))
                elif entity.isdigit():
                    self.starting_list.append((i, j, int(entity)))

                j += 1
            i += 1
        # self.print_properties()
    
    def starting_nodes(self):
        """Returns (via a generator) a sequence of starting nodes."""
        for starting_node in self.starting_list:
            yield starting_node

    def is_goal(self, node):
        """Returns true if the given node is a goal node."""
        return (node[0], node[1]) in self.goal_nodes

    @staticmethod
    def euclidean_distance(p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    @staticmethod
    def manhattan_distance(p1, p2):
        D = 2
        D2 = 2
        dx = abs(p1[0] - p2[0])
        dy = abs(p1[1] - p2[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def estimated_cost_to_goal(self, node):
        # return 0
        return self.manhattan_distance(node, self.goal_nodes[0])

    def outgoing_arcs(self, node):
        """Returns a sequence of Arc objects corresponding to all the
        edges in which the given node is the tail node. The label is
        automatically generated."""
        directions = [('N', -1, 0),
                      ('NE', -1, 1),
                      ('E', 0, 1),
                      ('SE', 1, 1),
                      ('S', 1, 0),
                      ('SW', 1, -1),
                      ('W', 0, -1),
                      ('NW', -1, -1)]
        for edge in directions:
            dir_label, dir_x, dir_y = edge
            next_x = node[0] + dir_x
            next_y = node[1] + dir_y
            fuel_left = node[2]

            if fuel_left != 0 and (next_x, next_y) not in self.obstacles:
                next_node = (next_x, next_y, fuel_left - 1)
                yield Arc(node, next_node, dir_label, 2)

        if (node[0], node[1]) in self.fuel and node[2] < 9:
            yield Arc(node, (node[0], node[1], 9), "Fuel up", 5)

    def print_properties(self):
        print("Obstacles - " + str(self.obstacles))
        print("Starting nodes - " + str(self.starting_list))
        print("Fuel - " + str(self.fuel))
        print("Goal nodes - " + str(self.goal_nodes))
        print("---------------")


class AStarFrontier(Frontier):

    def __init__(self, map_graph):
        self.container = []
        self.map_graph = map_graph
        self.start_node = list(map_graph.starting_nodes())
        self.visited = dict()  # Key = (x,y), value = fuel amount
        self.count = count()

    def add(self, path):
        cost = 0
        for arc in path:
            cost += arc.cost
        coord = (path[-1].head[0], path[-1].head[1])
        fuel_amount = path[-1].head[2]
        if coord not in self.visited or fuel_amount > self.visited[coord]:
            cost += self.map_graph.estimated_cost_to_goal(path[-1].head)
            heappush(self.container, (cost, next(self.count), path))

    def __iter__(self):
        while self.container:
            cost, _, path = heappop(self.container)
            coord = (path[-1].head[0], path[-1].head[1])
            fuel_amount = path[-1].head[2]
            if coord not in self.visited or fuel_amount > self.visited[coord]:
                print(self.visited)
                self.visited[coord] = fuel_amount
                yield path


def print_map(map_graph, frontier, solution):
    for node in frontier.visited:
        #print(frontier.visited)
        visit_pt = map_graph.map[node[0]][node[1]]
        if visit_pt not in ['S', 'G']:
            map_graph.map[node[0]][node[1]] = "."

    if solution is not None:
        for arc in solution:
            if arc.tail is not None:
                point = (arc.tail[0], arc.tail[1])
                visit_pt = map_graph.map[point[0]][point[1]]
                if visit_pt not in ['S', 'G']:
                    map_graph.map[point[0]][point[1]] = "*"

    for row in map_graph.map:
        line = ""
        for col in row:
            line += col
        print(line)
        
'''map_str = """\
+-------+
|     XG|
|X XXX  |
| S     |
+-------+
"""
map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('----------------------------')

map_str = """\
+--+
|GS|
+--+
"""
map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('----------------------------')

map_str = """\
+----+
|    |
| SX |
| X G|
+----+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('----------------------------')

map_str = """\
+------------+
|            |
|            |
|            |
|    S       |
|            |
|            |
| G          |
|            |
+------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('----------------------------')

map_str = """\
+------------+
|            |
|            |
|            |
|    S       |
|            |
|            |
| G          |
|            |
+------------+
"""

map_graph = RoutingGraph(map_str)
# changing the heuristic so the search behaves like LCFS
map_graph.estimated_cost_to_goal = lambda node: 0

frontier = AStarFrontier(map_graph)

solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('----------------------------')

map_str = """\
+---------------+
|    G          |
|XXXXXXXXXXXX   |
|           X   |
|  XXXXXX   X   |
|  X S  X   X   |
|  X        X   |
|  XXXXXXXXXX   |
|               |
+---------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('------------------------------')

map_str = """\
+------------+
|         X  |
| S       X G|
|         X  |
|         X  |
|         X  |
+------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('------------------------------')

map_str = """\
+---------+
|         |
|    G    |
|         |
+---------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('------------------------------')

map_str = """\
+-------------+
|         G   |
| S           |
|         S   |
+-------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)
'''
print('------------------------------')

map_str = """\
+------+
|      |
|S X   |
|XXXXX |
|G X   |
|      |
+------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)
'''
print('------------------------------')

map_str = """\
+-------------+
|             |
|             |
|     S       |
|             |
| G           |
+-------------+
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)

print('------------------------------')

map_str = """\
+-------------+
|             |
|  X          |
|  X S        |
|  XXXXXX     |
| G           |
+-------------+


map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)'''