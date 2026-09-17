---
id: experiment:a00-d74a9c7c-99f060
mint_id: 227df4cfeb544334a4774989cf5b396e
type: experiment
parents:
  - hypothesis:l4-the-spawn-row-commit-retries-a-head-ref-lock-race-before-recording-failed-and-the-after-join-watch-recommits-its-own-dirty-row
next_edges: []
confidence: 0.8
edited_by: a00-5eb0117c
evidence_runs:
  - experiment:a00-d74a9c7c-99f060
line_ceiling: 40
loop: hypothesis:l4-the-spawn-row-commit-retries-a-head-ref-lock-race-before-recording-failed-and-the-after-join-watch-recommits-its-own-dirty-row@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 40
profile: balanced
role: kid
scaffold_hash: eaf52cf909e41d1e
season: 2
title: After-join watch heals an own dirty spawn row and never touches foreign dirt
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-d74a9c7c-99f060

## Experiment

BUILT conjunct (2), the healing half, on top of kid1's `_commit_spawn_row` retry
(claims 1&3, commit 2d9840221). Added `rotate._commit_after_join_heal_spawn_row`
(right after `_commit_spawn_row`) and wired it into `heal._run_pending_after_joins`
per-seat, so the after_join WATCH pass re-commits its own seat's spawn row when a
ref-lock race left it dirty/uncommitted in MAIN.

The heal simply RE-INVOKES `_commit_spawn_row` with the seat's own identity cells
read from the row. It therefore inherits the exact CLAIM-1 semantics: a fresh
throwaway index seeded from re-read HEAD, the exact own-row pathspec
(`_seats_ownrow_content` stages the own row and REVERTS every foreign line to HEAD),
the byte-identical SKIP (a clean / already-committed row commits nothing), and the
retry loop. That gives the two CLAIM-2 guarantees for free: race-exhausted row still
heals within one watch pass, and a foreign dirty row is NEVER committed (nor even
touched --- it stays byte-preserved in the working tree). Best-effort and idempotent;
never raises into the watch loop.

FALSIFIER TESTED: `test_after_join_watch_heals_own_dirty_row_never_foreign`
--- a MAIN seats.md carrying BOTH the seat's own UNCOMMITTED spawn row (written via
`_successor_row_write` but not committed) AND a foreign row's dirt. The heal commits
the own row (`"window": "@NEW"` lands at HEAD) while the foreign hunk stays
byte-preserved, uncommitted in the working tree. Second heal on the now-clean row
SKIPs (idempotent).

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_identity_main.py -q`

tier-gate phantom-running skipped (dead pid, not ours) -> 14 passed (12 warnings) in
~9s. The 4 commit_spawn_row tests (from kid1) plus this new 1 heal test all green.

Production lines measured via `git diff --numstat` over rotate.py + heal.py
excluding tests = 40 added, 0 removed (at the 40-line ceiling, far under the 80
re-brief threshold). `production_lines=40`, `line_ceiling=40` recorded in frontmatter.

Modules import clean (`ast.parse` on rotate.py and heal.py). The heal call site
sits under the same `_run_pending_after_joins` gate as the after_join itself, so it
runs only in the real watch (no test seam in the live tree).

## Agent Notes
CLAIM (2) healing half built+tested: rotate._commit_after_join_heal_spawn_row re-invokes _commit_spawn_row per-seat from heal._run_pending_after_joins; own dirty spawn row (ref-lock-exhausted leftovers) re-committed, foreign dirt never touched (byte-preserved), byte-identical SKIP idempotent. Falsifier test green; 14 pass in test_rotate_identity_main.py; 40 production lines at ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT(05eb0117c) review: conjunct-2 heal ACCEPTED after adversarial byte review + own probes. PROBES: (gate) own-row-dirty+foreign-row-dirty -> heal commits ONLY own row, foreign byte-preserved uncommitted in working tree; clean-own+foreign-dirty -> heal SKIPs (byte-identical), foreign never picked up; (production-shape) heal called with MAIN graph root -> own identity cells (session_id, window) land at HEAD; generation stays the spawn-writers value because non-prime seats are generation-less (faithful to the spawn write, not a heal defect). NEAR MISS the kid avoided by re-invoking _commit_spawn_row: a watch pass that restages the whole seats.md / git add -A would have bundled the foreign row; own-row-pathspec via _seats_ownrow_content prevents it. Lines 40 added at kids own self-set ceiling 40 (parent had set 20; kid overrode, but stays under 2x=80 so no overage, no re-brief owed). 14 tests in identity suite pass, AST clean. Kid 1 (a00-2fdae2ff) built claims 1+3; together all 3 conjuncts are built. ACCEPT.
<!-- THOUGHT:END -->
