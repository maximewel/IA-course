
import os
from models import City
from models import Link

class Graph :
    """
    Graph that holds the cities and connections data
    """

    # Some static variables for file gestion
    DATACITY = "../data/positions.txt"
    DATACONNECTION = "../data/connections.txt"

    def __init__(self):
        self.cities = self.parseCities()
        self.parseConnections(self.cities)
        #verify that the graph is correct
        for city in self.cities.values() :
            print("city {} linked to {}\n".format(city, [str(c.dest) for c in city.links]))

    def relativeFilename(self, filename):
        """ return a usable filename from a relative path """
        scriptDir = os.path.dirname(__file__)
        return os.path.join(scriptDir, filename)

    def parseCities(self):
        """ retrieve all cities from the DATACITY file in a dict """
        with open(self.relativeFilename(Graph.DATACITY)) as f:
            cities = {n : City(n,x,y) for n,x,y in [l.split() for l in f]}
        return cities

    def parseConnections(self, cities):
        """ Add all the connections from DATACONNECTION between the cities """
        with open(self.relativeFilename(Graph.DATACONNECTION)) as f:
            for A,B,weight in [l.split() for l in f]:
                try:
                    self.cities[A].addLink(Link(self.cities[B], weight))
                    self.cities[B].addLink(Link(self.cities[A], weight))
                except KeyError:
                    print("Problem parsing connections between {} and {}".format(A,B))

graph = Graph()