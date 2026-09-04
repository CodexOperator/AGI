---
id: hypothesis:a01-842229f0-866d68
mint_id: cb14fece07fe4cf48716ce9321af821d
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
confidence: 0.0
scaffold_hash: 9c50dc31b2edb229
title: Worktree isolation prevents all 3 g4.1 collision types structurally — benefit unmeasured, cost proved negligible
verdict: pending
---
# hypothesis:a01-842229f0-866d68

## Hypothesis

**Claim:** The worktree isolation overhead is proved negligible (0.094s warm,
0.80s cold — `verdict:a00-4c4fbb51-0f3630`). The benefit side of that
equation — *whether worktree separation functionally prevents all three
g4.1 collision types* — has never been verified experimentally. It is
*cited* by sibling `verdict:a01-71c62f4b-49e913` as covering "all 3/3
collision types including the stale-.pyc race" but this is an analytical
claim, not a measured one. The stale-.pyc race claim is untested even
analytically: experiment `a01-398eadb0-23428a` enumerated 6 whole-tree
tools (`bash`, `run_experiment`, `write`, `edit`, `subagent`,
`ralph_start`) available to every pi-harness kid — and worktree isolation
contains their blast radius structurally, without any per-tool restriction.

**The specific claims:**

1. **`git commit -A` sweep (2026-08-31):** A `git commit -A` in worktree A
touches only worktree A's index and working files — it cannot sweep
worktree B's files into the commit. Worktree A's `.git`-linked object
store means `git add -A` stages files from worktree A only; the sibling's
half-written node in worktree B is invisible. **Structurally prevented by
the `git worktree` design itself** — each linked working tree has its own
`HEAD`, index, and per-worktree refs.

2. **`grid.py checkout --all` revert (2026-08-25):** `grid.py checkout
--all` is a `git checkout .` on its payload tree. If each kid lives in its
own worktree, a checkout called from worktree A operates only on worktree
A's files. Worktree B's uncommitted edits are in a different working tree;
they cannot be silently reverted. **Structurally prevented by worktree
boundaries** — `git checkout .` in one tree cannot touch files in another.

3. **Stale-.pyc race (2026-08-22):** Two kids in the same checkout: one
rewrites `.py` files while a sibling runs tests against them. `__pycache__`
dirs are per-working-tree under `git worktree` — each worktree has its own
`extensions/agi/bin/__pycache__/` parallel to the source. Kid A's writes
land in worktree A's `__pycache__`; Kid B's test imports from worktree B's
`__pycache__`. They cannot cross-contaminate. **Structurally prevented —
separate working directories = separate bytecode caches, regardless of
PYTHONDONTWRITEBYTECODE.** No interpreter flag needed.

**What about experiment `a01-390e52ad-e286a2` (stale-.pyc via
PYTHONDONTWRITEBYTECODE)?** That hypothesis proposes disabling the
bytecode cache entirely as the fix. Worktree isolation also fixes the
stale-.pyc incident — by a *different mechanism* (separate caches vs no
caches) — and covers the other 2 incidents too. This does not invalidate
that hypothesis; it means worktree isolation is a *broader* fix that
addresses the stale-.pyc gap explicitly left open by `a01-dd74693c-b77b37`
and `a00-2278675f-5a913a`, without needing the `-B` flag.

---

**Proves it:** A deliberate reproduction experiment demonstrates that each
of the three incident types cannot occur across worktree boundaries.
Method: create two worktrees (A and B) from the same repo. Place an
uncommitted file in each. From worktree A, run each of the three whole-tree
commands (`git commit -A`, `git checkout .`, a python import sequence that
would exercise `__pycache__` staleness). Verify after each that worktree
B's files are untouched and its git state is unmodified. Repeat with the
roles swapped. A single pass confirms structural prevention for each
incident type.

**Disproves it:** A test shows that worktree boundaries do NOT isolate in
practice — e.g., `git worktree prune` removes per-worktree refs
unexpectedly and orphans a kid's work, or `git gc` on one worktree
compresses the shared `.git/objects` and corrupts another worktree's
reachable objects, or Python's `.pyc` resolution resolves to a parent-path
cache across worktrees under certain import arrangements (`sys.path`
issues). Or: worktree isolation introduces a *new* collision mode where
the cost of sharing `.git/objects` across worktrees causes a cross-kid
git operation to block.

**Scope:** This hypothesis tests the *structural prevention* claim only,
not the hierarchy questions (whose worktree, merge before review among
nested tiers, what an iteration commit means across N branches). Those
remain open per goal:g4.1's explicit flag for a dedicated session.

---

**Relation to sibling hypotheses**

| Hypothesis | Mechanism | Collisions covered | Structural? | Harness change? |
|---|---|---|---|---|
| `a00-2278675f-5a913a` (worktree cost) | Measured overhead; proved at 0.09s | N/A (cost only) | Yes | Yes (dispatch creates worktrees) |
| `a01-dd74693c-b77b37` (designated committer) | Contract: one kid runs whole-tree commands | 2/3 (excludes .pyc race) | No | No |
| `a00-4ed0dccd-68c060` (command-scoped isolation) | Whitelist per kid | 3/3 claimed, blocked on pi SDK | No | Yes (pi tool filter needed) |
| `a01-390e52ad-e286a2` (stale-.pyc via `-B`) | PYTHONDONTWRITEBYTECODE | 1/3 (only .pyc race) | No | No (env var) |
| **this node** (worktree benefit) | Structure: separate trees prevent all 3 | 3/3, including .pyc race | **Yes** | Yes (already measured at 0.09s) |

`a01-390e52ad-e286a2` covers `.pyc` via interpreter flag (N=20 trial
protocol). This node covers the same `.pyc` incident via worktree
structure — each worktree has its own `__pycache__`, so the race cannot
happen. Both work; if worktree isolation is deployed for the other 2
incidents, the `-B` flag is unnecessary but harmless.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fills the benefit-side gap left open by verdict a01-71c62f4b-49e913: "worktree's
merge/review cost under nested tiers is still unmeasured" — but the gap this
closes is narrower: not merge cost but the functional claim that worktree
separation prevents collisions. Verdict a00-4c4fbb51-0f3630 proved the cost
half at 0.09s; this hypothesis targets the benefit half with a deliberate
reproduction protocol. The stale-.pyc claim is structural (separate
`__pycache__` dirs), not analytical — it maps to a concrete filesystem
separation that can be verified with `ls -d worktree-A/**/__pycache__/*` vs
`worktree-B/**/__pycache__/*` before and after a cross-worktree test run.
<!-- THOUGHT:END -->


## Agent Notes
Fills benefit-side gap of worktree isolation: cost proved (0.09s), structural prevention of all 3 g4.1 collision types unverified. Proposes deliberate reproduction experiment. Distinct from existing hyps covering cost (a00-2278675f-5a913a), designated-committer (a01-dd74693c-b77b37), command-whitelist (a00-4ed0dccd-68c060), .pyc-flag (a01-390e52ad-e286a2).
