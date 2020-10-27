# Question 4 : Research

## L’utilisation des différentes heuristiques a-t-elle une influence sur l’efficacité de la recherche ? (en termes du nombres de noeuds visités)
Oui ! Durant les test, il est très facile de se rendre compte que les heuristiques choisies ont une influence sur le nombre de villes visitées.\
\
Par exemple, en prenant les deux extrêmes admissibles (Heuristique __triviale__ =0, heuristique __birdview__), on voit que la birdview est systèmatiquement plus efficace.\
Cela est du au fonctionnement de A* :\
``` f(n) = g(n) + h(n) ```
\
g étant le coût du chemin, il ne change pas lorsque l'heuristique change. C'est donc à h(n), l'heuristique, d'apporter une information supplémentaire pour discriminer les chemins et les évaluer.\
L'idée est que plus l'heuristique donne d'information, plus A* sera efficace. Toujours avec la borne superieur de la réalité : pour rester admissible, la fonction ne suréstime jamais le coût.\
Ainsi, l'heuristique "parfait" est une heuristique qui pourra toujours donner une éstimation 'parfaite' et jamais superieure du coût réel du noeud.\
\
Dans notre cas, __birdview__ est l'algorithme qui se rapproche le plus de la réalité (sans être parfait, il ne tient pas compte de la forme/courbure/etc des routes ou des vitesses/obstacles de parcours), tandis que __trivial__ est celui qui donne le moins d'information (en faites, il revient même à faire le cas dégénéré de A* - c'est une recherche en coût uniforme sans apporter l'amélioration de la recherche greedy). Les résultats du pathfinding vérifient cette théorie.\
\
Si l'heuristique dépasse la réalité, càd n'est plus admissible, comme __Manhattan__, on gagne encore plus de performances. On est alors sur un algorithme _greedy_, encore plus performant que __birdview__, mais qui n'offre pas la guarantie de l'algorithme en coût uniforme de toujours trouver le chemin le plus optimal.


## Pouvez-vous trouver des exemples où l’utilisation de différentes heuristiques donne des résultats différents en termes de chemin trouvé ?

Oui ! Durant les recherches de pathfinding, on s'aperçoit parfois que la distance de manhattan peut renvoyer un chemin incorrect.\
C'est le seul qui renvoit parfois des résultats incorrects, car c'est le seul non admissible : Il peut suréstimer les coûts (et le fait souvent, dès que la route est oblique).\
\
Exemple :
En mode ligne de commande, tapez :\
``` python main.py paris prague ```\
Ce qui donne le résultat partiel (les 3 premiers heuristiques donnent le résultat identique au 4ème, avec un nombre de visite superieur):\
\
Time consummed by function aStar: 0.0s\
heurstic BIRDVIEW. 9 analysed cities, total weight 1089\
path : Paris (1062,870) => Brussels (983,992) => Amsterdam (957,1096) => Munich (679,835) => Prague (574,975).\
\
Time consummed by function aStar: 0.0s\
heurstic MANHATTAN. 6 analysed cities, total weight 1128\
path : Paris (1062,870) => Brussels (983,992) => Amsterdam (957,1096) => Hamburg (774,1175) => Berlin (626,1131) => Prague (574,975).\
\
On voit que la recherche avec manhattan -bien que plus efficace en terme de villes- n'a pas rendu le chemin le plus court.\
Ceci est dû au fait qu'un algorithme A* avec heuristique admissible suit le principe de la recherche en coût uniforme : Le chemin le plus court sera __toujours renvoyé__. Dans notre cas, les algorithmes __trivial__, __x__, __y__ et __birdview__ renvoient toujours le chemin le plus court.\
Manhattan est plus efficace car, suréstimant la réalité, elle penche plus vers un algorithme de recherche _greedy_, qui n'offre pas de guarantie de chemin optimal.\
\
A retenir : A* est un algorithme de recherche mêlant la recherche en coût uniforme __et__ la recherche greedy. Tant que l'heuristique est admissible, la guarantie de chemin optimal de coût uniforme est respecté. Dès qu'elle ne l'est plus, l'heuristique prend le pas - on est alors sur une recherche greedy, et le chemin obtenu n'est plus guarantit d'être optimal. Plus l'heuristique apporte d'information, plus la recherche est efficace (en nombre de noeuds visités)

## Dans un cas réel, quelle heuristique utiliseriez-vous ? Pourquoi ?
Toute heuristique admissible fournira le chemin le plus court identique. Cependant, on a vu que les heuristiques admissibles fournissant le plus d'information possible améliorent grandement l'efficacité de la recherche. C'est la valeur de h dans f = g + h qui va dicter les villes parcourues.\
Dans notre cas, c'est __birdivew__ qui est la plus efficace en étant optimale : Elle renvoit des informations entre les villes sur les 2 axes, tandis que les trois premières ne le font pas. C'est celle qui renvoit le plus d'informations en restant admissible. __C'est celle que je privilégierait sans autre information de contexte.__\
__Manhattan__ est à part car étant non admissible, elle ne respecte pas l'axiome d'A* et n'offre aucune guarantie de rendre le chemin le plus court. Elle est cependant plus efficace, et pourraît éventuellement être préférée si les performances sont cruciales, et que le chemin le plus court ne l'est pas (Ex : Petit logiciel embarqué ? Pourquoi pas ?). Mais c'est __très marginal__.

