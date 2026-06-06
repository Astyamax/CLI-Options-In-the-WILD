import os
import graph

os.makedirs("public/images", exist_ok=True)
print("\nAnalyses en cours pour GIT...")
graph.compare_options_graph(
    main_program="git", 
    save_path="public/images/graph_git.png", 
    show=False )