#!/usr/bin/env bash
# Installs nstack for Codex: links each skill into ~/.codex/skills and writes
# core.md into a marked block in ~/.codex/AGENTS.md. Idempotent; re-run after pulling.
# Claude Code uses the plugin instead:
#   /plugin marketplace add nelsongallardo/nstack && /plugin install nstack@nstack
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
dry_run=0
[ "${1:-}" = "--dry-run" ] && dry_run=1

run() { if [ "$dry_run" = 1 ]; then printf 'would: %s\n' "$*"; else "$@"; fi; }

run mkdir -p "$codex_home/skills"
for dir in "$root"/skills/*/; do
  name="$(basename "$dir")"
  target="$codex_home/skills/$name"
  if [ -L "$target" ]; then
    run ln -sfn "${dir%/}" "$target"
  elif [ -e "$target" ]; then
    printf 'skip %s: %s exists and is not an nstack link\n' "$name" "$target" >&2
  else
    run ln -s "${dir%/}" "$target"
  fi
done

agents="$codex_home/AGENTS.md"
begin='<!-- nstack:core begin -->'
end='<!-- nstack:core end -->'
block="$(printf '%s\n%s\n%s' "$begin" "$(<"$root/core.md")" "$end")"
if [ "$dry_run" = 1 ]; then
  printf 'would: write nstack core block into %s\n' "$agents"
else
  touch "$agents"
  rest="$(awk -v b="$begin" -v e="$end" '$0==b{skip=1} !skip{print} $0==e{skip=0}' "$agents")"
  tmp="$(mktemp)"
  if [ -n "$rest" ]; then printf '%s\n\n%s\n' "$rest" "$block" > "$tmp"; else printf '%s\n' "$block" > "$tmp"; fi
  mv "$tmp" "$agents"
fi
printf 'nstack installed for Codex (%s)\n' "$codex_home"
