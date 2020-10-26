
import os
from models.modelsdata import City, Link

class EdgeContainer():
    """ Class used to hold a simple (source, dest, weight) value for an edge Used in view to have unique edges"""
    def __init__(self, source, dest, weight):
        self.source = source
        self.dest = dest
        self.weight = weight

class Graph :
    """
    Graph that holds the cities and connections data
    """

    # Some static variables for file gestion
    DATACITY = "/data/positions.txt"
    DATACONNECTION = "/data/connections.txt"

    def __init__(self):
        #cities, links are stocked for future utilisation
        #cities for easily retrieving cities, links for view usage
        self.cities = self.parseCities()
        self.links = self.parseConnections(self.cities)

    def relativeFilename(self, filename):
        """ return a usable filename from a relative path by prepending the actual absolute path of this file """
        scriptDir = os.path.dirname(__file__).replace("\\","/")
        return scriptDir + filename

    def parseCities(self):
        """ retrieve all cities from the DATACITY file in a dict {name:city} """
        with open(self.relativeFilename(Graph.DATACITY)) as f:
            cities = {n : City(n,x,y) for n,x,y in [l.split() for l in f]}
        return cities

    def parseConnections(self, cities):
        """ Add all the connections from DATACONNECTION between the cities """
        links = []
        with open(self.relativeFilename(Graph.DATACONNECTION)) as f:
            for A,B,weight in [l.split() for l in f]:
                try:
                    #add A->B and A<-B, consider the graph as not oriented
                    self.cities[A].addLink(Link(self.cities[B], weight))
                    self.cities[B].addLink(Link(self.cities[A], weight))
                    links.append(EdgeContainer(A, B, weight)) #edge containers stock unique links for the view
                except KeyError:
                    print("Problem parsing connections between {} and {}".format(A,B))
        return links

    def getCityByName(self, cityName):
        """ return the city from its name, case insensitive. Return none if city is not registered. """
        try :
            #allow for case insensitive retrieving of cities
            for key,value in self.cities.items():
                if key.lower() == cityName.lower(): 
                    return value
        except KeyError :
            return None

    def allCities(self):
        """ return a string composed of all the cities of this graph """
        return ", ".join(list(self.cities.keys()))

    def __str__(self):
        string = "Graphe\n"
        for city in self.cities.values() :
            string += "city {} linked to {}\n".format(city, [str(c.dest) for c in city.links])
        return string

if __name__ == "__main__":  
    #to test the graph if this module is directly called
    graph = Graph()
    print(graph)