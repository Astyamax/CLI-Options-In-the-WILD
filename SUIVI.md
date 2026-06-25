# Suivi du projet Options in the Wild

Ce fichier récapitule les réunions, décisions, travaux réalisés et objectifs du projet. Il est organisé par ordre chronologique.

## Février 2026

### 15 février 2026 - S0

**Réunion**

- Rencontre en présentiel avec Xhevahire TËRNAVA à Télécom.
- Introduction du sujet et clarification des attentes du projet.

### 16 février 2026

**Travail réalisé**

- Théophile : premier code permettant d'exécuter `--help` pour un programme donné et de copier la sortie dans un fichier temporaire.

### 20 février 2026 - S1

**Réunion**

- Présentation de la première version du planning.

**Travail réalisé**

- Baptiste : ajout du planning au format Gantt.

## Mars 2026

### 16 mars 2026

**Réunion**

- Présentation de la première version du compteur.

**Décisions**

- Choix de la stratégie de comptage.
- Création d'un document de règles de comptage pour les futurs utilisateurs.

**Objectifs**

- Diversifier les programmes testés.
- Commencer la visualisation du nombre d'options.

## Avril 2026

### 2 avril 2026

**Travail réalisé**

## 24 Juin 2026
*Tout le monde* : Réunion avec Xhevahire TËRNAVA en présentiel à Télécom
    - Objectifs pour le 25 juin :
        - Rajouter la bibliographie sur le pdf de présentation 
        - Reprendre un peu la strucuture du pdf de présentation
        - Clean le projet
        - Analyser la complexité de quelques programmes
        - Préparer une sorte de teaser 
### Travail effectué
    - Yoan :
        - Moification des graphes sur la static page 

- Baptiste : code capable de compter les options de programmes usuels (`ls`, `cat`, `grep`, `sed`, `sort`, etc.) à partir de la commande d'aide.

**Objectif**

- Améliorer le compteur pour les programmes qui utilisent autre chose que `--help`.

### 14 avril 2026

**Travail réalisé**

- Yoan : implémentation d'une interface graphique simple pour tester le compteur.
- Les fichiers `code_final.py` et `code_v2.py` fonctionnent pour plusieurs programmes usuels.

**Objectifs**

- Rédiger une documentation regroupant les sources et les explications.
- Ajouter des fonctionnalités à l'interface graphique : détails, graphes chronologiques, graphe des options actuelles.
- Rédiger un README utilisateur.

### 20 avril 2026

**Travail réalisé**

- Baptiste : tests de `code_final.py`.
- Baptiste : ajout de la prise en charge de l'option `-usage`.
- Mise en place d'une solution pour générer un fichier CSV utilisable dans les futurs tracés.

### 28 avril 2026

**Travail réalisé**

- Yoan : modifications visuelles de l'interface.
- Yoan : réflexion sur l'intégration de graphiques dans l'interface.

## Mai 2026

### 1 mai 2026

**Travail réalisé**

- Yoan : création de `test_graph.py` pour tracer le nombre d'options en fonction des programmes testés.

### 4 mai 2026

**Travail réalisé**

- Yoan : premier tracé fonctionnel avec `test_graph.py`.
- Yoan : intégration du tracé dans l'interface avec comparaison de quelques programmes usuels.

**Problème identifié**

- Le nombre d'options affiché semble incomplet pour certains programmes.

### 5 mai 2026

**Travail réalisé**

- Baptiste : ajout d'une seconde interface.
- Baptiste : amélioration de `code_v2` et `code_final` avec prise en compte de `-h all` et `--help full`.

### 13 mai 2026

**Travail réalisé**

- Baptiste : restructuration complète du dépôt Git selon les conseils de l'encadrante.
- Théophile : ajout de sources.
- Théophile : début du programme de visualisation de l'évolution temporelle du nombre d'options.

**Réunion**

- Réunion en présentiel avec Xhevahire TËRNAVA à Télécom.

**Retours**

- L'interface et les graphes sont encourageants.
- Adapter l'algorithme aux programmes nécessitant `-h full`, comme `curl`.
- Clarifier ce qui doit être considéré comme une option, notamment pour les options avec espaces ou tirets.
- Commencer par analyser certains programmes en profondeur avant de chercher à tout automatiser.
- Produire des données statiques issues des résultats obtenus, en plus des données dynamiques.
- Mieux structurer le projet : `src/`, `data/`, `docs/`, `codebases/`, analyses, visualisations, interface et présentations.
- Ne pas analyser les programmes installés localement.
- Documenter les versions téléchargées, les dépôts Git et les mesures associées.
- Répartir les tâches pour le poster.

**Objectif**

- Adapter le compteur aux programmes dont l'aide complète ne renvoie pas forcément une liste d'options commençant par un tiret.

### 21 mai 2026

**Travail réalisé**

- Baptiste : renommage et modification des scripts Python selon les conseils de l'encadrante.

### 26 mai 2026

**Présentation**

