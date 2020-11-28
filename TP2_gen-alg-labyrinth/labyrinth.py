import matplotlib.pyplot as plt
#deap related imports
from deap import base
from deap import creator
from deap import tools
from collections import namedtuple
from deap import algorithms
import operator
from enum import Enum
#Math and function imports
import random
import time
import math        
from functools import reduce
import numpy as np

def Manhattan(source, target):
    """mahnattan distance between two coordinates tuples"""
    return abs(source[0]-target[0]) + abs(source[1]-target[1])

def display_labyrinth(grid, start_cell, end_cell, solution=None):
    """Display the labyrinth matrix and possibly the solution with matplotlib.
    Free cell will be in light gray.
    Wall cells will be in dark gray.
    Start and end cells will be in dark blue.
    Path cells (start, end excluded) will be in light blue.
    :param grid np.array: labyrinth matrix
    :param start_cell: tuple of i, j indices for the start cell
    :param end_cell: tuple of i, j indices for the end cell
    :param solution: list of successive tuple i, j indices who forms the path
    """
    grid = np.array(grid, copy=True)
    FREE_CELL = 19
    WALL_CELL = 16
    START = 0
    END = 0
    PATH = 2
    grid[grid == 0] = FREE_CELL
    grid[grid == 1] = WALL_CELL
    grid[start_cell] = START
    grid[end_cell] = END
    if solution:
        solution = solution[1:-1]
        for cell in solution:
            grid[cell] = PATH
    else:
        print("No solution has been found")
    plt.matshow(grid, cmap="tab20c")
    plt.show()
    

