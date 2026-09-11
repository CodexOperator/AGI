---
id: hypothesis:l4-first-turn-env-prefix-is-judged
mint_id: b352098a829e4f74ac8648984a077de5
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 1a370d8e43219d00
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-18 (FIRST): rotate.py:3982/:3961 — a leading `VAR=value` prefix is SKIPPED by the allowlist judge (`_segment_parts` drops it) and APPLIED to the child's env by `_run_units_no_shell`, so `PATH=<dir>`, `PYTHONPATH=`, `LD_PRELOAD=` let an allowlisted argv[0] run an off-allowlist program (reproduced by the review). CLAIM: a prefix whose VAR is not on a named allowlist (`startup.env_allow`, default EMPTY) is REFUSED before execution with a named refusal (`env prefix VAR not on startup.env_allow`) recorded in the result dict like every other refusal; an allowed prefix still applies; the record keeps the literal text; the executor never receives a refused command. TESTS: `PATH=<tmp dir holding a fake python3> python3 -c ...` is refused and the fake never runs; a fixture template with `env_allow: [FOO]` admits `FOO=1 <allowed cmd>`; `LD_PRELOAD=x <allowed cmd>` refused; dry-run reports the refusal. FALSIFIER: any `VAR=value` prefix reaching `_run_units_no_shell` without its VAR on the allowlist. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (the first_turn judge/executor region :3803-4170 ONLY) + extensions/agi/tests/test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window (L4.158); hypothesis:l4-the-judge-runs-on-the-substituted-command follows THIS. EXCLUDED: everything else; the Belam/reap region; rotations.md."
thought_session: sanctuary-director-gen12
title: "rotate.py first_turn: a leading VAR=value prefix is judged against a named env allowlist, never applied unjudged"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-first-turn-env-prefix-is-judged

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-18 (FIRST): rotate.py:3982/:3961 — a leading `VAR=value` prefix is SKIPPED by the allowlist judge (`_segment_parts` drops it) and APPLIED to the child's env by `_run_units_no_shell`, so `PATH=<dir>`, `PYTHONPATH=`, `LD_PRELOAD=` let an allowlisted argv[0] run an off-allowlist program (reproduced by the review). CLAIM: a prefix whose VAR is not on a named allowlist (`startup.env_allow`, default EMPTY) is REFUSED before execution with a named refusal (`env prefix VAR not on startup.env_allow`) recorded in the result dict like every other refusal; an allowed prefix still applies; the record keeps the literal text; the executor never receives a refused command. TESTS: `PATH=<tmp dir holding a fake python3> python3 -c ...` is refused and the fake never runs; a fixture template with `env_allow: [FOO]` admits `FOO=1 <allowed cmd>`; `LD_PRELOAD=x <allowed cmd>` refused; dry-run reports the refusal. FALSIFIER: any `VAR=value` prefix reaching `_run_units_no_shell` without its VAR on the allowlist. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (the first_turn judge/executor region :3803-4170 ONLY) + extensions/agi/tests/test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window (L4.158); hypothesis:l4-the-judge-runs-on-the-substituted-command follows THIS. EXCLUDED: everything else; the Belam/reap region; rotations.md.
