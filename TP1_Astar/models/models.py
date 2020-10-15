"""
Python TP A*
Author : Maxime Welcken
"""

class City:
    """ simple data class that hold the city name and position (node in the graph)"""

    def __init__(self, name, x, y):
        self.name, self.x, self.y = name, x, y
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
        self.weight = weight