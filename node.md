---
id: hypothesis:l4-the-judge-runs-on-the-substituted-command
mint_id: 4ad960a315104629a43a13809a723962
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 020edf5377c523fd
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-19: rotate.py:4106 — `_producing_refusal` judges the TEMPLATE `cmd`, but `_run_units_no_shell` executes the SUBSTITUTED `exec_cmd` (placeholders + `$VAR` expanded), so a placeholder or env value carrying an unquoted `;` or `|` adds a stage the judge never saw (reproduced by the review). CLAIM: after substitution the SAME judge (`_producing_refusal` + `_operator_refusal`) runs again on `exec_cmd`, and a refusal there is recorded with every expanded value scrubbed back to its literal `$VAR`/placeholder form (no secret in the record, fix b preserved); the template judgement stays as the first gate; the two judgements share one grammar (`_startup_units`). TESTS: a placeholder value `x; touch <tmp>/pwned` -> refused naming the injected verb, the file never appears, the record shows the placeholder not the value; an env var whose value carries `|` -> refused; a clean substitution still runs. FALSIFIER: an exec_cmd stage runs that the template judge never judged. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (first_turn region :3803-4170 ONLY) + extensions/agi/tests/test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-first-turn-env-prefix-is-judged. EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: "rotate.py first_turn: the allowlist judge re-runs on the SUBSTITUTED command, so a placeholder or env value cannot add an unjudged stage"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-judge-runs-on-the-substituted-command

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-19: rotate.py:4106 — `_producing_refusal` judges the TEMPLATE `cmd`, but `_run_units_no_shell` executes the SUBSTITUTED `exec_cmd` (placeholders + `$VAR` expanded), so a placeholder or env value carrying an unquoted `;` or `|` adds a stage the judge never saw (reproduced by the review). CLAIM: after substitution the SAME judge (`_producing_refusal` + `_operator_refusal`) runs again on `exec_cmd`, and a refusal there is recorded with every expanded value scrubbed back to its literal `$VAR`/placeholder form (no secret in the record, fix b preserved); the template judgement stays as the first gate; the two judgements share one grammar (`_startup_units`). TESTS: a placeholder value `x; touch <tmp>/pwned` -> refused naming the injected verb, the file never appears, the record shows the placeholder not the value; an env var whose value carries `|` -> refused; a clean substitution still runs. FALSIFIER: an exec_cmd stage runs that the template judge never judged. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (first_turn region :3803-4170 ONLY) + extensions/agi/tests/test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-first-turn-env-prefix-is-judged. EXCLUDED: everything else.
