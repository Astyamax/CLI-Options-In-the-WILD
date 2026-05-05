import code_v2

def compteur_generale(prog) :
    
    options = []
    aides = ["--help", "-h", "-help", "help", "-?","--usage", "--help full", "-h full", "--help all", "-h all"]
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
if __name__ == "__main__":
    programme_a_tester = "curl"
    resultats_options = compteur_generale(programme_a_tester)
    print(len(resultats_options))
    print(resultats_options)
