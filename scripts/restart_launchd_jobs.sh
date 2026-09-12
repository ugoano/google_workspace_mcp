#!/usr/bin/env bash
set -euo pipefail

LABELS=(
  "com.arno.google-workspace-mcp"
  "com.arno.google-workspace-mcp-personal"
)

if [[ "$#" -gt 0 ]]; then
  LABELS=("$@")
fi

uid="$(id -u)"

for label in "${LABELS[@]}"; do
  target="gui/${uid}/${label}"
  if [[ "${DRY_RUN:-}" == "1" ]]; then
    printf 'launchctl kickstart -k %s\n' "$target"
    continue
  fi

  /bin/launchctl kickstart -k "$target"
done
