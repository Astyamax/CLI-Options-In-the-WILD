import script_compteur

def compteur_generale(prog) :
    
    options = []
    aides = ["--help", "-h", "-help", "help", "-?","--usage", "--help full", "-h full", "--help all", "-h all"]
    for aide in aides:
        L = script_compteur.lister_commandes(prog, aide)
        if L == []:
            print(f"Impossible d'afficher l'aide avec {aide}")
        elif L != []: 
            print("on a obtenu des réponses avec ", aide)
            options += L
    options_uniques = []
    options_uniques = list(set(options))

    return options_uniques
