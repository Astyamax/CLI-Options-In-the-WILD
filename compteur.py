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



