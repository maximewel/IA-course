from search import ArtificialIntelligence
from search import CityNotFoundException
from search import NoPathException
from heuristics import HeuristicsEnum
from models.graph import Graph
import view
import os
import sys

def consoleMode(graph, ia):
    #"while" user input loop
    inputCitySource = ""
    inputCityDest = ""
    while(True):
        #get city from user
        print("Welcome to the A* path finder ! Enter your cities, press enter to quit")
        print("Available cities : {}".format(graph.allCities()))
        inputCitySource = input("\nOrigin city : ")
        if not inputCitySource:
            print("stopping")
            break
        inputCityDest = input("\nDestination city : ")
        print("\n\nAvailable heuristics : {}".format([h for h in HeuristicsEnum]))
        heuristicCode = int(input("Choose your heuristic : (nothing to do all heuristics)"))
        heuristic = HeuristicsEnum.heuristics[heuristicCode]

        try:
            #A* search
            path, iter = ia.aStar(inputCitySource, inputCityDest, heuristic)
            print(f"\nPath found after {iter} analysed cities. Here is the path : {path}")
            view.makeGraphicalGraph(graph, path)
        except CityNotFoundException as e:
            print(e)
        except NoPathException as e:
            print(e)

        input("Enter any key to continue")
        
    print("research done ! Thanks for choosing our company to find your city, we are better than google maps.")

def argumentMode(graph, ia):
    if(len(sys.argv) != 3):
        print("not enough arguments")
        raise Exception("Argument exception")

    # get cities
    inputCitySource = sys.argv[1]
    inputCityDest = sys.argv[2]


    for h in HeuristicsEnum:
        try:
            #A* search
            path, iter = ia.aStar(inputCitySource, inputCityDest, HeuristicsEnum.heuristics[h.value])
            print(f"heurstic {h.name}. {iter} analysed cities, total weight {path.weight}\n"
            f"path : {path}.\n")
        except CityNotFoundException as e:
            print(e)
        except NoPathException as e:
            print(e)

if __name__ == '__main__':
    #init IA once - the AI generates her graph
    graph = Graph()
    ia = ArtificialIntelligence(graph)

    if len(sys.argv) > 0:
        argumentMode(graph,ia)
    else:
        consoleMode(graph,ia)

