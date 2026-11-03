---
name: refactor
description: Change the structure of code without changing its behavior. Covers renames, extractions, consolidations, layering changes, API migrations, and deleting legacy paths. Use for "refactor", "clean this up", "restructure", "rename X to Y", "migrate callers", "remove the old API", or "simplify this module".
---

# Refactor

The structure changes. The behavior does not. If you find a bug or a missing feature, split it out. Ship the structural change first, against the pinned behavior.

## 1. Pin the behavior first

Record what the code does now with a characterization test, a snapshot of real output, or an equivalence harness that runs old and new side by side on the same inputs. A type check and lint are not a pin.

For a port or migration, the result must match the original exactly, bugs included. Fix the bugs afterwards, in their own change.

## 2. Subtract first

Remove dead code, one-caller wrappers, redundant validators, and orphan references before reshaping anything. Build on the simpler base.

## 3. Reshape

- The reshape must delete branches or invalid states, not add indirection. Boring code stays when its shape is already clear and local.
- Before adding a layer, ask whether it reduces reader load elsewhere by at least as much as it adds.
- Prefer returns over mutation, locals over fields, fields over module state, and module state over globals.
- For a mechanical change across many files, write the codemod or script. Do the first file by hand, run the script on that same file, and diff the result against your hand-made version. Then run it everywhere.

## 4. Migrate callers, then delete

For internal APIs, migrate every caller and delete the old API in the same change. No compatibility shims and no parallel old and new paths, unless an external consumer depends on the old API.

Update tests to assert the new contract. Delete tests that only protected pre-refactor internals.

## 5. Check renames against the files

Renames silently miss usages in strings, config, docs, SQL, serialized keys, and back-references. After each rename, grep for the old name across the repo, docs and migrations included. Name both sides of the rename in the PR.

## 6. Verify

Rerun the pin from step 1, and it must be unchanged. If the diff doesn't lower reader load somewhere, revert it.

Order the commits: subtraction, then the reshape, then cleanup.
