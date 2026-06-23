"""
Analyse des options de programmes CLI à partir d'un dossier de CSV.

Sous-commandes :
  latest     Crée un CSV avec le nombre d'options de la dernière version de chaque programme.
  by-year    Crée un CSV avec le nombre d'options par année pour chaque programme (depuis 2005).

Exemples :
  python analyze_options.py latest
  python analyze_options.py latest --csv-dir mon_dossier --output résultat.csv --failed erreurs.txt

  python analyze_options.py by-year
  python analyze_options.py by-year --csv-dir mon_dossier --output par_année.csv --since 2005
"""

import os
import glob
import argparse
import pandas as pd


# Utilitaires communs

def program_name_from_path(path: str) -> str:
    """Déduit le nom du programme depuis le nom de fichier.
    Ex : coreutils___cat.csv → cat, grep.csv → grep
    """
    basename = os.path.splitext(os.path.basename(path))[0]
    if "___" in basename:
        return basename.split("___", 1)[1]
    return basename


def load_and_parse(path: str) -> pd.DataFrame | None:
    """Charge un CSV, parse les dates et filtre les lignes invalides.
    Retourne None si le fichier est vide, illisible ou manque de colonnes.
    """
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"  [ERREUR lecture] {e}")
        return None

    if df.empty:
        return None

    required_cols = {"date", "nombre_options"}
    if not required_cols.issubset(df.columns):
        print(f"  [ERREUR colonnes] Colonnes manquantes : {required_cols - set(df.columns)}")
        return None

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "nombre_options"])

    return df if not df.empty else None


def iter_csv_files(csv_dir: str):
    """Génère les chemins de tous les CSV du dossier, triés."""
    files = sorted(glob.glob(os.path.join(csv_dir, "*.csv")))
    if not files:
        raise FileNotFoundError(f"Aucun fichier CSV trouvé dans '{csv_dir}'.")
    return files


# Sous-commande : latest

def cmd_latest(args):
    """Crée un CSV avec le nombre d'options de la dernière version de chaque programme."""
    try:
        csv_files = iter_csv_files(args.csv_dir)
    except FileNotFoundError as e:
        print(e)
        return

    results, failed = [], []

    for path in csv_files:
        prog = program_name_from_path(path)
        print(f"Traitement : {prog}  ({os.path.basename(path)})")

        df = load_and_parse(path)
        if df is None:
            print("  → Ignoré (CSV vide, illisible ou données invalides)")
            failed.append(prog)
            continue

        latest = df.loc[df["date"].idxmax()]
        results.append({
            "programme":     latest["programme"] if "programme" in df.columns else prog,
            "commande":      latest["commande"]  if "commande"  in df.columns else prog,
            "version":       latest["version"]   if "version"   in df.columns else "",
            "date":          str(latest["date"].date()),
            "nombre_options": int(latest["nombre_options"]),
        })
        print(f"  → version {latest.get('version', '?')} ({latest['date'].date()}) : {int(latest['nombre_options'])} options")

    # CSV de sortie
    if results:
        out_df = pd.DataFrame(results, columns=["programme", "commande", "version", "date", "nombre_options"])
        out_df.to_csv(args.output, index=False)
        print(f"\n✓ {len(results)} programmes écrits dans '{args.output}'")
    else:
        print("\nAucun résultat à écrire.")

    # Fichier des échecs
    if failed:
        with open(args.failed, "w", encoding="utf-8") as f:
            f.write("\n".join(failed) + "\n")
        print(f"✗ {len(failed)} programmes en échec listés dans '{args.failed}' : {', '.join(failed)}")
    else:
        print("Aucun programme en échec.")


# Sous-commande : by-year

def get_yearly_values(df: pd.DataFrame, since: int) -> list[dict]:
    """Pour chaque année de `since` à l'année max des données,
    conserve la ligne dont la date est la plus récente dans l'année.
    Les années sans release sont sautées (aucune ligne produite).
    """
    df = df.sort_values("date").copy()
    df["year"] = df["date"].dt.year
    year_max = int(df["year"].max())
    rows = []

    for year in range(since, year_max + 1):
        year_data = df[df["year"] == year]
        if year_data.empty:
            continue
        latest = year_data.loc[year_data["date"].idxmax()]
        rows.append({
            "année":          year,
            "nombre_options": int(latest["nombre_options"]),
            "version":        latest.get("version", ""),
        })

    return rows


def cmd_by_year(args):
    """Crée un CSV avec le nombre d'options par année pour chaque programme."""
    try:
        csv_files = iter_csv_files(args.csv_dir)
    except FileNotFoundError as e:
        print(e)
        return

    all_rows = []

    for path in csv_files:
        prog = program_name_from_path(path)
        print(f"Traitement : {prog}  ({os.path.basename(path)})")

        df = load_and_parse(path)
        if df is None:
            print("  → Ignoré")
            continue

        programme = df["programme"].iloc[0] if "programme" in df.columns else prog
        commande  = df["commande"].iloc[0]  if "commande"  in df.columns else prog

        yearly = get_yearly_values(df, args.since)
        if not yearly:
            print(f"  → Aucune donnée valide depuis {args.since}")
            continue

        for entry in yearly:
            all_rows.append({
                "programme":     programme,
                "commande":      commande,
                "année":         entry["année"],
                "nombre_options": entry["nombre_options"],
                "version":       entry["version"],
            })

        print(f"  → {len(yearly)} années enregistrées ({yearly[0]['année']}–{yearly[-1]['année']})")

    if all_rows:
        out_df = pd.DataFrame(all_rows, columns=["programme", "commande", "année", "nombre_options", "version"])
        out_df.to_csv(args.output, index=False)
        print(f"\n✓ {len(all_rows)} lignes écrites dans '{args.output}'")
    else:
        print("\nAucun résultat à écrire.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- latest --
    p_latest = subparsers.add_parser(
        "latest",
        help="Nombre d'options de la dernière version de chaque programme",
    )
    p_latest.add_argument("--csv-dir", default="csv",                 help="Dossier CSV source (défaut: csv)")
    p_latest.add_argument("--output",  default="latest_options.csv",  help="CSV de sortie (défaut: latest_options.csv)")
    p_latest.add_argument("--failed",  default="failed_programs.txt", help="Fichier des échecs (défaut: failed_programs.txt)")

    # -- by-year --
    p_year = subparsers.add_parser(
        "by-year",
        help="Nombre d'options par année pour chaque programme",
    )
    p_year.add_argument("--csv-dir", default="csv",                help="Dossier CSV source (défaut: csv)")
    p_year.add_argument("--output",  default="options_by_year.csv", help="CSV de sortie (défaut: options_by_year.csv)")
    p_year.add_argument("--since",   type=int, default=2005,       help="Année de départ (défaut: 2005)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "latest":
        cmd_latest(args)
    elif args.command == "by-year":
        cmd_by_year(args)


if __name__ == "__main__":
    main()