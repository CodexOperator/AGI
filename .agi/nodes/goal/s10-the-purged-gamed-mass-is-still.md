---
id: goal:s10
mint_id: 32ab6af9735040b6bc3242f903cc5ba8
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S10
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: retired
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S10: the purged gamed mass is still on disk inside agi-tree"
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

## Retired 2026-09-02 — the premise is gone, the residual is `goal:s25`

**Checked rather than assumed, which is what this goal asked for in the first
place.** `~/.hermes/agi-tree` holds **0 `.md` files and 0 `-extend*` nodes**;
`.claude/worktrees/wonderful-lamport-51c9a9/` is not in `git worktree list` and
does not exist. The 29,706-file mass this goal was written about is not on disk
anywhere. Fix (1) happened, by whatever route.

**Fix (2) did not, and it is the half that was never about today's 29k.**
`evidence_gate.build_corpus()` still takes a directory and `rglob`s it, so it
still resolves whatever it is handed. This goal said "do (2) regardless of (1)"
and it was right — deleting a stale tree removes today's fuel, not the hazard.
That residual is minted as **`goal:s25`** rather than kept alive here, because
this goal's title names a condition that is now false, and a goal whose premise
has evaporated cannot steer work honestly.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Retired on measurement, not on age. The sweep's rule this session was "horizon
unless provably moot", and this is the only one of 33 that cleared that bar:
its title asserts a file count and the file count is zero.

The judgement worth recording is that retiring it nearly lost a live defect.
This goal carried two fixes and only the first is moot. Marking it retired and
moving on would have deleted `build_corpus`'s missing guard from the tracker
entirely -- the goal's own closing line, "do (2) regardless of (1)", warning
against exactly the thing retiring it would do. Splitting the residual into
`goal:s25` is what makes the retirement honest rather than tidy.
<!-- THOUGHT:END -->