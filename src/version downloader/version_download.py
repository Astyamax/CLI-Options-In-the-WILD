import requests
from git import Repo
from datetime import datetime
import subprocess
import os
import sys

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def ask_commands(prompt_label):
    """Ask the user to enter a list of shell commands, one per line.
    An empty line ends the input."""
    print(f"\n{prompt_label}")
    print("Enter one command per line. Leave a blank line when done.")
    commands = []
    while True:
        line = input("  > ").strip()
        if line == "":
            break
        commands.append(line)
    return commands


def run_commands(commands, cwd, label):
    """Run a list of shell commands in sequence inside `cwd`.
    Returns True if all commands succeeded, False otherwise."""
    results = []
    for cmd in commands:
        print(f"  $ {cmd}")
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        success = proc.returncode == 0
        status = "✓" if success else "✗"
        # Print last 20 lines of output for brevity
        output_lines = proc.stdout.strip().splitlines()
        for line in output_lines[-20:]:
            print(f"    {line}")
        results.append((cmd, success, proc.returncode))
        if not success:
            print(f"  [{status}] Command failed (exit {proc.returncode}): {cmd}")
            break   # Stop on first failure within a stage
        else:
            print(f"  [{status}] OK")
    return all(r[1] for r in results), results


# ─────────────────────────────────────────────
# 1. Locate and clone repo
# ─────────────────────────────────────────────

repo_url = input("repo URL : ")

local_path = "downloads/tmp/"
subprocess.run(["rm", "-rf", local_path])
repo = Repo.clone_from(repo_url, local_path)
print("Cloned.")

# ─────────────────────────────────────────────
# 2. Collect one tag per year
# ─────────────────────────────────────────────

tagged_versions = []
for tag in repo.tags:
    try:
        commit = tag.commit
        date = datetime.fromtimestamp(commit.committed_date)
        tagged_versions.append((tag.name, date))
    except ValueError:
        continue

latest_per_year = {}
for tag_name, date in tagged_versions:
    year = date.year
    if year not in latest_per_year or date > latest_per_year[year][1]:
        latest_per_year[year] = (tag_name, date)

print("\n--- Latest version per year ---")
for year in sorted(latest_per_year):
    tag_name, date = latest_per_year[year]
    print(f"  {year}: {tag_name}  ({date.strftime('%Y-%m-%d')})")

# ─────────────────────────────────────────────
# 3. Ask for build and test commands once
# ─────────────────────────────────────────────

build_commands = ask_commands("Build commands (run from repo root after each checkout):")
test_commands  = ask_commands("Test commands  (run after a successful build):")

# ─────────────────────────────────────────────
# 4. Loop over every year
# ─────────────────────────────────────────────

report = []   # [(year, tag, build_ok, test_ok)]

abs_path = os.path.abspath(local_path)

for year in sorted(latest_per_year):
    tag_name, date = latest_per_year[year]
    print(f"\n{'='*60}")
    print(f"  {year}  →  {tag_name}  ({date.strftime('%Y-%m-%d')})")
    print(f"{'='*60}")

    # Checkout the tag
    repo.git.checkout(tag_name, force=True)
    # Clean untracked files to avoid stale build artifacts
    repo.git.clean("-fdx")
    # Sync submodules to the exact versions this tag was pinned to
    repo.git.submodule("update", "--init", "--recursive")

    # Build
    print("\n[BUILD]")
    build_ok, _ = run_commands(build_commands, abs_path, "build")

    # Tests (only if build passed)
    test_ok = False
    if build_ok:
        print("\n[TEST]")
        test_ok, _ = run_commands(test_commands, abs_path, "test")
    else:
        print("\n[TEST] Skipped (build failed)")

    report.append((year, tag_name, build_ok, test_ok))

# ─────────────────────────────────────────────
# 5. Summary
# ─────────────────────────────────────────────

print(f"\n{'='*60}")
print("  SUMMARY")
print(f"{'='*60}")
print(f"  {'Year':<6} {'Tag':<20} {'Build':<8} {'Tests'}")
print(f"  {'-'*50}")
for year, tag_name, build_ok, test_ok in report:
    b = "✓ pass" if build_ok else "✗ FAIL"
    t = "✓ pass" if test_ok else ("✗ FAIL" if build_ok else "— skip")
    print(f"  {year:<6} {tag_name:<20} {b:<8} {t}")