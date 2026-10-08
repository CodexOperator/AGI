---
id: experiment:a00-8382f2c3-a5d815
mint_id: ef490c9d45ff4a7aa0f8a54b7f4593d3
type: experiment
parents:
  - hypothesis:rotation-alert-t1-capture-cluster-templated
next_edges: []
confidence: 0.93
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director-engine
evidence_runs:
  - experiment:a00-8382f2c3-a5d815
loop: hypothesis:rotation-alert-t1-capture-cluster-templated@s2
model: stealth/space-bunny-alpha
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 1e637c1e42e3edcf
season: 2
title: Capture cluster prose templates
town: local-maxxing
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-8382f2c3-a5d815

## Experiment

Converted the three remaining capture-cluster messages to `prose_templates.render`:

| call site | template | fields |
|---|---|---|
| capture declined | `capture_declined.md` | `seat` |
| captured final card | `captured.md` | `seat`, `minutes`, `line` |
| captive deferred body | `captive_deferred_body.md` | `prefix`, `which` |

The deferred template receives the existing `DEFER_PREFIX`; it does not redefine the
prefix or change its loader. Added a focused exact-output test covering all three.

## Evidence

Representative expected bytes are asserted in `test_rotation_alert.py`:
`rotation: capture for a declined (AGI_HOOK_NO_SPAWN).`;
`rotation: CAPTURED a's final card (7 min stale): stop: threshold`; and
`<DEFER_PREFIX> (suite-lock-held) — the captive auto-rotate does not fire while that holds.`
This verifies the templates' format fields and preserves the existing prefix path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 7 residue (hypothesis:pass7-0926-residue-batch, test_brief.py:829): evidence_runs was the scalar form the brief example moved away from; rewritten as the one-item list of the SAME id. No evidence added or removed, verdict unchanged.
<!-- THOUGHT:END -->
