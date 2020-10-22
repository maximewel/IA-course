from astar_search import ArtificialIntelligence
from astar_search import CityNotFoundException
from astar_search import NoPathException
from heuristics import HeuristicsEnum
from models.graph import Graph
import os

if __name__ == '__main__':
    #init IA once - the AI generates her graph
    graph = Graph()
    ia = ArtificialIntelligence(graph)

    #"while" user input loop
    inputCitySource = ""
    inputCityDest = ""
    while(True):
        #get city from user
        #os.system("cls")
        print("Welcome to the A* path finder ! Enter your cities, press enter to quit")
        print("Available cities : {}".format(graph.allCities()))
        inputCitySource = input("Origin city : ")
        if not inputCitySource:
            print("stopping")
            break
        inputCityDest = input("Destination city : ")
        print("Available heuristics : {}".format([h for h in HeuristicsEnum]))
        heuristicCode = int(input("Choose heuristic : "))
        heuristic = HeuristicsEnum.heuristics[heuristicCode]

        try:
            #A* search
            path = ia.aStar(inputCitySource, inputCityDest, heuristic)
            print("found")
        except CityNotFoundException as e:
            print(e)
        except NoPathException as e:
            print(e)

        input("Enter any key to continue")
        
    print("research done ! Thanks for choosing our company to find your city, we are better than google maps.")