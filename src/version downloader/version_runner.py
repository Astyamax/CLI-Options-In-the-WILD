import argparse
import csv
import os
import re
import subprocess
import sys
from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parents[2]
DOSSIER_BUILDS = RACINE_PROJET / "builds"
DOSSIER_CSV = RACINE_PROJET / "csv"
DOSSIER_COMPAT = DOSSIER_BUILDS / "_compat"
DOSSIER_SCRIPT = Path(__file__).resolve().parent

if str(RACINE_PROJET) not in sys.path:
    sys.path.insert(0, str(RACINE_PROJET))

from src.compteur.compteur import compteur_generale


def preparer_libselinux_compat():
    source = DOSSIER_SCRIPT / "libselinux_stub.c"
    version_script = DOSSIER_SCRIPT / "libselinux_stub.map"
    lib = DOSSIER_COMPAT / "libselinux.so.1"

    if (
        lib.exists()
        and lib.stat().st_mtime > source.stat().st_mtime
        and lib.stat().st_mtime > version_script.stat().st_mtime
    ):
        return DOSSIER_COMPAT

    DOSSIER_COMPAT.mkdir(parents=True, exist_ok=True)

    commande = [
        "gcc",
        "-shared",
        "-fPIC",
        str(source),
        "-Wl,-soname,libselinux.so.1",
        f"-Wl,--version-script={version_script}",
        "-o",
        str(lib),
    ]
    resultat = subprocess.run(
        commande,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if resultat.returncode != 0:
        raise RuntimeError(f"Impossible de construire libselinux locale:\n{resultat.stdout}")

    return DOSSIER_COMPAT


def activer_libselinux_compat():
    compat = preparer_libselinux_compat()
    ancien_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
    chemins = [str(compat)]
    if ancien_ld_path:
        chemins.append(ancien_ld_path)
    os.environ["LD_LIBRARY_PATH"] = ":".join(chemins)


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
    activer_libselinux_compat()

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


def nom_fichier_csv(programme, commande):
    nom = commande.replace("/", "_").replace(" ", "_")
    nom = re.sub(r"[^a-zA-Z0-9_.-]", "_", nom)
    return f"{programme}_{nom}.csv"


def compter_pour_chaque_version(dossier_programme, programme, commande, dossier_csv):
    versions = lister_versions(dossier_programme)

    if not versions:
        print(f"Aucune version trouvee dans {dossier_programme}")
        return 1

    dossier_csv.mkdir(parents=True, exist_ok=True)
    chemin_csv = dossier_csv / nom_fichier_csv(programme, commande)

    ancien_dossier = Path.cwd()
    activer_libselinux_compat()

    with chemin_csv.open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        writer.writerow(["programme", "version", "commande", "nombre_options", "erreur"])

        for dossier_version in versions:
            print()
            print("=" * 60)
            print(f"Version : {dossier_version.name}")
            print(f"cd {dossier_version}")
            print(f"compteur_generale({commande!r})")
            print("=" * 60, flush=True)

            try:
                os.chdir(dossier_version)
                options = compteur_generale(commande)
            finally:
                os.chdir(ancien_dossier)

            erreur = ""
            if len(options) == 0:
                erreur = verifier_execution(commande, dossier_version)

            writer.writerow(
                [
                    programme,
                    dossier_version.name,
                    commande,
                    len(options),
                    erreur,
                ]
            )

    print()
    print(f"Resultats ecrits dans : {chemin_csv}")
    return 0


def verifier_execution(commande, dossier_version):
    try:
        resultat = subprocess.run(
            f"{commande} --help",
            shell=True,
            cwd=dossier_version,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            timeout=2,
    )
    except subprocess.TimeoutExpired:
        return "timeout"

    if resultat.returncode == 0:
        return ""

    lignes = resultat.stdout.strip().splitlines()
    return lignes[0] if lignes else f"code retour {resultat.returncode}"


def trouver_dossier_programme(programme):
    candidats = [
        DOSSIER_BUILDS / programme,
        DOSSIER_BUILDS / f"{programme}_builds",
    ]

    for candidat in candidats:
        if candidat.exists():
            return candidat

    return candidats[0]


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
    parser.add_argument(
        "--compteur",
        action="store_true",
        help="Execute compteur.py sur la commande au lieu d'executer directement la commande shell.",
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DOSSIER_CSV,
        help=f"Dossier ou stocker les CSV. Par defaut : {DOSSIER_CSV}",
    )

    args = parser.parse_args()

    dossier_programme = trouver_dossier_programme(args.programme)

    if not dossier_programme.exists():
        print(f"Dossier introuvable : {dossier_programme}")
        return 1

    if args.compteur:
        return compter_pour_chaque_version(
            dossier_programme,
            args.programme,
            args.commande,
            args.csv_dir,
        )

    return executer_pour_chaque_version(dossier_programme, args.commande)


if __name__ == "__main__":
    raise SystemExit(main())
