import argparse
import csv
from datetime import date
from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parents[2]
DOSSIER_CSV = RACINE_PROJET / "csv"
SORTIE_PAR_DEFAUT = RACINE_PROJET / "data" / "figures" / "options_par_annee.png"


def charger_matplotlib():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "matplotlib est requis. Installez les dependances avec : "
            "pip install -r requirements.txt"
        ) from exc
    return plt


def nom_commande(commande):
    if commande.startswith("./"):
        return commande[2:]
    return commande


def commande_depuis_nom_fichier(chemin_csv):
    nom = chemin_csv.stem
    if "._" in nom:
        return nom.split("._", 1)[1]
    return nom


def lire_csv(dossier_csv, inclure_erreurs=False):
    donnees = {}

    for chemin_csv in sorted(dossier_csv.glob("*.csv")):
        with chemin_csv.open(newline="", encoding="utf-8") as fichier:
            lecteur = csv.DictReader(fichier)
            contient_des_lignes = False

            colonnes_requises = {"date", "commande", "nombre_options"}
            if not lecteur.fieldnames or not colonnes_requises.issubset(lecteur.fieldnames):
                print(f"CSV ignore, colonnes manquantes : {chemin_csv}")
                continue

            for ligne in lecteur:
                contient_des_lignes = True
                commande = nom_commande(ligne["commande"].strip())
                donnees_commande = donnees.setdefault(commande, {})

                erreur = ligne.get("erreur", "").strip()
                if erreur and not inclure_erreurs:
                    continue

                try:
                    date_version = date.fromisoformat(ligne["date"])
                    nombre_options = int(ligne["nombre_options"])
                except (TypeError, ValueError):
                    continue

                annee = date_version.year

                # Une seule mesure par annee : garder la version la plus recente.
                mesure_actuelle = donnees_commande.get(annee)
                if mesure_actuelle is None or date_version > mesure_actuelle[0]:
                    donnees_commande[annee] = (date_version, nombre_options)

            if not contient_des_lignes:
                donnees.setdefault(commande_depuis_nom_fichier(chemin_csv), {})

    return donnees


def filtrer_commandes(donnees, commandes):
    if not commandes:
        return donnees

    commandes_demandees = {nom_commande(commande) for commande in commandes}
    return {
        commande: mesures
        for commande, mesures in donnees.items()
        if commande in commandes_demandees
    }


def tracer_carte_thermique(donnees, sortie, afficher=False):
    plt = charger_matplotlib()

    commandes = sorted(donnees)
    annees = sorted(
        {
            annee
            for mesures in donnees.values()
            for annee in mesures
        }
    )

    matrice = [
        [
            donnees[commande][annee][1]
            if annee in donnees[commande]
            else float("nan")
            for annee in annees
        ]
        for commande in commandes
    ]

    hauteur = max(8, len(commandes) * 0.27)
    fig, axe = plt.subplots(figsize=(18, hauteur))

    palette = plt.get_cmap("viridis").copy()
    palette.set_bad(color="#e5e7eb")
    image = axe.imshow(matrice, aspect="auto", interpolation="nearest", cmap=palette)

    axe.set_xticks(range(len(annees)), labels=annees, rotation=45, ha="right")
    axe.set_yticks(range(len(commandes)), labels=commandes)
    axe.tick_params(axis="y", labelsize=7)
    axe.set_xlabel("Annee")
    axe.set_ylabel("Commande")
    axe.set_title(
        "Evolution du nombre d'options des commandes par annee\n"
        "Gris : aucune mesure exploitable"
    )

    barre_couleur = fig.colorbar(image, ax=axe, pad=0.01)
    barre_couleur.set_label("Nombre d'options")

    fig.tight_layout()
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(sortie, dpi=200, bbox_inches="tight")
    print(f"Graphe genere : {sortie}")

    if afficher:
        plt.show()
    else:
        plt.close(fig)


def tracer_courbes(donnees, sortie, afficher=False):
    plt = charger_matplotlib()
    fig, axe = plt.subplots(figsize=(16, 9))
    commandes = sorted(donnees)
    couleurs = plt.get_cmap("tab20")

    for index, commande in enumerate(commandes):
        annees = sorted(donnees[commande])
        if not annees:
            continue
        nombres = [donnees[commande][annee][1] for annee in annees]
        style = "--" if commande.startswith("toybox ") else "-"
        axe.plot(
            annees,
            nombres,
            color=couleurs(index % 20),
            linestyle=style,
            marker="o",
            markersize=3,
            linewidth=1.6,
            label=commande,
        )

    axe.set_xlabel("Annee")
    axe.set_ylabel("Nombre d'options")
    axe.set_title(
        "Evolution du nombre d'options de 15 commandes connues\n"
        "Coreutils : trait plein - Toybox : pointilles"
    )
    axe.grid(alpha=0.25)
    axe.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)

    fig.tight_layout()
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(sortie, dpi=200, bbox_inches="tight")
    print(f"Graphe genere : {sortie}")

    if afficher:
        plt.show()
    else:
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Genere un graphe du nombre d'options par commande et par annee."
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DOSSIER_CSV,
        help=f"Dossier contenant les CSV. Par defaut : {DOSSIER_CSV}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=SORTIE_PAR_DEFAUT,
        help=f"Fichier image genere. Par defaut : {SORTIE_PAR_DEFAUT}",
    )
    parser.add_argument(
        "--mode",
        choices=("heatmap", "courbes"),
        default="heatmap",
        help="Type de graphe. La heatmap est recommandee pour toutes les commandes.",
    )
    parser.add_argument(
        "--commandes",
        nargs="*",
        help="Commandes a afficher, par exemple : --commandes ls cat cp",
    )
    parser.add_argument(
        "--inclure-erreurs",
        action="store_true",
        help="Inclure les lignes CSV contenant une erreur d'execution.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Afficher aussi le graphe dans une fenetre.",
    )
    args = parser.parse_args()

    donnees = lire_csv(args.csv_dir, args.inclure_erreurs)
    donnees = filtrer_commandes(donnees, args.commandes)

    if not donnees:
        print("Aucune donnee exploitable trouvee.")
        return 1

    if args.mode == "courbes":
        tracer_courbes(donnees, args.output, args.show)
    else:
        tracer_carte_thermique(donnees, args.output, args.show)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
