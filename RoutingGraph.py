from search import *
import math

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
            
    def starting_nodes(self):
        """Returns (via a generator) a sequence of starting nodes."""
        for starting_node in self.starting_list:
            yield starting_node

    def is_goal(self, node):
        """Returns true if the given node is a goal node."""
        return (node[0], node[1]) == self.goal_nodes[0]        
 
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
        
        raise NotImplementedError 
   
    
map_str = """\
+-------+
|  9  XG|
|X XXX  |
| S  0F |
+-------+
"""

graph = RoutingGraph(map_str)

print("Starting nodes:", sorted(graph.starting_nodes()))
print("Outgoing arcs (available actions) at starting states:")
for s in sorted(graph.starting_nodes()):
    print(s)
    for arc in graph.outgoing_arcs(s):
        print ("  " + str(arc))

node = (1,1,5)
print("\nIs {} goal?".format(node), graph.is_goal(node))
print("Outgoing arcs (available actions) at {}:".format(node))
for arc in graph.outgoing_arcs(node):
    print ("  " + str(arc))

node = (1,7,2)
print("\nIs {} goal?".format(node), graph.is_goal(node))
print("Outgoing arcs (available actions) at {}:".format(node))
for arc in graph.outgoing_arcs(node):
    print ("  " + str(arc))

node = (3,6,5)
print("\nIs {} goal?".format(node), graph.is_goal(node))
print("Outgoing arcs (available actions) at {}:".format(node))
for arc in graph.outgoing_arcs(node):
    print ("  " + str(arc))

node = (3,6,9)
print("\nIs {} goal?".format(node), graph.is_goal(node))
print("Outgoing arcs (available actions) at {}:".format(node))
for arc in graph.outgoing_arcs(node):
    print ("  " + str(arc))
        
print('------------------------------')

map_str = """\
+--+
|GS|
+--+
"""

graph = RoutingGraph(map_str)

print("Starting nodes:", sorted(graph.starting_nodes()))
print("Outgoing arcs (available actions) at the start:")
for start in graph.starting_nodes():
    for arc in graph.outgoing_arcs(start):
        print ("  " + str(arc))



node = (1,1,1)
print("\nIs {} goal?".format(node), graph.is_goal(node))
print("Outgoing arcs (available actions) at {}:".format(node))
for arc in graph.outgoing_arcs(node):
    print ("  " + str(arc))

print('------------------------------')
    
map_str = """\
+------+
|S    S|
|  GXXX|
|S     |
+------+
"""

graph = RoutingGraph(map_str)
print("Starting nodes:", sorted(graph.starting_nodes()))

print('------------------------------')
map_str = """\
+-------+
|     XG|
|X XXX  |
| S     |
+-------+
"""

map_graph = RoutingGraph(map_str)
print("Starting nodes:", sorted(graph.starting_nodes()))
print("Outgoing arcs (available actions) at the start:")
for start in graph.starting_nodes():
    for arc in graph.outgoing_arcs(start):
        print ("  " + str(arc))