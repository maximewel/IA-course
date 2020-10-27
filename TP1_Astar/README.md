# TP 1 : A * search
* This project is a standalone and can be downloaded (folder TP1_ASTAR/)
* It has a dependance on the "graphviz" python module. If you do not wish to see the view, disable the call to the view and/or use the command line mode

## What is it ?
The TP1 of IA is an implementation of the A* search algorithm with different heuristics.\
The data/ folder in "models/" is given as a data source, the rest of the code is entirely made in-house

## structure
The project is composed of :
* The main.py module at the root, the entry point of the progrmm (controller)
* The "models/" folder containing the data models (graph, cities, links, path)
* The "search/" folder containing the A* search algorithm and the 5 heuristics
* The "view/" folder containing a simple view displaying a graph (console mode only)
* The "doc/" folder containing the responses to Q2 and Q4 as markdown files

## User instructions
The project can be called using two modes.

### Console mode
This mode is an interactive one.
\Use it by calling the main without arguments :\
```Python main.py```\
You will be prompted to enter a source city, dest city, and choose between the 5 heuristics.\
The module calculates the shortest path, displays it using graphviz, and allows you to restart.

### Command line mode
This mode is more practical for testing and comparing.
\Use it by calling the main with two existing cities :\
```Python main.py paris brussels```\
The main then calls the A* algorithm using all 5 of the heuristics succesivelly.\
All the results are displayed on the console. You can compare the lenght of the paths, the visited cites, the time each function took to perform, and the resulting path for each of them.