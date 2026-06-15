import argparse
import csv
import re
import struct
import subprocess
from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parents[2]
DOSSIER_BUILDS = RACINE_PROJET / "builds"
DOSSIER_CSV = RACINE_PROJET / "csv"

DATES_TOYBOX = {
    "v0.0.3": "2007-06-17",
    "v0.0.7": "2008-11-12",
    "v0.0.9.2": "2009-04-19",
    "v0.4.1": "2012-11-13",
    "v0.4.7": "2013-11-19",
    "v0.5.1": "2014-11-19",
    "v0.6.1": "2015-11-03",
    "v0.7.2": "2016-10-21",
    "v0.7.5": "2017-10-12",
    "v0.7.8": "2018-10-31",
    "v0.8.2": "2019-10-18",
    "v0.8.4": "2020-10-24",
    "v0.8.6": "2021-12-01",
    "v0.8.8": "2022-08-12",
    "v0.8.10": "2023-07-30",
    "v0.8.11": "2024-04-08",
    "v0.8.13": "2025-10-14",
}

DATES_FFMPEG = {
    "n4.2": "2019-08-05",
    "n4.4": "2021-04-08",
    "n5.1": "2022-07-22",
    "n6.1": "2023-11-10",
    "n7.1": "2024-09-30",
}

MOTIF_OPTION_FFMPEG = re.compile(
    r"^\s*(-{1,2}[A-Za-z][A-Za-z0-9_.-]*)\b",
    re.MULTILINE,
)


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


def lire_chaine(data, sections, adresse):
    if adresse == 0:
        return ""

    for section in sections:
        debut = section["adresse"]
        fin = debut + section["taille"]
        if debut <= adresse < fin and section["type"] != 8:
            offset = section["offset"] + adresse - debut
            fin_chaine = data.find(b"\0", offset)
            return data[offset:fin_chaine].decode("utf-8", errors="replace")

    raise ValueError(f"Adresse ELF introuvable : 0x{adresse:x}")


def lire_table_toybox(binaire):
    data = binaire.read_bytes()

    if data[:4] != b"\x7fELF" or data[4] != 2 or data[5] != 1:
        raise ValueError(f"Format ELF64 little-endian attendu : {binaire}")

    entete = struct.unpack_from("<HHIQQQIHHHHHH", data, 16)
    offset_sections = entete[5]
    taille_section = entete[10]
    nombre_sections = entete[11]

    sections = []
    for index in range(nombre_sections):
        valeurs = struct.unpack_from(
            "<IIQQQQIIQQ",
            data,
            offset_sections + index * taille_section,
        )
        sections.append(
            {
                "type": valeurs[1],
                "adresse": valeurs[3],
                "offset": valeurs[4],
                "taille": valeurs[5],
                "lien": valeurs[6],
                "taille_entree": valeurs[9],
            }
        )

    symbole_toy_list = None
    for section in sections:
        if section["type"] != 2:
            continue

        table_chaine = sections[section["lien"]]
        taille_entree = section["taille_entree"] or 24
        nombre_symboles = section["taille"] // taille_entree

        for index in range(nombre_symboles):
            valeurs = struct.unpack_from(
                "<IBBHQQ",
                data,
                section["offset"] + index * taille_entree,
            )
            offset_nom, _, _, _, adresse, taille = valeurs
            nom = lire_chaine(
                data,
                [table_chaine],
                table_chaine["adresse"] + offset_nom,
            )
            if nom == "toy_list":
                symbole_toy_list = (adresse, taille)
                break

        if symbole_toy_list:
            break

    if symbole_toy_list is None:
        raise ValueError(f"Symbole toy_list introuvable : {binaire}")

    adresse_table, taille_table = symbole_toy_list
    section_table = next(
        section
        for section in sections
        if section["adresse"] <= adresse_table < section["adresse"] + section["taille"]
    )
    offset_table = section_table["offset"] + adresse_table - section_table["adresse"]

    commandes = {}
    taille_entree = 32

    for offset in range(offset_table, offset_table + taille_table, taille_entree):
        adresse_nom, _, adresse_options, _ = struct.unpack_from("<QQQQ", data, offset)
        nom = lire_chaine(data, sections, adresse_nom)
        options = lire_chaine(data, sections, adresse_options)
        if nom != "toybox":
            commandes[nom] = options

    return commandes


def compter_options_toybox(chaine_options):
    if not chaine_options:
        return 0

    definition = chaine_options.split("[", 1)[0]
    options = {
        f"--{nom}"
        for nom in re.findall(r"\(([^)]+)\)", definition)
    }

    sans_options_longues = re.sub(r"\([^)]+\)", "", definition)
    sans_contraintes = re.sub(r"[<>=]-?\d+", "", sans_options_longues)

    for caractere in sans_contraintes:
        if caractere.isalpha() or caractere.isdigit():
            options.add(f"-{caractere}")

    return len(options)


