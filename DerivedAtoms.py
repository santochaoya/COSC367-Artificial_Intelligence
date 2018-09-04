import re

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
    
    
def forward_deduce(knowledge_base):
    """a (complete) set of atoms (strings) that can be derived (to be true) 
    from the knowledge base in an alphebetal order"""
    
    derived_atoms = []
    Clauses = list(clauses(knowledge_base))
    counter = 0
    
    while counter < len(Clauses):      
        for clause in Clauses:
            if not clause[1] or set(clause[1]).issubset(set(derived_atoms)):
                derived_atoms.append(clause[0])
                Clauses.remove(clause)
                counter = 0
            else:
                counter += 1
                
    return set(derived_atoms)
    
    
    
    
kb = """
a :- b.
b.
"""
print(", ".join(sorted(forward_deduce(kb))))

print("=============================")

kb = """
good_programmer :- correct_code.
correct_code :- good_programmer.
"""
print(", ".join(sorted(forward_deduce(kb))))

print("=============================")

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
print(", ".join(sorted(forward_deduce(kb))))

print("=============================")

