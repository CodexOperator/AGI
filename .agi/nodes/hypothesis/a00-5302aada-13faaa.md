---
id: hypothesis:a00-5302aada-13faaa
mint_id: 225bf59068a24cebadc31fc45130bbca
type: hypothesis
parents:
  - goal:g7.31.1.2.1
next_edges: []
confidence: 0.5
edited_by: a00-5302aada
evidence_runs:
  - hypothesis:a00-5302aada-13faaa
line_ceiling: 40
loop: goal:g7.31.1.2.1@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f3b60763c1709600
season: 2
title: Restart preserves harness env while dropping credential-none secrets
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# Credential filtering survives the built restart seam

## Experiment

The claimed held-restart seam does not exist on this checkout: there is no
`extensions/agi/bin/adapters/tmux_hold.py`, no `HOLD_PANE` symbol under
`extensions/agi/bin`, and `dispatch._reap_one` calls `adapter.restart`
directly. Therefore the inherited claim about an early return from that
missing branch cannot be reproduced or repaired on these bytes.

I tested the prerequisite that is present: adapter `restart` builds its
`Popen` environment through `child_env`. A new focused case in
`extensions/agi/tests/test_credential_none_spawn.py` gives a credential-none
pi harness `AGI_HARNESS_MARKER=present`, captures the restart environment,
and asserts both that the marker survives and `OPENROUTER_API_KEY` does not.

## Result

`python3 -m pytest extensions/agi/tests/test_credential_none_spawn.py -q`
passed: **13 passed, 4 warnings in 4.98s**. This proves the direct restart
seam performs selective sanitisation rather than returning an empty
environment. It does not prove the absent held-pane seam carries that map;
that end-state remains unbuilt rather than failed.

## Verdict basis

Lean proved at 50%: the environment-filter half is demonstrated on the real
restart function, while every claim specific to tmux hold is untestable until
`tmux_hold` and its restart call site land.

## Agent Notes
Added a real restart-env marker regression test (13 passed), but this checkout has no tmux_hold or HOLD_PANE branch to build or probe.
