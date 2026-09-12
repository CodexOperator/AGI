---
id: experiment:a00-2d7579bc-687b0f
mint_id: 3472cf5935614652b81aabb819cab8d3
type: experiment
parents:
  - hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-2d7579bc-687b0f
loop: hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5be0436e26a13c0b
season: 2
title: A00 2d7579bc 687b0f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2d7579bc-687b0f

## Experiment

Fix of the two defects the parent measured on the prior kid's tier-parent probe gate (cli.py), build order not measurement.

DEFECT 1 (primary): `--dry-run` wrote on the PASS path. The old code only dry-ran the REFUSAL branch; on a passing gate control fell through to `rec["status"]="done"` and `ap.write_text`. Rewrote `_parent_probe_gate` to return `(error, active, covered)`, and in `cmd_done` added a dry-run short-circuit that returns 0 BEFORE any write when the gate passes:

    [dry-run] tier-parent probe gate: PASS (N probe(s) cover conjunct(s) 1, 2, 3, 4)

No rec mutation, no write_text, no _mirror_terminal_into_manifest, no _append_verdict_to_node on either dry-run path.

DEFECT 2: the gate counted a conjunct as covered on a bare `{"conjunct": int}`. Added `_PROBE_KEYS` (all six: conjunct/class/cmd/expected/observed/result), `_PROBE_CLASSES` = {auth, gate, wire}, and `_probe_defect(p)` naming a missing key or a bad class. A malformed probe does NOT cover its conjunct and is named in the refusal ("Malformed probe(s) not counted: conjunct 1: missing key(s): result") while keeping the existing "claim conjunct(s): N, M" wording. `--probes '[{"conjunct":1}]'` -- the exact shape that used to slip through -- now refuses.

## Evidence

python3 -m pytest extensions/agi/tests/test_cli.py -q  ->  28 passed (24 prior + 4 added).
- test_done_parent_dry_run_pass_path_never_writes: PASS gate under --dry-run -> rc 0, record still `"status": "running"` and no `"verdict"` on disk, node bytes byte-identical, stdout names the gate PASS.
- test_done_parent_probe_missing_result_does_not_cover: probe missing `result` -> rc 2, refusal names "claim conjunct(s): 1" and "missing key(s): result", record untouched.
- test_done_parent_probe_bad_class_does_not_cover: `class:"bash"` -> rc 2, refusal names conjunct 4 and the bad class.
- test_done_parent_bare_conjunct_probe_covers_nothing: `[{"conjunct":1}]` full-would-be-slip -> rc 2, "claim conjunct(s): 1, 2, 3, 4".
Existing test_done_kid_tier_unchanged_by_probe_gate and test_done_parent_dry_run_prints_gate_without_writing (refusal path) stay green. python3 -m py_compile extensions/agi/bin/cli.py -> OK. Prior remaining gate tests (accepted_with_one_probe_per_conjunct etc.) also green. File scope respected: only extensions/agi/bin/cli.py and extensions/agi/tests/test_cli.py touched; zoom.py / dispatch.py / parent-section prose untouched.

## Agent Notes
Fixed both defects on disk bytes: dry-run now inert on the pass path (prints [dry-run] tier-parent probe gate: PASS, returns 0 before any write), and a probe lacking any of the six keys or a non-auth/gate/wire class does not cover its conjunct and is named in the refusal. 28/28 cli tests pass.
