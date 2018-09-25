import itertools

def joint_prob(network, assignment):
    '''given a belief network and a complete assignment of all the variables in the network,
     returns the probability of the assignment.'''
    prob = 1

    for key in assignment.keys():
        # get the bool value of parent of the current node
        b_value = []
        for v in network[key]['Parents']:
            b_value.append(assignment[v])
        b_value = tuple(b_value)

        #calculate the joint probability
        if assignment[key]:
            prob = prob * network[key]['CPT'][b_value]
        else:
            prob = prob * (1 - network[key]['CPT'][b_value])

    return prob


def query(network, query_var, evidence):
    '''given a belief network, the name of a variable in the network, and some evidence,
    returns the posterior distribution of query_var. '''
    hidden_vars = network.keys() - evidence.keys() - {query_var}
    prob_true = 0
    prob_false = 0

    for values in itertools.product((True, False), repeat=len(hidden_vars)):
        hidden_assignments = {var: val for var, val in zip(hidden_vars, values)}

        #add query_var true and false to evidence and hidden assignments
        assi_true = dict({query_var : True}, **evidence, **hidden_assignments)
        assi_false = dict({query_var : False}, **evidence, **hidden_assignments)

        #calculate probilities of assignment true and false
        prob_true += joint_prob(network, assi_true)
        prob_false += joint_prob(network, assi_false)

    #normalized the probilities
    sum_probs = prob_true + prob_false
    result = {True : prob_true / sum_probs, False : prob_false / sum_probs}

    return result


network = {
    'Virus': {
        'Parents': [],
        'CPT': {
            (): 0.01
        }},

    'A': {
        'Parents': ['Virus'],
        'CPT': {
            (True,): 0.95,
            (False,): 0.1,
        }},

    'B': {
        'Parents': ['Virus'],
        'CPT': {
            (True,): 0.9,
            (False,): 0.05,
        }},
}

answer = query(network, 'Virus', {'A': True})
print("The probability of carrying the virus\n"
      "if test A is positive: {:.5f}"
      .format(answer[True]))

answer = query(network, 'Virus', {'B': True})
print("The probability of carrying the virus\n"
      "if test B is positive: {:.5f}"
      .format(answer[True]))