import argparse
import csv
from datetime import date
from pathlib import Path
from statistics import mean, median, quantiles


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


def extraire_dernieres_mesures(donnees):
    mesures = []

    for commande, valeurs_par_annee in donnees.items():
        if not valeurs_par_annee:
            continue

        date_version, nombre_options = max(
            valeurs_par_annee.values(),
            key=lambda mesure: mesure[0],
        )
        mesures.append((commande, date_version, nombre_options))

    mesures.sort(key=lambda mesure: (mesure[2], mesure[0]))
    return mesures


def categorie_commande(commande):
    if commande == "ffmpeg":
        return "FFmpeg", "#7c3aed"
    if commande.startswith("toybox "):
        return "Toybox", "#0f766e"
    return "Coreutils", "#2563eb"


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


def tracer_boxplot(donnees, sortie, afficher=False):
    plt = charger_matplotlib()

    mesures = extraire_dernieres_mesures(donnees)

    if not mesures:
        raise ValueError("No usable latest-version data found.")

    valeurs = [mesure[2] for mesure in mesures]
    moyenne = mean(valeurs)
    mediane = median(valeurs)
    minimum = min(valeurs)
    maximum = max(valeurs)
    premier_quartile, _, troisieme_quartile = quantiles(
        valeurs,
        n=4,
        method="inclusive",
    )

    fig, axe = plt.subplots(figsize=(12, 10))
    axe.boxplot(
        valeurs,
        vert=True,
        widths=0.32,
        whis=(0, 100),
        showmeans=True,
        showfliers=False,
        patch_artist=True,
        boxprops={"facecolor": "#dbeafe", "edgecolor": "#1f2937", "linewidth": 1.5},
        whiskerprops={"color": "#1f2937", "linewidth": 1.5},
        capprops={"color": "#1f2937", "linewidth": 1.5},
        medianprops={"color": "#dc2626", "linewidth": 2},
        meanprops={
            "marker": "D",
            "markerfacecolor": "#f59e0b",
            "markeredgecolor": "#92400e",
            "markersize": 8,
        },
    )

    nombre_mesures = len(mesures)
    points = []

    afficher_etiquettes = nombre_mesures <= 30

    for index, (commande, date_version, nombre_options) in enumerate(mesures):
        decalage = (((index * 37) % 101) - 50) / 500
        position_x = 1 + decalage
        categorie, couleur = categorie_commande(commande)

        axe.scatter(
            position_x,
            nombre_options,
            color=couleur,
            edgecolor="white",
            linewidth=0.7,
            s=48,
            zorder=3,
        )

        points.append(
            {
                "commande": commande,
                "date": date_version,
                "valeur": nombre_options,
                "x": position_x,
                "couleur": couleur,
                "cote_droit": categorie != "Toybox",
            }
        )

    if afficher_etiquettes:
        def repartir_positions(points_cote, ecart=2.2):
            points_tries = sorted(points_cote, key=lambda point: point["valeur"])
            position_precedente = None

            for point in points_tries:
                position = point["valeur"]
                if position_precedente is not None:
                    position = max(position, position_precedente + ecart)
                point["position_etiquette"] = position
                position_precedente = position

            return points_tries

        for cote_droit in (False, True):
            points_cote = repartir_positions(
                [point for point in points if point["cote_droit"] == cote_droit]
            )
            position_texte = 1.24 if cote_droit else 0.76
            alignement = "left" if cote_droit else "right"

            for point in points_cote:
                axe.annotate(
                    (
                        f"{point['commande']}: {point['valeur']} "
                        f"({point['date'].year})"
                    ),
                    xy=(point["x"], point["valeur"]),
                    xytext=(position_texte, point["position_etiquette"]),
                    ha=alignement,
                    va="center",
                    fontsize=8,
                    color=point["couleur"],
                    bbox={
                        "facecolor": "white",
                        "edgecolor": "none",
                        "alpha": 0.82,
                        "pad": 0.4,
                    },
                    arrowprops={
                        "arrowstyle": "-",
                        "color": point["couleur"],
                        "alpha": 0.45,
                        "linewidth": 0.8,
                    },
                )

    axe.axhline(moyenne, color="#f59e0b", linestyle="--", linewidth=1.3, alpha=0.8)
    axe.axhline(mediane, color="#dc2626", linestyle=":", linewidth=1.3, alpha=0.8)

    resume = (
        f"Commands: {nombre_mesures}\n"
        f"Minimum: {minimum}\n"
        f"Maximum: {maximum}\n"
        f"Mean: {moyenne:.1f}\n"
        f"Median: {mediane:.1f}\n"
        f"Q1: {premier_quartile:.1f}\n"
        f"Q3: {troisieme_quartile:.1f}"
    )
    axe.text(
        0.98,
        0.98,
        resume,
        transform=axe.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "#9ca3af", "alpha": 0.9},
    )

    axe.scatter([], [], color="#2563eb", label="Coreutils")
    axe.scatter([], [], color="#0f766e", label="Toybox")
    axe.scatter([], [], color="#7c3aed", label="FFmpeg")
    axe.plot([], [], color="#dc2626", linestyle=":", label="Median")
    axe.plot([], [], color="#f59e0b", linestyle="--", label="Mean")
    axe.legend(loc="upper left")

    axe.set_xticks([1], ["Latest available version"])
    axe.set_ylabel("Number of options")
    axe.set_title(
        "Distribution of option counts for all available commands\n"
        "One point per command, using its latest available version"
    )
    axe.grid(axis="y", alpha=0.25)
    axe.set_xlim(0.55, 1.45)

    fig.tight_layout()
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(sortie, dpi=200, bbox_inches="tight")
    print(f"Graph generated: {sortie}")

    if afficher:
        plt.show()
    else:
        plt.close(fig)


