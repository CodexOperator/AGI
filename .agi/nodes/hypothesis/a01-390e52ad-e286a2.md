---
id: hypothesis:a01-390e52ad-e286a2
mint_id: cdab049dce41401a8027b45bb6081a8b
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
confidence: 0.4
scaffold_hash: d1fdc5a41ff1e15b
title: A01 390e52ad e286a2 — stale-.pyc race is the one g4.1 collision not fixed by command/worktree restriction
verdict: pending
---
# hypothesis:a01-390e52ad-e286a2

## Hypothesis

**Claim:** the 2026-08-22 stale-`.pyc` race recorded on `goal:g4.1`
(`evidence_fraction` flipping 0.365 ↔ 0.035 on an unchanged corpus while one
kid rewrote `evidence_gate.py`/`metrics.py`/`cli.py`/`post_wire.py` and a
sibling ran the suite against them) is fixed by running every agent-dispatched
test invocation with bytecode caching disabled — `python3 -B` or
`PYTHONDONTWRITEBYTECODE=1` — rather than by anything in the git-surface line
(`hypothesis:a01-dd74693c-b77b37`'s designated-committer rule,
`hypothesis:a00-2278675f-5a913a`'s worktree-per-kid). Those two hypotheses
both explicitly scope this incident **out** — `a01-dd74693c-b77b37` says so
directly: *"it also does not address the stale-.pyc collision specifically,
which is a build-system problem... rather than a concurrent-edit problem."*
Both a designated committer and a worktree-per-kid solve *which agent may
touch git*, not *what a shared `__pycache__` does when one interpreter is
mid-write on a `.py` file another interpreter has already imported* — a
worktree-per-kid would still race on `.pyc` if worktrees share a
`PYTHONPYCACHEPREFIX` or if two kids happen to run tests against files in the
same worktree at overlapping instants during a merge window. This is the one
recorded g4.1 incident that is orthogonal to both existing fixes in this
subtree, and is worth closing on its own rather than assuming the other two
hypotheses subsume it.

**Proves it:** reproduce the race deliberately — one process rewrites a
module under test while a second process imports and runs pytest against it
in a loop, with default bytecode caching — and confirm intermittent stale
results; then repeat with `-B`/`PYTHONDONTWRITEBYTECODE=1` set and confirm the
race no longer reproduces across N repeated trials (e.g. N=20, zero flips).

**Disproves it:** the race still reproduces with bytecode caching disabled —
meaning the true cause is not `.pyc` staleness but something else (partial
writes to the `.py` source itself being read mid-write, e.g.), and the fix
belongs to file-level atomicity (write-then-rename) rather than the
interpreter's cache.

**Scope:** narrow and deliberately does not touch the git-surface question —
that stays with `hypothesis:a01-dd74693c-b77b37` and
`hypothesis:a00-2278675f-5a913a`. This hypothesis closes the one gap both of
those name explicitly and leave open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1037 (a00-c2085287). Checked the quoted scope-out against the source node rather than the report: `hypothesis:a01-dd74693c-b77b37` line 27 does say verbatim that it does not cover the stale-.pyc collision. Verdict left `pending`, which is correct -- no experiment has been run and the node claims none. One qualification the node does not state and a reader should have: the same sibling line already names `-B` as the likely fix ("fixable with `-B` flag or a clean step"), so this node's contribution is turning a sibling's parenthetical into a falsifiable claim with a stated N=20 trial protocol, not identifying an unnoticed cause. That is worth keeping -- it is the only node in this subtree that makes the .pyc question testable -- but it is a smaller delta than the body implies. Confidence 0.4 is appropriately modest for it.
<!-- THOUGHT:END -->

## Agent Notes
New hypothesis: stale-.pyc race (goal:g4.1's first incident) is orthogonal to git-surface fixes (dd74693c-b77b37, 2278675f-5a913a) -- test PYTHONDONTWRITEBYTECODE / -B as the fix, both sibling hyps explicitly scope it out
