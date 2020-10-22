import numpy as np
import heapq
import time
import copy
from models.modelsdata import Path

# define Python user-defined exceptions
class CityNotFoundException(Exception):
    """ Exception raised when the city is not found in the graph. """

    def __init__(self, city):
        self.city = city
        self.message = f"{self.city} is not in the graph !"
        super().__init__(self.message)

class NoPathException(Exception):
    """ Exception raised when no path is found between the given, existing cities """

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.message = f"No path found between {source} and {dest}"
        super().__init__(self.message)


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

    def __init__(self, graph) :
        #init the graph
        self.graph = graph

    @simpleTimeIt
    def aStar(self, citySourceName, cityDestName, heuristic) :
        """ implementation of the A* search implementation (cityblock/Manhattan + depth) """

        #get cities from user strings (with verifiation of existence)
        citySource = self.graph.getCityByName(citySourceName)
        cityDest = self.graph.getCityByName(cityDestName)
        if citySource is None:
            raise CityNotFoundException(citySourceName)
        if cityDest is None:
            raise CityNotFoundException(cityDestName)

        #init path and history
        frontiere = [Path(citySource)]
        history = {}
        iteration = 0

        while frontiere:
            iteration += 1
            #take the state with the least value
            path = heapq.heappop(frontiere)
            currentCity = path.currentCity
            #add it to ours history
            history[currentCity] = path.f
            #stop condition
            if currentCity == cityDest:
                return path, iteration
            #verify all next states
            for link in currentCity.links:
                newPath = copy.deepcopy(path)
                newPath.addLink(link)
                nextCity = link.dest
                # Calculate f = g + h with g as as depth, h as cityblock
                newPath.f = heuristic(currentCity, cityDest) + newPath.weight
                # did we visit this state ? Is the depth lesser than the already visited one ?
                if nextCity not in history or newPath.f < history[nextCity]:
                    heapq.heappush(frontiere, newPath)
        raise NoPathException(citySourceName, cityDestName)