import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.compteur.compteur import compteur_generale
from Visualisation.graphes.graph import compare_options_graph

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
    prog = entree_programme.get().strip()

    if not prog:
        messagebox.showwarning("Attention", "Veuillez entrer un nom de programme.")
        return

    label_resultat.config(text=f"Analyse de '{prog}' en cours...", fg="#e67e22") # Orange
    fenetre.update()

    try:
        FigureCanvasTkAgg = load_figure_canvas()
        options_trouvees = compteur_generale(prog)
        nombre_options = len(options_trouvees)

        liste_options = ', '.join(options_trouvees)
        if len(liste_options) > 150:
            liste_options = liste_options[:150] + "... [Liste complète trop longue pour l'affichage]"

        label_resultat.config(
            text=f"'{prog}' possède {nombre_options} option(s).\n\nAperçu : {liste_options}",
            fg="#27ae60"
        )

        for widget in zone_graphique.winfo_children():
            widget.destroy()

        figure_creee = compare_options_graph(prog, show=False, return_fig=True)
        canvas = FigureCanvasTkAgg(figure_creee, master=zone_graphique)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as erreur:
        messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{erreur}")
        label_resultat.config(text="Erreur lors de l'analyse.", fg="#c0392b") # Rouge erreur

def main():
    global fenetre, entree_programme, label_resultat, zone_graphique

    fenetre = tk.Tk()
    fenetre.title("Options in the Wild - Dashboard")
    fenetre.geometry("800x800")
    fenetre.configure(bg="#f8f9fa")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
    style.configure("TEntry", padding=5)

    # --- HEADER (Titre principal) ---
    titre = tk.Label(fenetre, text="Options in the Wild", font=("Segoe UI", 20, "bold"), bg="#f8f9fa", fg="#2c3e50")
    titre.pack(pady=(20, 5))

    sous_titre = tk.Label(fenetre, text="Analyseur de complexité des lignes de commande", font=("Segoe UI", 11, "italic"), bg="#f8f9fa", fg="#7f8c8d")
    sous_titre.pack(pady=(0, 20))

    # --- ZONE DE RECHERCHE ---
    frame_recherche = tk.Frame(fenetre, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=1)
    frame_recherche.pack(pady=10, fill=tk.X, padx=40)

    label_consigne = tk.Label(frame_recherche, text="Nom du programme (ex: git, ffmpeg, ls) :", font=("Segoe UI", 11, "bold"), bg="#ffffff")
    label_consigne.pack(pady=(0, 10))

    entree_programme = ttk.Entry(frame_recherche, font=("Consolas", 14), width=30, justify="center")
    entree_programme.pack(pady=5)

    bouton_calculer = ttk.Button(frame_recherche, text="Analyser", command=lancer_comptage)
    bouton_calculer.pack(pady=(10, 0))

    # --- ZONE DE RÉSULTAT (Texte) ---
    label_resultat = tk.Label(fenetre, text="Prêt à lancer l'analyse.", font=("Segoe UI", 11), bg="#f8f9fa", fg="#34495e", wraplength=700, justify="center")
    label_resultat.pack(pady=20)

    # --- ZONE GRAPHIQUE ---
    zone_graphique = tk.Frame(fenetre, bg="#f8f9fa")
    zone_graphique.pack(pady=10, fill=tk.BOTH, expand=True, padx=40)

    # Lancement de l'application
    fenetre.mainloop()

if __name__ == "__main__":
    main()
