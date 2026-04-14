import sys
import subprocess
import re  

def lister_commandes(programme, aide):

    result = subprocess.run([programme, aide], capture_output=True, text=True, check=True)
    if result.returncode != 0:
        print("Erreur : impossible d'afficher l'aide avec ", aide)
        return []


    texte_aide = result.stdout
    motif_option = re.compile(r"(--[a-zA-Z0-9-]+|-[a-zA-Z0-9])")
    options_trouvees = motif_option.findall(texte_aide)
    options_uniques = set(options_trouvees)

    return list(options_uniques)

print(lister_commandes("mysql", "--help"))

