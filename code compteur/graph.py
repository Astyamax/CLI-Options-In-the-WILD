import sys
import matplotlib.pyplot as plt
from pathlib import Path

# Ajouter le chemin vers code_compteur pour les imports
sys.path.insert(0, str(Path(__file__).parent / "code compteur"))

from code_final import compteur_generale

# Programmes classiques de référence pour la comparaison
CLASSIC_PROGRAMS = ["ls", "grep", "sed", "sort", "cat", "curl", "tar"]


def compare_options_graph(main_program: str, comparison_programs: list = None, save_path: str = None, show: bool = True, return_fig: bool=False) -> dict:
    """
    Trace un graphe pour comparer le nombre d'options d'un programme avec d'autres.
    
    Args:
        main_program (str): Le programme principal à analyser
        comparison_programs (list): Liste des programmes à comparer (défaut: CLASSIC_PROGRAMS)
        save_path (str): Chemin pour sauvegarder le graphe (optionnel)
        show (bool): Afficher le graphe (défaut: True)
    
    Returns:
        dict: Dictionnaire avec le nombre d'options pour chaque programme
    """
    if comparison_programs is None:
        comparison_programs = CLASSIC_PROGRAMS
    
    # Ajouter le programme principal à la liste s'il n'y est pas déjà
    programs_to_analyze = [main_program] + [p for p in comparison_programs if p != main_program]
    
    # Analyser tous les programmes
    options_count = {}
    for program in programs_to_analyze:
        try:
            options = compteur_generale(program)
            options_count[program] = len(options)
            print(f"✓ {program}: {len(options)} options")
        except Exception as e:
            print(f"✗ {program}: Erreur - {e}")
            options_count[program] = 0
    
    # Créer le graphe
    programs = list(options_count.keys())
    counts = list(options_count.values())
    
    # Colorer le programme principal différemment
    colors = ['#FF6B6B' if p == main_program else '#4ECDC4' for p in programs]
    
    fig = plt.figure(figsize=(12, 6))
    bars = plt.bar(programs, counts, color=colors, edgecolor='black', linewidth=1.5)
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('Programmes', fontsize=12, fontweight='bold')
    plt.ylabel('Nombre d\'options', fontsize=12, fontweight='bold')
    plt.title(f'Comparaison du nombre d\'options\n({main_program} en rouge)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    # Sauvegarder si demandé
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Graphe sauvegardé: {save_path}")
    
    # Afficher le graphe
    if return_fig:
        return fig 
    if show:
        plt.show()
    else:
        plt.close()
    
    return options_count


if __name__ == "__main__":
    import sys
    
    # Programme principal à analyser (passé en argument)
    program = sys.argv[1] if len(sys.argv) > 1 else "ls"
    
    # Tracer le graphe
    compare_options_graph(program)