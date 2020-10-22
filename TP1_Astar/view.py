"""
view class for the graph using graphviz
"""
import graphviz
from models import graph

def makeGraphicalGraph(graph, path=None):
    dot = graphviz.Graph(comment='TP2')
    coloredCities = path.getAllCitiesNames()

    #retrieve all cities as nodes
    for city in graph.cities.values():
        if city.name in coloredCities :
            dot.node(city.name, city.name, color="red")
        else :
            dot.node(city.name, city.name)

    
    #retrive all edges (kept from the graph initialization, as the graph is immuable)
    for edgeContainer in graph.links :
        if edgeContainer.source in coloredCities and edgeContainer.dest in coloredCities :
            dot.edge(edgeContainer.source, edgeContainer.dest, label=edgeContainer.weight, color="red")
        else :
            dot.edge(edgeContainer.source, edgeContainer.dest, label=edgeContainer.weight)

    #visualize
    dot.render('graph.gv', view=True)