## Suivi Projet Artishow
## 15 Février 2026 (S0)
Entretien avec Xhevahire TËRNAVA en présentiel à Télécom pour qu'elle puisse nous introduire le projet et nous expliquer ce qu'on doit réaliser.

## 16 Février 2026
*Théophile* : Premier code permettant d'éxécuter pour un programme donné la commande "--help" dans le terminal et de copier la réponse dans un fichier temporaire.


## 20 Février 2026 (S1)
*Tout le monde* : Entretien pour présenter notre première version du planning.
- Baptiste: 
    - Ajout du planning au format gantt

## 16 mars 2026
*Tout le monde* : Entretien pour présenter notre première version du compteur
- Choix de la stratégie de comptage
- Création d'un document pour instaurer les règles de comptage pour les futurs clients


## Objectifs prochaine séance
- Diversification 
- Début de visualisation du nombre d'options

## 2 Avril 2026
- Baptiste : 
    - Code capable de compter les programmes de base (ls,cat, grep, sed, sort...) avec la commande help 
- Objectif: améliorer le code pour compter le nombre d'options avec des programmes utilisant autre chose que help

## 14 Avril 2026
- Yoan: Implémentation d'une interface graphique simple pour tester le code 
- Les codes code_final.py et code_v2.py fonctionnent pour des programmes usuels
- Objectifs prochaine séance: faire une documentation qui regroupe les sources et tout un tas d'explication, ajouter des features à l'interface graphique (détails, graphes crhonologiques, graphe option actuelle), faire un readme pour users 

## 20 Avril 2026
- Baptiste: 
    - Tests du code code_final.py 
    - Ajout de l'option -usage

- Implémentation d'une solution pour renvoyer un fichier csv pour les futurs tracés

## 28 Avril 2026
- Yoan: modification visuelle de l'interface, réflexion sur la manière d'intégrer des graphiques à l'interface

## 1 Mai 2026
- Yoan: création d'un fichier test test_graph.py pour tracer le nombre d'options en fonction des programmes testés 

## 4 Mai 2026
-Yoan: succès du tracer pour le code test_graph.py, implémentation du tracer dans l'interface avec comparaison de quelques programmes usuels. Il semble qu'il y ait un problème avec le nombre d'options (cela n'affiche pas la totalité du nombre d'options).

## 5 Mai 2026
-Baptiste: 
    - Ajout interface numero 2 
    - Amelioration de code_v2 et code_final : prise en compte des aides -h all et --help full

## 13 Mai 2026
- Baptiste:
    - Restructuration complete du git selon les conseils de l'encadrante.
- Théophile:
    - Ajout source
    - Début programme pour tracer le graphique de l'évolution temporelle du nombre d'options d'un programme

*Tout le monde* : Réunion avec Xhevahire TËRNAVA en présentiel à Télécom pour discuter de l'avancement.
    => Feedbacks :
        - Bonne interface et graph
        - Il faut adapter notre algorithme aux programmes qui nécessitent -h full (ex. curl, ...), réfléchir à quoi considérer comme une option (avec les espaces ou dash avant le nom de l'option)
        - Focus d'abord sur certains programmes à analyser en profondeur avant d'automatiser tout notre algorithme
        - Tirer des static data (nos résultats qu'on a trouvé) et des dynamic data
        - Il faut mieux structurer notre projet et notre git (/src/.py et /src/.sh puis /src/script/version....py , /data/.csv , /docs, /codebases/curl et /codebases/cat etc, /analysis-visualisations_UI, presentations/)
        - Ne pas analyser les programmes installés
        - Pour Baptiste : télécharger la dernière version de certains programmes et travailler dessus en documentant dans /docs la version, le repo git, etc (CLOC)
        - Split les tâches pour le poster de présentation

*Objectifs pour la prochaine séance :* Adapter notre algorithme pour les programmes qui nécessitent "-h full" et renvoient une liste d'options sans dash.

## 21 Mai 2026
- Baptiste:
    - Renommage et modification des scripts python selon les conseils de l'encadrante.

## 26 Mai 2026
*Tout le monde* : Présentation de notre projet devant d'autres élèves.
=> Feedbacks des audits : https://grist.r2.enst.fr/o/docs/dxB11dMKKnN4/Artishow-2026/p/16

## 6 Juin 2026
- Yoan :
    - Ajout d'une page statique pour la présentation du projet
- Baptiste :
    - Amelioration du regex dans le script compteur
- Théophile :
    - Début affiche de présentation du projet avec réflexion sur le contenu et la mise en page
    => https://canva.link/pm4tcq6ijldun7b 

## 9 Juin 2026
- Yoan :
    - Modif de interface2.py pour adopter le nouveau code compteur 
    - Modif de graph.py pour adopter le nouveau code compteur
    - Modif de la page statique
- Loïs :
    - Création de fichiers csv pour des dizaines de programme de Coreutils contenant le nombre d'options en fonction de la version du programme
- Théophile et Loïs : 
    - Tracer le graphe d'évolution temporelle du nombre d'options pour plusieurs programmes (à vérifier avec la prof encadrante car il n'y a pas vraiment d'augmentation globalement)

## 10 Juin 2026
*Tout le monde* : Réunion avec Xhevahire TËRNAVA en présentiel à Télécom
    - Présentation du programme qui permet de download toutes les versions disponibles et créer le fichier csv avec le nombre d'options selon la version.
    - Présentation de la modif du code du compteur (modif REGEX)
    - Présentation des 2 graphes 
    - Présentation du début du poster
    - Présentation de la page statique
    - Feedbacks : 
        - Essayer le programme avec ffmpeg
        - Ne pas mettre un tableau sur le poster
        - Moins de texte
        - Vendre le projet en disant que c'est le premier outil de ce genre, que c'est super utile
        - Finir le poster en se posant la question du nombre d'option dans le futur avec l'usage de l'IA qui facilite la programmation
        - Pour l'évolution faire une moyenne de l'augmentation du nombre d'options dans le temps 
        - Sur la page statique faire un menu qui propose 2 choses: un outils statique qui permet de rentrer un programme et une version puis renvoie le nombre d'options (en s'appuyant sur notre base de données), ainsi que la possibilité de télécharger notre outils dynamique ainsi qu'un readme pour dire aux utilisateurs comment run notre programme. 
    - Objectifs:
        - Loïs: implémenter toybox
        - Baptiste: aider à rendre le programme dynamique et remplir la base de données des csv files (pour l'outils statique)
        - Yoan: intégrer les 2 outils dans la page statique (outils statique et dynamique). Faire un menu avec: côté dynamique (proposer le download de l'outil avec readme), côté "pick" (faire un outils où on rentre le nom du programme, l'implémentation (TOYBOX, GNU, BUSYBOX)), côté history (visuels sur l'évolution du nomnbre d'options), côté "about" (poster, pdf expliquant le projet).
        - Théophile: modifier le poster pour le rendre plus lisible/attractif
### Travail effectué
- Baptiste : 
    - Création de programme créant le fichier zip
    - Création de la page HTML "téléchargement" pour le site