- Présentation du projet devant d'autres élèves.
- Retours d'audit : https://grist.r2.enst.fr/o/docs/dxB11dMKKnN4/Artishow-2026/p/16

## Juin 2026

### 6 juin 2026

**Travail réalisé**

- Yoan : ajout d'une page statique de présentation du projet.
- Baptiste : amélioration des expressions régulières dans le compteur.
- Théophile : début de l'affiche de présentation, avec réflexion sur le contenu et la mise en page.
- Lien Canva : https://canva.link/iry1ais1wmsqqi1

### 9 juin 2026

**Travail réalisé**

- Yoan : adaptation de `interface2.py` au nouveau compteur.
- Yoan : adaptation de `graph.py` au nouveau compteur.
- Yoan : modification de la page statique avec trois menus à compléter.
- Loïs : création de CSV pour plusieurs dizaines de programmes Coreutils, avec le nombre d'options selon la version.
- Théophile et Loïs : tracé de l'évolution temporelle du nombre d'options pour plusieurs programmes.

**Point à vérifier**

- Les graphes ne montrent pas forcément d'augmentation globale nette ; ce point doit être discuté avec l'encadrante.

### 10 juin 2026

**Réunion**

- Réunion en présentiel avec Xhevahire TËRNAVA à Télécom.

**Présentations**

- Programme de téléchargement des versions disponibles et génération des CSV historiques.
- Modification du compteur et des expressions régulières.
- Deux premiers graphes.
- Début du poster.
- Page statique.

**Retours**

- Tester le programme avec `ffmpeg`.
- Éviter les tableaux dans le poster.
- Réduire la quantité de texte.
- Mieux valoriser le projet comme un outil original et utile.
- Conclure le poster sur l'évolution future du nombre d'options, notamment avec l'usage de l'IA.
- Pour l'évolution, calculer une moyenne de l'augmentation du nombre d'options dans le temps.
- Sur la page statique, proposer :
  - un outil statique pour rechercher un programme, une implémentation et une version ;
  - le téléchargement de l'outil dynamique ;
  - un README expliquant comment exécuter l'outil.

**Objectifs attribués**

- Loïs : intégrer Toybox.
- Baptiste : aider à rendre le programme dynamique et remplir la base de CSV pour l'outil statique.
- Yoan : intégrer les outils dans la page statique.
- Théophile : rendre le poster plus lisible et plus attractif.

**Travail réalisé après réunion**

- Baptiste : création du programme générant le fichier ZIP.
- Baptiste : création de la page HTML de téléchargement.

### 22 juin 2026

**Réunion**

- Réunion en présentiel avec Xhevahire TËRNAVA à Télécom.

**Objectifs de fin de semaine**

- Finaliser la page statique avec présentation des résultats, téléchargement des données CSV et téléchargement de l'outil ZIP.
- Créer un CSV historique et un CSV des dernières versions.
- Exclure les programmes pour lesquels l'outil échoue ou détecte zéro option.
- Supprimer les CSV individuels si les fichiers agrégés suffisent.
- Énumérer dans les détails techniques les programmes testés et ceux pour lesquels l'outil n'a pas fonctionné.
- Préparer la présentation orale et la démonstration pour le jury du 26 juin.
- Nettoyer le fichier de suivi.
- Nettoyer le dépôt Git.

**Objectifs pour le 24 juin**

- Finaliser la page statique.
- Créer les CSV agrégés.
- Préparer la démonstration technique.

**Travail réalisé**

- Baptiste : correction d'un bug dans le téléchargement du fichier ZIP.
- Baptiste : réintégration de la page de téléchargement dans la page statique.
- Yoan : modification de la page statique pour accueillir trois sections : recherche, téléchargement et présentation des résultats.

### 23 juin 2026

**Travail réalisé**

- Baptiste : rédaction du PDF de détails techniques.
- Baptiste : ajout du PDF sur la page statique.
- Théophile : ajout de `data/create_csv.py` pour générer :
  - un CSV `latest` avec le nombre d'options des dernières versions ;
  - un CSV `history` avec le nombre d'options par année.
- Théophile : génération des fichiers `latest` et `history` depuis les CSV du dossier `csv`.
- Théophile : création de `failed_programs.txt`, qui liste les programmes pour lesquels le nombre d'options n'a pas pu être déterminé.
- Yoan : modification de la bibliographie pour l'intégrer à la page statique.

### 24 juin 2026

**Travail réalisé**

- Yoan : modification des graphes sur la page statique.
- Intégration des données de recherche du site dans un fichier JavaScript dédié.
- Correction du déploiement pour que les scripts de recherche et les données du site soient copiés dans `public/`.
- Baptiste : Ajout de la bibliographie sur le pdf : technical_details.pdf
- Baptiste : Suppresions de fichier pour nettoyer le git

### 25 juin 2026

**Travail réalisé**

- Yoan : ajout des logos utilisés pour le poster
- Baptiste : ajout poster sur le site
- Baptiste : Refonte de la naviguation du site web

