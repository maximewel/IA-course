"""
Author : Maxime Welcklen

chromosome.py : A class that holds the functions related to the fitness and evaluation of a chromosome
"""

def Manhattan(source, target):
    """mahnattan distance between two coordinates tuples"""
    return abs(source[0]-target[0]) + abs(source[1]-target[1])

def valid(case, grid):
    """ return wether a case is valid (in board, not a wall) """
    x,y = case[0], case[1]
    w, h = grid.shape[0], grid.shape[1]
    return x in range(w) and y in range(h) and grid[x][y] == 0

def eval_and_correct(individual, target, start, end, grid):
    """ compute the path of the chromosome, do on-the-fly corrections """
    #init
    currentCase = start
    path = [start]
    idealistic = Manhattan(start, end)
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
        if currentManhattan < minManhattan:
            minManhattan = currentManhattan
            distinctCells = len(set(path))

    #return the minimal mahnattan value (the "closer" case of the end with the least amount of steps") as fitness value
    #add the difference between idealistinc and distincts cells to try and optimize
    return minManhattan + abs(idealistic - distinctCells)