def nom_fichier_toybox(commande):
    nom = "".join(
        caractere
        if re.match(r"[a-zA-Z0-9_.-]", caractere)
        else f"_{ord(caractere):02x}"
        for caractere in commande
    )
    return f"toybox_._toybox_{nom}.csv"


def generer_csv_toybox(dossier_programme, dossier_csv):
    versions = lister_versions(dossier_programme)
    commandes_par_version = {}
    toutes_les_commandes = set()

    for dossier_version in versions:
        commandes = lire_table_toybox(dossier_version / "toybox")
        commandes_par_version[dossier_version.name] = commandes
        toutes_les_commandes.update(commandes)

    dossier_csv.mkdir(parents=True, exist_ok=True)
    commandes_triees = sorted(toutes_les_commandes)

    print(
        f"Generation de {len(commandes_triees)} CSV "
        f"pour {len(versions)} versions de Toybox."
    )

    for index, commande in enumerate(commandes_triees, start=1):
        chemin_csv = dossier_csv / nom_fichier_toybox(commande)

        with chemin_csv.open("w", newline="", encoding="utf-8") as fichier:
            writer = csv.writer(fichier, lineterminator="\n")
            writer.writerow(
                ["programme", "version", "date", "commande", "nombre_options", "erreur"]
            )

            for dossier_version in versions:
                version = dossier_version.name
                commande_complete = f"./toybox {commande}"

                if commande not in commandes_par_version[version]:
                    nombre_options = 0
                    erreur = "commande absente dans cette version"
                else:
                    nombre_options = compter_options_toybox(
                        commandes_par_version[version][commande]
                    )
                    erreur = ""

                writer.writerow(
                    [
                        "toybox",
                        version,
                        DATES_TOYBOX.get(version, ""),
                        commande_complete,
                        nombre_options,
                        erreur,
                    ]
                )

        print(f"[{index}/{len(commandes_triees)}] {chemin_csv.name}")

    print(f"CSV Toybox generes dans : {dossier_csv}")
    return 0


def compter_options_ffmpeg(binaire):
    try:
        resultat = subprocess.run(
            [str(binaire), "-hide_banner", "-help", "full"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return 0, "timeout"

    if resultat.returncode != 0:
        lignes = resultat.stdout.strip().splitlines()
        erreur = lignes[0] if lignes else f"code retour {resultat.returncode}"
        return 0, erreur

    options = set(MOTIF_OPTION_FFMPEG.findall(resultat.stdout))
    return len(options), ""


def generer_csv_ffmpeg(dossier_programme, dossier_csv):
    versions = [
        dossier
        for dossier in lister_versions(dossier_programme)
        if (dossier / "ffmpeg").is_file()
    ]

    if not versions:
        print(f"Aucune version FFmpeg trouvee dans {dossier_programme}")
        return 1

    dossier_csv.mkdir(parents=True, exist_ok=True)
    chemin_csv = dossier_csv / "ffmpeg_._ffmpeg.csv"

    with chemin_csv.open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier, lineterminator="\n")
        writer.writerow(
            ["programme", "version", "date", "commande", "nombre_options", "erreur"]
        )

        for dossier_version in versions:
            version = dossier_version.name
            nombre_options, erreur = compter_options_ffmpeg(
                dossier_version / "ffmpeg"
            )
            writer.writerow(
                [
                    "ffmpeg",
                    version,
                    DATES_FFMPEG.get(version, ""),
                    "./ffmpeg",
                    nombre_options,
                    erreur,
                ]
            )
            print(
                f"{version}: {nombre_options} options"
                + (f" - {erreur}" if erreur else "")
            )

    print(f"CSV FFmpeg genere : {chemin_csv}")
    return 0


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
        nargs="?",
        help="Commande shell a executer dans chaque dossier de version.",
    )
    parser.add_argument(
        "--tous-csv",
        action="store_true",
        help="Genere les CSV du programme analyse.",
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DOSSIER_CSV,
        help=f"Dossier de sortie des CSV. Par defaut : {DOSSIER_CSV}",
    )

    args = parser.parse_args()

    dossier_programme = DOSSIER_BUILDS / args.programme

    if not dossier_programme.exists():
        print(f"Dossier introuvable : {dossier_programme}")
        return 1

    if args.tous_csv:
        if args.programme == "toybox":
            return generer_csv_toybox(dossier_programme, args.csv_dir)
        if args.programme == "ffmpeg":
            return generer_csv_ffmpeg(dossier_programme, args.csv_dir)
        parser.error("--tous-csv est disponible pour toybox et ffmpeg")

    if not args.commande:
        parser.error("commande est obligatoire sans --tous-csv")

    return executer_pour_chaque_version(dossier_programme, args.commande)


if __name__ == "__main__":
    raise SystemExit(main())
