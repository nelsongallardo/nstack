# nstack evals

Each case checks that a realistic request loads the right nstack skill(s), using `tool_used: Skill` graders. Every skill must be covered by at least one case (`scripts/check.sh` enforces this).

Run from the repo root:

```
claude plugin eval . --scaffold --trust-plugin --ablation none --runs 1 -j 4 \
  --allow-tools Write Edit "Bash(git *)" "Bash(npm *)" "Bash(node *)" "Bash(ls *)" "Bash(cat *)"
```

- `--ablation none`: skip the no-plugin arm; these graders can only pass with the plugin.
- `--runs 1` for a quick check after a description or core.md change; `--runs 3` before a release.
- Results land in `evals/results/` (gitignored).
