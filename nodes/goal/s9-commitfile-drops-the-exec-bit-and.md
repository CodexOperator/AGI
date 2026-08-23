---
confidence: 1.0
goal_id: S9
goal_kind: short-term
id: "goal:s9"
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S9: `commit_file()` drops the exec bit and mis-hashes symlinks"
type: goal
---

Found 2026-08-23 by `exp:grid-payload-roundtrip`, confirmed at the cited lines.
`bin/grid.py`:

- **`:154`** — `git hash-object -w str(path.resolve())`. `Path.resolve()`
  dereferences a symlink *before* hashing, so the object committed is the
  **target file's bytes**, not the link text. Not a dropped-metadata edge case: a
  silently wrong object, no error, no warning.
- **`:160`** — the tree line is `f"100644 blob {blob}\tnode.md\n"`. Mode is
  hardcoded, so any `100755` payload comes back `100644` and any `120000` comes
  back a regular file.

**Benign today, and it will not stay that way.** Grid only ever commits regular
node `.md` files under the fixed name `node.md`, and node files are not symlinks
and not executable — so nothing is currently wrong on disk. The defect activates
the moment a *payload* goes through the same call, which is exactly what
**G6.3** picked and what **G6.7** is built on. This is the rare case where the
right time to fix a latent bug is before its first caller, because both callers'
falsifiers are byte-comparisons that it would fail.

Fix: read the mode from `os.lstat()` (100644 / 100755 / 120000) and, for a
symlink, hash the `readlink()` target text via `hash-object --stdin` rather than
the dereferenced file — which is what `git add` does internally, built from the
four primitives `grid.py` already calls. A matching mode/symlink-aware read path
is needed in whatever resolves a payload back out. Estimated ~15–20 lines, and
the experiment's mode-aware variant is a working reference implementation
(`sessions/iter-9007/kid-c/sandbox/`, which is gitignored — port it, do not
depend on it).

Test: the experiment's own table is the regression suite — a 100755 file and a
120000 symlink, three version bumps each, sha256 against a non-git baseline.

Blocks **G6.3** and **G6.7**. One fix, two callers.
