# Labyrinth TP with genetic algorithm
This TP proposes an implementation of a genetic algorithm to solve a simple labyrinth.\
This README explains its key implementation points.

## Specifications
Let's define the problem first :
* The environnement is a M*N grid (M*M actually, they are square)
* On the grid are walls (value=1) and empty cells (value=0)
* The goal is to find a path form start to end (tested with (0,0) -> (w-1,h-1))
* The grids are 10\*10 to 40\*40, the algorithm must work on each one of them, there are given time limite for each of them

## Chromosome encoding
### stocked values
The solve_lab function has the start case and end case as parameters.\
Stocking a list of cells would be terrible :
* The generation of a **valid** path (with adjacent cells) would take a lot of verification -and thus time
* The storage would be non-efficient (tuples of x,y)
* The read-write times would be at least double the time of a simpler solution

In lieu of cells, the **steps** are stocked. Only foor steps have to be stocked :\
```Left Right Top Bottom```\
```00 01 10 11```\
The chromosome is then easily converted to a list of cells by applying these steps from the start_cell.\
The steps can be generated fully randomly - your next cell is necessarily adjacent to your current cell ! But is it valid ?

### Invalid path gestion
With the fully random step generation, two things can go wrong :
* The next step moves the chromosome into a wall
* The next step moves the chromosome outside of the grid

The usual gestions of an invalid path are :
* Ignoring the problem while parsing(just reading the next case), as we did in "le compte est bon !"
* Correcting the problem - changing the gene to be a valid one
* Declare this chromosome with an "invalid" fitness, thus not selecting it further

The third method is put away because on a 40*40 grid, disbanding all chromosomes going *once* into a wall would be catastrophic.\
The first method is not taken because we could have very instable chromosome : The mutation of a single gene could escalade into the ignoring / de-ignoring of a dozen other genes.\
Therefore, the second one is choosen. While parsing the chromosome path, if an invalid step is found, its associated gene is remplaced **randomly** by another gene into the 4 possibilities.\
The "random" correction is very important to not favorize a direction above the others. Favorising a direction could emplify the problem of local maximum that the genetic algorithms already endure.

### Bits or bytes ?
In the snippet above, "00","01","10","11" are written in binaries. And of course, binaries are virtually perfect here : The whole space is touched (2^2 = 4, 4 directions) so there is no problem of invalid code. But the solution presented later mixes the chromosomes together in a random fashion, and results in no-same-length offpsring.\

As such, a binary encoding, which would be faster, could have a problem of "dangling bit" : an offspring chromosome could perfectily be composed of an impair number of bits, which would have to be adressed.\

For the sake of simplicity, and because our code is only one integer, the option to "bite the bullet" and go with integers is more raisonnable.

## Choice of a methodology
Before going further in the details of the implementation, let's state that the developpement of the genetic algorithm went through three phases. This section offers a very quick review of the plan of these 
## The classical
The first methodology tested was a very classical, "le compte est bon"-like genetic algorithm.\
The evaluation functon of this classical first try 

## Fast and Furious

## A refined approach
## Fitness function

## Selection

## Crossover

## Mutate

## Stopping condition

## Hyper-parameters