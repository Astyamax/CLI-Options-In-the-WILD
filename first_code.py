import sys
import subprocess
import tempfile

# Erreur si trop d'arguments
if len(sys.argv) != 2:
        print("Usage: python script.py <programme>")
        sys.exit(1)


prog = sys.argv[1]

try:
     result = subprocess.run(
        [programme, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Fichier temporaire
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as f:
        f.write(result.stdout)
        f.seek(0)  # Retour au début du fichier
