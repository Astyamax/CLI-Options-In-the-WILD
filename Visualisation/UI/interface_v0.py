import tkinter as tk
from tkinter import messagebox #pour afficher une erreur si besoin 
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMPTEUR_DIR = PROJECT_ROOT / "src" / "compteur"
GRAPHES_DIR = PROJECT_ROOT / "Visualisation" / "graphes"
for path in (COMPTEUR_DIR, GRAPHES_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from compteur import compteur_generale
from graph import compare_options_graph

def load_figure_canvas():
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "matplotlib est requis pour afficher les graphes. "
            "Installez les dépendances avec: pip install -r requirements.txt"
        ) from exc
    return FigureCanvasTkAgg

def lancer_comptage():
    
    prog = entree_programme.get().strip() #lit le texte tapé dans l'interface et enlève les espaces inutiles 
    
    if not prog:
        return

    label_resultat.config(text="Analyse en cours...")
    fenetre.update() #force la mise à jour de la fenêtre 
    
    try:
        FigureCanvasTkAgg = load_figure_canvas()
        options_trouvees = compteur_generale(prog) #lance le compteur avec le champ d'entrée
        nombre_options = len(options_trouvees)
        label_resultat.config(text=f"Le programme '{prog}' possède {nombre_options} option(s) :\n{','.join(options_trouvees)}")
    
        for widget in zone_graphique.winfo_children():
            widget.destroy() #supprime les anciens widgets présents dans la zone graphique

        figure_creee = compare_options_graph(prog, show=False,return_fig=True)

        canvas = FigureCanvasTkAgg(figure_creee,master=zone_graphique)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as erreur:
        messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{erreur}")
        label_resultat.config(text="Erreur lors de l'analyse.")

def main():
    global fenetre, entree_programme, label_resultat, zone_graphique

    #création de la fenêtre
    fenetre = tk.Tk()
    fenetre.title("Options in the Wild - Compteur")
    fenetre.geometry("700x700")
    fenetre.config(padx=20, pady=20)

    label_consigne = tk.Label(fenetre, text="Entrez le nom du programme à analyser :", font=("Arial", 12))
    label_consigne.pack(pady=(0, 10))

    entree_programme = tk.Entry(fenetre, font=("Arial", 14), width=20, justify="center")
    entree_programme.pack(pady=10)

    bouton_calculer = tk.Button(fenetre, text="Compter les options", font=("Arial", 12, "bold"), fg="black", command=lancer_comptage)
    bouton_calculer.pack(pady=15)

    label_resultat = tk.Label(fenetre, text="Prêt à analyser.", font=("Arial", 11, "italic"), fg="blue")
    label_resultat.pack(pady=10)

    zone_graphique=tk.Frame(fenetre)
    zone_graphique.pack(pady=10,fill=tk.BOTH,expand=True)

    #lancement de l'app
    fenetre.mainloop()

if __name__ == "__main__":
    main()
