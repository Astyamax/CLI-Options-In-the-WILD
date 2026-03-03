#!/usr/bin/env python3

import argparse
import re
import shutil
import subprocess
from typing import Dict, List


DEFAULT_PROGRAMS = ["cat", "ls", "grep", "sed", "sort"]
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
    return parser.parse_args()


def analyze_program(program: str) -> Dict[str, object]:
    if shutil.which(program) is None:
        return {"program": program, "status": "N/A (introuvable)", "count": None, "options": []}

    result = subprocess.run(
        [program, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )

    options = sorted(set(OPTION_PATTERN.findall(result.stdout)))
    return {"program": program, "status": "ok", "count": len(options), "options": options}


def print_table(results: List[Dict[str, object]], verbose: bool) -> None:
    print(f"{'programme':<12} nb_options")
    print(f"{'-' * 9:<12} {'-' * 10}")

    for item in results:
        if item["status"] != "ok":
            print(f"{item['program']:<12} {item['status']}")
            continue

        print(f"{item['program']:<12} {item['count']}")
        if verbose:
            joined = ", ".join(item["options"])
            print(f"  options: {joined}")


def main() -> int:
    args = parse_args()
    programs = args.programs if args.programs else DEFAULT_PROGRAMS
    results = [analyze_program(program) for program in programs]
    print_table(results, args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


