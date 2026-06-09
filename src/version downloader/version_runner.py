import argparse
import re
import subprocess
from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parents[2]
DOSSIER_BUILDS = RACINE_PROJET / "builds"


def lister_versions(dossier_programme):
    versions = []
    for dossier in dossier_programme.iterdir():
        if dossier.is_dir():
            versions.append(dossier)
    return sorted(versions, key=cle_version)


def cle_version(chemin):
    morceaux = re.split(r"(\d+)", chemin.name)
    return [int(morceau) if morceau.isdigit() else morceau for morceau in morceaux]


def executer_pour_chaque_version(dossier_programme, commande):
    versions = lister_versions(dossier_programme)

    if not versions:
        print(f"Aucune version trouvee dans {dossier_programme}")
        return 1

    code_retour_final = 0

    for dossier_version in versions:
        print()
        print("=" * 60)
        print(f"Version : {dossier_version.name}")
        print(f"cd {dossier_version}")
        print(f"$ {commande}")
        print("=" * 60, flush=True)

        resultat = subprocess.run(commande, shell=True, cwd=dossier_version)

        if resultat.returncode != 0:
            code_retour_final = resultat.returncode
            print(f"Commande echouee pour {dossier_version.name} avec le code {resultat.returncode}")

    return code_retour_final


def main():
    parser = argparse.ArgumentParser(
        description="Execute une commande shell dans chaque dossier de version disponible."
    )
    parser.add_argument(
        "programme",
        help="Nom du programme dans builds, par exemple coreutils ou toybox.",
    )
    parser.add_argument(
        "commande",
        help="Commande shell a executer dans chaque dossier de version.",
    )

    args = parser.parse_args()

    dossier_programme = DOSSIER_BUILDS / args.programme

    if not dossier_programme.exists():
        print(f"Dossier introuvable : {dossier_programme}")
        return 1

    return executer_pour_chaque_version(dossier_programme, args.commande)


if __name__ == "__main__":
    raise SystemExit(main())
