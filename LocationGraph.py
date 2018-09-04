from search import *
import math


class GetDis():
    """return the distance between nodes"""

    def __init__(self, p1, p2):
        """get two nodes"""
        self.p1 = p1
        self.p2 = p2

    def getdis(self):
        """return coordinates of two nodes"""
        x1, y1 = self.p1
        x2, y2 = self.p2

        distance = float(math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2)))
        return distance


class Bidirection():
    """return the full edges of bidirectional maps"""

    def __init__(self, edges):
        self.edges = edges

    def fullmap(self):
        """return full maps of all bidirectional edges"""
        full_map = [] #store bidirectional edges in a list

        for edge in self.edges:
            start, end = edge
            full_map.append((start, end))
            full_map.append((end, start))

        return set(full_map)


class LocationGraph(Graph):
    """return information of a set of nodes and the connectiong
    between them on a 2D plane"""

    def __init__(self, nodes, locations, edges, starting_list, goal_nodes):
        """Initialises an explicit graph.
                Keyword arguments:
                nodes -- a set of nodes
                locations -- location of each node in 2D plane
                edges -- a sequence of tuples in the form (tail, head, cost)
                starting_list -- the list of starting nodes (states)
                goal_node -- the set of goal nodes (states)
                """
                
        assert all(tail in nodes and head in nodes for tail, head, *_ in edges) \
            , "An edge must link two existing nodes!"
        assert all(node in nodes for node in starting_list), \
            "The starting_states must be in nodes."
        assert all(node in nodes for node in goal_nodes), \
            "The goal states must be in nodes."

        self.nodes = nodes
        self.locations = locations
        self.edges = Bidirection(edges).fullmap()
        self.starting_list = starting_list
        self.goal_nodes = goal_nodes

    def outgoing_arcs(self, starting_node):
        """Returns a sequence of Arc objects orderd by alphabetically
        corresponding to all the edges in which the given node is the
        tail node. The label is automatically generated. The cost is
        automatically calculated"""

        arcs = []

        for edge in self.edges:
            tail_node, head_node = edge
            link_cost = GetDis(self.locations[tail_node], self.locations[head_node]).getdis()

            if tail_node == starting_node:
                arc = Arc(tail=tail_node, head=head_node, label=str(tail_node) + '->' + str(head_node), cost=link_cost)
                arcs.append(arc)

        return sorted(arcs)

    def starting_nodes(self):
        """Returns (via a generator) a sequence of starting nodes."""
        for starting_node in self.starting_list:
            yield starting_node

    def is_goal(self, node):
        """Returns true if the given node is a goal node."""
        return node in self.goal_nodes

# Examples

'''graph = LocationGraph(nodes=set('ABC'),
                      locations={'A': (0, 0),
                                 'B': (3, 0),
                                 'C': (3, 4)},
                      edges={('A', 'B'), ('B','C'),
                             ('C', 'A')},
                      starting_list=['A'],
                      goal_nodes={'C'})

for arc in graph.outgoing_arcs('A'):
    print(arc)

for arc in graph.outgoing_arcs('B'):
    print(arc)

for arc in graph.outgoing_arcs('C'):
    print(arc)

print('===================================================')
graph = LocationGraph(nodes=set('ABC'),
                      locations={'A': (0, 0),
                           ''      'B': (3, 0),
                                 'C': (3, 4)},
                      edges={('A', 'B'), ('B', 'C'),
                             ('B', 'A'), ('C', 'A')},
                      starting_list=['A'],
                      goal_nodes={'C'})


for arc in graph.outgoing_arcs('A'):
    print(arc)

for arc in graph.outgoing_arcs('B'):
    print(arc)

for arc in graph.outgoing_arcs('C'):
    print(arc)


print('===================================================')
pythagorean_graph = LocationGraph(
    nodes=set("abc"),
    locations={'a': (5, 6),
               'b': (10,6),
               'c': (10,18)},
    edges={tuple(s) for s in {'ab', 'ac', 'bc'}},
    starting_list=['a'],
    goal_nodes={'c'})

for arc in pythagorean_graph.outgoing_arcs('a'):
    print(arc)
'''