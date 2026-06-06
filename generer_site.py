import os
import graph

dossier_sauvegarde = "data/figures"
os.makedirs(dossier_sauvegarde, exist_ok=True)

print("\nAnalyses en cours pour git")
graph.compare_options_graph(
    main_program="git", 
    save_path=f"{dossier_sauvegarde}/graph_git.png", 
    show=False )

print("\nAnalyses en cours pour curl")
graph.compare_options_graph(
    main_program="curl", 
    save_path=f"{dossier_sauvegarde}/graph_curl.png", 
    show=False
)