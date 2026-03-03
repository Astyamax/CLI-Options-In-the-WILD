import re
import shutil
import subprocess
import sys


DEFAULT_PROGRAMS = ["cat", "ls", "grep", "sed", "sort"]
OPTION_PATTERN = re.compile(r"--[A-Za-z0-9][A-Za-z0-9-]*|-[A-Za-z0-9]")


def count_options(program: str) -> str:
    if shutil.which(program) is None:
        return "N/A (introuvable)"

    result = subprocess.run(
        [program, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )

    options = set(OPTION_PATTERN.findall(result.stdout))
    return str(len(options))

def main() -> int:
    programs = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_PROGRAMS

    print(f"{'programme':<12} nb_options")
    print(f"{'-' * 9:<12} {'-' * 10}")

    for program in programs:
        count = count_options(program)
        print(f"{program:<12} {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

