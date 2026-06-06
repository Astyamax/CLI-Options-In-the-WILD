import os
import sys

sys.path.insert(0, './Visualisation/graphes')

import graph


dossier_sauvegarde = "data/figures"
os.makedirs(dossier_sauvegarde, exist_ok=True)

print("\nAnalyses en cours pour git")
graph.compare_options_graph(
    main_program="git", 
    save_path=f"{dossier_sauvegarde}/graph_git.png", 
    show=False
)

# 2. On commande le graphique pour 'curl'
print("\nAnalyses en cours pour curl")
graph.compare_options_graph(
    main_program="curl", 
    save_path=f"{dossier_sauvegarde}/graph_curl.png", 
    show=False
)

