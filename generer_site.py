import os
import sys


sys.path.insert(0, './Visualisation/graphes')

import graph

print("--- DÉBUT DE LA GÉNÉRATION DES IMAGES ---")

# On utilise ton dossier existant dans l'architecture !
dossier_sauvegarde = "data/figures"
os.makedirs(dossier_sauvegarde, exist_ok=True)

# 1. On commande le graphique pour 'git'
print("\nAnalyses en cours pour GIT...")
graph.compare_options_graph(
    main_program="git", 
    save_path=f"{dossier_sauvegarde}/graph_git.png", 
    show=False
)

# 2. On commande le graphique pour 'curl'
print("\nAnalyses en cours pour CURL...")
graph.compare_options_graph(
    main_program="curl", 
    save_path=f"{dossier_sauvegarde}/graph_curl.png", 
    show=False
)

print("\n--- GÉNÉRATION TERMINÉE ! ---")
print(f"Tes images sont prêtes dans le dossier {dossier_sauvegarde}/")