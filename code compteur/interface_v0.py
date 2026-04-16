import tkinter as tk
from tkinter import messagebox
import code_final  

def lancer_comptage():
    
    prog = entree_programme.get().strip()
    
    label_resultat.config(text="Analyse en cours...")
    fenetre.update() 
    
    try:
        options_trouvees = code_final.compteur_generale(prog)
        nombre_options = len(options_trouvees)
        label_resultat.config(text=f"Le programme '{prog}' possède {nombre_options} option(s) :\n{','.join(options_trouvees)}")
    
    except Exception as erreur:
        messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{erreur}")
        label_resultat.config(text="Erreur lors de l'analyse.")

#création de la fenêtre 
fenetre = tk.Tk()
fenetre.title("Options in the Wild - Compteur")
fenetre.geometry("400x250") 
fenetre.config(padx=20, pady=20) 




label_consigne = tk.Label(fenetre, text="Entrez le nom du programme à analyser :", font=("Arial", 12))
label_consigne.pack(pady=(0, 10)) 


entree_programme = tk.Entry(fenetre, font=("Arial", 14), width=20, justify="center")
entree_programme.pack(pady=10)


bouton_calculer = tk.Button(fenetre, text="Compter les options", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=lancer_comptage)
bouton_calculer.pack(pady=15)


label_resultat = tk.Label(fenetre, text="Prêt à analyser.", font=("Arial", 11, "italic"), fg="blue")
label_resultat.pack(pady=10)

#lancement de l'app
fenetre.mainloop()