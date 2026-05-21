# How to use CLI Options in the Wild

## Purpose
This project analyzes CLI programs and counts the options available in their help output.

## Run the main analyzer
From the repository root:

```bash
python src/compteur.py [PROGRAMS ...] [OPTIONS]
```

### Available options
- `-v`, `--verbose` — show detected options for each program
- `--json` — output results in JSON format
- `--csv` — output results in CSV format
- `-o`, `--output PATH` — write results to the specified file
- `--timeout N` — set a per-command timeout in seconds (default: 5.0)
- `--short-only` — count only short options like `-x`
- `--long-only` — count only long options like `--option`

### Example

```bash
python src/compteur.py ls grep --json
```

## Shell helper
The `script/compteur.sh` file is a simple shell helper for running the analyzer in a scripted environment.

## Project layout
- `src/` contains the main Python source code
- `script/` contains shell helpers
- `data/` contains raw downloads and figures
- `docs/` contains user documentation and planning materials
- `codebases/` contains legacy code and early versions
- `analysis/` contains visualizations and UI prototypes
- `presentations/` contains final deliverables
