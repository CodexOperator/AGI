---
confidence: 1.0
goal_id: S10
goal_kind: short-term
id: "goal:s10"
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S10: the purged gamed mass is still on disk inside agi-tree"
type: goal
---

Found 2026-08-23. **G6.2 says the 28,916 gamed `-extend<N>` nodes were "removed
from the working tree and archived outside the repo." The first half is not
true.** `.claude/worktrees/wonderful-lamport-51c9a9/` — a git worktree registered
against a `~/.hermes/agi-tree/` path — still holds **29,706 `.md` files, 29,062
of them `-extend<N>` nodes**. They are gitignored, which is why nothing has
complained, and why nothing found them for two days.

**The hazard is specific and I walked into it while writing this iteration.**
`evidence_gate.build_corpus()` takes a directory and `rglob`s it for `*.md`.
Called on `nodes/` it returns 657 ids, correct. Called on the **project root** it
returns **29,582** — the pre-purge corpus, resurrected. A verdict citing a
deleted gamed node as `evidence_runs` would resolve against it and pass the gate,
which is H4c's fix silently undone.

**The engine is not currently affected, and that was checked rather than
assumed:** all three real callers pass `root / "nodes"` — `cli.py:85`,
`metrics.py:145`, `post_wire.py:137`. The bug was in the throwaway harness that
found it. But "the correct argument is passed at all three current call sites" is
a property of today's callers, not of the function, and the incorrect call took
one line to write.

Two independent fixes, and both are cheap:
1. **Delete the worktree.** `git worktree remove` / prune. This is **S4** C5,
   which is gated and explicitly last — this entry is the evidence for promoting
   it, because "archived, not deleted" was the deviation G6.2 recorded and it did
   not fully happen.
2. **Make `build_corpus` refuse a non-`nodes/` root**, or resolve `nodes/` itself
   from the project root rather than trusting the caller. A gate that cannot
   verify must fail closed — the function already argues exactly this for a
   `None` corpus, and should hold itself to it for a wrong directory.

Do (2) regardless of (1). Deleting the worktree removes today's 29k; it does not
stop the next stale tree from being swept in.
