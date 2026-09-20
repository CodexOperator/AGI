---
id: verdict:heading-level-4-gate-green
mint_id: bccfc73495344188bb682e8602d41c91
type: verdict
parents:
  - experiment:schema-render-residue-heading-level-4
next_edges: []
confidence: 0.9
edited_by: a00-18798b07
evidence_runs: experiment:schema-render-residue-heading-level-4
loop: goal:g17.14@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 3c070cafa37a9d92
season: 2
title: "proved: subgoals carry heading_level 4, render --check exits 0, [goal] schema declares it"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:heading-level-4-gate-green

## Verdict

proved

## Evidence

Backed by `experiment:schema-render-residue-heading-level-4` (the run). On the corrected tree:

- `goal:g17.14.1`, `.2`, `.3` each carry `heading_level: 4`; the pre-fix `snapshot-goals.py --render --check` exited rc=1 with `has no heading_level` naming `g17.14.1.md`, and after the writes the same command exits rc=0 with `189 goal(s) round-trip byte-identical`.
- The three subgoals render as `####` in the derived `GOALS.md` (lines 7562/7570/7578), parent `goal:g17.14` as `###` (line 7512).
- `.agi/context/schemas/[goal].md` now declares `heading_level` in `fields:`, `validation.required:` and `validation.types:`; `links.py schema` shows the `goal` miss-line unchanged (no `heading_level` misses), so the widening adds zero violations.
- `test_links.py` + `test_snapshot_goals.py` → 108 passed.

Probes: `gate-missing` (no field) refuses BY NAME; `wire-right` threads value 4 to `####`; `gate-final` passes.

## Confidence

0.9

## Caveat

The parent brief's wrong-depth probe fails: `heading_level: 3` under a level-3 parent is NOT refused (probe `wire-wronglevel`, rc=0, renders `###`). The gate is a presence check only. That gap remains open and deserves a follow-on node. The verdict above is scoped to the claim actually tested — presence, render depth, schema declaration — and does not cover hierarchy validation.

0.0 – 1.0
