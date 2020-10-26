from enum import Enum
from math import sqrt

# List of all heuristics as functions
def trivialHeuristic(citySource, cityDest):
    return 0

def horizontalDistance(citySource, cityDest):
    return abs(citySource.x - cityDest.x)

def verticalDistance(citySource, cityDest):
    return abs(citySource.y - cityDest.y)

def birdViewDistance(citySource, cityDest):
    return sqrt((citySource.x - cityDest.x)**2 +  (citySource.y - cityDest.y)**2)

def manhattanDistance(citySource, cityDest):
    return horizontalDistance(citySource, cityDest) + verticalDistance(citySource, cityDest)

class HeuristicsEnum(Enum):
    """ Enum class that safely holds and maps the heuristics functions """

    TRIVIAL = 1
    DISTANCEX = 2
    DISTANCEY = 3
    BIRDVIEW = 4
    MANHATTAN = 5

    def describe(self):
        return self.name, self.value
        
    def __str__(self):
        return 'type {} for heuristic {}'.format(self.value, self.name)

#link heuristics to enum via this dictionnary.
HeuristicsEnum.heuristics = {
    HeuristicsEnum.TRIVIAL.value : trivialHeuristic,
    HeuristicsEnum.DISTANCEX.value : horizontalDistance,
    HeuristicsEnum.DISTANCEY.value : verticalDistance,
    HeuristicsEnum.BIRDVIEW.value : birdViewDistance,
    HeuristicsEnum.MANHATTAN.value : manhattanDistance
}