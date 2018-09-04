from search import *
import math
import heapq

class RoutingGraph(Graph):
    """a subclass of Graph which convers a map string ot a form of graph"""
    
    def __init__(self, map_str):
        """initialises an routing graph."""
        self.map_str = map_str
        self.map_graph = []
        self.starting_list = []
        self.goal_nodes = []
        
        self.getMap(self.map_str)
        
    def getMap(self, map_str):
        """convert a map string to a form(row, column)"""
        
        #convert map string to a list with only useful information:
        #divide map string into a list with row of graph
        filter_map = (map_str.strip()).split('\n')
        
        #divide each string in row's element as column of graph
        for element in filter_map:
            self.map_graph.append(list(element.strip()))
        
        for i in range(len(self.map_graph)):
            for j in range(len(self.map_graph[i])):
                r, c = i, j
                if self.map_graph[r][c] == 'S':
                    self.starting_list.append((r, c, math.inf))
                elif self.map_graph[r][c].isdigit():
                    self.starting_list.append((r, c, int(self.map_graph[r][c])))
                elif self.map_graph[r][c] == 'G':
                    self.goal_nodes.append((r, c))
                
        #print("starting nodes : {}\ngoal node : {}\n".
              #format(self.starting_list, self.goal_nodes))
            
    def starting_nodes(self):
        """Returns (via a generator) a sequence of starting nodes."""
        for starting_node in self.starting_list:
            yield starting_node

    def is_goal(self, node):
        """Returns true if the given node is a goal node."""
        return (node[0], node[1]) in self.goal_nodes        
 
    def outgoing_arcs(self, tail):
        """Given a node it returns a sequence of arcs (Arc objects)
        which correspond to the actions that can be taken in that
        state (node)."""
        available_dir = []
        directions = [('N' , -1, 0),
                      ('NE', -1, 1),
                      ('E' ,  0, 1),
                      ('SE',  1, 1),
                      ('S' ,  1, 0),
                      ('SW',  1, -1),
                      ('W' ,  0, -1),
                      ('NW', -1, -1)]
        
        available_dir = []
            
        for direction in directions:
            dir_r = tail[0] + direction[1]
            dir_c = tail[1] + direction[2]
            
            if self.map_graph[dir_r][dir_c] not in ['X', '+', '-', '|'] and tail[2] > 0:
                head = (dir_r, dir_c, tail[2] - 1)
                yield Arc(tail, head, direction[0], 2)
        
        if self.map_graph[tail[0]][tail[1]] == 'F' and tail[2] < 9:
            head = (tail[0], tail[1], 9)
            yield Arc(tail, head, 'Fuel up', 5)
                
            
    def estimated_cost_to_goal(self, node):
        """Return the estimated cost to a goal node from the given
        state. This function is usually implemented when there is a
        single goal state. The function is used as a heuristic in
        search. The implementation should make sure that the heuristic
        meets the required criteria for heuristics."""
        pace = max(abs(self.goal_nodes[0][0] - node[0]), abs(self.goal_nodes[0][1] - node[1]))
        return pace * 2
       
        
class AStarFrontier(Frontier):
    """return a paht from starting node to goal with lowest cost"""
    
    def __init__(self, map_graph):
        """The constructor takes no argument. It initialises the
                container to an empty list."""
        self.container = []
        self.map_graph = map_graph
        self.visited = []

    def add(self, path):     
        if path[-1].head not in self.visited:
            self.container.append(path)
        
    def __iter__(self):
        while self.container:
            shortest_cost = 9999
            
            path_index = heapq.nsmallest(1, 
                                         range(len(self.container)), 
                                         key = lambda path : sum(arc.cost for arc in self.container[path])
                                         + self.map_graph.estimated_cost_to_goal(self.container[path][-1].head))
            result = self.container[path_index[0]]

            #introductions for sentenses above
            '''for i in range(len(self.container)):
                arc_cost = sum(arc.cost for arc in self.container[i])
                #print('path : {}'.format(self.container[i]))
                heuristics_cost = self.map_graph.estimated_cost_to_goal(self.container[i][-1].head)
                #print("heuristics cost : {}".format(heuristics_cost))
                total_cost = heuristics_cost + arc_cost
                #print("total cost : {}".format(total_cost))
                    
                if total_cost < shortest_cost:
                    shortest_cost = total_cost
                    
                    result = self.container[i]
                    #print(result)
                    #result = heapq.nsmallest(1, self.container, key = lambda path : sum(arc.cost for arc in path) + heuristics_cost)
            '''
                
            self.container.remove(result)
            
            if result[-1].head not in self.visited:
                #print(self.visited)
                self.visited.append(result[-1].head)
                yield result


def print_map(map_graph, frontier, solution):
    """Given a path (a sequence of Arc objects), prints the map graph within 
    standard form."""
    path_map = map_graph.map_graph
    
    if solution:
        for selected_path in solution:
            r, c = selected_path.head[0], selected_path.head[1]
            if path_map[r][c] not in ['S', 'G']:
                path_map[r][c] = '*'
    
    for available_path in frontier.visited:
        r, c = available_path[0], available_path[1]
        if path_map[r][c] not in ['S', 'G', '*']:
            path_map[r][c] = '.'
            
    for map_line in path_map:
        map_line = ''.join(map_line)
        print(map_line)
        
        
   
map_str = """\
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
"""

map_graph = RoutingGraph(map_str)
frontier = AStarFrontier(map_graph)
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)