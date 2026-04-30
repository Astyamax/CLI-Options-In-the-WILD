import matplotlib.pyplot as plt
import code_final

PROGRAMMES_CLASSIQUES = ["ls","grep","cat","tar"]

def afficher_graphique_seul(programme_cible):
    print(f"Cible :{programme_cible}")
    liste_programmes = [programme_cible]
    for p in PROGRAMMES_CLASSIQUES:
        if p!= programme_cible:
            liste_programmes.append(p)

    noms = []
    comptes = []


    for prog in liste_programmes:
        print(f"Recherche des options pour '{prog}'")
        try:
            options=code_final.compteur_generale(prog)
            noms.append(prog)
            comptes.append(len(options))
        except Exception as e:
            print(f"Impossible d'analyser {prog} : {e}")

    plt.figure(figsize=(10,6))
    couleurs = ['#FF6B6B' if nom == programme_cible else '#4ECDC4' for nom in noms]
    barres = plt.bar(noms, comptes, color=couleurs, edgecolor='black')

    for barre in barres:
        hauteur = barre.get_height()
        plt.text(barre.get_x() + barre.get_width()/2., hauteur,
                 f'{int(hauteur)}', ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('Programmes', fontsize=12, fontweight='bold')
    plt.ylabel("Nombre d'options", fontsize=12, fontweight='bold')
    plt.title(f"Comparaison du nombre d'options ({programme_cible} en rouge)", fontsize=14, fontweight='bold')
    plt.show()

if __name__ == "__main__":
    afficher_graphique_seul("git")