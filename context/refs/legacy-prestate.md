---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Legacy Pre-State Baseline

Captured for cavekit-topology-fold R10 + cavekit-git-remote R4 (post-archive verification compares against this baseline).

## Local directory `~/autoresearch-tree/`

- Exists on disk: ✓ (`/home/ubuntu/autoresearch-tree/.git/HEAD` is a regular file)
- Status as of 2026-05-04: in place, working tree state independent of fold

## GitHub repo `CodexOperator/autoresearch-tree`

- `gh repo view CodexOperator/autoresearch-tree --json isArchived -q .isArchived` → `false` (NOT archived as of 2026-05-04)
- Latest commit `414424a` (per HANDOFF-autoresearch-2026-05-01.md and local git log)

## Post-fold expected state (deferred until bug-sweep clears)

- `~/autoresearch-tree/` local directory: still present (removal is a deferred-todo item, not in this build cycle)
- `CodexOperator/autoresearch-tree` GitHub repo: archived (`isArchived: true`) with README updated to point at `CodexOperator/agi`

This baseline file is the comparison point for T-068, T-069, T-070 (Tier 7).
