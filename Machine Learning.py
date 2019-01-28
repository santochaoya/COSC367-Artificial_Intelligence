def accuracy(predicted_labels, correct_labels):
    '''returns the accuracy of a classifier based on the given arguments.'''

    sum = 0
    for i in range(len(predicted_labels)):
        if predicted_labels[i] == correct_labels[i]:
            sum += 1

    return sum / len(correct_labels)

print(accuracy((True, False, True, False),
               (True, True, False, False)))

print(accuracy((1, 1, 0, 1), (1, 1, 1, 1)))
