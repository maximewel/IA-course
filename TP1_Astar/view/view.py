"""
view class for the graph using graphviz
"""
import graphviz
from models import graph

def makeGraphicalGraph(graph, path=None):
    """ Make a graphical view of a non-oriented graph, with an eventual given path. Display the path in red. """
    dot = graphviz.Graph(comment='TP2')
    
    coloredCities = path.getAllCitiesNames()
    #order the cities to draw the linked path in red
    orderOfCities = {coloredCities[i] : i for i in range(len(coloredCities))}
    

    #retrieve all cities as nodes of the graph
    for city in graph.cities.values():
        dot.node(city.name, city.name, color = "red" if city.name in coloredCities else "black")
    
    #retrive all edges (unique edges kept from the graph initialization, as the graph is immuable)
    for edgeContainer in graph.links :
        linked = False
        try :
            #Check if this link is in the path to the best solution
            if abs(orderOfCities[edgeContainer.dest]-orderOfCities[edgeContainer.source]) == 1:
                linked = True
        except KeyError :
            #cities are not in the path : linked stays false
            pass
        #path is black if 
        dot.edge(edgeContainer.source, edgeContainer.dest, label=edgeContainer.weight, color = "red" if linked else "black")

    #visualize
    dot.render('graph.gv', view=True)