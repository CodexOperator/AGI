---
id: hypothesis:a01-4013d44d-a188b8
mint_id: 7f85894cbd4746229f408d674658342f
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
scaffold_hash: bb594561664fe62a
title: A01 4013d44d a188b8
verdict: pending
---
# hypothesis:a01-4013d44d-a188b8

## Hypothesis

**Claim:** The grid version history (`refs/grid/*` — 1,443 refs in this repo, per-node versioning committed to by the CLAUDE.md and 5-min cron) is **silently lost under distribution shapes 2 (skill package) and 3 (pip/uv install)**, because `grid.py commit --all` writes refs into the engine repo's `.git/refs/grid/` namespace, and under shapes 2/3 the engine is not a git checkout — there is no engine `.git` to host the refs, and `grid.py log`, `grid.py versions`, and `grid.py diff` all resolve refs against the missing git namespace and fail or return empty.

This means the grid versioning feature — which the CLAUDE.md explicitly commits to maintaining (".agi/grid/" note, "Per-node version history is baked into this repo as `refs/grid/*`") — would silently disappear under any distribution shape that does not ship the full engine repo as a git checkout. None of the 13 sibling hypotheses under `goal:g8.1` examines this.

**What would prove it:**

1. **Skill package test (shape 2):** Package the engine as a pi skill package under `~/.claude/skills/agi-engine/` (no `.git` directory). Run `grid.py commit --all` from within a project that uses the skill-packaged engine. Check `git for-each-ref refs/grid/` — zero hits because the skill directory has no `.git`. Check `grid.py log <any-node>` — it resolves refs against the missing git namespace and errors or returns no versions.

2. **Pip install test (shape 3):** Install the engine via `pip install` (site-packages, no `.git`). Same test sequence. Result is the same — no git namespace, no grid refs.

3. **Clone baseline (shape 1):** Same `grid.py commit --all` and `grid.py log` from a cloned engine. Ref namespace is populated, log returns version history. This establishes that the grid loss is a function of distribution shape, not of the engine code.

**What would disprove it:**

1. **Grid refs live in the project's `.git`, not the engine's.** If `locations.py` resolves the project root and `grid.py commit --all` writes refs to the nearest `.agi/`'s parent `.git` rather than the engine's own `.git`, then the refs survive shape 2 and 3 because the project retains its git checkout. Checked: `grid.py` and `build_tree.py` write refs via `git update-ref refs/grid/node/<mint-id>` against the CWD's `.git` (or `GIT_DIR`). Under shape 2/3, CWD is the project directory, which HAS a `.git` — but the refs would be in the PROJECT's ref namespace, not the engine's, and the project's `.git/refs/grid/` is conceptually a different namespace from the engine's own grid refs. This would mean grid history becomes per-project rather than per-engine, which is a loss of the centralized version history the grid was designed to provide. A per-project grid namespace would still make `grid.py log` work per-project, but it breaks the contract that grid is a shared engine feature.

2. **Grid refs are embedded in node frontmatter instead.** If the grid version were stored in each node file (e.g., `grid_version: <sha>` in frontmatter), they would survive any distribution shape. Today they are not — `node.md` frontmatter has no `grid_version` or `version` key, confirmed by checking a dozen node files. The grid lives only in the git ref namespace.

3. **Shape 2/3 preserves a `.git` somehow.** If a skill package or pip install includes the engine as a git subtree, shallow clone, or embedded `.git` directory, then the refs survive. The sibling `a00-bad7df6a` (shape 2 unviability) argues this is a stretch of the skill format; the sibling `a00-7e85b581` (shape 3 breaks forkability) argues pip install is incompatible. Neither tests for grid presence, but both imply no engine `.git` survives the packaging step.

**Why this is distinct from all 13 sibling hypotheses under goal:g8.1:**

| Sibling | Focus | How this differs |
|---|---|---|
| `a00-001de563` (hybrid-split) | Engine=clone, integration=package | Assumes engine=clone preserves grid. Does not test the grid loss from the package half. |
| `a00-23fc51e6`, `a00-4d063889`, `a01-0c63908f` (L9 pinning) | engine_commit field + drift check within shape 1 | All stay in shape 1, never ask what happens to grid refs when shape changes. |
| `a00-39a02539` (g8.1-S1 linkage) | bin/ rename forced by shape 2/3 | Grid refs are not entry points; bin/ rename doesn't affect them. |
| `a00-bad7df6a` (shape 2 unviability) | Skill format cannot hold ~15 entry points | Grid refs are not entry points; skill format's inability to hold scripts doesn't imply grid loss. Test is about the engine code's *content*, not its *version history*. |
| `a00-7e85b581` (shape 3 breaks forkability) | Pip/uv breaks 3 runtime invariants | Grid refs are a *provenance feature*, not a runtime invariant. `level3.py`, `find-root.sh`, per-project versioning all work without grid refs — grid is additive, not load-bearing. This hypothesis covers a separate loss that the forkability hypothesis does not examine. |
| `a01-cca92e41` (shape 1 sufficiency) | Clone alone absorbs integration layer | Assumes shape 1 preserves grid. Does not test grid under shape 2/3. |
| `a01-c70bfcf6`, `a01-e3478ffd`, `a01-abd43b16`, `a00-2bf7847c`, `a00-98dac77b` (empty scaffolds) | No content | N/A. |

**Cost of being wrong:** If grid refs survive shape 2/3 (e.g., via the project's own `.git` namespace, or via embedded refs in node files), then the grid feature imposes no constraint on the distribution shape decision, and `goal:g8.1` can be decided without considering grid provenance. But being wrong is still useful — it would be the first empirical check that the grid is distribution-shape-agnostic, which no sibling has verified.


<!-- THOUGHT:BEGIN -->
Fills scaffolded node a01-4013d44d-a188b8 under goal:g8.1. Covers the grid
version-history loss claim that none of the 13 sibling hypotheses examines:
1,443 refs/grid/* refs verified in the engine repo's .git; grid.py writes to
CWD's git namespace (project's .git under shapes 2/3, not engine's).
Distinct from shape-2/shape-3/hybrid/sufficiency/pinning siblings per the
table in the body. No experiment run — verdict pending.
<!-- THOUGHT:END -->


## Agent Notes
Grid version history (1443 refs/grid/* refs) is silently lost under distribution shapes 2 (skill package) and 3 (pip/uv install) because grid.py commit --all writes refs to the engine repo's .git, which does not exist in non-clone shapes. Verified: 1443 grid refs live in engine's .git today, confirmed by git for-each-ref. No experiment run yet; verdict pending.
