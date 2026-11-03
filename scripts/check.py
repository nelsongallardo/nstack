#!/usr/bin/env python3
"""Fail if any nstack skill is not wired up so agents will actually load it.

A skill that exists but isn't wired in is invisible in practice: agents pick
skills reliably only when the always-on core.md names them, the description
says it holds the user's own rules, and an eval proves it fires.
Run: python3 scripts/check.py   (also runs from .githooks/pre-commit)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_SKILL_LINES = 150
MAX_CORE_LINES = 80
DESC_PREFIX = "The user's own"
FILE_TYPE_HINT = re.compile(r"\.[a-z0-9]+ (?:or \.[a-z0-9]+ )?files?\b|any \.[a-z0-9]+")

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip().strip('"')
    return out


skills = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
core = (ROOT / "core.md").read_text()
core_lines = core.count("\n")
if core_lines > MAX_CORE_LINES:
    fail(f"core.md has {core_lines} lines; keep it under {MAX_CORE_LINES}")

map_rows = [line for line in core.splitlines() if line.startswith("|")]
map_names = set(re.findall(r"`([a-z0-9-]+)`", "\n".join(map_rows)))

grader_text = "\n".join(p.read_text() for p in (ROOT / "evals").glob("*/graders/*.md"))
rules_text = "\n".join(p.read_text() for p in (ROOT / "rules").glob("*.md"))

for name in skills:
    path = ROOT / "skills" / name / "SKILL.md"
    if not path.exists():
        fail(f"{name}: missing SKILL.md")
        continue
    text = path.read_text()
    fm = frontmatter(text)
    where = f"skills/{name}/SKILL.md"
    if fm.get("name") != name:
        fail(f"{where}: frontmatter name must be '{name}'")
    desc = fm.get("description", "")
    if not desc.startswith(DESC_PREFIX):
        fail(f"{where}: description must start with \"{DESC_PREFIX} ...\" so agents see it holds rules they don't know")
    lines = text.count("\n")
    if lines > MAX_SKILL_LINES:
        fail(f"{where}: {lines} lines; move detail into references/ (limit {MAX_SKILL_LINES})")
    if name not in map_names:
        fail(f"{name}: no row in the core.md situation map; agents won't load it")
    if not re.search(r"\)\?" + re.escape(name) + r'"', grader_text):
        fail(f"{name}: no eval case with a tool_used Skill grader for it (evals/<case>/graders/)")
    if FILE_TYPE_HINT.search(desc) and f"nstack:{name}" not in rules_text:
        fail(f"{name}: description names a file type but rules/ has no path rule loading nstack:{name}")

for stale in sorted(map_names - set(skills)):
    if stale in {"nstack"}:
        continue
    if re.search(r"\|\s*`" + re.escape(stale) + "`", core) or re.search(r",\s*`" + re.escape(stale) + "`", core):
        fail(f"core.md map names `{stale}`, which is not a skill")

for rule in sorted((ROOT / "rules").glob("*.md")):
    text = rule.read_text()
    if not frontmatter(text) and not text.startswith("---\npaths:"):
        fail(f"rules/{rule.name}: needs paths frontmatter")
    for ref in re.findall(r"nstack:([a-z0-9-]+)", text):
        if ref not in skills:
            fail(f"rules/{rule.name}: references missing skill nstack:{ref}")

if errors:
    print("nstack check failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"nstack check ok: {len(skills)} skills wired (core map, description, eval, path rules)")