## Aller plus loin : chercher la définition d’heuristique “consistente” ou “monotone”
"In the study of path-finding problems in artificial intelligence, a heuristic function is said to be consistent, or monotone, if its estimate is always less than or equal to the estimated distance from any neighbouring vertex to the goal, plus the cost of reaching that neighbour." ([wikipedia]([wikipedia](https://en.wikipedia.org/wiki/Consistent_heuristic)))\
\
h1 ≤ c(n1,n2) + h2
\
Un heuristique consistente a un coût h(n1)\
On peut aller au noeud n2, avec un cout C. \
n1 --- C --- n2\
On a l'heuristique h(n2)\
L'heuristique est consistente ssi le coût h(n1) <= h(n2) + C, càd que la valeur h(n1) n'est jamais superieure à la valeur du cout d'un déplacement plus l'heuristique sur le nouveau noeud sur lequel on s'est déplacé.

### Quel est son impact sur les performances de l’algorithme A* ?
"In the A* search algorithm, using a consistent heuristic means that once a node is expanded, the cost by which it was reached is the lowest possible, under the same conditions that Dijkstra's algorithm requires in solving the shortest path problem"([wikipedia]([wikipedia](https://en.wikipedia.org/wiki/Consistent_heuristic)))\
\
A* devient bien plus efficace car il ne __repasse jamais__ sur un noeud déja traversé. Il n'y a donc plus besoin de garder une historique, et il n'y a plus besoin d'effectuer les checks sur la frontière (déja enlevé ici grâce à la heapQ) et sur l'history.\
Il y a donc :
* Gain d'efficacité en temps (check history)
* Gain mémoire (pas besoin de garder l'history)

### Si vous assurez à votre algorithme une heuristique monotone, comment pourriez-vous améliorer votre de code ?
Mon code tient actuellement compte de la re-traversée d'une ville avec un meilleur coût de f.\
Je retiens les villes et leurs F respectifs dans un dictionnaire history {ville:chemin.f}. Cela veut dire que pour chaque ville, je dois vérifier si elle a déja été traversée, si mon nouveau chemin est plus efficace, etc... Car un 2ème chemin peut très bien être exploré en second mais arriver "plus vite" à la ville en question, à cause de l'inconsistence des heuristiques.\
\
Si les villes ne peuvent pas être traversées deux fois, la solution la plus simple pour améliore le code serait de se débarasser du superflux :
* Plus d'history (mémoire)
* Plus de comparaison des F par rapport aux anciennes villes si elles sont dans l'history (temps)
* On garde uniquement la frontière, sans effectuer le check "est-ce que la ville est déja dans la frontière ?" (déja le cas, grâce à heapQ)

### Parmi les 5 heuristiques ci-dessus, il y en a des monotones? Si non, proposer une héuristique monotone pour notre problème du voyageur (pas besoin de l’implémenter)
1. __trivial__ Oui : 0 <= cout + 0
2. __x__ Oui : h1 <= c+h2 car dans le pire des cas, c = différence(h1,h2) si les villes sont sur le même axe horizontal. Sinon, la différence en Y rajoute du poid au coût mais pas à l'heuristique.
3. __y__ Oui : Pareil, h1 <= c+h2 car si les villes sont alignées verticalement, c= différence(h1,h2), et si les villes ne sont pas alignées, cela rajoute du poid au coût mais pas à la différence des heuristiques
4. __birdview__ Oui : le birdview renvoit la distance euclidienne entre la ville et la destination. Si on imagine que la destination est au centre, le pire des cas possible est si les villes sont alignées A--B--destination. Dans ce cas, diff(h1,h2) = C, car le déplacement en ligne droite = la différence de rayon entre les deux villes. Si les villes ne sont pas alignées, on aura forcément c > diff(h1,h2) car la différence (h1,h2) = différence de rayon entre R1,R2 les rayons des cercles C1,C2 centrés en destination et passant par les villes. Cette différence de rayon est forcément inferieur au coût de déplacement si les villes ne sont pas alignées, et égal si elles le sont.
5. __manhattan__ : Non : N'étant pas admissible, l'heuristique peut suréstimer la valeur du cout de déplacement. On peut donc se retrouver avec h1 > c+h2 si.Par exemple, si h1 et h2 ont une liaison en ligne droite, manhattan suréstime le trajet entre h1 et h2 (car il prend le trajet "rectangulaire"). Si le trajet de h2 à déstination est parfaitement rectangulaire, la suréstimation est donc sur le cout C entre h1 et h2, diff(h1,h2) > C (la différence des heuristiques est plus grande que le coût), donc h1 > c + h2.<ul>


Pour l'heuristique, j'utiliserais __Birdview__ si je n'ai aucune limitation technique (liée au hardware). C'est celle qui est la plus efficace des 4 premières, elle est admissible, et elle est consistente. J'enlèverais le check sur l'history.\
Si vraiment le hardware est limité, je pourrais envisager le __Manhattan__, en gardant à l'ésprit que le chemin trouvé n'est pas forcément le plus optimal.