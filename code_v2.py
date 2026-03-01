import sys
import subprocess
import re  

if len(sys.argv) != 2:
    print("Usage: python script.py <programme>")
    sys.exit(1)

prog = sys.argv[1]


result = subprocess.run([prog, "--help"], capture_output=True, text=True, check=True)
texte_aide = result.stdout


motif_option = re.compile(r"(--[a-zA-Z0-9-]+|-[a-zA-Z0-9])")
options_trouvees = motif_option.findall(texte_aide)
options_uniques = set(options_trouvees)

print(f"Programme : {prog}")
print(f"Nombre d'options uniques trouvées : {len(options_uniques)}")
print(f"Aperçu des options : {list(options_uniques)}")