def tracer_violinplot(donnees, sortie, afficher=False):
    plt = charger_matplotlib()
    mesures = extraire_dernieres_mesures(donnees)

    if not mesures:
        raise ValueError("No usable latest-version data found.")

    valeurs = [mesure[2] for mesure in mesures]
    moyenne = mean(valeurs)
    mediane = median(valeurs)
    minimum = min(valeurs)
    maximum = max(valeurs)
    premier_quartile, _, troisieme_quartile = quantiles(
        valeurs,
        n=4,
        method="inclusive",
    )

    fig, axe = plt.subplots(figsize=(12, 10))
    violin = axe.violinplot(
        valeurs,
        positions=[1],
        widths=0.7,
        orientation="vertical",
        showmeans=True,
        showmedians=True,
        showextrema=True,
        quantiles=[[0.25, 0.75]],
    )

    for corps in violin["bodies"]:
        corps.set_facecolor("#bfdbfe")
        corps.set_edgecolor("#1f2937")
        corps.set_alpha(0.75)
        corps.set_linewidth(1.3)

    for nom_element in ("cbars", "cmins", "cmaxes", "cquantiles"):
        violin[nom_element].set_color("#1f2937")
        violin[nom_element].set_linewidth(1.2)

    violin["cmeans"].set_color("#f59e0b")
    violin["cmeans"].set_linewidth(2)
    violin["cmedians"].set_color("#dc2626")
    violin["cmedians"].set_linewidth(2)

    for index, (commande, _, nombre_options) in enumerate(mesures):
        decalage = (((index * 37) % 101) - 50) / 360
        _, couleur = categorie_commande(commande)
        axe.scatter(
            1 + decalage,
            nombre_options,
            color=couleur,
            edgecolor="white",
            linewidth=0.45,
            s=28,
            alpha=0.72,
            zorder=3,
        )

    resume = (
        f"Commands: {len(mesures)}\n"
        f"Minimum: {minimum}\n"
        f"Maximum: {maximum}\n"
        f"Mean: {moyenne:.1f}\n"
        f"Median: {mediane:.1f}\n"
        f"Q1: {premier_quartile:.1f}\n"
        f"Q3: {troisieme_quartile:.1f}"
    )
    axe.text(
        0.98,
        0.98,
        resume,
        transform=axe.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "#9ca3af", "alpha": 0.9},
    )

    axe.scatter([], [], color="#2563eb", label="Coreutils")
    axe.scatter([], [], color="#0f766e", label="Toybox")
    axe.scatter([], [], color="#7c3aed", label="FFmpeg")
    axe.plot([], [], color="#dc2626", linewidth=2, label="Median")
    axe.plot([], [], color="#f59e0b", linewidth=2, label="Mean")
    axe.legend(loc="upper left")

    axe.set_xticks([1], ["Latest available version"])
    axe.set_ylabel("Number of options (symlog scale)")
    axe.set_title(
        "Distribution of option counts for all available commands\n"
        "One point per command, using its latest available version"
    )
    axe.grid(axis="y", alpha=0.25)
    axe.set_xlim(0.5, 1.5)
    axe.set_yscale("symlog", linthresh=10, linscale=1.2)
    axe.set_ylim(bottom=min(0, minimum))

    fig.tight_layout()
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(sortie, dpi=200, bbox_inches="tight")
    print(f"Graph generated: {sortie}")

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
        choices=("heatmap", "courbes", "boxplot", "violin"),
        default="heatmap",
        help="Type de graphe : heatmap, courbes, boxplot ou violin.",
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
    elif args.mode == "boxplot":
        tracer_boxplot(donnees, args.output, args.show)
    elif args.mode == "violin":
        tracer_violinplot(donnees, args.output, args.show)
    else:
        tracer_carte_thermique(donnees, args.output, args.show)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
