# Recherche d'un encodage pour représenter un problème donné

* Étant donné les chiffres 0 à 9 et les opérateurs +, -, * et /, trouver une séquence qui représentera un nombre cible donné. Les opérateurs seront appliqués séquentiellement de gauche à droite.
* Ainsi, étant donné le nombre cible 23, la séquence 6+5*4/2+1 serait une solution possible.
* Si 75.5 est le nombre choisi, alors 5/2+9*7-5 serait une solution possible.

## Schématiser un encodage et les différentes étapes pour résoudre ce problème avec un algorithme génétique

### Codage trival</ul>
Ce code part du principe que chaque gène est codé sur un short (8bits), et est considéré comme une valeur numérique entre 0 et 9. Les valeurs gènes d'opérations (+-*/) sont codés sur un short aussi, mais seules les valeurs 0-3 sont valides. On a alors une succéssion de gènes numériques/opérations :\
Chromosome 5/2+9 : |5|3|2|1|9| - total 40 bits\
Avantage : Facile à coder/décoder, facile à mettre en place\
Désavantage : Peut économe en place (un short de 8 bits pour coder 0-9 et 0-3)

### Codage semi-binaire</ul>
Ce code améliore le codage des opérations. Prenant des valeurs de 0 à 3, on a simplement besoin de 2 bits :\
```00 01 10 11```\
```+  -  *  /```\
Chromosome 5/2+9 : |5(8b)|11|2(8b)|00|9(8b)| - total 28 bits\
Un peut plus dur à mettre en place (il faut coder en binaire), mais à priori, comme il n'y a de toute façon que 4 opérations possibles (tout l'espace engendré par 2^2), on a pas de vérification à mettre en place pour les mutations - toutes les mutations d'opération sont valables

### Codage binaire</ul>
Ce code améliore l'espace pris par les chiffres entre les opérations. Prenant des valeurs de 0 à 9, on a besoin de log2(9)=4 bits.\
```00 01 ..... 1001```\
```0  1  .....  9```\
Chromosome 5/2+9 : |0101|11|0010|00|1001| - total 16bits\
Avantage : Beaucoup plus économe en place\
Désavantage : Durant les mutations, il faut prendre garde : Un chiffre ne peut pas prendre une valeur >9. Or, l'espace engendré par 2^4bits = 16 possibilitées (0-15). Il faut donc mettre des vérifications en place.