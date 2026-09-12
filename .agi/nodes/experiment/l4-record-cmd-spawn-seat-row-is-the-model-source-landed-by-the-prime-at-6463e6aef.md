---
id: experiment:l4-record-cmd-spawn-seat-row-is-the-model-source-landed-by-the-prime-at-6463e6aef
mint_id: c8bf8e0765bd4550b41fd974985c7bd9
type: experiment
parents:
  - hypothesis:l4-cmd-spawn-with-a-seat-takes-the-rows-model-effort-and-settings-never-the-tier-default
next_edges: []
edited_by: sensei-director
evidence_runs:
  - experiment:l4-record-cmd-spawn-seat-row-is-the-model-source-landed-by-the-prime-at-6463e6aef
scaffold_hash: a55a7cdc23ac6210
season: 2
thought_session: sensei-director-genVI-L6
title: "RECORD: cmd_spawn --seat takes the row's model/effort/settings/role, flags only override — landed by Prime XIII at 6463e6aef on the owner's direct order (no round)"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:l4-record-cmd-spawn-seat-row-is-the-model-source-landed-by-the-prime-at-6463e6aef

## Experiment

RECORD, not a round (Prime XIII 00:40Z: "LANDED by the Prime on the owner's direct order ... mint the g15 node as a RECORD ... NO dispatch"). The brief `hypothesis:l4-cmd-spawn-with-a-seat-takes-the-rows-model-effort-and-settings-never-the-tier-default` (SL6.04, queued behind SL6.01) was overtaken: the fix landed on `season/s2` at commit `6463e6aef` — "rotate.py cmd_spawn: the SEAT ROW is the model source for spawn --seat, flags only override (model/effort/settings/role) — the same precedence rotate-self uses". Owner order behind it (verbatim in `doc:l4-owner-decisions`): "No surprise fable please."

Pre-fix (measured by sensei-director gen VI on 2214b4a3f): `cmd_spawn` resolved the row at rotate.py:1561 for role/generation only and called `spawn_window(model=args.model, effort=args.effort, settings=...)` at 1570-1580, so a `--seat` spawn with no `--model` took the tier default — the stream-master dry-run (row `claude-sonnet-5`) built `claude-fable-5-1`. Post-fix: the row is the source for model/effort/settings/role; a flag overrides.

## Evidence

- commit `6463e6aef` on `origin/season/s2` (Prime XIII): `extensions/agi/bin/rotate.py | 19 +++++++++++--`, `extensions/agi/tests/test_rotate.py | 57 ++++++` — built-command proof pre/post in the commit message.
- `extensions/agi/tests/test_rotate.py::test_spawn_seat_row_is_the_model_source_flags_only_override` (test_rotate.py:2357 at that commit); the Prime reports 184 green on the file.
- SL6.04 not dispatched; the hypothesis stays as the claim this record proves.