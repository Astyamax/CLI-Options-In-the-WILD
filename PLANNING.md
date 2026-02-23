# Suivi de Projet : CLI Options in the Wild

| Semaine / Date | Objectifs de la période | Tâches Asynchrones individuelles (Binôme) | Tâches Synchrones / Points de contact |
| :--- | :--- | :--- | :--- |
| **S1** (20/02)  | Cadrage & Planification  | Lecture de l'article de base, comptage manuel de 10 programmes et premier programme test. | Livrable du 20/02 et point sur les attentes. |
| **S2-S3** (23/02-13/03)  | Détermination des tâches, Prototypage & Choix Technique  | Création du compteur Bash minimal et test sur 5 programmes simples (cat, ls, grep, sed, sort). Étude de faisabilité Python argparse vs Bash. | Point avec encadrants, présentation des écarts manuel/auto et décision finale Bash ou Python. |
| **S4-S5** (16/03-03/04)  | Gestion de la diversité (Début)  | Pôle Parsing : Implémentation de la gestion des alias (ex: tar) et options cachées (curl --help all). Pôle Git : Apprentissage du script d'automatisation d'exécution. | Mise en commun sur le dépôt Git et revue de code croisée. |
| **S7-S8** (10/04-15/04)  | Cas complexes & Pipeline  | Résolution du problème des sous-commandes (ex: git clone, init) et des pagers (ne pas rester bloqué). | Point d'étape encadrants et démonstration du script validé sur l'ensemble des cas d'usage simples et complexes. |
| **S9-S10** (21/04-05/05)  | Voyage dans le temps (Git)  | Pôle Git : Script pour cloner 1 dépôt, checkout 3-5 tags, et compiler. Pôle Parsing : Sécurisation du parseur contre les erreurs de compilation / format cassé. | Fusion Git & Parsing : le script de parsing est injecté dans le script temporel Git. |
| **S11** (13/05)  | Passage à l'échelle massive  | Action de groupe : Lancement des scripts sur la liste cible de 20 à 50+ programmes (Catégories : Réseau, Serveurs, Médias, CLI modernes) et génération des CSV/JSON. | Point d'étape encadrants non-noté : Vérification de l'intégrité de la base de données générée. |
| **S12** (27/05)  | Semaine de Buffer/Débogage  | Traitement des cas d'erreur (programmes qui refusent de compiler ou dont le format d'aide a muté au fil des décennies) et documentation du code. | Session "Hackathon" interne pour finaliser la collecte de données. |
| **S13-S14** (10/06-15/06)  | Analyse & Visualisation  | Utilisation de Matplotlib pour générer les graphiques et comparaison de la croissance des options vs Lignes de Code (LoC). | Analyse conjointe des résultats : L'IA a-t-elle eu un impact ? Quels programmes explosent ?  |
| Dernière semaine  | Vulgarisation de notre travail et finalisation du suivi.md  | Faire le readme.md et faire un poster (autres idées créatives). | Répétition de la soutenance (si applicable) et vérification de l'arborescence du GitLab. |

```mermaid
%%{init: { 'theme': 'default', 'gantt': { 'leftPadding': 200 } } }%%
gantt
    title Suivi de Projet – CLI Options in the Wild
    dateFormat YYYY-MM-DD
    excludes weekends
    axisFormat %e %b %y
    tickInterval 1month
    weekday monday

    section Phases du Projet
    S1 – Cadrage et Planification                :milestone, m1, 2026-02-20, 0d
    S2-S3 – Prototypage et Choix Technique       :s2, 2026-02-23, 2026-03-13
    S4-S5 – Gestion de la diversite (Debut)      :s4, 2026-03-16, 2026-04-03
    Pause                                         :crit, pause, 2026-04-04, 2026-04-09
    S7-S8 – Cas complexes et Pipeline            :s7, 2026-04-10, 2026-04-15
    S9-S10 – Voyage dans le temps (Git)          :s9, 2026-04-21, 2026-05-05
    S11 – Passage a l echelle massive            :s11, 2026-05-13, 2026-05-19
    S12 – Buffer / Debogage                      :s12, 2026-05-27, 2026-06-02
    S13-S14 – Analyse et Visualisation           :s13, 2026-06-10, 2026-06-15
    Derniere semaine – Vulgarisation et Soutenance :last, 2026-06-16, 2026-06-22

    section Taches Asynchrones
    Lecture article + comptage manuel 10 prog        :a1, 2026-02-20, 1d
    Compteur Bash minimal + test 5 prog              :a2, 2026-02-23, 2026-03-13
    Parsing – alias et options cachees               :a4a, 2026-03-16, 2026-04-03
    Git – script automatisation execution            :a4b, 2026-03-16, 2026-04-03
    Sous-commandes et pagers                         :a7, 2026-04-10, 2026-04-15
    Git – clone, checkout tags, compiler             :a9a, 2026-04-21, 2026-05-05
    Parsing – securisation erreurs                   :a9b, 2026-04-21, 2026-05-05
    Lancement scripts 20-50+ programmes              :a11, 2026-05-13, 2026-05-19
    Traitement erreurs et documentation              :a12, 2026-05-27, 2026-06-02
    Graphiques Matplotlib et analyse LoC             :a13, 2026-06-10, 2026-06-15
    README, poster et idees creatives                :alast, 2026-06-16, 2026-06-22

    section Taches Synchrones / Livrables
    Livrable S1 + point attentes                     :milestone, t1, 2026-02-20, 0d
    Revue de code croisee                            :milestone, t4, 2026-04-03, 0d
    Fusion Git et Parsing                            :milestone, t9, 2026-05-05, 0d
    Hackathon interne                                :milestone, t12, 2026-06-02, 0d
    Analyse conjointe resultats                      :milestone, t13, 2026-06-15, 0d

    section Points Encadrants (horaires ICS)
    S1 Point attentes – 20/02 08h30-10h00 + 10h15-11h45          :milestone, enc1, 2026-02-20, 0d
    S2-S3 Decision Bash/Python – 13/03 08h30-10h00 + 10h15-11h45 :milestone, enc2, 2026-03-13, 0d
    S7-S8 Demo script – 15/04 08h30-10h00 + 10h15-11h45          :milestone, enc3, 2026-04-15, 0d
    S11 Integrite BDD – 13/05 (pas de seance ICS cette semaine)   :crit, milestone, enc4, 2026-05-13, 0d
    Soutenance – 22/06 08h30-10h00 + 10h15-11h45 + 13h30-16h45   :milestone, enc5, 2026-06-22, 0d

    section Equipe
    Yoan Francois – Application Interface            :active, eq1, 2026-02-20, 2026-06-22
    Baptiste Guerif – Application Code               :active, eq2, 2026-02-20, 2026-06-22
    Lois Chow-Chine-Galinaud – Git repos analysis   :active, eq3, 2026-02-20, 2026-06-22
    Theophille Berthelot – Data analysis              :active, eq4, 2026-02-20, 2026-06-22
```