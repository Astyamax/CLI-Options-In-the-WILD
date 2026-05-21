# CLI Options in the Wild

## Project overview
This repository collects the project artifacts for the CLI option counting tool. It includes the main source code, analysis notebooks and visualizations, documentation, legacy code, and project planning materials.

## Repository structure
- `src/` — production Python source code
- `script/` — shell scripts and execution helpers
- `data/` — raw downloaded data and generated figures
- `docs/` — user documentation, planning, and sources
- `codebases/` — legacy code, experiments, and previous versions
- `analysis/` — analysis scripts, visualizations, UI prototypes
- `presentations/` — posters, slides, and deliverables

## Getting started
1. Use `python src/compteur.py --help` to view available options.
2. Review `docs/how-to-use.md` for usage examples and `docs/which-params-used.md` for parameter behavior.
3. Legacy code and experiments are available under `codebases/old_versions/`.

## Notes
- The current counter implementation analyzes CLI help output and counts options.
- Environment folders and temporary files are excluded from Git using `.gitignore`.

