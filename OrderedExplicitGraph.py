from search import *

class DFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []

    def add(self, path):
        self.container.append(path)

    def __iter__(self):
        while self.container:
            result = self.container.pop()
            yield result
            

class OrderedExplicitGraph(ExplicitGraph):
    """return a graph which child nodes whith alphaetical order"""
    
    def __init__(self, nodes, edges, starting_list, goal_nodes):
        self.nodes = nodes
        self.edges = edges
        self.starting_list = starting_list
        self.goal_nodes = goal_nodes

        self.edges = list(self.edges)
        self.edges = sorted(self.edges, key=lambda edge: (edge[0], edge[1]), reverse=True)

    def outgoing_arcs(self, node):
        """Returns a sequence of Arc objects corresponding to all the
        edges in which the given node is the tail node. The label is
        automatically generated."""

        for edge in self.edges:

            if len(edge) == 2:  # if no cost is specified
                tail, head = edge
                cost = 1  # assume unit cost
            else:
                tail, head, cost = edge
            if tail == node:
                yield Arc(tail, head, str(tail) + '->' + str(head), cost)


def main():
    graph = OrderedExplicitGraph(nodes=set('SABG'),
                             edges={('S', 'A'), ('S','B'),
                                    ('B', 'S'), ('A', 'G')},
                             starting_list=['S'],
                             goal_nodes={'G'})

    solutions = generic_search(graph, DFSFrontier())
    solution = next(solutions, None)
    print_actions(solution)
    
    flights = OrderedExplicitGraph(nodes={'Christchurch', 'Auckland', 
                                          'Wellington', 'Gold Coast'},
                                   edges={('Christchurch', 'Gold Coast'),
                                          ('Christchurch','Auckland'),
                                          ('Christchurch','Wellington'),
                                          ('Wellington', 'Gold Coast'),
                                          ('Wellington', 'Auckland'),
                                          ('Auckland', 'Gold Coast')},
                                   starting_list=['Christchurch'],
                                   goal_nodes={'Gold Coast'})
    
    my_itinerary = next(generic_search(flights, DFSFrontier()), None)
    print_actions(my_itinerary)    
   
   
    graph = OrderedExplicitGraph(nodes=set('SAG'),
                                 edges={('S','A'), ('S', 'G'), ('A', 'G')},
                                 starting_list=['S'],
                                 goal_nodes={'G'})
                                 
    solutions = generic_search(graph, DFSFrontier())
    solution = next(solutions, None)
    print_actions(solution)
    
    graph = OrderedExplicitGraph(nodes=set('SAG'),
                                 edges={('S', 'G'), ('S','A'), ('A', 'G')},
                                 starting_list=['S'],
                                 goal_nodes={'G'})
    
    solutions = generic_search(graph, DFSFrontier())
    solution = next(solutions, None)
    print_actions(solution)    
if __name__ == "__main__":
    main()