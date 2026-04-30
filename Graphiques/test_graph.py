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
            options=code_final.compteur_general(prog)
            noms.append(prog)
            comptes.append(len(options))
        except Exception as e:
            print(f"Impossible d'analyser {prog} : {e}")
            