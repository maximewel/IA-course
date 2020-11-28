"""
Author : Maxime Welcklen
Old_eval : old fitness function of the CXOnePoint algorithm
Contains placeholder values to avoid having a red file - although it's a good christmas tree impression
"""

""" -- PLACEHOLDER VALUES -- """
import random
start_cell = end_cell = ENCODING_MIN = ENCODING_MAX = ""
def Manhattan(start, end):
    return 0
class a:
    def apply(self, case):
        return 0
def _parse_code(gene):
    return a()
def valid(mv):
    return True
""" -- END PLACEHOLDER VALUES -- """


def eval_and_correct(individual, target):
    """ compute the path of the chromosome, do on-the-fly corrections """
    #init
    currentCase = start_cell
    path = [start_cell]
    idealistic = Manhattan(start_cell, end_cell)
    minManhattan = idealistic
    
    #iterate over every gene of the chromosome, keep index for eventual correction
    for i in range(len(individual)):
        #parse next case, correct if necessary
        gene = individual[i]
        nextCase = _parse_code(gene).apply(currentCase)
        while not valid(nextCase):
            #correct code of chromosome randomly
            individual[i] = random.randint(ENCODING_MIN, ENCODING_MAX)
            nextCase = _parse_code(individual[i]).apply(currentCase)
        currentCase = nextCase

        #process manhattan
        currentManhattan = Manhattan(currentCase, target)

        #we found the end - stop here !
        if currentManhattan == 0:
            return 0

        path.append(currentCase)
        #check if we went closer to the end case : keep its parameters in head
        if currentManhattan < minManhattan:
            minManhattan = currentManhattan
            distinctCells = len(set(path))

    #return the minimal mahnattan value (the "closer" case of the end with the least amount of steps") as fitness value
    #add the difference between idealistinc and distincts cells to try and optimize
    #very efficient on little walls pourcentages - ~10%
    return minManhattan + abs(idealistic - distinctCells)