# Question 2 : Parmi ces heuristiques, lesquelles sont admissibles ?

## Problème de départ
Supposons que l’on veuille se rendre à la villeB. 
Pour tout noeud n, on va s’intéresser aux heuristiques suivantes
* h0(n) = 0
* h1(n) ="la distance entrenetBsur l’axe desx"
* h2(n) ="la distance entrenetBsur l’axe desy"
* h3(n) ="la distance à vol d’oiseau entrenetB"
* h4(n) ="la distance de Manhattan entrenetB"

## Conditions d'admissibilité
### Théorème 
Une fonction heuristique est admissible si 
* ∀n, 0 ≤ h(n) ≤ h*(n) avec h*(n) = coût optimal réel de n au but
* Autrement dit : ne surestime jamaisle coût réel
* Une fonction heuristique admissible est donc toujours optimiste !

## Analyse des heuristiques
L'analyse des heuristiques consiste à déterminer si les heuristiques sont admissibles, càd si elles sont toujours optimistesdcf

### H0(n)

### H1(n)

### H2(n)

### H3(n)

### H4(n)