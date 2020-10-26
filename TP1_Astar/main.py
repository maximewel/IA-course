from search.AI import ArtificialIntelligence, CityNotFoundException, NoPathException
from search.heuristics import HeuristicsEnum
from models.graph import Graph
from view.view import makeGraphicalGraph
import os
import sys

def consoleMode(graph, ia):
    """ loop on user input, put a graphical view of the path for each research. """
    #"while" user input loop
    inputCitySource = ""
    inputCityDest = ""
    while(True):
        #get cities from user
        print("\nWelcome to the A* path finder ! Enter your cities, press enter to quit")
        print("Available cities : {}".format(graph.allCities()))
        inputCitySource = input("Origin city : ")
        if not inputCitySource:
            print("stopping")
            break
        inputCityDest = input("Destination city : ")
        #get heuristic from user
        print("\nAvailable heuristics :")
        for h in HeuristicsEnum:
            print(h) #uses the __str()__ defined in the enum for each indexed enum
        heuristicCode = int(input("Choose your heuristic :"))
        heuristic = HeuristicsEnum.heuristics[heuristicCode]

        try:
            #A* search
            path, iter = ia.aStar(inputCitySource, inputCityDest, heuristic)
            print(f"Path found after {iter} analysed cities. Here is the path : {path}")
            makeGraphicalGraph(graph, path)
        # custom exceptions are already correctly formatted with an error code
        except CityNotFoundException as e:
            print(e)
        except NoPathException as e:
            print(e)

        #loop again
        input("Enter any key to continue")
        
    print("research done ! Thanks for choosing our company to find your city, we are better than google maps.")

def argumentMode(graph, ia):
    if(len(sys.argv) != 3):
        print("2 arguments expected (citysource, citydest), number not correct")
        raise Exception("Argument exception")

    # get cities
    inputCitySource = sys.argv[1]
    inputCityDest = sys.argv[2]


    #try all heuristics for this destination
    for h in HeuristicsEnum:
        try:
            #A* search, print the path, its weight, and the number of visited cities
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

    #If the input is in format [python main city1 city2] - go argument mode
    if len(sys.argv) > 1:
        argumentMode(graph,ia)
    else:
        #go console mode
        consoleMode(graph,ia)