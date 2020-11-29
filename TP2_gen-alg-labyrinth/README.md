# Labyrinth TP with genetic algorithm
This TP proposes an implementation of a genetic algorithm to solve a simple labyrinth.\
This README explains its key implementation points.

## Specifications
Let's define the problem first :
* The environnement is a M\*N grid (M\*M actually, they are square)
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
### The classical
The first methodology tested was a very classical, "le compte est bon"-like genetic algorithm.\
The evaluation functon of this classical first try is kept as an archive in misc/old_eval.\
It was promising : The evaluation looked at the case that came the closer to the end (manhattan-wise), and returned a value of this manhattan + the difference between its path and the "perfect-path" to the end. The results were often very very close -if not identical- to the optimized path.\
It proved its limitation time-wise (it is pretty slow) and with complexe path (ex : "doors", "walls" it kept planting into, etc...).

### Fast and Furious
The **FAST AND FURIOUS** approach (It *must* be yelled) is the first try with a genetic algorithm with growing chromosomes.\
Its implementation is kept verbatim in labyrinth_speedy.py as a comparaison for our third method (and a fallback would it fail, but it dit not fail)
* The results are very, very, very fast : <1s for 40/*40, and ~2s for 100\*100 grids !
* This algorithm does not yield an optimized path - it yields the first path it come into

This algorithm is PERFECT would we search for a fast path from A to B (Game pathfinding maybe ?) : the <1s for 40\*40 grid is very promising.\
But as we kept bumping into sub-optimized path, and because the TP is graded according to standard deviation starting from 5%, a refinement method had to be implemented.

### A refined approach
The idea here is to combine the first approaches :
* A first phase with growing chromosomes going for a fast search
* A second phase of refining the path found during the fisrt phase (-> minimizing the length)

This method is the one used in labyrinth.py and is the one corresponding the most to the condtions of the TP (fast, find solutions, has refined - but not necessarily optimized - path)

## Fitness function
The fitness function's responsibility is to give a [multi]-value evaluation of the population, individual by individual.\
The first method's fitness took care of evaluating the closer-to-the-end case of the path.\
With the **growing chromosomes**, the length of the individuals is **exponentially growing** as the crosover go, meaning that we can be **less vigilant** about each case of the path, while still ensuring **progressive convergence of the path**.\
As such, during the step-by-step analysis, this function now only check if the end case is reached. It then evaluated the individual based on the last case reached by its path.\
\
After some research on the best fitness function, i found this source(https://www.researchgate.net/publication/233786685_A-Mazer_with_Genetic_Algorithm) that talked about a ratio rather than a simple weight as i did with my first method.\
The idea of a ratio between the distance to the start and the distance to the end is very promising. Our fitness function returns:\
```((float(Manhattan(target, currentCase)) / Manhattan(start_cell, currentCase)) * 100, i+1)```

### Error correction
The fitness function is the one evaluating the chromosome - and its path.\
The angle taken by this algorithm is to go as fast as possible. As such, going 2 times on the data (on each path of each individual) to correct and then evaluate them is a no-no. To avoid this double data loop, the correction is directly done on-the-fly during the fitness function.

### multiple values
The fitness function returns two values : 
* The ratio value, that will be explained next
* The length traveled to reach this ratio - either the length to go to the end of the path, or to reach the target.

\
```creator.create("FitnessMin", base.Fitness, weights=(-10000.0, -10.0))```\
The function does not treat the two values identically - it is weighed :
* The first value, the ratio, is treated with asbolute priority (weight -10 000)
* The second value, the length or number of steps, is a low priority (weight -10)

\
```creator.create("Individual", list, fitness=creator.FitnessMin)```\
The fitnessMin and negative weights means that the selection will try to minimize these values as much as possible.\
This means that the selection will take first the chromosome with the smallest ratio, and amongst them, the individuals with the smalles path lenght (steps).

### The ratio
The ratio used is :
```(target ~ currentCase / start_cell ~ currentCase) * 100```\
With the '~' operator beeing the manhattan distance between the cases.
#### Quotient
The quotient is : ```target ~ currentCase```\
This is the distance between the target and the current case.\
The quotient represents the **ideal distance that the chromosome has to travel to reach its goal**

#### Divisor
The divisor is : ```start_cell ~ currentCase```\
This is the distance between the start case and the current case.\
The divsor represents the **ideal distance already traveled by the chromosome from the start**

#### Result
As the fitness is a fitnessMin, the division is minimized.\
To minimize a division is to **minimize its quotient**, and to **maximize its divisor**. It means that the algorithm tries to **minimize the length between its last case and the target** while **maximizing its ideal travel from the start case**.\
Which is perfectly what we want. This ratio avoid some known problems and has some interesting values :
* If the individual does a "snake path" that wriggles a lot, as the ideal distance is taken form the start, it will not grant him a lot of points
* If the individual is "stuck in a wall", it will not grant him points - the number of steps is not taken in the ratio, only the path is has travelled since the start
* The individual tries to reach the target by making its distance smaller
* The individual tries to travel a lot by maximizing its distance from the start, avoiding beeing stuck "just next to the final case but with a wall in the middle"
* The individual tends to not be stuck in loops, because going back on its track does not earn him points
* The quotient naturally converges to 0, the sability does not have to be checked
* The ratio takes into account twisted path - we do not know what is the optimized path, but we can try to guess it by minmaxing the movements

The result is multiplied by 100 to have more distinction between the results.\
Also, a problem has to be taken in account : The divisor can not be 0. A such, if start==current, a big value is returned to avoid this individual. (This individual would not have moved, and would be infinitely bad !)

## Stopping condition
The stopping conditions are directly linked to the fitness function above. It is the moment when the algorithm stops the main loop of selection, mutation, crossover and yields a winner.\
This algorithm has two phases - thus two stopping conditions, the first result beeing pipelined into the second phase.\
Of course, aditionnally to these two stopping condition, the "time" condition is implemented. But it is not interessting and will not be discussed here.
### Phase I - growing phase
The growing phase is fast : About 10 iterations on a 40*40 grid. Its stopping condition is easy : **Stop when one of your individual is are on the end_cell**\
```if fitnessesAtTarget:```\
```    toolbox.register("mate", tools.cxOnePoint)```\
\
The second phase can then go on, with one - or many- chromosomes reaching the target.\
As there are 10 winners in the tournament, the 10 "best chromosomes" are selected to go on phase II. They contain at least one already reaching the target, probably in an suboptimal way.\
**It is essential that the growing algorithm stops here** : As the growing goes, the individuals become exponentially bigger. The computation of the fitness function is directly linked to the length of the individuals : Letting it go further will lead to disastrous wait time for each iteration, and the result would not be pretty.\
The force of this growing phase is to converge very fast : The first few iteration have chromosomes that could possibly not reach the target because they are too small, but that will slowly converge to the solution iteration by iteration. But this force is also a weakness after that point - we can not continue with this method when the target is reached, as we do not want bigger chromosomes\
The labyrinth_speedy.py implementation stops there.\

### Phase II - refinement phase and stagnancy avoidance
During the refinement phase, the fitness function yields a tuple :
```(ratio, length)```\
The length is used in this second refinement phase.\
We have only chromosomes close to the path, with the winner already in the pool.\
The goal is to refine the path. The fitness function naturally tries to minimize the second parameter, even though it prioritizes the first one. Therefore, by changing the crossover of the individuals from "growing" to "fixed size", the individuals will naturally converge to a better path.\
\
This value can never reach 0. However, it can not continually go smaller either. As such, a notion of "stability" - or its opposite, "stagnancy" is introduced.
* During this phase, at each iteration, the minimun value of all the path values (fit[2]) is kept in memory
* A counter of stagnancy is incremented each time the length stagnates between iterations
* When the stagnancy counter reaches the fixes limit (5), the algorithm stops, judging it can not find a smaller path after failing to do so 5 times.

## Deap algorithm tools
The cycle of a genetic algorithm goes through steps :
* Selection
* Mutation
* Crossover

Each of these steps is important, and dictates the behavior of the algorithm. Let's review them.
### Selection
For both phases, the selection phase is the same :
* Seltournament(pop, tournSize)

The tournament selects the best individuals - not THE global best, but the local best amongst a portion of the population.\
This selection is adapted to both of our phases, softening the "local maximum" problem while keeping good individual through cycles.\
\
\
It has been thought but not tested to use once a selBest(pop, reaching-indiv-count) when going from phase 1 to phase 2, to select only the individuals that reach the target. It could introduce a very heavy diversity problem during phase 2, or it could lead to a big amelioration of its refinement. But the implementation of this feature would have taken time that i did not have.

### Mutate
The mutation function used is the same for both phases.
```toolbox.register("mutate", tools.mutUniformInt, low=ENCODING_MIN, up=ENCODING_MAX, indpb=0.1)```\
As the code work with integers (0->3) for directions, the function can not be "flipbit".\
The "mutUniformInt" built-in deap function mutates the individual by changing one of its gene with a random integer.\
The borns of the integers are simply the smaller and bigger value of the code, and the probability to flip each integer is kept at 10%.
### Crossover


## Hyper-parameters
### Chromosome length
### Pop size and tournament
### Mutations probabilities

## Pros, cons and ameliorations

## Conclusion
The fixed-length chromosomes method is :
* Very slow at converging to the solution
* Very good at optimizing the solutions
* Easily trapped by obstacles
The growing-length chromosomes method is :
* Very fast at converging to the solution
* Very bad (incapable) of optimizing solution
* Not easily trapped by obstacles (also due to the ratio)

Combining both strategies yielded very good results, altghough the hyper-parameters are more optimized for phase1 and are not changed to fit more to phase 2.\
This implementation represents a successfull proof-of-concept of the application of both strategies to converge rapidly to an acceptable solution.\
This philosophy could be pushed further, maybe by separating the two phases in different "while" loop to make the code more understandable, and to trully differentiate and optimize each phase. This could mean pushing the strategies to their true limits, and could yield even better results while staying very fast.\
The dual-strategies algorithm is also very flexible with the given grids - adapting its size to the shape and size of the terrain.\
Finally, the optimization of the paths is not a focus point of this algorithm. The speed is clearly the objective here, and the results show that the results path are always good, but not everytime quite perfect - with a high risk of local maximum due to phase I. But this is expected with the current implementation.