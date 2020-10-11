from taquin_viewer import TaquinViewerHTML
from state_modele import State
from taquin_search import ArtificialIntelligence

# TAQUIN CONFIGURATIONS
taquin_trivial = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
]

taquin_easy = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

# your algorithm should reach the solution in few hundred iterations
taquin_medium = [
    [0, 1, 2],
    [7, 4, 3],
    [5, 8, 6]
]

# your algorithm will need more then 100'000 iterations (not mine, thanks oriented :-) )
taquin_hard = [
    [4, 0, 2],
    [3, 5, 1],
    [6, 7, 8]
]

# just impossible
taquin_impossible = [
    [1, 2, 3],
    [4, 5, 6],
    [8, 7, 0]
]

def pathFromState(state) :
    """
     return the parent's path from a final state """

    stateCurrent = state
    statesPath = []
    while stateCurrent.parent is not None :
        statesPath.insert(0, stateCurrent)
        stateCurrent = stateCurrent.parent
    statesPath.insert(0, stateCurrent) #last step
    return statesPath

def pathToHTML(path, filename) :
    """print a state path to a html file view """

    i = 1
    with TaquinViewerHTML(filename + '.html') as viewer:
        for board in path:
            viewer.add_taquin_state(board.values, "move" + str(i))
            i = i+1 #so we know how much moves our algo found

if __name__ == '__main__':

    #init AI, change this line to change the difficulty
    #startBoard = taquin_trivial
    #startBoard = taquin_easy
    #startBoard = taquin_medium
    startBoard = taquin_hard
    #startBoard = taquin_impossible

    stateStart = State(startBoard)
    ia = ArtificialIntelligence(stateStart)

    #search oriented
    print("Astar search starting")
    stateFinal = ia.aStar()
    print("\nsearch done")
    statesPath = pathFromState(stateFinal)
    pathToHTML(statesPath, "Astar_search")

    #do one to have a comparative

    #search breadth to compare # of moves
    print("breadth search starting")
    stateFinal = ia.searchBreadth()
    print("\nsearch done")
    statesPath = pathFromState(stateFinal)
    pathToHTML(statesPath, "breadth_search")
    