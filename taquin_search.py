import numpy as np
from sortedcontainers import SortedDict

# given this final state
final_values = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def cityBlock(array) :
    ''' return the summ of the cityblock (manathan) distance from each case to its expected coordinates '''
    diff = 0
    for x in range(cityBlock.length) :
        for y in range(cityBlock.length) :
            # the final board is constant, it is more effective 
            # to map its values to an array (or we would be in o(n^2) with 2 matrixes)
            expectedCoordinates = cityBlock.mapped[array[x][y]] 
            diff += abs(x - expectedCoordinates[0]) + abs(y - expectedCoordinates[1])
    return diff

#avoid calculating lenght each time
cityBlock.length = len(final_values) 
# mapping of final, constant board as [value=>(x,y)]
cityBlock.mapped = []
for x in range(cityBlock.length) :
    for y in range(cityBlock.length) :
        cityBlock.mapped.insert(final_values[x][y], (x,y))

class ArtificialIntelligence :

    def __init__(self, init) :
        self.init = init #stock initial board

    def searchBreadth(self):
        ''' implementation of the breadth first algorithm '''
        iteration = 1
        frontiere = [self.init]
        history = set()

        while frontiere:
            print("\riteration count : {}, frontiere number :{}".format(iteration, len(frontiere)), end="")
            etat = frontiere.pop(0) #get first state in frontiere
            history.add(etat)
            if etat.final(final_values):
                return etat

            ops = etat.applicable_operators()
            for op in ops:
                new = etat.apply(op)
                if new not in history and new.legal():
                    #breadth first : Place children last, explore all children of depth D before going to D+1
                    frontiere.append(new)
            iteration += 1
        raise Exception("no solution")


    def searchDepth(self):
        ''' implementation of the depth first implementation'''
        iteration = 1
        frontiere = [self.init]
        history = set()

        while frontiere:
            print("\riteration count : {}, frontiere number :{}".format(iteration, len(frontiere)), end="")
            etat = frontiere.pop(0)
            history.add(etat)
            if etat.final(final_values):
                return etat
            ops = etat.applicable_operators()
            for op in ops:
                new = etat.apply(op)
                if (new not in frontiere) and new not in history and new.legal():
                    #depth first : Place children first, explore all children's children before going up
                    frontiere.insert(0, new)
            iteration += 1
        raise Exception("no solution")

    def searchIterativeDepth(self) :
        ''' recursive implementation of the iterative depth first algorithm '''
        depth = 1
        result = None
        while result is None :    
            history = set()    
            print("Depth : {}".format(depth))
            # will call itself recursively from the given depth
            result = self.searchIterativeDepthStep(self.init, depth, history) 
            depth += 1
        return result


    def searchIterativeDepthStep(self, state, depth, history) :
        ''' perform a step of the depth first algorithm with depth '''
        # terminal conditions : stop if result is found
        if state.final(final_values):
            return state
        history.add(state)

        # terminal conditions : stop depth is 1 or below (1 means we are the last depth to be seen)
        if depth <= 1 :
            return None

        ops = state.applicable_operators()
        for op in ops:
            new = state.apply(op)
            if new not in history and new.legal():
                # call each children, wich will call his children, etc... Resulting in depth first
                # the "frontiere" here is the recursive call, there is no data structure to stock it
                result = self.searchIterativeDepthStep(new, depth-1, history)
                if result is not None :
                    return result #stop at result found, do not compare results if multiple are found (depth first)

    def searchOriented(self) :
        ''' implementation of the oriented search implementation (cityblock + depth)'''
        iteration = 1
        frontiere = [self.init] #init at depth 0, cumulatedScore 0 (see model initialisation)
        history = set()

        while frontiere:
            print("\riteration count : {}".format(iteration), end="")
            etat = frontiere.pop(0)
            history.add(etat)
            if etat.final(final_values):
                return etat
            ops = etat.applicable_operators()
            for op in ops:
                new = etat.apply(op)
                if new not in history :
                    # discriminate by cumulated heuristic(cityblock/manathan) value, parent's depth, and own cityblock
                    new.cumulatedScore = etat.cumulatedScore + new.depth + cityBlock(new.values) 
                    frontiere.insert(new.cumulatedScore, new) #pop(0) : We try to take the fastest path possible
            iteration += 1
        raise Exception("no solution")