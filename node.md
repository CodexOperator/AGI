---
id: experiment:a01-095cec0b-115104
mint_id: 81fb8a4daba0433691114fb810167099
type: experiment
parents:
  - hypothesis:a01-dd74693c-b77b37
next_edges: []
edited_by: season.py
scaffold_hash: c45f6521ba0b3f60
season: 1
thought_session: season
title: A01 095cec0b 115104
---
# experiment:a01-095cec0b-115104

## Experiment

**Objective:** Logically verify hypothesis `a01-dd74693c-b77b37` — that restricting whole-tree commands to one designated committer per iteration eliminates the g4.1 collision pattern — by analyzing the hypothesis' claims against source data, assessing feasibility of the mechanism, and checking the status quo's track record.

**Method:** Source-code and document review. Four verification passes:

### Pass 1 — Factual verification against goal:g4.1

**Claim:** 2 of 3 recorded g4.1 collisions came from whole-tree commands.

Checked against g4.1's own narrative (`.agi/nodes/goal/g4.1-parallel-kids-share-one-working-tree.md`):

| Collision | Date | Command | Whole-tree? | Covered? |
|-----------|------|---------|-------------|----------|
| Stale-.pyc race — kid rewriting files while sibling runs tests | 2026-08-22 | (none — no command) | No | 1/3 not covered |
| `grid.py checkout --all` silently reverts sibling's uncommitted edits | 2026-08-25 | `grid.py checkout --all` | Yes | 1/2 covered |
| `git commit -A` sweeps sibling's half-written node + human's engine edits | 2026-08-31 | `git commit -A` | Yes | 2/2 covered |

**Result:** ✓ Claim verified. Exactly 2 of 3 involve whole-tree commands. The stale-.pyc race correctly scoped out — it is a build-system issue (`.pyc` cache invalidation), not a concurrent-edit problem.

### Pass 2 — Contract enforceability analysis

**Claim:** The restriction is enforceable via the agent contract (the brief's existing instructions) and costs zero lines of code beyond the brief.

Examined two sources:

1. **`extensions/agi/lib/agent-prompt.md` (permanent agent contract):** Rule 5 says *"Commit your work. Before signaling done, run: git add -A && git -c user.email=auto@autoresearch -c user.name=autoresearch commit -m ..."* This is a contradiction: the permanent prompt instructs agents to run the exact whole-tree commands the hypothesis proposes banning (for non-committers).

2. **Iteration-level context.md (session-specific override):** Contains *"DO NOT run git. No commit, no add, no push, no stash, no checkout. Automation owns all remote traffic and the parent owns commits."* This is the current blanket ban — already stricter than the hypothesis (zero committers vs one designated committer).

**Finding:** The iteration-level context override mechanism already exists and is proven effective for enforcing git restrictions. The hypothesis' mechanism is the same pattern — just specifying a committer. Feasibility: ✓ demonstrated by current practice. However, the permanent prompt (agent-prompt.md Rule 5) still contradicts both the current ban and the proposed relaxation — it tells agents to commit, which would need updating if the designated-committer approach is adopted.

### Pass 3 — Status quo track record vs hypothesis prediction

**Claim:** The restriction prevents the collision pattern. The status quo (all-git-banned since 2026-08-31) should have zero new g4.1 collisions.

The iteration context has carried the blanket ban since after the 2026-08-31 incident. No new tree-collisions reported in any subsequent iteration. The policy-forbids-git layer has been effective.

**Important caveat:** The status quo is STRICTER than the hypothesis (ban ALL vs ban all-but-one-committer). The zero-collision record is consistent with the hypothesis but cannot distinguish between "the restriction works" and "a designated committer would also be safe." Testing the relaxation requires actual parallel-agent experimentation across 3+ iterations — not possible in this single-agent isolated session.

### Pass 4 — Cross-comparison with sibling hypothesis a00-2278675f-5a913a (worktree isolation)

The sibling hypothesis proposed worktree isolation as the g4.1 fix. Experiment a00-67c6ae64-feb32a measured `git worktree add --detach` at:
- **Warm cache:** 0.094s mean (56× faster than the <5s bound)
- **Cold cache:** 0.80s mean (19× faster than the <15s bound)
- **2-kid overhead:** 0.19s total

**Implication for this hypothesis:** Worktree isolation was measured at effectively zero cost (0.09s checkout). It solves ALL 3/3 collision types, including the stale-.pyc race that the designated-committer approach scopes out. This hypothesis' stated advantage — "zero cost, cheaper than worktree" — is now moot: worktree is also near-zero cost and covers a wider problem space. The designated-committer approach remains a valid lighter-weight option for the 2/3 case, but the "cheaper" claim no longer holds.

## Evidence

Source documents examined:

- `nodes/goal/g4.1-parallel-kids-share-one-working-tree.md` — three collision records, 2 from whole-tree commands, stale-.pyc race explicitly non-command
- `extensions/agi/lib/agent-prompt.md` Rule 5 — `git add -A && git commit` instruction, contradicts current iteration-level ban
- `sessions/iter-1023/a01-095cec0b/context.md` — iteration-level blanket git ban in effect
- `nodes/experiment/a00-67c6ae64-feb32a.md` — worktree timing data (0.094s warm, 0.80s cold) from sibling
- `nodes/hypothesis/a01-dd74693c-b77b37.md` — hypothesis text: claims verified against g4.1

All analysis performed via document review — no runtime experiment.