# Selection des 15 commandes

Le graphe retient des commandes largement connues sous Unix et dont les donnees
montrent une augmentation globale du nombre d'options. La selection cherche un
equilibre entre trois criteres :

- une commande couramment utilisee ou facilement identifiable ;
- une serie couvrant plusieurs versions et plusieurs annees ;
- une hausse visible entre la premiere et la derniere mesure.

Les lignes Coreutils couvrent principalement la periode 2005-2026. Les lignes
Toybox couvrent des periodes plus courtes, car certaines commandes ont ete
ajoutees progressivement a cette suite.

| Suite | Commande | Premiere mesure | Derniere mesure | Evolution |
|---|---|---:|---:|---:|
| Coreutils | `ls` | 91 (2005) | 97 (2026) | +6 |
| Coreutils | `sort` | 42 (2005) | 59 (2026) | +17 |
| Coreutils | `date` | 21 (2005) | 31 (2026) | +10 |
| Coreutils | `chmod` | 16 (2005) | 23 (2026) | +7 |
| Coreutils | `cut` | 17 (2005) | 25 (2026) | +8 |
| Coreutils | `du` | 44 (2005) | 49 (2026) | +5 |
| Coreutils | `tail` | 20 (2005) | 24 (2026) | +4 |
| Toybox | `grep` | 20 (2013) | 43 (2025) | +23 |
| Toybox | `tar` | 49 (2019) | 73 (2025) | +24 |
| Toybox | `ls` | 26 (2012) | 39 (2025) | +13 |
| Toybox | `cp` | 13 (2008) | 23 (2025) | +10 |
| Toybox | `mv` | 4 (2013) | 11 (2025) | +7 |
| Toybox | `sed` | 7 (2015) | 12 (2025) | +5 |
| Toybox | `ps` | 19 (2015) | 25 (2025) | +6 |
| Toybox | `head` | 1 (2012) | 6 (2025) | +5 |

`sort`, `date`, `grep` et `tar` illustrent les augmentations les plus fortes.
`cp`, `mv`, `chmod` et `sed` montrent l'enrichissement progressif de commandes
classiques. `ls` est volontairement conserve dans les deux suites afin de
comparer l'evolution de deux implementations d'une meme commande. Enfin, `du`,
`tail`, `ps` et `head` apportent des exemples de hausses plus moderees, mais
regulieres ou durables.

Le nombre d'options mesure les interfaces exposees par les binaires analyses.
Il ne constitue pas a lui seul une mesure de qualite ou de complexite interne.
