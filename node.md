---
id: hypothesis:l4-first-turn-filters-truncate
mint_id: 8fbfb5cd248545ef9dfb2821405188ee
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 251db21472ffd550
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (v) `_run_units_no_shell` (rotate.py:3978-3997) appends EVERY stage's stdout to the merged output (`chunks.append(merged)` inside the stage loop), so a `| head -4` / `| sed -n 1,40p` filter truncates nothing — measured on my own first turn 07:02Z: the STARTUP block carried the full `provisioning.py status` (12 outstanding keys) ahead of its `head -4` copy, `git status -sb` twice and `write.py -h` twice (~1.5k tokens per rotation, every seat). CLAIM: per `|` pipeline only the LAST stage's stdout is appended; every stage's stderr is still merged in order; `;` units still concatenate; the byte cap and truncation flag unchanged. TESTS: a 100-line producer `| head -3` → exactly 3 lines; a failing middle stage's stderr present; two `;` units both present; the dry-run record unchanged. FALSIFIER: a producer's stdout present in the output when a filter followed it. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_run_units_no_shell` ONLY) + extensions/agi/tests/test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-the-judge-runs-on-the-substituted-command. EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: the no-shell first_turn executor emits only the LAST stage's stdout per pipeline, so | head -N and | sed filters actually truncate
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-first-turn-filters-truncate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (v) `_run_units_no_shell` (rotate.py:3978-3997) appends EVERY stage's stdout to the merged output (`chunks.append(merged)` inside the stage loop), so a `| head -4` / `| sed -n 1,40p` filter truncates nothing — measured on my own first turn 07:02Z: the STARTUP block carried the full `provisioning.py status` (12 outstanding keys) ahead of its `head -4` copy, `git status -sb` twice and `write.py -h` twice (~1.5k tokens per rotation, every seat). CLAIM: per `|` pipeline only the LAST stage's stdout is appended; every stage's stderr is still merged in order; `;` units still concatenate; the byte cap and truncation flag unchanged. TESTS: a 100-line producer `| head -3` → exactly 3 lines; a failing middle stage's stderr present; two `;` units both present; the dry-run record unchanged. FALSIFIER: a producer's stdout present in the output when a filter followed it. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_run_units_no_shell` ONLY) + extensions/agi/tests/test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-the-judge-runs-on-the-substituted-command. EXCLUDED: everything else.
