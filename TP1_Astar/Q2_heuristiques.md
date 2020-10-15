# Question 2 : Parmi ces heuristiques, lesquelles sont admissibles ?

## Problème de départ
Supposons que l’on veuille se rendre à la ville B. 
Pour tout noeud n, on va s’intéresser aux heuristiques suivantes
* h0(n) = 0
* h1(n) = "la distance entre n et B sur l'axe des x"
* h2(n) = "la distance entre n et B sur l’axe des y"
* h3(n) = "la distance à vol d’oiseau entre n et B"
* h4(n) = "la distance de Manhattan entre n et B"

## Conditions d'admissibilité
### Théorème 
Une fonction heuristique est admissible si 
* ∀n, 0 ≤ h(n) ≤ h*(n) avec h*(n) = coût optimal réel de n au but
* Autrement dit : ne surestime jamaisle coût réel
* Une fonction heuristique admissible est donc toujours optimiste !

## Analyse des heuristiques
L'analyse des heuristiques consiste à déterminer si les heuristiques sont admissibles, càd si elles sont toujours optimistes

### H0(n)
* h0(n) = 0</ul>
__Admissible car l'heuristique converge__, cependant, l'intuition indique que ce n'est pas efficace...\
Plus précisément, cela revient à _ne pas utiliser d'heuristique et à effectuer une recherche aveugle_.

### H1(n)
* h1(n) = "la distance entre n et Bsur l'axe des x"</ul>
Prenons le cas de la ville B à atteindre depuis le point n, et fixons le point A à l'angle droit :\
A -- n\
|\
B\
Nous réfléchissons avec une distance sur l'axe des x.\
Le cas trivial est que les ville B et n soient horizontales, avec A=B dans ce cas :\
B -- n\
Dans ce cas, on a h*(n) = h1(n) = 1. L'heuritstique est admissible.\
Ensuite, la ville B peut se déplacer sur l'axe verticale. Cependant, un déplacement sur l'axe verticale augmente H*(n) sans changer h1(n). __L'heuristique reste donc optimiste, et admissible__.\
_L'intuission nous indique qu'omettre l'axe Y peut quand même mener à certaines erreurs de raisonnement, et donc de perte de temps de la part de l'algorithme_


### H2(n)
* h2(n) = "la distance entre n et B sur l’axe des y"</ul>
Même raisonnement que pour h1(n) : __Admissible__, _mais omettre l'axe X est un risque de perte de temps._

### H3(n)
* h3(n) = "la distance à vol d’oiseau entre n et B"</ul>
Dans la meilleur des cas : Les deux villes sont directement reliées, et h3(n) = h*(n)\
Dans le pire des cas : Les deux villes ne sont pas reliées, donc h3(n) < h*(n).
En effet, la plus petite distance entre deux points étant une droite, la distance à vol d'oiseau ne peut pas être superieure à une autre distance passant par un point intermediaire, sauf dans un monde avec téléportation.\
L'__heuristique est donc admissible__ _si et seulement si les villes ne disposent pas de téléporteur ou de mécanisme de distortion de l'éspace-temps._

### H4(n)
* h4(n) = "la distance de Manhattan entre n et B"</ul>
Les villes peuvent être reliées directement par une droite.\
La distance de manhattan consiste à faire (abs(x) + abs(y)).\
Selon le théorène des triangle, on a : d(B,n) <= d(B,a) + d(a,n)\
Ainsi, le théorème ne pourra jamais être optimiste. Mathématiquement :
* Dans le meilleur des cas, les villes sont reliées par des routes perpendiculaires aux axes {x, y}, et h4(n)=h*(n)
* Dans le pire des cas, du moment que la route est oblique, h4(n)>h*(n)
L'heuristique est donc __non admissible.__
