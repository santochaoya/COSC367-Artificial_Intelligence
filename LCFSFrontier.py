import heapq
from search import *
import math
from LocationGraph import *

class LCFSFrontier(Frontier):
    """"implement of lowest-cost-first search """

    def __init__(self):
        """The constructor takes no argument. It initialises the
                container to an empty list."""
        self.container = []

    def add(self, path):
        self.container.append(path)
                
    def __iter__(self):
        while self.container:
            result = heapq.nsmallest(1, self.container, key = lambda path : sum(arc.cost for arc in path))
            self.container.remove(result[-1])
            yield result[-1]

# Examples
def main():
    graph = LocationGraph(nodes=set('ABC'),
                          locations={'A': (0, 0),
                                     'B': (3, 0),
                                     'C': (3, 4)},
                          edges={('A', 'B'), ('B', 'C'),
                                 ('B', 'A'), ('C', 'A')},
                          starting_list=['A'],
                          goal_nodes={'C'})

    solution = next(generic_search(graph, LCFSFrontier()))
    print_actions(solution)

    print('===================================================')

    graph = LocationGraph(nodes=set('ABC'),
                          locations={'A': (0, 0),
                                     'B': (3, 0),
                                     'C': (3, 4)},
                          edges={('A', 'B'), ('B', 'C'),
                                 ('B', 'A')},
                          starting_list=['A'],
                          goal_nodes={'C'})

    solution = next(generic_search(graph, LCFSFrontier()))
    print_actions(solution)

    print('===================================================')

    pythagorean_graph = LocationGraph(
    nodes=set("abc"),
    locations={'a': (5, 6),
               'b': (10,6),
               'c': (10,18)},
    edges={tuple(s) for s in {'ab', 'ac', 'bc'}},
    starting_list=['a'],
    goal_nodes={'c'})

    solution = next(generic_search(pythagorean_graph, LCFSFrontier()))
    print_actions(solution)



if __name__ == "__main__":
    main()