import numpy as np
import heapq

# given this final state
final_values = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def cityBlock(array) :
    """ return the summ of the cityblock (manathan) distance from each case to its expected coordinates """
    diff = 0
    for x in range(cityBlock.length) :
        for y in range(cityBlock.length) :
            # don't calculate cityblock for 0, else the heuristic is not admissible
            value = array[x][y]
            if value != 0 :
                # the final board is constant, it is more effective 
                # to map its values to an array (or we would be in o(n^2) with 2 matrixes)
                expectedCoordinates = cityBlock.mapped[value]
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
        """ implementation of the breadth first algorithm, kept from TP1 \n
        Used as a 'perfect' reference : It is a long (time-wise) algorithm, but it always finds the best path"""
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
                if new not in history:
                    #breadth first : Place children last, explore all children of depth D before going to D+1
                    frontiere.append(new)
            iteration += 1
        raise Exception("no solution")

    def aStar(self) :
        """ implementation of the A* search implementation (cityblock/Manhattan + depth) """
        iteration = 1
        frontiere = [self.init] #init with depth 0
        history = {}

        while frontiere:
            print("\riteration count : {}".format(iteration), end="")
            #take the state with the least value
            etat = heapq.heappop(frontiere)
            #add it to ours history
            history[etat] = etat.f
            #stop condition
            if etat.final(final_values):
                return etat
            #verify all next states
            for op in etat.applicable_operators():
                new = etat.apply(op)
                # Calculate f = g + h with g as as depth, h as cityblock
                new.f = cityBlock(new.values) + new.depth
                # did we visit this state ? Is the depth lesser than the already visited one ?
                if new not in history or history[etat] > new.f :
                    heapq.heappush(frontiere, new)
            iteration += 1
        raise Exception("no solution")