import re
from search import *

def clauses(knowledge_base):
    """Takes the string of a knowledge base; returns an iterator for pairs
    of (head, body) for propositional definite clauses in the
    knowledge base. Atoms are returned as strings. The head is an atom
    and the body is a (possibly empty) list of atoms.

    Author: Kourosh Neshatian

    """
    ATOM   = r"[a-z][a-zA-z\d_]*"
    HEAD   = r"\s*(?P<HEAD>{ATOM})\s*".format(**locals())
    BODY   = r"\s*(?P<BODY>{ATOM}\s*(,\s*{ATOM}\s*)*)\s*".format(**locals())
    CLAUSE = r"{HEAD}(:-{BODY})?\.".format(**locals())
    KB     = r"^({CLAUSE})*\s*$".format(**locals())

    assert re.match(KB, knowledge_base)

    for mo in re.finditer(CLAUSE, knowledge_base):
        yield mo.group('HEAD'), re.findall(ATOM, mo.group('BODY') or "")
        
        
class KBGraph(ExplicitGraph):
    """return a standard from of graph with variables nodes, edge list, starting nodes, goal nodes"""
    
    def __init__(self, kb, query):
        """
        initialses an KBGraph.
        Keyword arguments:
        kb -- a set of knowledge bases from class clauses,
        query -- a set of atoms whether derived or not.
        """

        self.kb = list(clauses(kb))
        self.query = query
        
        nodes = []
        edge_list = []
        starting_list = []        
        
        for clause in self.kb:
            
            if clause[0] not in nodes:
                nodes.append(clause[0])
                
            if clause[1] == []:
                starting_list.append(clause[0])
                
            for atom in clause[1]:
                if atom not in nodes:
                    nodes.append(atom)
                    
                edge_list.append((atom, clause[0]))
                
        for goal in self.query:
            if goal not in nodes:
                nodes.append(goal)
        
        ExplicitGraph.__init__(self, nodes, edge_list, starting_list, goal_nodes = self.query, estimates=None)
        

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


class BFSFrontier(Frontier):
    """Implements a frontier container appropriate for breadth-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []

    def add(self, path):
        self.container.append(path)

    def __iter__(self):
        while self.container:
            result = self.container.pop(0)
            yield result



kb = """
a :- b, c.
b :- d, e.
b :- g, e.
c :- e.
d.
e.
f :- a,
     g.
"""

query = {'a'}


if next(generic_search(KBGraph(kb, query), BFSFrontier()), None):
    print("The query is true.")
else:
    print("The query is not provable.")
    
print("===================================")

kb = """
a :- b, c.
b :- d, e.
b :- g, e.
c :- e.
d.
e.
f :- a,
     g.
"""

query = {'a', 'b', 'd'}
if next(generic_search(KBGraph(kb, query), DFSFrontier()), None):
    print("The query is true.")
else:
    print("The query is not provable.")
    
print("===================================")
    
kb = """
all_tests_passed :- program_is_correct.
all_tests_passed.
"""

query = {'program_is_correct'}
if next(generic_search(KBGraph(kb, query), BFSFrontier()), None):
    print("The query is true.")
else:
    print("The query is not provable.")
    
print("===================================")

kb = """
a :- b.
"""

query = {'c'}
if next(generic_search(KBGraph(kb, query), BFSFrontier()), None):
    print("The query is true.")
else:
    print("The query is not provable.")
    
print("===================================")
 
kb = ""

query = {'proposition'}
if next(generic_search(KBGraph(kb, query), BFSFrontier()), None):
    print("The query is true.")
else:
    print("The query is not provable.")