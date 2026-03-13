import argparse
import csv
import json
import re
import shutil
import subprocess
from io import StringIO
from typing import Dict, List

# --- NOUVEAU CODE ICI ---
PROGRAM_CONFIGS = {
    "cat": ["--help"],
    "ls": ["--help"],
    "grep": ["--help"],
    "sed": ["--help"],
    "sort": ["--help"],
    "curl": ["--help", "all"],
    "tar": ["--help"]
}
# ------------------------

OPTION_PATTERN = re.compile(r"--[A-Za-z0-9][A-Za-z0-9-]*|-[A-Za-z0-9]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compte les options CLI detectees dans la sortie --help."
    )
    parser.add_argument(
        "programs",
        nargs="*",
        help="Programmes a analyser. Si vide, utilise une liste par defaut.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Affiche les options detectees pour chaque programme.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Affiche les resultats au format JSON.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Affiche les resultats au format CSV.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Chemin du fichier de sortie (texte, JSON ou CSV).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout en secondes pour chaque commande --help (defaut: 5).",
    )
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument(
        "--short-only",
        action="store_true",
        help="Ne compte que les options courtes de type -x.",
    )
    filter_group.add_argument(
        "--long-only",
        action="store_true",
        help="Ne compte que les options longues de type --option.",
    )
    return parser.parse_args()


def filter_options(options: List[str], short_only: bool, long_only: bool) -> List[str]:
    if short_only:
        return [opt for opt in options if opt.startswith("-") and not opt.startswith("--")]
    if long_only:
        return [opt for opt in options if opt.startswith("--")]
    return options


def analyze_program(program: str, timeout: float, short_only: bool, long_only: bool) -> Dict[str, object]:
    if shutil.which(program) is None:
        return {"program": program, "status": "N/A (introuvable)", "count": None, "options": []}
    try:
        result = subprocess.run(
            [program, "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"program": program, "status": "Timeout", "count": None, "options": []}
    except OSError as exc:
        return {"program": program, "status": f"Erreur execution: {exc}", "count": None, "options": []}

    options = sorted(set(OPTION_PATTERN.findall(result.stdout)))
    options = filter_options(options, short_only=short_only, long_only=long_only)
    return {"program": program, "status": "ok", "count": len(options), "options": options}


def as_text(results: List[Dict[str, object]], verbose: bool) -> str:
    lines = [f"{'programme':<12} nb_options", f"{'-' * 9:<12} {'-' * 10}"]
    for item in results:
        if item["status"] != "ok":
            lines.append(f"{item['program']:<12} {item['status']}")
            continue
        lines.append(f"{item['program']:<12} {item['count']}")
        if verbose:
            joined = ", ".join(item["options"])
            lines.append(f"  options: {joined}")

    ok_results = [item for item in results if item["status"] == "ok" and item["count"] is not None]
    total_programs = len(results)
    success_programs = len(ok_results)
    total_options = sum(int(item["count"]) for item in ok_results)
    avg_options = (total_options / success_programs) if success_programs else 0.0
    top3 = sorted(ok_results, key=lambda item: int(item["count"]), reverse=True)[:3]

    lines.append("")
    lines.append("summary")
    lines.append("-------")
    lines.append(f"programmes_total: {total_programs}")
    lines.append(f"programmes_ok: {success_programs}")
    lines.append(f"options_total: {total_options}")
    lines.append(f"options_moyenne: {avg_options:.2f}")
    if top3:
        top3_text = ", ".join(f"{item['program']}({item['count']})" for item in top3)
    else:
        top3_text = "N/A"
    lines.append(f"top3: {top3_text}")
    return "\n".join(lines)


def as_csv(results: List[Dict[str, object]]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["program", "status", "count", "options"])
    for item in results:
        options = ";".join(item["options"])
        writer.writerow([item["program"], item["status"], item["count"], options])
    return buffer.getvalue().strip("\n")


def main() -> int:
    args = parse_args()
    programs = args.programs if args.programs else DEFAULT_PROGRAMS
    results = [
        analyze_program(
            program,
            args.timeout,
            short_only=args.short_only,
            long_only=args.long_only,
        )
        for program in programs
    ]
    results.sort(key=lambda item: (item["status"] != "ok", -(item["count"] or 0), item["program"]))

    if args.json and args.csv:
        raise SystemExit("Erreur: utilise seulement un format entre --json et --csv.")

    if args.json:
        output_text = json.dumps(results, indent=2, ensure_ascii=False)
    elif args.csv:
        output_text = as_csv(results)
    else:
        output_text = as_text(results, args.verbose)

    print(output_text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out:
            out.write(output_text + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
