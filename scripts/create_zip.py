import zipfile
import os

files_to_zip = [
    ('Visualisation/UI/interface2.py', 'Visualisation/UI/interface2.py'),
    ('Visualisation/graphes/graph.py', 'Visualisation/graphes/graph.py'),
    ('Visualisation/__init__.py', 'Visualisation/__init__.py'),
    ('Visualisation/UI/__init__.py', 'Visualisation/UI/__init__.py'),
    ('src/compteur/compteur.py', 'src/compteur/compteur.py'),
    ('src/compteur/script_compteur.py', 'src/compteur/script_compteur.py'),
    ('src/compteur/__init__.py', 'src/compteur/__init__.py'),
    ('src/__init__.py', 'src/__init__.py'),
    ('requirements.txt', 'requirements.txt'),
]

# Try to also add graphes/__init__.py if it exists
optional = [
    ('Visualisation/graphes/__init__.py', 'Visualisation/graphes/__init__.py'),
]

os.makedirs('downloads', exist_ok=True)

with zipfile.ZipFile('downloads/interface_comptage.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for src, arc in files_to_zip + optional:
        if os.path.exists(src):
            zf.write(src, arc)
            print(f'Added: {src}')
        else:
            print(f'SKIPPED (not found): {src}')

size = os.path.getsize('downloads/interface_comptage.zip')
print(f'ZIP created: downloads/interface_comptage.zip ({size} bytes)')
