---
id: experiment:a00-d1c78f96-ba8955
mint_id: ebba4cd2f51c4960ac0549d399337ab0
type: experiment
parents:
  - hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct
next_edges: []
confidence: 0.95
evidence_runs:
  - experiment:a00-d1c78f96-ba8955
loop: hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7e0fd2681120b828
season: 2
title: A00 d1c78f96 ba8955
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d1c78f96-ba8955

## Experiment

Fix DEFECT 2: `--dry-run` on `done` still WROTE when the tier-parent probe gate
was INACTIVE. The dry-run guard `if bool(getattr(args,"dry_run",False)) and
_probe_active:` was scoped to `_probe_active`; whenever the gate did not apply
(kid tier, `disproved`, lean < :50) the guard fell through to
`rec["status"] = "done"` and `ap.write_text(...)`. The parent had proven it on
disk: `--dry-run` on a `disproved` verdict returned rc=0 and mutated
agent.json to `"status": "done"`. A dry-run flag that mutates is worse than
no flag.

Change (cli.py `cmd_done` only): make the dry-run exit UNCONDITIONAL on the
gate's activity. When `--dry-run` is set, `cmd_done` prints the gate's
decision and returns 0 BEFORE any rec mutation, before `ap.write_text`,
before `_mirror_terminal_into_manifest`, and before
`_append_verdict_to_node`:
- gate active + refusing -> existing refusal wording verbatim, return 0
- gate active + passing -> `[dry-run] tier-parent probe gate: PASS (...)`
- gate inactive -> one true `not applicable (<reason>)` line: `tier=kid`,
  `verdict=disproved`, or `target hypothesis has no claim conjuncts to
  count`. No pass is invented for a gate never evaluated.

No rewrite of either prior kid's work; only the dry-run guard was restructured
and the not-applicable branch added.

## Evidence

`python3 -m pytest extensions/agi/tests/test_cli.py -q` -> **30 passed**
(11 probe/dry-run tests: 9 existing + 2 new).

Real command surface, tmp project (parent's exact repro shape):

CASE 1 parent + disproved + `--dry-run`:
  `[dry-run] tier-parent probe gate: not applicable (verdict=disproved)` rc=0
  agent.json on disk stays `{"id": "a00-p", "tier": "parent", "status":
  "running"}` exactly; node bytes unchanged; no verdict stamp.

CASE 2 kid tier + proved + `--dry-run`:
  `[dry-run] tier-parent probe gate: not applicable (tier=kid)` rc=0
  agent.json stays `"status": "running"`; node bytes unchanged.

Regression on the real surface:
  active-refusing: refusal wording verbatim, rc=0, `"status": "running"`.
  active-passing:  `PASS (2 probe(s) cover conjunct(s) 1, 2)`, rc=0, status
  stays `running`.

New tests (test_cli.py): `test_done_dry_run_inactive_gate_disproved_never_writes`
(parent + disproved, no probes) and
`test_done_dry_run_inactive_gate_kid_tier_never_writes` (kid tier), both assert
exit 0, stdout marks the gate not-applicable, the record reads
`{"id": "a00-p", "tier": ..., "status": "running"}` byte-identical, and the
node bytes are untouched.

## Agent Notes
made --dry-run exit unconditional on probe-gate activity so an inactive gate (kid tier/disproved/lean<50) never writes; not-applicable reason line added; 2 new tests, 30 passed, both inactive cases proven on real command surface
