---
id: hypothesis:l4-rollover-counts-visions-after-the-ladder-bump
mint_id: 685d5b9d60464a2ebf3ba90ac5f38bfa
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-are-one-tree-under-the-season
next_edges: []
edited_by: sanctuary-director
scaffold_hash: a52d510b17f93303
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-3 (season correctness): season.py:990-994 `cmd_rollover` computes `per_town = count_visions_per_town(nodes_dir)` BEFORE the ladder bump at :1033, so the new season's cap is judged against the OLD season's counts and the s2→s3 rollover refuses every new vision (reproduced end-to-end by the review). CLAIM: the per-town count used to admit rollover visions is taken AFTER the bump (season-scoped per-town count for the NEW season = 0 at rollover), or the count is scoped explicitly to the new season number; a rehearsal (`--dry-run`) prints the counts it would use with the season they are scoped to. TESTS in extensions/agi/tests/test_season*.py: a fixture with a full s2 (cap reached) rolls to s3 and mints its visions (none refused); the cap still refuses within one season. FALSIFIER: a rollover on a full season that refuses a vision. VERIFY ON THE REAL TREE: `season.py rollover --dry-run` (or the equivalent read-only rehearsal) on the live graph prints the s3 counts as 0 — paste it; NEVER a real rollover (the owner's). CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/season.py (cmd_rollover region ONLY) + its tests. SERIAL on season.py behind g15-2 (hypothesis:l4-town-base-honours-the-recorded-base-branch) — do not start until it is harvested. EXCLUDED: spawn_gate.py, rotate.py."
title: cmd_rollover counts per-town visions AFTER the ladder bump — the s2→s3 rollover admits new visions
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rollover-counts-visions-after-the-ladder-bump

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-3 (season correctness): season.py:990-994 `cmd_rollover` computes `per_town = count_visions_per_town(nodes_dir)` BEFORE the ladder bump at :1033, so the new season's cap is judged against the OLD season's counts and the s2→s3 rollover refuses every new vision (reproduced end-to-end by the review). CLAIM: the per-town count used to admit rollover visions is taken AFTER the bump (season-scoped per-town count for the NEW season = 0 at rollover), or the count is scoped explicitly to the new season number; a rehearsal (`--dry-run`) prints the counts it would use with the season they are scoped to. TESTS in extensions/agi/tests/test_season*.py: a fixture with a full s2 (cap reached) rolls to s3 and mints its visions (none refused); the cap still refuses within one season. FALSIFIER: a rollover on a full season that refuses a vision. VERIFY ON THE REAL TREE: `season.py rollover --dry-run` (or the equivalent read-only rehearsal) on the live graph prints the s3 counts as 0 — paste it; NEVER a real rollover (the owner's). CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/season.py (cmd_rollover region ONLY) + its tests. SERIAL on season.py behind g15-2 (hypothesis:l4-town-base-honours-the-recorded-base-branch) — do not start until it is harvested. EXCLUDED: spawn_gate.py, rotate.py.
