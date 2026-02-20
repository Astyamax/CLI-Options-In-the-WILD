import sys
import subprocess
import tempfile

# Erreur si trop d'arguments
if len(sys.argv) != 2:
        print("Usage: python script.py <programme>")
        sys.exit(1)


prog = sys.argv[1]


result = subprocess.run([prog, "--help", ">> tmp.txt"])


    

