import numpy as np
import heapq
import time

def simpleTimeIt(f) :
    """ simple decorator that indicates how much time the function took """
    def inner(*args) :
        start = time.time()
        result = f(*args)
        end = time.time()
        print("Time consummed by function {}: {}s".format(f.__name__, end-start))
        return result
    
    #polite decorator
    inner.__doc__ = f.__doc__
    inner.__name__ = f.__name__
    inner.__dict__.update(f.__dict__)    
    return inner


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

    @simpleTimeIt
    def aStarV1(self) :
        """ Initial implementation of the A* search implementation (cityblock/Manhattan + depth) """
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
                if new not in history or new.f < history[new]:
                    heapq.heappush(frontiere, new)
            iteration += 1
        raise Exception("no solution")