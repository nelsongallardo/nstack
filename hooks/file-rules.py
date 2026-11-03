#!/usr/bin/env python3
"""PostToolUse hook: when a tool touches a file that matches a rule in rules/,
tell the agent to load the matching nstack skill. Each rule fires once per session.

Reads the hook event JSON on stdin and prints hookSpecificOutput.additionalContext.
Works in Claude Code (Read/Edit/Write/MultiEdit/NotebookEdit) and Codex (apply_patch).
"""
import json
import os
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or pathlib.Path(__file__).resolve().parent.parent)
PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.M)


def glob_to_regex(pattern: str) -> re.Pattern:
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(r"(?:^|/)" + out + r"$")


def load_rules():
    rules = []
    for path in sorted((ROOT / "rules").glob("*.md")):
        text = path.read_text()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            continue
        globs = re.findall(r'^\s*-\s*"([^"]+)"', m.group(1), re.M)
        rules.append((path.stem, [glob_to_regex(g) for g in globs], m.group(2).strip()))
    return rules


def touched_paths(event: dict) -> list[str]:
    tool_input = event.get("tool_input") or {}
    paths = [tool_input.get(k) for k in ("file_path", "path", "notebook_path")]
    for value in tool_input.values():
        if isinstance(value, str):
            paths += PATCH_FILE.findall(value)
    return [p.strip() for p in paths if isinstance(p, str) and p.strip()]


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    paths = touched_paths(event)
    if not paths:
        return
    session = re.sub(r"[^A-Za-z0-9_-]", "", str(event.get("session_id") or "nosession"))[:80]
    state = pathlib.Path(tempfile.gettempdir()) / "nstack-file-rules" / session
    messages = []
    for name, patterns, body in load_rules():
        marker = state / name
        if marker.exists():
            continue
        if any(p.search(path) for p in patterns for path in paths):
            state.mkdir(parents=True, exist_ok=True)
            marker.touch()
            messages.append(body)
    if messages:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "\n\n".join(messages),
        }}))


if __name__ == "__main__":
    main()
