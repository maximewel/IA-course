"""
Python TP A*
Author : Maxime Welcken
"""
import copy

class City:
    """ simple data class that hold the city name and position (node in the graph)"""

    def __init__(self, name, x, y):
        self.name, self.x, self.y = name, int(x), int(y)
        #prepare the city's links
        self.links = []

    def __str__(self):
        return "{} ({},{})".format(self.name, self.x, self.y)

    def addLink(self, link):
        self.links.append(link)

class Link:
    """
    Simple connection to city B.\n
    Not oriented (no concept of src/dest - just the dest city) the source city is the city this link is atached to.\n
    Weighted
    """
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = int(weight)

class Path:
    """ Path - holds a city source and a serie of links to a destination """
    def __init__(self, citySource):
        self.citySource = citySource
        self.currentCity = citySource
        self.path = []
        self.weight = 0
        self.f = 0

    def addLink(self, link):
        """ Add a link to this path's links. Automatically compute the new weight """
        self.path.append(link)
        self.currentCity = link.dest
        self.weight += link.weight

    def clone(self):
        """ Retun a path identical to this path, but with an independant list of links """
        path = Path(self.citySource)
        path.weight = self.weight
        path.currentCity = self.currentCity
        path.path = [l for l in self.path] #shallow copy - no link is recreated, but lists are independant
        return path

    def getAllCitiesNames(self):
        return [self.citySource.name] + [link.dest.name for link in self.path] #ordered because list keep order

    def __str__(self):
        return " => ".join([str(self.citySource)] + [str(link.dest) for link in self.path])

    def __hash__(self):
        return str(self).__hash__()

    def __lt__(self, other):
        return self.f < other.f #Used in heapQ algorithm