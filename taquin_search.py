import numpy as np
from sortedcontainers import SortedDict

# given this final state
final_values = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def cityBlock(array) :
    diff = 0
    for x in range(cityBlock.length) :
        for y in range(cityBlock.length) :
            expectedCoordinates = cityBlock.mapped[array[x][y]]
            diff += abs(x - expectedCoordinates[0]) + abs(y - expectedCoordinates[1])
    return diff

cityBlock.length = len(final_values)
#init cityBlock once
mapped = []
for x in range(cityBlock.length) :
    for y in range(cityBlock.length) :
        mapped.insert(final_values[x][y], (x,y))
cityBlock.mapped = mapped


class ArtificialIntelligence :

    def __init__(self, init) :
        self.init = init

    def searchBreadth(self):
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
                if new not in history and new.legal():
                    #breadth first : Place children last, explore all children of depth D before going to D+1
                    frontiere.append(new)
            iteration += 1
        raise Exception("no solution")


    def searchDepth(self):
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
        depth = 1
        result = None
        while result is None :    
            history = set()    
            print("Depth : {}".format(depth))
            result = self.searchIterativeDepthStep(self.init, depth, history)
            depth += 1
        return result


    def searchIterativeDepthStep(self, state, depth, history) :
        print("inside, depth = {}".format(depth))
        if state.final(final_values):
            return state
        history.add(state)

        if depth <= 1 :
            return None

        ops = state.applicable_operators()
        for op in ops:
            new = state.apply(op)
            if new not in history and new.legal():
                result = self.searchIterativeDepthStep(new, depth-1, history)
                if result is not None :
                    return result

    def searchOriented(self) :
        iteration = 1
        frontiere = [self.init]
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
                    new.cumulatedScore = etat.cumulatedScore + new.depth + cityBlock(new.values)
                    frontiere.insert(new.cumulatedScore, new)
            iteration += 1
        raise Exception("no solution")