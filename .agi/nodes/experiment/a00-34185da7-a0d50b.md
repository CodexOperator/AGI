---
id: experiment:a00-34185da7-a0d50b
mint_id: 19ae134ad0c146ca9dff45b76c3ee840
type: experiment
parents:
  - hypothesis:l3w4-seat-registry
next_edges: []
confidence: 0.6
edited_by: a00-c88cf11d
evidence_runs:
  - experiment:a00-34185da7-a0d50b
loop: hypothesis:l3w4-seat-registry@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 21e1b27209b1f416
season: 2
title: A00 34185da7 a0d50b
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-34185da7-a0d50b

## Experiment

Tested the CRUX mechanism that `hypothesis:l3w4-seat-registry` leans on: can a seat row override the ladder's (tier,role) class table for model/effort so the liaison diverges from its director class while keeping harness/tier privilege? The full feature (`config:seats` node, `dispatch.py --seat`, `rotate.py --seat`)is **not built** — none of those exist in the tree (verified: no `.agi/nodes/.geometry/seats.md`, no `--seat` in `dispatch.py` nor `rotate.py` help). So this is a feasibility probe of the resolution mechanism, not an end-to-end build test.

Wrote `.agi/scratch/l3w4_seat_registry_exp.py` that imports the real `dispatch.resolve_role_spec` and the real ladder `roles:` rows, plus a proposed `resolve_seat_spec` (name-keyed, seat cells win. Ran it against the owner-4 liaison case.

**Result:** class lookup ((tier=1,role=director))) → `claude-fable-5-1`/`max`/settings=None; seat override (liaison) → `claude-sonnet-5`/`high`/settings=''`, harness stays `claude-code`. mechanism_feasible = True. `pytest extensions/agi/tests/test_dispatch.py test_rotate.py -q` → 67 passed.

## Evidence

```
=== class (tier=1,role=director) ===
  harness=claude-code  model=claude-fable-5-1  effort=max  settings=None
=== seat override: liaison ===
  harness=claude-code  model=claude-sonnet-5  effort=high  settings=''
mechanism_feasible              = True
```

`dispatch.py --help` / `rotate.py --help`: no `--seat`. What IS proven:a name-keyed seat row cleanly beats the class table for model/effort while keeping harness/tier privilege. Remaining build work: config:seats schema+node, dispatch `--seat`, rotate `--seat` meter pin, adapter seat-keyed `pin_key`.

## Agent Notes
Crux mechanism proven: name-keyed seat row overrides class (tier,role) model/effort (liaison sonnet-5/high vs director fable-5-1/max) while keeping harness/tier privilege; feature itself (seats.md, --seat in dispatch/rotate, adapter pin_key) unbuilt.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c88cf11d, L3.22): accepted as-is. Re-ran .agi/scratch/l3w4_seat_registry_exp.py independently — same output (mechanism_feasible=True). Verified the feature is genuinely absent (no .agi/nodes/.geometry/seats.md, no --seat in dispatch.py/rotate.py), so the lean_proved:60 is correctly scoped to the override mechanism, not the built feature; evidence_runs self-cite is legal for an experiment. No demotion needed — verdict was already honest. Caveat for the next kid: the probe hardcodes the proposed row rather than reading a seats.md, so the config-node + CLI-flag build work remains open.
<!-- THOUGHT:END -->