def solve_labyrinth(grid, start_cell, end_cell, max_time_s):
    """Attempt to solve the labyrinth by returning the best path found
    :param grid np.array: numpy 2d array
    :start_cell tuple: tuple of i, j indices for the start cell
    :end_cell tuple: tuple of i, j indices for the end cell
    :max_time_s float: maximum time for running the algorithm
    :return list: list of successive tuple i, j indices who forms the path
    """

    """ ----- CHROMOSOME INITIALISATION ----- """
    """ --- SIZE --- """
    #terrain shape
    h = grid.shape[0]
    w = grid.shape[1]
    #With the non-fixed length genetic algorithm, the length will grow : We have to start little (so that we can slowly go toward goal)
    CHROMOSOME_LENGTH = math.ceil((h + w) / 8) #ceil : at least 1 at start or we could have problems

    """ --- ENCODING --- """
    #tuple that code the operations as (apply, str) representation to avoid creating classes for each direction
    Code = namedtuple("Code", ["apply", "str"])

    #operations as (apply, str) tuple. apply on the tuple representing the current case, yield the next case
    DIRECTIONS = {
        0: Code(lambda caseTuple: (caseTuple[0]-1, caseTuple[1]), "left"),
        1: Code(lambda caseTuple: (caseTuple[0]+1, caseTuple[1]), "right"),
        2: Code(lambda caseTuple: (caseTuple[0], caseTuple[1]-1), "top"),
        3: Code(lambda caseTuple: (caseTuple[0], caseTuple[1]+1), "bottom")
    }
    ENCODING_MIN, ENCODING_MAX = 0, len(DIRECTIONS)-1

    """ --- CHROMOSMOE DISPLAY AND DECODING --- """

    def _parse_code(code):
        """ Convert integer geneetic code to a Code namedtuple """
        return DIRECTIONS[code]
        
    def _decode(individual):
        """ Parse each code of the full chromosome (aka individual) """
        return [_parse_code(gene) for gene in individual]

    #DEPRECATED, useless on 40*40 maps... Specifically when there is a view to display the chromosome
    def display_chromosome(individual):
        """ Convert chromosome to a readable format (Path of cells : (0,0)->(1,1)->...) """
        return " -> ".join(str(cell) for cell in chromosome_as_cells(individual))

    def chromosome_as_cells(individual):
        """ Return the chromosome as a list of successive cells - stop if "end" is found """
        path = [start_cell]
        for code in _decode(individual):
            path.append(code.apply(path[-1])) #append each move to the last case of the list (=current case)
            if path[-1] == end_cell:
                #immediatly stop once the end is found
                return path
        #return the complete path if the end is never reached
        return path

    """ --- BEST AND WINNERS SEARCHES --- """
    def find_path_lenght(indiv):
        """ return the lenght of the path of the individual as a list of cells
            ->len(indiv)+1 because len(indiv) is the number of steps, not cells
            ->stop the count if end_cell is reached
        """
        return len(chromosome_as_cells(indiv))

    def find_best(population):
        """ use npt o find the best amongst a list of solutions (see test_min) """
        index = np.argmin(np.array([ind.fitness.values[0] for ind in population]))
        return population[index]

    def find_winners(population):
        return list(filter(lambda pop: pop.fitness.values[0] == 0, population))

    def find_winner(winners):
        """ return the winner amongst the winners """
        #case : no winner
        if len(winners) == 0:
            return None
        #case : one winner
        if len(winners) == 1:
            return winners[0]

        #case : Take the best winner
        return list(reduce(lambda ind1, ind2: ind1 if find_path_lenght(ind1) < find_path_lenght(ind2) else ind2, winners))

    """ --- FITNESSES --- """
    def valid(case):
        """ return wether a case is valid (in board, not a wall) """
        x, y = case[0], case[1]
        return x in range(w) and y in range(h) and grid[x][y] == 0

    def eval_and_correct(individual, target):
        """ compute the path of the chromosome, do on-the-fly corrections """
        #init : start_cell is always assumed
        currentCase = start_cell
        #iterate over every gene of the chromosome, keep index instead of foreach for eventual correction
        for i in range(len(individual)):
            #parse next case, correct if necessary
            gene = individual[i]
            nextCase = _parse_code(gene).apply(currentCase)
            while not valid(nextCase):
                #correct code of chromosome randomly - random to avoid favorising a direction
                individual[i] = random.randint(ENCODING_MIN, ENCODING_MAX)
                nextCase = _parse_code(individual[i]).apply(currentCase)
            currentCase = nextCase

            #we found the end - stop here !
            if currentCase == target:
                return (0, i+1) #i+1 : iterations start at 0, and we want the number of steps

        #we use (end ~ current) / (start ~ current) * 100 (as a pourcentage)
        if start_cell == currentCase: return (1000,1000) #very bad for our calcul (division by zero)
        return ((float(Manhattan(target, currentCase)) / Manhattan(start_cell, currentCase)) * 100, i+1)

    toolbox = base.Toolbox()
    def fitness(individual, target):
        """ Fitness of the chromosome with on-the-fly correction of failing genes """
        return eval_and_correct(individual, target)

    toolbox.register("fitness", fitness)
    # negative values : fitness tries to reach smallest possible numbers in (ratio, length)
    # weights : ratio is always a TOP priority (0 = reached target !)
    creator.create("FitnessMin", base.Fitness, weights=(-10000.0, -10.0))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    """ --- MUTATIONS AND SELECTION --- """
    toolbox.register("mate", tools.cxMessyOnePoint)
    toolbox.register("mutate", tools.mutUniformInt, low=ENCODING_MIN, up=ENCODING_MAX, indpb=0.1)
    toolbox.register("select", tools.selTournament)

    """ --- POPULATION INITIALISATION --- """
    toolbox.register("init_gene", random.randint, ENCODING_MIN, ENCODING_MAX)
    toolbox.register("init_individual", tools.initRepeat, creator.Individual, toolbox.init_gene, CHROMOSOME_LENGTH)
    toolbox.register("init_population", tools.initRepeat, list, toolbox.init_individual)

    def evaluate_population(population, target):
        for ind in population:
            ind.fitness.values = toolbox.fitness(ind, target)
    toolbox.register("evaluate", evaluate_population)


    # genetic algorithm hyper-parameters
    MUTPB = 0.6
    CXPB = 0.7
    populationSize = 300
    tournSize = 10
    #init pop, fitness
    pop = toolbox.init_population(n=populationSize)
    toolbox.evaluate(pop, end_cell)

    #REFINED SEARCH
    #init parameters
    start = time.time()
    timePassed = iterations = 0
    caseFound = False
    #stagnancy supervisors
    sameLenghtCounter = 0 #stagnancy counter
    sameLengthStop = 5 #stagnancy stop
    lastLengthPath = 0 #stagnancy memory
    #main loop
    while timePassed < max_time_s and sameLenghtCounter < sameLengthStop:
        print(f"\r iteration {iterations}", end="")

        # --- SEL ---
        offspring = toolbox.select(pop, len(pop), tournSize)
        offspring = list(map(toolbox.clone, offspring))

        # --- MATE&MUTATE ---
        #mate
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
        #mutate
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)

        #remplace pop & eval new pop
        pop = offspring
        toolbox.evaluate(pop, end_cell)

        #phase 1 - growing chromosomes, did we reach the final case ?
        if not caseFound:
            #keep fitness to give actual length of path to user (fit[2])
            fitnessesAtTarget = [ind.fitness.values for ind in pop if ind.fitness.values[0] == 0]
            if fitnessesAtTarget:
                #enter phase 2, change mutation algorithm
                caseFound = True
                toolbox.register("mate", tools.cxOnePoint)
                print(f"\ncase found, now mutating with cxOnePoint without growing")
                print(f"Current length : {[fit[1] for fit in fitnessesAtTarget]}")
        #phase 2 - we are in standard mutation, trying to refine the path
        else:
            #check for stagnancy : can we go faster ?
            fastestPath = np.min([ind.fitness.values[1] for ind in pop if ind.fitness.values[0] == 0])
            sameLenghtCounter += 1 if fastestPath == lastLengthPath else 0
            lastLengthPath = fastestPath
        
        #end of this cycle - calculate time & iterations
        iterations += 1
        timePassed = time.time() - start

    #end of cycles :-)
    winners = find_winners(pop)
    if winners:
        finalChromosome = find_winner(winners)
        print("\nWinner found !")
    else:
        finalChromosome = find_best(pop)
        print("\nNo winner found, fallback on best path")

    print(f"chromosone found in {iterations} iterations in {timePassed}s")
    print(f"The population was composed of {len(pop)} individuals, with {tournSize} selectionned at each iteration")
    print(f"Lenght of the final individual : {find_path_lenght(finalChromosome)}")
    lengths = np.array([find_path_lenght(indiv) for indiv in pop])
    print(f"mean length of the last population : {np.mean(lengths)}, min : {np.min(lengths)}, max : {np.max(lengths)}")
    return chromosome_as_cells(finalChromosome)