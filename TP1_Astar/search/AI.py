import numpy as np
import heapq
import time
import copy
from models.modelsdata import Path

# define custom exception to discriminate path not found and city not found

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
    """ simple decorator that indicates how much time the function took to perform """
    def inner(*args) :
        start = time.time()
        result = f(*args)
        end = time.time()
        print("Time consummed by function {}: {:.2}s".format(f.__name__, end-start))
        return result
    
    #polite decorator
    inner.__doc__ = f.__doc__
    inner.__name__ = f.__name__
    inner.__dict__.update(f.__dict__)    
    return inner

class ArtificialIntelligence :
    """ ArtificialIntelligence : Class that allows to stock a graph, and ask best paths between cities using the A* algorithm """

    def __init__(self, graph) :
        """ graph to work with A*. """
        #stock the graph
        self.graph = graph

    @simpleTimeIt
    def aStar(self, citySourceName, cityDestName, heuristic) :
        """ 
        implementation of the A* search implementation (heuristic + depth).<br>
        return path, iteration
        """

        #get cities from user strings (with verifiation of existence)
        citySource = self.graph.getCityByName(citySourceName)
        cityDest = self.graph.getCityByName(cityDestName)
        if citySource is None:
            raise CityNotFoundException(citySourceName)
        if cityDest is None:
            raise CityNotFoundException(cityDestName)

        #init path and history (HISTORY could be ignored if and only if the heuristic is consistent)
        frontiere = [Path(citySource)]
        history = {}
        iteration = 0 #to count total cities analysed

        while frontiere:
            iteration += 1
            #take the path with the least value, extract its last city
            path = heapq.heappop(frontiere)
            currentCity = path.currentCity
            #add it to the history
            history[currentCity] = path.f

            #stop condition
            if currentCity == cityDest:
                return path, iteration

            #compute all next possible path
            for link in currentCity.links:
                newPath = path.clone() #get new path from current path (with its own links list)
                newPath.addLink(link) #new weight is automatically added here
                nextCity = link.dest
                # Calculate f = g + h with g as depth, h as heuristic
                newPath.f = heuristic(nextCity, cityDest) + newPath.weight
                # did we visit this state ? Is the depth lesser than the already visited one ?
                if nextCity not in history or newPath.f < history[nextCity]: #not usefull with consistent algorithm
                    heapq.heappush(frontiere, newPath)

        raise NoPathException(citySourceName, cityDestName)