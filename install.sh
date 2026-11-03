#!/usr/bin/env bash
# Installs the parts of nstack that the Claude Code plugin can't carry, plus Codex support.
# Idempotent: re-run after every pull.
#   - Claude Code: copies path-scoped rules into ~/.claude/rules/ (copies, not symlinks:
#     Claude Code doesn't load path-scoped rules through symlinks that leave the project).
#     The skills and core.md come from the plugin:
#       /plugin marketplace add nelsongallardo/nstack && /plugin install nstack@nstack
#   - Codex: links each skill into ~/.codex/skills and writes core.md into a marked
#     block in ~/.codex/AGENTS.md.
#   - This clone: enables the pre-commit hook that runs scripts/check.py.
# Usage: install.sh [--dry-run]
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
dry_run=0
[ "${1:-}" = "--dry-run" ] && dry_run=1

run() { if [ "$dry_run" = 1 ]; then printf 'would: %s\n' "$*"; else "$@"; fi; }

python3 -I "$root/scripts/check.py"

# Claude Code path rules
run mkdir -p "$claude_home/rules"
for old in "$claude_home"/rules/nstack-*.md; do
  [ -e "$old" ] || continue
  [ -e "$root/rules/$(basename "$old")" ] || run rm "$old"
done
for rule in "$root"/rules/nstack-*.md; do
  run cp "$rule" "$claude_home/rules/$(basename "$rule")"
done

# Codex skills
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
for link in "$codex_home"/skills/*; do
  [ -L "$link" ] || continue
  case "$(readlink "$link")" in
    "$root"/skills/*) [ -d "$(readlink "$link")" ] || run rm "$link" ;;
  esac
done

# Codex core block
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

# Pre-commit hook for this clone
if [ -d "$root/.git" ]; then
  run git -C "$root" config core.hooksPath .githooks
fi

printf 'nstack installed: Claude rules in %s/rules, Codex in %s\n' "$claude_home" "$codex_home"
