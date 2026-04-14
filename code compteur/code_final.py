import code_v2

def compteur_generale(prog) :
    
    options = []
    aides = ["--help", "-h", "-help", "help", "--usage","-usage","usage", "-?", "--?", "?"]
    for aide in aides:
        L = code_v2.lister_commandes(prog, aide)
        if L == []:
            print(f"Impossible d'afficher l'aide avec {aide}")
        elif L != []: 
            print("on a obtenu des réponses avec ", aide)
            options += L
    options_uniques = []    
    for option in options:
        if option not in options_uniques:
            options_uniques.append(option)
    return options_uniques

