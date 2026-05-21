# Supported CLI parameters and program analysis

The analyzer counts options found in the help output of target programs.

## Program configuration
The default program list is defined in `src/compteur.py` and includes several common Unix commands.

For each supported program, the analyzer currently uses the associated help argument(s). Most programs are analyzed with `--help`, while some commands use custom arguments such as `-h`.

## Option counting behavior
- Short options are detected with a pattern like `-x`
- Long options are detected with a pattern like `--option`
- The analyzer counts each unique option once
- `--short-only` limits counting to short options
- `--long-only` limits counting to long options

## Notes
- The analyzer does not parse full command-line syntax; it extracts options from help output text.
- If a target program is not available on the system, it is reported as `N/A (introuvable)`.
- To support a new program, update `PROGRAM_CONFIGS` in `src/compteur.py` with the correct help argument(s).
