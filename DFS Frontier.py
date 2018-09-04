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
        print('end frontier : {}'.format(self.container))
        

    def __iter__(self):
        while self.container:
            result = self.container.pop()
            #print('result : {}, frontier : {}'.format(result, self.container))
            yield result
        
        
def main():
    # Example 1
    '''graph = ExplicitGraph(nodes = set('SAG'),
                          edge_list = [('S','A'), ('S', 'G'), ('A', 'G')],
                          starting_list = ['S'],
                          goal_nodes = {'G'})
    solutions = generic_search(graph, DFSFrontier())
    solution = next(solutions, None)
    print_actions(solution)'''
    
    # Example 2
    graph = ExplicitGraph(nodes = set('SAG'),
                          edge_list = [('S', 'G'), ('S','A'), ('A', 'G')],
                          starting_list = ['S'],
                          goal_nodes = {'G'})
    solutions = generic_search(graph, DFSFrontier())
    print(solutions)
    solution = next(solutions, None)
    print_actions(solution)
    
    '''# Example 3
    available_flights = ExplicitGraph(
        nodes=['Christchurch', 'Auckland', 
               'Wellington', 'Gold Coast'],
        edge_list=[('Christchurch', 'Gold Coast'),
                   ('Christchurch','Auckland'),
                   ('Christchurch','Wellington'),
                   ('Wellington', 'Gold Coast'),
                   ('Wellington', 'Auckland'),
                   ('Auckland', 'Gold Coast')],
        starting_list=['Christchurch'],
        goal_nodes={'Gold Coast'})
    
    my_itinerary = next(generic_search(available_flights, DFSFrontier()), None)
    print_actions(my_itinerary)    
    
    # Example 4
    graph = ExplicitGraph(nodes=['Knowledge',
                                 'Commerce',
                                 'Wisdom',
                                 'Wealth',
                                 'Happiness'],
                          edge_list=[('Knowledge', 'Wisdom'),
                                 ('Commerce', 'Wealth'),
                                 ('Happiness', 'Happiness')],
                          starting_list=['Commerce'],
                          goal_nodes={'Happiness'})
    
    solutions = generic_search(graph, DFSFrontier())
    solution = next(solutions, None)
    print_actions(solution)'''
    
    
if __name__ == "__main__":
    main()