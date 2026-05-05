import sys
import subprocess
import re  

def lister_commandes(programme, aide):
    commande_base = programme.split()
    commande_complete = commande_base + aide.split()
    
    try:
        result = subprocess.run(commande_complete, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL, text=True, check=False, timeout=2)
    except subprocess.TimeoutExpired:
        return []
    if result.returncode != 0:
        #print("Erreur : impossible d'afficher l'aide avec ", aide)
        return []


    texte_aide = result.stdout
    motif_option = re.compile(r"(--[a-zA-Z0-9-]+|-[a-zA-Z0-9])")
    options_trouvees = motif_option.findall(texte_aide)
    options_uniques = set(options_trouvees)

    return list(options_uniques)
if __name__ == "__main__":
    print(lister_commandes("mysql", "--help"))

