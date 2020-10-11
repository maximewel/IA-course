# IA course
This github is composed of the different TPs proposed during the artificial intelligence course of the software engineering bachelor, 3rd year, HE-Arc Neuchâtel.

## 1_taquin
A few simple searches algorithm for the "taquin" game as an introduction to search algorithms

### Structure of the project

4 python modules are presented in the project :
* Model, wich represents the model of a taquin game's board
* Main, the entry point of the program that calls the searches
* Search, the AI class that has the search algorithms
* viewer, a pre-made file that act as the view of the program (board -> html)

### Work done
* applicable operators, constructor and swap in the taquin model
* The AI class as a whole (cityblock and searches)
* the main function : Usage of the searches and the viewer

## 2_Astar
An A* search implementation for the taquin game

### Structure of the project
* The main modules are imported from the project 1
* The AI class is changed to implement the A* search

### Main changes
* Utilisation of a dictionary for history and the heapQ (priority queue) algorithm library for the fronteer, in order to optimize the search

## TP1 : Astar
* the data folder contain a set of data to make the searches on

### Work done
* Todo
