"""
Author : Maxime Welcklen
A simple test for the best_ind function (what's faster to retrieve min individual ?)
"""
from random import randint
import numpy as np
import time

class Population:
    def __init__(self, value):
        self.fakeFitness = value

    def getFitness(self):
        return self.fakeFitness

if __name__ == "__main__":
    n = 1000000
    #test the best_individual with normal list and NP list
    #fitnesses = [ind.fitness.values[0] for ind in population]
    print("Generating fitnesses")
    population = [Population(randint(0, n)) for i in range(n)]
    
    print("Start tab min")
    start = time.time()
    fitnesses = [ind.getFitness() for ind in population]
    min_fit = min(fitnesses)
    print(population[fitnesses.index(min_fit)])
    now = time.time(); timeTab = now - start
    print(f"tab time : {timeTab}")

    #https://stackoverflow.com/questions/54624235/how-to-search-list-of-objects-for-index-of-minimum
    #directly find the key
    print("Start direct min")
    start = time.time()
    index = min(range(len(population)), key = lambda i: population[i].getFitness())
    print(population[index])
    now = time.time(); timeDirect = now - start
    print(f"tab time : {timeDirect}")

    print("Start np min")
    start = time.time()
    index = np.argmin(np.array(fitnesses))
    print(population[index])
    now = time.time(); timeNp = now - start
    print(f"np time : {timeNp}")

    #result : Numpy is always faster :-0
    #(if i am not mistaken it is coded in C)


#original function to optimze
def find_best(population):
    fitnesses = [ind.fitness.values[0] for ind in population]
    min_fit = min(fitnesses)
    return population[fitnesses.index(min_fit)]