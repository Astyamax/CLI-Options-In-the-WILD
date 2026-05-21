#!/usr/bin/env bash

set -u

default_programs=(cat ls grep sed sort)

if [ "$#" -gt 0 ]; then
  programs=("$@")
else
  programs=("${default_programs[@]}")
fi

printf "%-12s %s\n" "programme" "nb_options"
printf "%-12s %s\n" "---------" "----------"

for prog in "${programs[@]}"; do
  if ! command -v "$prog" >/dev/null 2>&1; then
    printf "%-12s %s\n" "$prog" "N/A (introuvable)"
    continue
  fi

  help_text="$("$prog" --help 2>&1 || true)"

  count="$(
    printf "%s\n" "$help_text" \
      | grep -Eo -- '--[[:alnum:]][[:alnum:]-]*|-[[:alnum:]]' \
      | sort -u \
      | wc -l \
      | tr -d ' '
  )"

  printf "%-12s %s\n" "$prog" "$count"
done
