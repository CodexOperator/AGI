---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Implementation Tracking: tier0

Build site: /home/ubuntu/autoresearch-tree/context/plans/build-site.md

| Task | Status | Notes |
|------|--------|-------|
| T-001 | DONE | Pytest baseline 166 passed / 1 known fail (`test_field_set_is_exactly_six`). Recorded in `context/refs/pytest-baseline-prefold.md`. Note: handoff said 274 tests; current collection is 167. Discrepancy documented. |
| T-002 | DONE | `gh auth status` → ✓ CodexOperator authenticated, https protocol, scopes include repo + workflow. |
| T-003 | DONE | Branch `agi-unification` created in `~/.hermes/agi/` from `master` tip (`3d550de`). Verified via `git branch -a`. NOTE: agi default branch is `master`, not `main` — git-remote tasks must reference `master` accordingly. |
| T-004 | DONE | Remote `origin` → `https://github.com/CodexOperator/agi-tree.git` added to `~/.hermes/agi-tree/`. NOT pushed (gated to T-067). Working tree is DIRTY (user's prior research session left modifications + untracked files). Default branch: `master`. Push will require commit/stash/co-ord with user before T-067 — flagged for builder. |
| T-005 | DONE | Commit-message style conventions captured for both repos in `context/refs/commit-style-conventions.md`. agi=freeform descriptive, ar-tree=type-prefixed. Recommend `fold:` prefix for fold commits. |
| T-006 | DONE | Legacy `~/autoresearch-tree/` exists; `CodexOperator/autoresearch-tree` not archived. Recorded in `context/refs/legacy-prestate.md`. |

## Risks/findings flagged for downstream tiers

- **agi-tree dirty working tree** — `M autoresearch-tree.config.json`, `M autoresearch.jsonl`, `M src/chain_engine/chains.py`, untracked `nodes.db`, `.chain_cache.pkl`, `exp-a01-extend-2000hop.py`, `.claude/worktrees/`. T-067 (push agi-tree main verbatim) will fail without resolving this. **Action needed before Tier 7**: ask user whether to commit, stash, or `.gitignore` these.
- **agi default branch is `master`, not `main`** — git-remote.md R1/R2 reference "main"; should be `master` (or rename, but that's an extra concern). Builders must use `master`.
- **agi-tree default branch is `master`** with currently-checked-out `iter24-extend-300hop`. Spec says "main pushed as-is" — interpret as `master`.
- **Pytest count discrepancy** vs handoff (167 collected vs handoff's 274). Operative baseline is 167/166-pass. Post-fold expectation set accordingly in baseline file.
