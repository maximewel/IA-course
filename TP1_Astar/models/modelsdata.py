"""
Python TP A*
Author : Maxime Welcken
"""

class City:
    """ simple data class that hold the city name and position (node in the graph)"""

    def __init__(self, name, x, y):
        self.name, self.x, self.y = name, int(x), int(y)
        self.links = []

    def __str__(self):
        return "{} ({},{})".format(self.name, self.x, self.y)

    def addLink(self, link):
        self.links.append(link)

class Link:
    """
    Simple connection between to city B.\n
    Not oriented (no concept of src/dest - just the dest city)\n
    Weighted
    """
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = int(weight)

class Path:

    def __init__(self, citySource):
        self.citySource = citySource
        self.currentCity = citySource
        self.path = []
        self.weight = 0
        self.f = 0

    def addLink(self, link):
        self.path.append(link)
        self.currentCity = link.dest
        self.weight += link.weight

    def __str__(self):
        return " => ".join([self.citySource.name] + [link.dest.name for link in self.path])

    def __hash__(self):
        return str(self).__hash__()

    def __lt__(self, other):
        return self.f < other.f